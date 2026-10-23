/* =========================================================
   MOTORLAB — 서버 통신 (요청·응답 형식은 backend/server.py 상단 주석 참고)
   화면은 FastAPI가 같은 주소에서 제공한다 → http://localhost:8000
   ========================================================= */
window.API = (function () {
  const BASE = location.protocol === "file:" ? "http://localhost:8000" : "";

  class ApiError extends Error {
    constructor(code, message) { super(message || code); this.code = code; }
  }

  async function request(path, body) {
    let res;
    try {
      res = await fetch(BASE + path, body
        ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }
        : undefined);
    } catch {
      throw new ApiError("NETWORK", "서버에 연결할 수 없습니다.");
    }
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new ApiError(data.error?.code || (res.status === 422 ? "BAD_REQUEST" : "UPSTREAM"), data.error?.message);
    return data;
  }

  // POST /api/chat/stream — Server-Sent Events 형식으로 진행 상태와 결과를 받는다
  async function chatStream(body, onEvent) {
    let res;
    try {
      res = await fetch(BASE + "/api/chat/stream", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
    } catch {
      throw new ApiError("NETWORK", "서버에 연결할 수 없습니다.");
    }
    if (!res.ok || !res.body) {
      const data = await res.json().catch(() => ({}));
      throw new ApiError(data.error?.code || "UPSTREAM");
    }
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buf = "", result = null;
    for (;;) {
      const { value, done } = await reader.read();
      if (done) break;
      buf += decoder.decode(value, { stream: true });
      let i;
      while ((i = buf.indexOf("\n\n")) >= 0) {
        const line = buf.slice(0, i).replace(/^data: /, "");
        buf = buf.slice(i + 2);
        if (!line.trim()) continue;
        const ev = JSON.parse(line);
        if (ev.type === "error") throw new ApiError(ev.code);
        if (ev.type === "result") result = ev.data;
        else onEvent(ev);
      }
    }
    if (!result) throw new ApiError("UPSTREAM");
    return result;
  }

  return {
    ApiError,
    status: () => request("/api/status"),
    cars: () => request("/api/cars"),
    carDocs: (id) => request(`/api/cars/${encodeURIComponent(id)}/docs`),
    chatStream,
    explore: (query, model) => request("/api/explore", { query, model }),
    compare: (car_ids, model) => request("/api/compare", { car_ids, model }),
    factcheck: (car_id, claim, model) => request("/api/factcheck", { car_id, claim, model }),
  };
})();
