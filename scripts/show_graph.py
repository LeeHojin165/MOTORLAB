"""LangGraph 구조 출력 (검증 4.3) — python -m scripts.show_graph"""
from backend.rag.graph import graph

if __name__ == "__main__":
    g = graph().get_graph()
    print("노드:", [n for n in g.nodes])
    print("간선:", [(e.source, e.target) for e in g.edges])
    print("\nMermaid:\n" + g.draw_mermaid())
