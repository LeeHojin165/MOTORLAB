"""LLM · 임베딩 생성과 공통 오류.

모델 이름이 claude- 로 시작하면 Anthropic Messages API, 그 외는 OpenAI 호환 API로 호출한다.
(SSAFY GMS는 두 API를 모두 같은 키로 중계한다)
"""
from __future__ import annotations

import json
import re
import time
from functools import lru_cache

import requests
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from backend.config import settings


class ServiceError(Exception):
    """화면에 보낼 수 있는 오류. message에는 내부 정보(키, 스택)를 넣지 않는다 (NF2004)."""

    def __init__(self, code: str, message: str = ""):
        super().__init__(message or code)
        self.code = code


def require_key() -> None:
    if not settings.has_api_key:
        raise ServiceError("NO_API_KEY", "API 키가 설정되지 않았습니다.")


def pick_model(model: str | None) -> str:
    """화면에서 보낸 모델 이름을 허용 목록으로 제한한다."""
    if not model:
        return settings.answer_model
    if model not in settings.models:
        raise ServiceError("BAD_REQUEST", "지원하지 않는 모델입니다.")
    return model


@lru_cache(maxsize=1)
def get_embeddings() -> OpenAIEmbeddings:
    require_key()
    return OpenAIEmbeddings(model=settings.embedding_model, api_key=settings.openai_api_key, base_url=settings.openai_base_url)


@lru_cache(maxsize=8)
def get_chat(model: str) -> ChatOpenAI:
    require_key()
    kwargs = {}
    # 추론형 모델(gpt-5, o-시리즈)은 temperature를 지원하지 않는다
    if not re.match(r"^(o\d|gpt-5)", model):
        kwargs["temperature"] = 0
    return ChatOpenAI(model=model, api_key=settings.openai_api_key, base_url=settings.openai_base_url,
                      timeout=60, max_retries=2, **kwargs)


def _ask_claude(prompt: str, model: str, retries: int = 3) -> str:
    for attempt in range(retries):
        r = requests.post(
            settings.anthropic_base_url.rstrip("/") + "/messages",
            headers={"x-api-key": settings.anthropic_api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            json={"model": model, "max_tokens": 2048, "temperature": 0, "messages": [{"role": "user", "content": prompt}]},
            timeout=90,
        )
        if r.status_code in (429, 500, 502, 503, 529) and attempt < retries - 1:
            time.sleep(2 ** (attempt + 1))
            continue
        r.raise_for_status()
        return "".join(b.get("text", "") for b in r.json().get("content", []) if b.get("type") == "text")
    return ""


def ask(prompt: str, model: str | None = None) -> str:
    require_key()
    model = model or settings.answer_model
    if model.startswith("claude"):
        return _ask_claude(prompt, model).strip()
    return get_chat(model).invoke(prompt).content.strip()


def parse_json(text: str, default):
    """LLM 응답에서 첫 JSON 값을 꺼낸다. 코드 블록이나 앞뒤 설명이 섞여도 동작."""
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    pairs = sorted((("[", "]"), ("{", "}")), key=lambda p: (text.find(p[0]) == -1, text.find(p[0])))
    for opener, closer in pairs:   # 먼저 나오는 괄호 종류부터 시도
        start = text.find(opener)
        end = text.rfind(closer)
        if start != -1 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                continue
    return default
