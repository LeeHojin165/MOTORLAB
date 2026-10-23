"""질의응답 서비스 — 수집 → LangGraph(retrieve → generate) 를 진행 상태와 함께 흘려보낸다 (F2009 · F2012)"""
from __future__ import annotations

import logging
import queue
import threading
from typing import Iterator

from backend.collect import collector
from backend.domain import prompts
from backend.domain.cars import get_car
from backend.llm import ServiceError, ask, pick_model, require_key
from backend.rag.graph import graph, public
from backend.store import vectorstore as vs

log = logging.getLogger("motorlab")
STEPS = ["검색어 추출", "후보 문서 선별", "문서 수집 · 색인", "근거 검색", "답변 생성"]


def _run(car_id: str, question: str, top_k: int, search_type: str, compare_rag: bool, model: str | None, emit) -> None:
    require_key()
    model = pick_model(model)
    car = get_car(car_id)
    if car is None:
        raise ServiceError("NO_RESULT", "차량을 찾을 수 없습니다.")
    if vs.raw(vs.META).count() == 0:
        raise ServiceError("NO_INDEX", "색인이 없습니다.")
    progress = lambda step, detail: emit({"type": "progress", "step": step, "label": STEPS[step], "detail": detail})

    progress(0, "검색어를 추출하는 중")
    try:
        report = collector.collect(car, question, progress)
    except ServiceError:
        raise
    except Exception:   # 외부 문서 출처 장애 — 이미 색인된 문서로 계속 진행
        log.exception("collect failed")
        report = {"queries": [], "cache_hits": [], "selected": [], "rejected": [], "error": True}
        progress(2, "외부 문서 수집에 실패해 이미 색인된 문서로 답합니다")

    progress(3, f"{'MMR' if search_type == 'mmr' else '유사도'} 검색 · Top-{top_k}")
    state = {"car": car, "question": question, "top_k": top_k, "search_type": search_type, "model": model}
    for update in graph().stream(state, stream_mode="updates"):
        if "retrieve" in update:
            state.update(update["retrieve"])
            ev = state["evidence"]
            progress(3, f"근거 {len(ev)}건 (메타데이터 1 + 문서 {len(ev) - 1}, 중복 제거 후)")
            progress(4, f"{model}로 근거 기반 답변 작성 중")
        if "generate" in update:
            state.update(update["generate"])

    result = {
        "answer": state["answer"],
        "citations": [public(e) for e in state["citations"]],
        "retrieved": [public(e) for e in state["evidence"]],
        "collect": report,
        "docs": vs.docs_of(car_id),
        "model": model,
    }
    if compare_rag:   # F2015: 같은 질문을 근거 없이
        result["norag_answer"] = ask(prompts.NO_RAG.format(car=f"{car['name']} ({car['year']})", question=question), model)
    emit({"type": "result", "data": result})


def chat_events(car_id: str, question: str, top_k: int, search_type: str, compare_rag: bool, model: str | None = None) -> Iterator[dict]:
    q: queue.Queue = queue.Queue()

    def worker():
        try:
            _run(car_id, question, top_k, search_type, compare_rag, model, q.put)
        except ServiceError as e:
            q.put({"type": "error", "code": e.code})
        except Exception:
            log.exception("chat failed")   # 상세 내용은 서버 로그에만 (NF2004)
            q.put({"type": "error", "code": "UPSTREAM"})
        finally:
            q.put(None)

    threading.Thread(target=worker, daemon=True).start()
    while (item := q.get()) is not None:
        yield item
