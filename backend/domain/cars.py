"""자동차 도메인 데이터 (데이터 준비 영역 — 도메인에 묶인 부분은 이 패키지에 모은다, NF2005)

- data/cars_source.json   : 직접 정리한 제원 (항목 메타데이터 원본)
- data/cars_enriched.json : scripts/build_data.py 결과 (사진 정보 + 위키 문서 묶음 포함)
"""
from __future__ import annotations

import json
from functools import lru_cache

from backend.config import settings

FUEL = {"gasoline": "가솔린", "diesel": "디젤", "electric": "전기", "hybrid": "하이브리드", "hydrogen": "수소전기"}
SOURCE_LABEL = {"meta": "차량 메타데이터", "wiki": "위키백과", "pdf": "PDF 문서"}


@lru_cache(maxsize=1)
def load_cars() -> list[dict]:
    enriched = settings.data_dir / "cars_enriched.json"
    path = enriched if enriched.exists() else settings.data_dir / "cars_source.json"
    cars = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(cars, dict):
        cars = cars["cars"]
    return sorted(cars, key=lambda c: (c["year"], c["name"]))


def get_car(car_id: str) -> dict | None:
    return next((c for c in load_cars() if c["id"] == car_id), None)


def public_car(c: dict) -> dict:
    """화면에 내려줄 필드 (문서 본문은 빼고 제목만)."""
    out = {k: v for k, v in c.items() if k not in ("docs", "wikiTitles", "imageFile")}
    out["bundleDocs"] = [{"title": d["title"], "lang": d["lang"]} for d in c.get("docs", [])]
    return out


def index_text(c: dict) -> str:
    """항목 1건 = 검색 텍스트 1개 (F2001).
    사용자가 이름·연도·제조사뿐 아니라 '후륜 수동 쿠페', '제로백 4초 전기차'처럼
    제원 조건으로도 찾기 때문에 모든 제원 속성을 한 텍스트에 넣는다."""
    s = c.get("suspension") or {}
    na = "확인되지 않음"

    def v(x, unit=""):
        return f"{x:,}{unit}" if isinstance(x, (int, float)) and not isinstance(x, bool) else (x or na)

    return "\n".join(filter(None, [
        f"차량: {c['name']} ({c['nameEn']}) · {c['year']}년 · 제조사 {c['maker']} · {c['country']}",
        f"기준 트림: {c.get('trim') or na} · 차종: {c['bodyType']} · 동력원: {FUEL[c['fuel']]}",
        f"엔진/모터: {v(c.get('engine'))} · 변속기: {v(c.get('transmission'))} · 구동방식: {c['drive']} ({c['driveCode']})",
        f"최고출력: {v(c.get('powerText'))} · 최대토크: {v(c.get('torqueNm'), ' N·m')}",
        f"0–100km/h: {v(c.get('zeroTo100'), '초')} · 최고속도: {v(c.get('topSpeed'), ' km/h')} · 공인 연비/주행거리: {v(c.get('efficiency'))}",
        f"전장 {v(c.get('length'), 'mm')} · 전폭 {v(c.get('width'), 'mm')} · 전고 {v(c.get('height'), 'mm')} · 휠베이스 {v(c.get('wheelbase'), 'mm')} · 공차중량 {v(c.get('weight'), 'kg')}",
        f"서스펜션: 앞 {s.get('front') or na} / 뒤 {s.get('rear') or na}",
        f"승차감: {c['ride']}" if c.get("ride") else None,
    ]))


def own_doc_titles(c: dict) -> list[tuple[str, str]]:
    """선택한 차량 자체를 다룬 문서 (lang, title) — 수집 시 항상 포함한다 (F2003/F2004)."""
    return [(d["lang"], d["title"]) for d in c.get("docs", [])]
