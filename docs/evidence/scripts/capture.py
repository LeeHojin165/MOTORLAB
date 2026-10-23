"""화면 캡처 (항목 26) — Chrome을 헤드리스로 띄우고 DevTools 프로토콜(CDP)로 조작해 PNG 저장

  python docs/evidence/scripts/capture.py <base_url> <장면 이름...>

장면은 아래 SCENES에 정의한다. 서버는 미리 띄워 둔다 (예: uvicorn backend.server:app --port 8010).
"""
import base64
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import quote

import requests
import websocket

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT = 9333
OUT = Path("docs/evidence/screens")


class Tab:
    def __init__(self, ws_url):
        self.ws = websocket.create_connection(ws_url, timeout=120, suppress_origin=True)
        self.i = 0

    def send(self, method, **params):
        self.i += 1
        self.ws.send(json.dumps({"id": self.i, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self.i:
                if "error" in msg:
                    raise RuntimeError(msg["error"])
                return msg.get("result", {})

    def js(self, expr):
        r = self.send("Runtime.evaluate", expression=expr, awaitPromise=True, returnByValue=True)
        return r.get("result", {}).get("value")

    def goto(self, url, settle=1.5):
        self.send("Page.navigate", url=url)
        self.wait("document.readyState === 'complete'", 30)
        time.sleep(settle)

    def wait(self, expr, timeout=180, every=0.5):
        end = time.time() + timeout
        while time.time() < end:
            if self.js(f"!!({expr})"):
                return True
            time.sleep(every)
        raise TimeoutError(expr)

    def shot(self, name):
        OUT.mkdir(parents=True, exist_ok=True)
        data = self.send("Page.captureScreenshot", format="png")["data"]
        (OUT / name).write_bytes(base64.b64decode(data))
        print("  saved", OUT / name)


def chat_url(base, car, q=None):
    return f"{base}/chat.html?car={car}" + (f"&q={quote(q)}" if q else "")


def set_settings(tab, base, **kw):
    """화면 설정(localStorage)을 바꾼 뒤 다시 읽히도록 한다."""
    tab.goto(base + "/chat.html", settle=0.5)
    s = {"top_k": 6, "search_type": "similarity", "compare_rag": False, "show_retrieved": False, "model": "gpt-4o", **kw}
    tab.js(f"localStorage.setItem('motorlab.settings', {json.dumps(json.dumps(s))}); sessionStorage.clear(); true")


DONE = "document.querySelector('#chatLog .steps.is-done')"
SCROLL_TOP = "(() => { const l = document.querySelector('#chatLog'); const m = [...l.querySelectorAll('.msg')].pop(); l.scrollTop = m ? m.offsetTop - 80 : 0; return true })()"


def scene_answer(tab, base):
    """13_progress(처리 중) → 08_citations · 15_screen · 19_source_types(완료)"""
    set_settings(tab, base)
    tab.goto(chat_url(base, "hyundai-pony-1975", "포니가 한국 최초의 고유 모델로 불리는 이유와 디자인은 누가 했어?"), settle=0)
    tab.wait("document.querySelector('#chatLog .steps:not(.is-done) .step.is-run')", 30)
    time.sleep(2.5)
    tab.shot("13_progress.png")
    tab.wait(DONE, 240)
    time.sleep(1)
    tab.js(SCROLL_TOP)
    tab.shot("15_screen.png")


def scene_citations(tab, base):
    """08 · 19 — 메타데이터와 위키백과가 함께 인용되는 제원 질문"""
    set_settings(tab, base)
    tab.goto(chat_url(base, "hyundai-pony-1975", "엔진 배기량과 최고출력은 얼마야?"), settle=0)
    tab.wait(DONE, 180)
    time.sleep(1)
    tab.js(SCROLL_TOP)
    tab.shot("08_citations.png")
    tab.shot("19_source_types.png")


def scene_no_evidence(tab, base):
    set_settings(tab, base)
    tab.goto(chat_url(base, "tesla-roadster-2008", "미국 출시 당시 가격은 얼마였어?"), settle=0)
    tab.wait(DONE, 180)
    time.sleep(1)
    tab.js(SCROLL_TOP)
    tab.shot("09_no_evidence.png")


def scene_switch(tab, base):
    """항목 10 — 포르쉐에서 대화 후 포니로 바꿔 질문"""
    set_settings(tab, base)
    tab.goto(chat_url(base, "porsche-911-992-2019", "이 차의 최고출력은?"), settle=0)
    tab.wait(DONE, 180)
    tab.shot("10_car_a.png")
    tab.goto(chat_url(base, "hyundai-pony-1975", "방금 말한 차보다 출력이 높아?"), settle=0)
    tab.wait(DONE, 180)
    time.sleep(1)
    tab.shot("10_car_b.png")


def scene_mmr(tab, base):
    """항목 6 · 16 — 같은 질문을 Top-k / 검색 방식만 바꿔 실행 (검색됐지만 인용되지 않은 근거까지 표시)"""
    q = "포드 모델 T는 어떻게 대량 생산되었고 가격은 어떻게 변했어?"
    for name, kw in (("06_topk3.png", {"top_k": 3}), ("16_similarity.png", {"top_k": 8}), ("16_mmr.png", {"top_k": 8, "search_type": "mmr"})):
        set_settings(tab, base, show_retrieved=True, **kw)
        tab.goto(chat_url(base, "ford-model-t-1908", q), settle=0)
        tab.wait(DONE, 180)
        time.sleep(1)
        tab.js("(() => { const s = document.querySelector('#chatLog .sources--retrieved') || document.querySelector('#chatLog .sources'); const l = document.querySelector('#chatLog'); l.scrollTop = s.offsetTop - 120; return true })()")
        tab.shot(name)


def scene_rag_compare(tab, base):
    set_settings(tab, base, compare_rag=True)
    tab.goto(chat_url(base, "kia-ev3-2024", "롱레인지 모델의 배터리 용량과 WLTP 1회 충전 주행거리는?"), settle=0)
    tab.wait(DONE, 180)
    time.sleep(1)
    tab.js(SCROLL_TOP)
    tab.shot("17_rag_compare.png")


def scene_explore(tab, base):
    set_settings(tab, base)
    tab.goto(base + "/index.html#workspace", settle=2)
    tab.js("document.querySelector('[data-view=\"explore\"], [data-tab=\"explore\"], [aria-controls=\"view-explore\"]')?.click(); true")
    time.sleep(0.5)
    tab.js("(() => { const i = document.querySelector('#exploreInput'); i.value = '1990년 이전에 나온 후륜구동 차량 중 수동 변속기를 쓰는 차'; document.querySelector('#exploreForm').requestSubmit(); return true })()")
    tab.wait("document.querySelector('#exploreResults .car-card, #exploreResults .empty-state, #exploreResults .alert')", 180)
    time.sleep(1.5)
    tab.js("(() => { const e = document.querySelector('#exploreSummary'); window.scrollTo(0, e.getBoundingClientRect().top + scrollY - 90); return true })()")
    time.sleep(0.8)
    tab.shot("11_explore.png")


def scene_fact(tab, base):
    set_settings(tab, base)
    tab.goto(base + "/index.html#workspace", settle=2)
    tab.js("document.querySelector('[data-view=\"fact\"], [data-tab=\"fact\"], [aria-controls=\"view-fact\"]')?.click(); true")
    time.sleep(0.5)
    tab.js("(() => { const s = document.querySelector('#factCar'); s.value = 'audi-quattro-1980'; s.dispatchEvent(new Event('change')); document.querySelector('#factClaim').value = '아우디 콰트로는 5기통 터보 엔진을 얹은 사륜구동 차다'; document.querySelector('#factForm').requestSubmit(); return true })()")
    tab.wait("document.querySelector('#factResult .sources, #factResult .notice, #factResult .alert')", 180)
    time.sleep(1.5)
    tab.js("(() => { const e = document.querySelector('#factForm'); window.scrollTo(0, e.getBoundingClientRect().top + scrollY - 90); return true })()")
    time.sleep(0.8)
    tab.shot("12_factcheck.png")


def scene_no_index(tab, base):
    tab.goto(chat_url(base, "ford-model-t-1908", "최고출력은?"), settle=0)
    tab.wait("document.querySelector('#chatLog .alert, #chatLog .warn, #chatLog .steps.is-done')", 60)
    time.sleep(1)
    tab.shot("13_no_index.png")


def scene_no_key(tab, base):
    tab.goto(chat_url(base, "ford-model-t-1908", "최고출력은?"), settle=0)
    tab.wait("document.querySelector('#chatLog .steps.is-done')", 60)
    time.sleep(1)
    tab.shot("13_no_key.png")


def scene_upstream(tab, base):
    tab.goto(chat_url(base, "ford-model-t-1908", "최고출력은?"), settle=0)
    tab.wait("document.querySelector('#chatLog .steps.is-done')", 120)
    time.sleep(1)
    tab.shot("21_error_screen.png")


SCENES = {k[6:]: v for k, v in globals().items() if k.startswith("scene_")}

if __name__ == "__main__":
    base, names = sys.argv[1].rstrip("/"), sys.argv[2:]
    profile = tempfile.mkdtemp(prefix="motorlab-cdp-")
    chrome = subprocess.Popen([CHROME, "--headless=new", f"--remote-debugging-port={PORT}", f"--user-data-dir={profile}",
                               "--window-size=1440,1000", "--hide-scrollbars", "--lang=ko-KR", "about:blank"])
    try:
        for _ in range(50):
            try:
                targets = requests.get(f"http://127.0.0.1:{PORT}/json", timeout=1).json()
                page = next(t for t in targets if t["type"] == "page")
                break
            except Exception:
                time.sleep(0.2)
        tab = Tab(page["webSocketDebuggerUrl"])
        tab.send("Page.enable")
        tab.send("Emulation.setDeviceMetricsOverride", width=1440, height=1000, deviceScaleFactor=1, mobile=False)
        for n in names:
            print("장면:", n)
            SCENES[n](tab, base)
    finally:
        chrome.terminate()
