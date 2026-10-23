"""항목 3·4: 같은 질문 세 번(세 번째는 띄어쓰기·문장부호만 바꿈) — 검색어 / 선별 / 버림 / 처리 시간"""
import sys, time
from backend.collect import collector
from backend.domain.cars import get_car
from backend.store import vectorstore as vs

car = get_car(sys.argv[1])
q = sys.argv[2]
variant = "  " + q.rstrip("?") + "  "   # 공백과 물음표만 다른 같은 질문
print(f"차량: {car['name']} / 질문: {q}")
for run, question in ((1, q), (2, q), (3, variant)):
    before = vs.counts()["chunk_count"]
    t = time.time()
    rep = collector.collect(car, question, lambda s, d: print(f"   [진행 {s}] {d}"))
    dt = time.time() - t
    print(f"--- {run}회차{' (공백·물음표만 다르게)' if run == 3 else ''}: {dt:.1f}초 · 청크 {before} → {vs.counts()['chunk_count']}")
    print("   질문 캐시 적중(프롬프트 1 생략):", rep.get("question_cached"))
    print("   검색어(프롬프트 1):", rep["queries"])
    print("   검색어 캐시 적중:", rep["cache_hits"])
    print("   색인된 문서(프롬프트 2 선별):", rep["selected"])
    print("   버려진 문서:", rep["rejected"])
