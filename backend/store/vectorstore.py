"""Vector Store 영역 — ChromaDB 컬렉션 두 개

car_meta : 차량 1대 = 청크 1개. 청크 ID = 차량 ID → 다시 색인해도 덮어쓰기만 일어난다 (F2002)
car_docs : 외부 문서 청크. 청크 ID = "{차량 ID}:{문서 ID}:{순번}" (F2005)
           같은 문서를 여러 차량이 수집해도 차량 ID가 앞에 붙어 서로 덮어쓰지 않는다.
           메타데이터: car_id, car_name, source_type(wiki|pdf), lang, title, url, page,
                       doc_id, query, section, chunk_index, chunk_id, collected_at
"""
from __future__ import annotations

import hashlib
from datetime import date
from functools import lru_cache

import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.config import settings
from backend.domain.cars import index_text
from backend.llm import get_embeddings

META = "car_meta"
DOCS = "car_docs"


@lru_cache(maxsize=1)
def _client() -> chromadb.ClientAPI:
    settings.chroma_dir.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(settings.chroma_dir))


@lru_cache(maxsize=2)
def store(name: str) -> Chroma:
    return Chroma(collection_name=name, client=_client(), embedding_function=get_embeddings(),
                  collection_metadata={"hnsw:space": "cosine"})


def raw(name: str):
    """임베딩 없이 개수·메타데이터만 볼 때 (API 키가 없어도 동작)."""
    return _client().get_or_create_collection(name, metadata={"hnsw:space": "cosine"})


def doc_id(lang: str, title: str) -> str:
    return f"{lang}-" + hashlib.md5(title.encode("utf-8")).hexdigest()[:10]


def splitter() -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=min(settings.chunk_overlap, settings.chunk_size // 2),
        separators=["\n== ", "\n\n", "\n", ". ", "다. ", " ", ""],
    )


# ---------------- 색인 ----------------
def index_meta(cars: list[dict]) -> int:
    docs = [Document(page_content=index_text(c), metadata={
        "car_id": c["id"], "car_name": c["name"], "year": c["year"], "maker": c["maker"],
        "fuel": c["fuel"], "drive_code": c["driveCode"], "body_type": c["bodyType"],
        "source_type": "meta", "title": f"{c['name']} · 차량 메타데이터", "chunk_id": c["id"],
    }) for c in cars]
    store(META).add_documents(docs, ids=[c["id"] for c in cars])   # upsert
    return raw(META).count()


def index_document(car: dict, *, source_type: str, lang: str, title: str, text: str,
                   url: str | None = None, query: str = "", page: int | None = None) -> int:
    """문서 1건을 청킹해 car_docs에 넣는다. 같은 차량·문서를 다시 넣으면 덮어쓴다."""
    did = doc_id(lang, title) if page is None else f"pdf-{doc_id(lang, title)}-p{page}"
    pieces = splitter().split_text(text)
    if not pieces:
        return 0
    today = date.today().isoformat()
    ids, docs = [], []
    for i, piece in enumerate(pieces):
        cid = f"{car['id']}:{did}:{i}"
        meta = {"car_id": car["id"], "car_name": car["name"], "source_type": source_type, "lang": lang,
                "title": title, "url": url or "", "doc_id": did, "query": query, "chunk_index": i,
                "chunk_id": cid, "collected_at": today}
        if page is not None:
            meta["page"] = page
        ids.append(cid)
        docs.append(Document(page_content=piece, metadata=meta))
    # 문서가 짧아져 청크 수가 줄었을 때 남는 이전 청크 제거
    old = raw(DOCS).get(where={"$and": [{"car_id": car["id"]}, {"doc_id": did}]}, include=[])["ids"]
    stale = [x for x in old if x not in set(ids)]
    if stale:
        raw(DOCS).delete(ids=stale)
    store(DOCS).add_documents(docs, ids=ids)
    return len(ids)


def prune(valid_ids: set[str]) -> int:
    """차량 목록에서 빠진(또는 ID가 바뀐) 차량의 청크를 두 컬렉션에서 지운다."""
    removed = 0
    stale_meta = [i for i in raw(META).get(include=[])["ids"] if i not in valid_ids]
    if stale_meta:
        raw(META).delete(ids=stale_meta)
        removed += len(stale_meta)
    docs = raw(DOCS).get(include=["metadatas"])
    stale_docs = [i for i, m in zip(docs["ids"], docs["metadatas"]) if m.get("car_id") not in valid_ids]
    if stale_docs:
        raw(DOCS).delete(ids=stale_docs)
        removed += len(stale_docs)
    return removed


# ---------------- 조회 ----------------
def counts() -> dict:
    metas = raw(DOCS).get(include=["metadatas"])["metadatas"]
    return {
        "meta_count": raw(META).count(),
        "chunk_count": len(metas),
        "doc_count": len({(m["car_id"], m["doc_id"]) for m in metas}),
    }


def docs_of(car_id: str) -> list[dict]:
    """차량별로 색인된 문서 목록 (제목·출처 종류)."""
    metas = raw(DOCS).get(where={"car_id": car_id}, include=["metadatas"])["metadatas"]
    seen = {}
    for m in metas:
        seen.setdefault(m["doc_id"], {"title": m["title"], "source_type": m["source_type"], "lang": m.get("lang", ""),
                                      "url": m.get("url", ""), "chunks": 0})["chunks"] += 1
    return list(seen.values())


def meta_chunk(car_id: str) -> Document | None:
    r = raw(META).get(ids=[car_id], include=["documents", "metadatas"])
    if not r["ids"]:
        return None
    return Document(page_content=r["documents"][0], metadata=r["metadatas"][0])
