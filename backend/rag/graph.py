"""RAG 파이프라인 — LangGraph 두 노드 (F2006 · F2007 · F2008 · F2014)

  START → retrieve → generate → END

retrieve : 선택 차량의 메타데이터 청크(항상 [근거 1]) + car_docs에서 그 차량으로 범위를 좁힌
           유사도/MMR 검색 결과를 병합하고 중복 청크를 제거해 번호를 붙인다.
generate : 프롬프트 3으로 근거만 사용해 답하고, 본문의 [근거 n]을 찾아 실제 인용된 근거만 남긴다.
"""
from __future__ import annotations

import hashlib
import re
from functools import lru_cache
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from backend.config import settings
from backend.domain import prompts
from backend.domain.cars import SOURCE_LABEL
from backend.llm import ServiceError, ask
from backend.store import vectorstore as vs

CITE_RE = re.compile(r"\[근거\s*([\d,\s]+)\]")


class RagState(TypedDict, total=False):
    car: dict
    question: str
    top_k: int
    search_type: str
    model: str
    evidence: list[dict]
    answer: str
    citations: list[dict]


def _evidence(doc, n: int, score: float | None = None) -> dict:
    m = doc.metadata
    return {
        "n": n, "chunk_id": m.get("chunk_id"), "type": m.get("source_type"), "lang": m.get("lang", ""),
        "title": m.get("title"), "url": m.get("url") or None, "page": m.get("page"), "query": m.get("query", ""),
        "score": score, "text": doc.page_content,
    }


def search_docs(car_id: str, question: str, k: int, search_type: str) -> list[tuple]:
    """car_docs에서 해당 차량 청크만 검색. 반환: [(Document, score|None)]"""
    if k <= 0:
        return []
    store = vs.store(vs.DOCS)
    flt = {"car_id": car_id}
    if search_type == "mmr":
        fetch_k = max(settings.mmr_fetch_k, k * 3)
        return [(d, None) for d in store.max_marginal_relevance_search(question, k=k, fetch_k=fetch_k,
                                                                       lambda_mult=settings.mmr_lambda, filter=flt)]
    return [(d, round(1 - dist, 3)) for d, dist in store.similarity_search_with_score(question, k=k, filter=flt)]


def retrieve(state: RagState) -> RagState:
    car = state["car"]
    meta = vs.meta_chunk(car["id"])
    if meta is None:
        raise ServiceError("NO_INDEX", "메타데이터 색인이 없습니다.")
    # "어떤 역사를 가진 차야?"처럼 대상이 빠진 질문도 그 차량 문서가 잡히도록 차량 이름을 붙여 검색
    query = f"{car['name']} {car['nameEn']} {state['question']}"
    found = search_docs(car["id"], query, state["top_k"] - 1, state["search_type"])

    # 병합 + 중복 제거: 같은 청크 ID, 또는 공백을 뺀 본문이 같은 청크는 하나만 남긴다
    evidence, seen = [_evidence(meta, 1)], {meta.metadata["chunk_id"]}
    hashes = set()
    for doc, score in found:
        h = hashlib.md5(re.sub(r"\s+", "", doc.page_content).encode()).hexdigest()
        if doc.metadata.get("chunk_id") in seen or h in hashes:
            continue
        seen.add(doc.metadata.get("chunk_id"))
        hashes.add(h)
        evidence.append(_evidence(doc, len(evidence) + 1, score))
    return {"evidence": evidence}


def format_context(evidence: list[dict]) -> str:
    blocks = []
    for e in evidence:
        src = SOURCE_LABEL.get(e["type"], e["type"]) + (f"·{e['lang'].upper()}" if e["type"] == "wiki" and e["lang"] else "")
        page = f" p.{e['page']}" if e.get("page") else ""
        blocks.append(f"[근거 {e['n']}] ({src}) {e['title']}{page}\n{e['text']}")
    return "\n\n".join(blocks)


def normalize_citations(answer: str) -> str:
    """[근거 1, 3] → [근거 1][근거 3]"""
    return CITE_RE.sub(lambda m: "".join(f"[근거 {n}]" for n in re.findall(r"\d+", m.group(1))), answer)


def drop_unknown(answer: str, evidence: list[dict]) -> str:
    """근거 목록에 없는 번호(LLM이 지어낸 번호)는 본문에서 지운다."""
    valid = {e["n"] for e in evidence}
    return re.sub(r"\s?\[근거 (\d+)\]", lambda m: m.group(0) if int(m.group(1)) in valid else "", answer)


def cited(answer: str, evidence: list[dict]) -> list[dict]:
    nums = {int(n) for n in re.findall(r"\[근거 (\d+)\]", answer)}
    return [e for e in evidence if e["n"] in nums]


def generate(state: RagState) -> RagState:
    car = state["car"]
    prompt = prompts.ANSWER.format(car=f"{car['name']} ({car['year']})", context=format_context(state["evidence"]))
    answer = drop_unknown(normalize_citations(ask(prompt + f"\n\n질문: {state['question']}", state.get("model"))), state["evidence"])
    return {"answer": answer, "citations": cited(answer, state["evidence"])}


@lru_cache(maxsize=1)
def graph():
    g = StateGraph(RagState)
    g.add_node("retrieve", retrieve)
    g.add_node("generate", generate)
    g.add_edge(START, "retrieve")
    g.add_edge("retrieve", "generate")
    g.add_edge("generate", END)
    return g.compile()


def public(e: dict) -> dict:
    """화면에 보낼 근거 (본문은 짧은 발췌만)."""
    snippet = re.sub(r"\s+", " ", e["text"])
    return {k: e[k] for k in ("n", "chunk_id", "type", "lang", "title", "url", "page", "score", "query")} | {
        "snippet": snippet[:160] + ("…" if len(snippet) > 160 else "")}
