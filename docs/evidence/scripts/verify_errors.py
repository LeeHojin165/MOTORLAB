"""항목 13·21 — 화면이 받는 이벤트/응답 그대로 출력 (FastAPI TestClient)"""
import sys
from fastapi.testclient import TestClient
from backend.server import app

c = TestClient(app)
print("상황:", sys.argv[1])
st = c.get("/api/status").json()
print("GET /api/status → api_key_ok:", st["api_key_ok"], "· meta_count:", st["meta_count"])
r = c.post("/api/chat/stream", json={"car_id": "ford-model-t-1908", "question": "최고출력은?"})
print("POST /api/chat/stream →", r.status_code)
print(r.text.strip())
r = c.post("/api/explore", json={"query": "전기차"})
print("POST /api/explore →", r.status_code, r.text)
