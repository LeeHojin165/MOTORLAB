"""항목 10·11·12 — 서비스 함수 호출"""
import json
from backend.domain.cars import get_car, load_cars
from backend.services import features
from backend.services.chat import chat_events


def answer(car_id, q):
    for e in chat_events(car_id, q, 6, "similarity", False):
        if e["type"] == "result":
            return e["data"]["answer"]
        if e["type"] == "error":
            return f"오류 {e['code']}"


print("=" * 20, "항목 10 — 항목 A(포르쉐 911 992)에서 대화 후 항목 B(현대 포니)로 바꿔 질문")
print("A 질문: 이 차의 최고출력은?\nA 답변:", answer("porsche-911-992-2019", "이 차의 최고출력은?"))
print("\nB 질문: 방금 말한 차보다 출력이 높아?\nB 답변:", answer("hyundai-pony-1975", "방금 말한 차보다 출력이 높아?"))

print("\n" + "=" * 20, "항목 11 — 조건 기반 탐색")
query = "1990년 이전에 나온 후륜구동 차량 중 수동 변속기를 쓰는 차"
out = features.explore(query)
print("질의:", query)
print("읽어 낸 조건:", out["conditions"], "/ 후보", out["candidates"], "대")
cars = {c["id"]: c for c in load_cars()}
bad = 0
for r in out["results"]:
    c = cars[r["car_id"]]
    ok = c["year"] < 1990 and c["driveCode"] == "RWD" and ("수동" in str(c.get("transmission")) or "MT" in str(c.get("transmission")))
    bad += not ok
    print(f"  {'OK ' if ok else 'NG '} {c['year']} {c['name']} · 구동 {c['driveCode']} · 변속기 {c.get('transmission')}")
print(f"결과 {len(out['results'])}대 중 조건 불일치 {bad}대")

print("\n" + "=" * 20, "항목 12 — 특화 기능(제원 비교 · 사실 확인)의 근거")
cmp = features.compare(["porsche-911-992-2019", "hyundai-pony-1975"])
print("비교 요약:\n" + cmp["summary"])
print("근거:", [(c["n"], c["type"], c["title"]) for c in cmp["citations"]])
fc = features.factcheck("audi-quattro-1980", "아우디 콰트로는 5기통 터보 엔진을 얹은 사륜구동 차다")
print("\n사실 확인 판정:", fc["verdict"])
print(fc["explanation"])
print("근거:", [(c["n"], c["type"], c["title"]) for c in fc["citations"]])
