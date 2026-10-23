"""외부 문서 수집 (F2003 · F2004 · NF2002)

1) 차량 자체 문서는 항상 색인한다 — 선별·길이 규칙보다 우선
   (data/cars_enriched.json 의 문서 묶음을 쓰고, 없으면 위키백과에서 직접 가져온다)
2) 프롬프트 1로 질문에 필요한 검색어를 뽑는다
   이미 받은 (차량, 질문)이면 그때 뽑은 검색어를 그대로 쓴다 — LLM은 temperature 0에서도
   같은 질문에 다른 검색어를 낼 수 있어, 검색어 캐시만으로는 같은 질문의 재수집을 막지 못한다
3) 이미 수집한 (차량, 검색어)는 건너뛴다 — data/collect_cache.json
4) 새 검색어는 위키백과에서 후보를 모아, 본문을 받기 전에 프롬프트 2로 제목·요약만 보고 고른다
5) 고른 문서의 본문과 원문 URL을 받아 car_docs 컬렉션에 청킹·색인한다
"""
from __future__ import annotations

import json
import re
import threading
from datetime import datetime
from typing import Callable

from backend.collect import wikipedia
from backend.config import settings
from backend.domain import prompts
from backend.llm import ask, parse_json
from backend.store import vectorstore as vs

CACHE_FILE = settings.data_dir / "collect_cache.json"
_lock = threading.Lock()


def _load() -> dict:
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    return {}


def _save(cache: dict) -> None:
    CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")


def _key(car_id: str, query: str) -> str:
    return f"{car_id}::{query.strip().lower()}"


def _question_key(car_id: str, question: str) -> str:
    """공백·대소문자·끝 문장부호만 다른 질문은 같은 질문으로 본다."""
    q = re.sub(r"\s+", " ", question).strip().lower().rstrip("?.!？。 ")
    return f"{car_id}::question::{q}"


def car_label(car: dict) -> str:
    return f"{car['name']} ({car['nameEn']}, {car['year']}년, {car['maker']})"


def ensure_own_docs(car: dict) -> list[str]:
    """차량 자체 문서를 색인한다. 이미 색인돼 있으면 아무것도 하지 않는다."""
    with _lock:
        cache = _load()
        key = _key(car["id"], "__own__")
        if key in cache and vs.docs_of(car["id"]):   # 캐시만 믿지 않고 실제 색인도 확인
            return []
        added = []
        docs = car.get("docs") or []
        if not docs and not settings.offline_collect:   # 묶음에 없으면 영문 위키에서 직접
            hits = wikipedia.search("en", car["nameEn"], 1)
            if hits:
                t = hits[0]["title"]
                docs = [{"lang": "en", "title": t, "url": wikipedia.page_url("en", t), "text": wikipedia.extract("en", t)}]
        for d in docs:
            if vs.index_document(car, source_type="wiki", lang=d["lang"], title=d["title"], text=d["text"],
                                 url=d.get("url"), query="(차량 문서)"):
                added.append(d["title"])
        cache[key] = {"at": datetime.now().isoformat(timespec="seconds"), "selected": added, "rejected": []}
        _save(cache)
        return added


def extract_queries(car: dict, question: str) -> list[str]:
    """프롬프트 1 — 검색어 추출 (JSON 배열)."""
    out = parse_json(ask(prompts.QUERY_EXTRACT.format(max_queries=settings.max_queries, car=car_label(car), question=question), settings.utility_model), [])
    queries = [q.strip() for q in out if isinstance(q, str) and q.strip()]
    return list(dict.fromkeys(queries))[: settings.max_queries]


def select_candidates(car: dict, question: str, candidates: list[dict]) -> list[int]:
    """프롬프트 2 — 후보 선별 (선택한 번호의 JSON 배열)."""
    if not candidates:
        return []
    listing = "\n".join(f"[{i}] {c['title']} — {c['snippet'][:160]}" for i, c in enumerate(candidates))
    out = parse_json(ask(prompts.CANDIDATE_SELECT.format(max_pick=3, car=car_label(car), question=question, candidates=listing), settings.utility_model), [])
    return sorted({i for i in out if isinstance(i, int) and 0 <= i < len(candidates)})


def collect(car: dict, question: str, progress: Callable[[int, str], None] = lambda *_: None) -> dict:
    own = ensure_own_docs(car)

    cache = _load()
    qkey = _question_key(car["id"], question)
    repeated = qkey in cache
    if repeated:   # 같은 질문 — 프롬프트 1을 다시 부르지 않고 그때 뽑은 검색어를 쓴다
        queries = cache[qkey]["queries"]
        progress(0, ("이미 받은 질문 — 검색어 재사용: " + " · ".join(queries)) if queries else "이미 받은 질문 — 추가 검색어 없음")
    else:
        queries = extract_queries(car, question)
        progress(0, ("검색어: " + " · ".join(queries)) if queries else "추가 검색어 없음 (차량 문서로 충분)")

    new = [q for q in queries if _key(car["id"], q) not in cache]
    hits = [q for q in queries if q not in new]
    report = {"queries": queries, "question_cached": repeated, "cache_hits": hits, "own_docs": own,
              "selected": [], "rejected": [], "offline": settings.offline_collect}

    if not repeated and not new:   # 수집할 것이 없어도 질문 → 검색어는 기록해 둔다
        _remember_question(qkey, queries)

    if not new:
        progress(1, "이미 수집한 검색어 — 선별 생략" if queries else "선별할 후보 없음")
        progress(2, f"이미 수집된 문서 사용 ({len(vs.docs_of(car['id']))}건)")
        return report
    if settings.offline_collect:
        progress(1, "외부 호출 제한 모드 — 제공된 문서 묶음만 사용")
        progress(2, f"수집 생략 · 색인된 문서 {len(vs.docs_of(car['id']))}건")
        return report

    known = {d["title"] for d in vs.docs_of(car["id"])}
    candidates, origin = [], []
    for q in new:
        for c in wikipedia.search("ko", q, settings.search_per_query):
            if c["title"] not in known and c["title"] not in {x["title"] for x in candidates}:
                candidates.append(c)
                origin.append(q)
    picked = select_candidates(car, question, candidates)
    report["selected"] = [candidates[i]["title"] for i in picked]
    report["rejected"] = [c["title"] for i, c in enumerate(candidates) if i not in picked]
    progress(1, f"후보 {len(candidates)}건 중 {len(picked)}건 선별" + (f": {', '.join(report['selected'])}" if picked else ""))

    chunks = 0
    for i in picked:
        c = candidates[i]
        text = wikipedia.extract(c["lang"], c["title"])
        if text:
            chunks += vs.index_document(car, source_type="wiki", lang=c["lang"], title=c["title"], text=text,
                                        url=wikipedia.page_url(c["lang"], c["title"]), query=origin[i])
    progress(2, f"{len(picked)}건 수집 · 청크 {chunks}개 색인" if picked else "새로 색인할 문서 없음")

    with _lock:
        cache = _load()
        now = datetime.now().isoformat(timespec="seconds")
        for q in new:
            cache[_key(car["id"], q)] = {
                "at": now,
                "selected": [candidates[i]["title"] for i in picked if origin[i] == q],
                "rejected": [c["title"] for i, c in enumerate(candidates) if origin[i] == q and i not in picked],
            }
        if not repeated:
            cache[qkey] = {"at": now, "queries": queries}
        _save(cache)
    return report


def _remember_question(qkey: str, queries: list[str]) -> None:
    with _lock:
        cache = _load()
        cache[qkey] = {"at": datetime.now().isoformat(timespec="seconds"), "queries": queries}
        _save(cache)
