"""도메인 특화 기능 (F2010) 과 조건 기반 차량 탐색 (F2011)

- explore   : 메타데이터 색인에서 후보를 찾고, LLM이 조건에 맞는 차량만 고른다
- compare   : 2~3대의 메타데이터 청크를 근거로 제원 차이를 요약한다
- factcheck : 차량 문서를 검색해 주장이 사실인지 판정한다
모두 검색된 문서만 근거로 쓰고, 인용된 근거를 함께 돌려준다.
"""
from __future__ import annotations

from backend.collect import collector
from backend.domain import prompts
from backend.domain.cars import get_car
from backend.llm import ServiceError, ask, parse_json, pick_model, require_key
from backend.rag.graph import cited, drop_unknown, format_context, normalize_citations, public, retrieve
from backend.store import vectorstore as vs


def _ready() -> None:
    require_key()
    if vs.raw(vs.META).count() == 0:
        raise ServiceError("NO_INDEX", "색인이 없습니다.")


def explore(query: str, model: str | None = None) -> dict:
    _ready()
    model = pick_model(model)
    k = min(20, vs.raw(vs.META).count())
    hits = vs.store(vs.META).similarity_search(query, k=k)
    listing = "\n\n".join(f"car_id={d.metadata['car_id']}\n{d.page_content}" for d in hits)
    out = parse_json(ask(prompts.EXPLORE.format(query=query, candidates=listing), model), {})
    allowed = {d.metadata["car_id"] for d in hits}
    results = [r for r in out.get("results", []) if isinstance(r, dict) and r.get("car_id") in allowed]
    return {"conditions": [c for c in out.get("conditions", []) if isinstance(c, str)], "candidates": len(hits),
            "results": [{"car_id": r["car_id"], "reason": str(r.get("reason", ""))} for r in results]}


def compare(car_ids: list[str], model: str | None = None) -> dict:
    _ready()
    model = pick_model(model)
    evidence = []
    for cid in car_ids:
        doc = vs.meta_chunk(cid)
        if doc is None:
            raise ServiceError("NO_RESULT", "차량을 찾을 수 없습니다.")
        evidence.append({"n": len(evidence) + 1, "chunk_id": cid, "type": "meta", "lang": "", "title": doc.metadata["title"],
                         "url": None, "page": None, "score": None, "query": "", "text": doc.page_content})
    summary = drop_unknown(normalize_citations(ask(prompts.COMPARE.format(context=format_context(evidence)), model)), evidence)
    return {"summary": summary, "citations": [public(e) for e in cited(summary, evidence)], "model": model}


def factcheck(car_id: str, claim: str, model: str | None = None) -> dict:
    _ready()
    model = pick_model(model)
    car = get_car(car_id)
    if car is None:
        raise ServiceError("NO_RESULT", "차량을 찾을 수 없습니다.")
    collector.ensure_own_docs(car)
    evidence = retrieve({"car": car, "question": claim, "top_k": 6, "search_type": "mmr"})["evidence"]
    out = parse_json(ask(prompts.FACTCHECK.format(car=f"{car['name']} ({car['year']})", claim=claim,
                                                  context=format_context(evidence)), model), {})
    verdict = out.get("verdict") if out.get("verdict") in ("true", "false", "unknown") else "unknown"
    explanation = drop_unknown(normalize_citations(str(out.get("explanation") or "판정에 필요한 근거를 찾지 못했습니다.")), evidence)
    return {"verdict": verdict, "explanation": explanation, "citations": [public(e) for e in cited(explanation, evidence)], "model": model}
