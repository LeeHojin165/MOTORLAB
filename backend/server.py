"""FastAPI 서버 (F2013: 화면과 서버 분리) — 실행: uvicorn backend.server:app --reload

요청 · 응답 형식
  GET  /api/status                → {meta_count, doc_count, chunk_count, api_key_ok, settings}
  GET  /api/cars                  → [Car]
  GET  /api/cars/{car_id}/docs    → [{title, source_type, lang, url, chunks}]
  POST /api/chat/stream           {car_id, question, top_k?, search_type?, compare_rag?, model?}
                                  → text/event-stream
                                    data: {"type":"progress","step":0-4,"label","detail"}
                                    data: {"type":"result","data":{answer, citations, retrieved, collect, docs, norag_answer?}}
                                    data: {"type":"error","code":"NO_API_KEY|NO_INDEX|NO_RESULT|UPSTREAM"}
  POST /api/explore               {query}            → {conditions, candidates, results:[{car_id, reason}]}
  POST /api/compare               {car_ids}          → {summary, citations}
  POST /api/factcheck             {car_id, claim}    → {verdict, explanation, citations}
  오류(JSON API): HTTP 4xx/5xx + {"error": {"code", "message"}}
"""
from __future__ import annotations

import json
import logging
from typing import Literal

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from backend.config import settings
from backend.domain.cars import load_cars, public_car
from backend.llm import ServiceError
from backend.services import features
from backend.services.chat import chat_events
from backend.store import vectorstore as vs

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("motorlab")

app = FastAPI(title="MOTORLAB API", version="1.0")
STATUS = {"NO_API_KEY": 503, "NO_INDEX": 503, "NO_RESULT": 404, "UPSTREAM": 502, "BAD_REQUEST": 400}


@app.exception_handler(ServiceError)
async def service_error(_: Request, e: ServiceError):
    return JSONResponse(status_code=STATUS.get(e.code, 500), content={"error": {"code": e.code, "message": str(e)}})


@app.exception_handler(Exception)
async def unknown_error(_: Request, e: Exception):
    log.exception("unhandled")   # 화면에는 오류 추적 정보를 보내지 않는다 (NF2004)
    return JSONResponse(status_code=500, content={"error": {"code": "UPSTREAM", "message": "일시적인 오류가 발생했습니다."}})


class ChatIn(BaseModel):
    car_id: str
    question: str = Field(min_length=1, max_length=500)
    top_k: int = Field(default_factory=lambda: settings.top_k, ge=2, le=15)
    search_type: Literal["similarity", "mmr"] = Field(default_factory=lambda: settings.search_type)
    compare_rag: bool = False
    model: str | None = None


class ExploreIn(BaseModel):
    query: str = Field(min_length=1, max_length=300)
    model: str | None = None


class CompareIn(BaseModel):
    car_ids: list[str] = Field(min_length=2, max_length=3)
    model: str | None = None


class FactIn(BaseModel):
    car_id: str
    claim: str = Field(min_length=1, max_length=300)
    model: str | None = None


@app.get("/api/status")
def status():
    return {
        **vs.counts(),
        "api_key_ok": settings.has_api_key,
        "settings": {
            "chunk_size": settings.chunk_size, "chunk_overlap": settings.chunk_overlap, "top_k": settings.top_k,
            "search_type": settings.search_type, "mmr_fetch_k": settings.mmr_fetch_k,
            "answer_model": settings.answer_model, "utility_model": settings.utility_model,
            "models": list(settings.models), "embedding_model": settings.embedding_model,
            "offline_collect": settings.offline_collect,
        },
    }


@app.get("/api/cars")
def cars():
    return [public_car(c) for c in load_cars()]


@app.get("/api/cars/{car_id}/docs")
def car_docs(car_id: str):
    return vs.docs_of(car_id)


@app.post("/api/chat/stream")
def chat_stream(body: ChatIn):
    def sse():
        for event in chat_events(body.car_id, body.question.strip(), body.top_k, body.search_type, body.compare_rag, body.model):
            yield "data: " + json.dumps(event, ensure_ascii=False) + "\n\n"
    return StreamingResponse(sse(), media_type="text/event-stream", headers={"Cache-Control": "no-cache"})


@app.post("/api/explore")
def explore(body: ExploreIn):
    return features.explore(body.query.strip(), body.model)


@app.post("/api/compare")
def compare(body: CompareIn):
    return features.compare(body.car_ids, body.model)


@app.post("/api/factcheck")
def factcheck(body: FactIn):
    return features.factcheck(body.car_id, body.claim.strip(), body.model)


# 화면 (같은 주소에서 제공하므로 CORS 설정이 필요 없다)
app.mount("/", StaticFiles(directory=settings.frontend_dir, html=True), name="frontend")
