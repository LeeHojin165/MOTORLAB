"""항목 17·18 (F2015) — 대표 질문을 RAG 없이 / 근거를 붙여 각각 답하게 해 나란히 기록

서비스와 같은 경로(chat_events, compare_rag=True)를 쓴다: 같은 모델이 같은 질문에
프롬프트 3(근거만 사용)과 NO_RAG 프롬프트(근거 없음)로 각각 답한다.
결과: docs/evidence/17_rag_compare.json
"""
import json
import time
from pathlib import Path

from backend.domain.cars import get_car
from backend.services.chat import chat_events

QUESTIONS = [
    ("hyundai-pony-1975", "엔진 배기량과 최고출력은 얼마야?"),
    ("kia-ev3-2024", "롱레인지 모델의 배터리 용량과 WLTP 1회 충전 주행거리는?"),
    ("bmw-ix3-2026", "최고출력과 배터리 용량은 얼마야?"),
    ("hyundai-ioniq9-2025", "퍼포먼스 AWD의 0-100km/h 가속 시간과 최대토크는?"),
    ("daewoo-tico-1991", "공차중량과 최고출력은 얼마야?"),
    ("tesla-roadster-2008", "미국 출시 당시 가격은 얼마였어?"),
    ("kgm-torres-evx-2023", "배터리 제조사와 배터리 종류는 뭐야?"),
]

out = []
for car_id, q in QUESTIONS:
    car = get_car(car_id)
    t = time.time()
    data = None
    for e in chat_events(car_id, q, 6, "similarity", True, "gpt-4o"):
        if e["type"] == "result":
            data = e["data"]
        elif e["type"] == "error":
            data = {"error": e["code"]}
    rec = {"car": f"{car['year']} {car['name']}", "car_id": car_id, "question": q, "seconds": round(time.time() - t, 1),
           "norag_answer": data.get("norag_answer"), "rag_answer": data.get("answer"),
           "citations": [{"n": c["n"], "type": c["type"], "lang": c["lang"], "title": c["title"], "url": c["url"]}
                         for c in data.get("citations", [])]}
    out.append(rec)
    print(f"■ {rec['car']} — {q}  ({rec['seconds']}초)")
    print("  [RAG 없이]", rec["norag_answer"])
    print("  [RAG]", rec["rag_answer"])
    print("  [인용 근거]", [(c["n"], c["type"], c["title"]) for c in rec["citations"]])
    print()

Path("docs/evidence/17_rag_compare.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
