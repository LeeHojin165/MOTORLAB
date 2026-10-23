"""항목 6·7·8·9·16·20 — 서비스 경로(chat_events)와 retrieve 노드를 그대로 호출"""
import re, time
from backend.domain.cars import get_car
from backend.rag.graph import graph, retrieve
from backend.services.chat import chat_events

car = get_car("ford-model-t-1908")
Q = "포드 모델 T는 어떻게 대량 생산되었고 가격은 어떻게 변했어?"


def ev_list(k, st):
    ev = retrieve({"car": car, "question": Q, "top_k": k, "search_type": st})["evidence"]
    return [f"[{e['n']}] {e['type']} · {e['title']} · {e['chunk_id']}" for e in ev]


def run(question, label, **kw):
    t = time.time()
    result = None
    for e in chat_events(car["id"], question, kw.get("top_k", 6), kw.get("search_type", "similarity"), kw.get("compare_rag", False)):
        if e["type"] == "progress":
            print(f"   [진행 {e['step']} {e['label']}] {e['detail']}")
        elif e["type"] == "result":
            result = e["data"]
        else:
            print("   오류:", e)
    print(f"--- {label}: {time.time() - t:.1f}초")
    return result


print("=" * 20, "항목 7 — LangGraph 구조")
g = graph().get_graph()
print("노드:", list(g.nodes))
print("간선:", [(e.source, e.target) for e in g.edges])

print("\n" + "=" * 20, "항목 6 — Top-k 3 vs 8 (유사도)")
for k in (3, 8):
    print(f"Top-k={k}:")
    print("\n".join("   " + x for x in ev_list(k, "similarity")))

print("\n" + "=" * 20, "항목 16 — 유사도 vs MMR (Top-k=6)")
a, b = ev_list(6, "similarity"), ev_list(6, "mmr")
for i in range(max(len(a), len(b))):
    print(f"   유사도 {a[i] if i < len(a) else '-':<70} | MMR {b[i] if i < len(b) else '-'}")

print("\n" + "=" * 20, "항목 8·20 — 답변 생성, 첫 번째/두 번째 처리 시간")
r1 = run(Q, "1회차")
r2 = run(Q, "2회차")
print("\n답변:\n" + r2["answer"])
nums = sorted({int(n) for n in re.findall(r"\[근거 (\d+)\]", r2["answer"])})
print("\n본문 인용 번호:", nums)
print("화면 근거 목록:", [(c["n"], c["type"], c["title"]) for c in r2["citations"]])
print("일치:", nums == [c["n"] for c in r2["citations"]])

print("\n" + "=" * 20, "항목 9 — 문서에 없는 질문")
r3 = run("포드 모델 T의 2024년 경매 최고 낙찰가는 얼마야?", "문서 밖 질문")
print("답변:\n" + r3["answer"])
print("인용된 근거:", [(c["n"], c["title"]) for c in r3["citations"]])
