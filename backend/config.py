"""실행 설정 — 모든 값은 환경변수(.env)에서 읽는다. API 키는 코드에 넣지 않는다(NF2003)."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


def _int(name: str, default: int) -> int:
    return int(os.getenv(name, default))


def _float(name: str, default: float) -> float:
    return float(os.getenv(name, default))


def _chroma_dir() -> Path:
    """ChromaDB(1.5.x)는 경로에 한글 등 비ASCII 문자가 있으면 HNSW 인덱스를 다시 읽지 못한다.
    CHROMA_DIR이 없으면 프로젝트 data/chroma를 쓰되, 경로가 ASCII가 아니면 ASCII 경로로 옮긴다."""
    if os.getenv("CHROMA_DIR"):
        return Path(os.environ["CHROMA_DIR"])
    for cand in (ROOT / "data" / "chroma", Path.home() / ".motorlab" / "chroma",
                 Path(os.getenv("PUBLIC", "C:/Users/Public")) / "motorlab" / "chroma"):
        if str(cand).isascii():
            return cand
    return ROOT / "data" / "chroma"


@dataclass(frozen=True)
class Settings:
    # LLM · 임베딩 (OpenAI 호환. SSAFY GMS는 OPENAI_BASE_URL만 바꾸면 된다)
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", "").strip())
    openai_base_url: str | None = field(default_factory=lambda: os.getenv("OPENAI_BASE_URL") or None)
    # Claude (Anthropic Messages API). GMS는 같은 키를 쓰므로 비어 있으면 OPENAI_API_KEY를 쓴다
    anthropic_api_key: str = field(default_factory=lambda: (os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY", "")).strip())
    anthropic_base_url: str = field(default_factory=lambda: os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com/v1"))
    # 답변 생성(프롬프트 3)·특화 기능 기본 모델 / 검색어 추출·후보 선별(프롬프트 1·2) 모델 / 화면에서 고를 수 있는 모델
    answer_model: str = field(default_factory=lambda: os.getenv("ANSWER_MODEL", "gpt-4o"))
    utility_model: str = field(default_factory=lambda: os.getenv("UTILITY_MODEL", "gpt-4o-mini"))
    models: tuple = field(default_factory=lambda: tuple(m.strip() for m in os.getenv(
        "MODELS", "gpt-4o,gpt-4o-mini,claude-sonnet-4-5-20250929").split(",") if m.strip()))
    embedding_model: str = field(default_factory=lambda: os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"))

    # 청킹 · 검색 (F2005 / F2006 / F2014)
    chunk_size: int = field(default_factory=lambda: _int("CHUNK_SIZE", 1000))
    chunk_overlap: int = field(default_factory=lambda: _int("CHUNK_OVERLAP", 200))
    top_k: int = field(default_factory=lambda: _int("TOP_K", 6))
    search_type: str = field(default_factory=lambda: os.getenv("SEARCH_TYPE", "similarity"))  # similarity | mmr
    mmr_fetch_k: int = field(default_factory=lambda: _int("MMR_FETCH_K", 20))
    mmr_lambda: float = field(default_factory=lambda: _float("MMR_LAMBDA", 0.5))

    # 문서 수집 (F2004 / NF2002 / NF2006)
    wiki_contact: str = field(default_factory=lambda: os.getenv("WIKI_CONTACT", "student project"))
    wiki_interval: float = field(default_factory=lambda: _float("WIKI_INTERVAL", 1.0))
    search_per_query: int = field(default_factory=lambda: _int("SEARCH_PER_QUERY", 4))
    max_queries: int = field(default_factory=lambda: _int("MAX_QUERIES", 3))
    offline_collect: bool = field(default_factory=lambda: os.getenv("OFFLINE_COLLECT", "0") == "1")

    # 경로
    data_dir: Path = ROOT / "data"
    chroma_dir: Path = field(default_factory=_chroma_dir)
    frontend_dir: Path = ROOT / "frontend"

    @property
    def has_api_key(self) -> bool:
        return bool(self.openai_api_key)


settings = Settings()
