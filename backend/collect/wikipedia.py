"""위키백과 API 클라이언트 (NF2006: 호출 간격 · 재시도 · 식별 가능한 User-Agent)"""
from __future__ import annotations

import html
import re
import threading
import time

import requests

from backend.config import settings

UA = f"MotorLab/1.0 ({settings.wiki_contact}) python-requests"
_lock = threading.Lock()
_last = 0.0


def _get(lang: str, params: dict, retries: int = 4) -> dict:
    global _last
    params = {"format": "json", "formatversion": "2", **params}
    for attempt in range(retries):
        with _lock:   # 여러 요청이 동시에 와도 간격을 지킨다
            wait = settings.wiki_interval - (time.time() - _last)
            if wait > 0:
                time.sleep(wait)
            _last = time.time()
        try:
            r = requests.get(f"https://{lang}.wikipedia.org/w/api.php", params=params,
                             headers={"User-Agent": UA}, timeout=20)
            if r.status_code in (429, 500, 502, 503, 504):
                raise requests.HTTPError(response=r)
            r.raise_for_status()
            return r.json()
        except (requests.HTTPError, requests.ConnectionError, requests.Timeout) as e:
            if attempt == retries - 1:
                raise
            resp = getattr(e, "response", None)
            delay = int(resp.headers.get("Retry-After", 0)) if resp is not None else 0
            time.sleep(min(delay or 2 ** (attempt + 1), 60))
    return {}


def search(lang: str, query: str, limit: int) -> list[dict]:
    data = _get(lang, {"action": "query", "list": "search", "srsearch": query, "srlimit": limit, "srprop": "snippet"})
    return [{"lang": lang, "title": x["title"], "snippet": html.unescape(re.sub(r"<[^>]+>", "", x.get("snippet", "")))}
            for x in data.get("query", {}).get("search", [])]


def extract(lang: str, title: str, limit: int = 12000) -> str:
    data = _get(lang, {"action": "query", "prop": "extracts", "explaintext": 1, "exsectionformat": "wiki",
                       "titles": title, "redirects": 1})
    pages = data.get("query", {}).get("pages", [])
    text = pages[0].get("extract", "") if pages else ""
    for marker in ("\n== 같이 보기", "\n== 각주", "\n== 참고 문헌", "\n== 외부 링크", "\n== See also", "\n== References", "\n== External links"):
        i = text.find(marker)
        if i > 0:
            text = text[:i]
    return re.sub(r"\n{3,}", "\n\n", text).strip()[:limit]


def page_url(lang: str, title: str) -> str:
    return f"https://{lang}.wikipedia.org/wiki/" + requests.utils.quote(title.replace(" ", "_"))
