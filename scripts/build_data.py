"""MOTORLAB 데이터 준비 스크립트 (1회 실행용, 서버 아님)

data/cars_source.json(직접 정리한 제원)을 읽어 다음을 만든다.
  1) 위키백과 문서 본문(한국어·영어) 수집      → 브라우저 내 검색에 쓰는 외부 문서
  2) 대표 사진 다운로드 + 라이선스·저작자 기록  → frontend/assets/cars/
  3) 영문 위키 인포박스 치수와 제원 대조        → data/verify_report.md
  4) 서버가 읽는 차량 데이터 + 문서 묶음          → data/cars_enriched.json
  5) 출처와 이용 조건 목록                       → data/SOURCES.md

외부 API 예절(NF2006): 요청 간격, 재시도, 식별 가능한 User-Agent.
수집 캐시(NF2002): data/cache/ 에 응답을 저장해 이미 수집한 차량은 다시 호출하지 않는다.

사용법:  python scripts/build_data.py            (캐시 사용)
         python scripts/build_data.py --refresh  (캐시 무시하고 다시 수집)
"""
from __future__ import annotations

import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "cars_source.json"
CACHE = ROOT / "data" / "cache"
IMG_DIR = ROOT / "frontend" / "assets" / "cars"
OUT_JSON = ROOT / "data" / "cars_enriched.json"
REPORT = ROOT / "data" / "verify_report.md"
SOURCES = ROOT / "data" / "SOURCES.md"

# 위키미디어 정책: 연락 가능한 정보를 User-Agent에 넣는다. 제출 전 본인 연락처로 바꿀 것.
try:  # 연락처는 .env의 WIKI_CONTACT 하나로 관리
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except ImportError:
    pass
CONTACT = __import__("os").getenv("WIKI_CONTACT") or "student project"
UA = f"MotorLabEdu/0.2 ({CONTACT}) python-urllib"
INTERVAL = 1.0          # 요청 간격(초)
RETRIES = 5
TEXT_LIMIT_KO = 9000    # 문서당 저장할 최대 글자 수
TEXT_LIMIT_EN = 7000
IMG_WIDTH = 1280

_last = 0.0


def get(url: str, binary: bool = False):
    global _last
    for attempt in range(RETRIES):
        wait = INTERVAL - (time.time() - _last)
        if wait > 0:
            time.sleep(wait)
        _last = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            return data if binary else json.loads(data.decode("utf-8"))
        except urllib.error.HTTPError as e:  # 429/5xx: Retry-After를 따르고, 없으면 5s·10s·20s… 대기
            if attempt == RETRIES - 1 or e.code not in (429, 500, 502, 503, 504):
                raise
            delay = int(e.headers.get("Retry-After") or 5 * 2 ** attempt)
            print(f"    retry {attempt + 1}: HTTP {e.code}, {delay}s 대기", flush=True)
            time.sleep(delay)
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt == RETRIES - 1:
                raise
            print(f"    retry {attempt + 1}: {e}")
            time.sleep(5 * 2 ** attempt)


def api(lang: str, **params) -> dict:
    params = {"format": "json", "formatversion": "2", **params}
    return get(f"https://{lang}.wikipedia.org/w/api.php?" + urllib.parse.urlencode(params))


def wiki_url(lang: str, title: str) -> str:
    return f"https://{lang}.wikipedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))


def strip_html(s: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s or ""))).strip()


def clean_extract(text: str, limit: int) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text or "")
    # 참고문헌·외부 링크 이후는 잘라낸다
    for marker in ["\n== 같이 보기", "\n== 각주", "\n== 참고 문헌", "\n== 외부 링크", "\n== See also", "\n== References", "\n== External links", "\n== Notes"]:
        i = text.find(marker)
        if i > 0:
            text = text[:i]
    return text.strip()[:limit]


# ---------- 인포박스 치수 파싱 (검증용) ----------
def _first_mm(value: str):
    value = value.replace(",", "")
    m = re.search(r"\{\{\s*convert\s*\|\s*([\d.]+)\s*\|\s*(mm|in|cm|m)\b", value, re.I)
    if not m:
        m = re.search(r"([\d.]+)\s*(mm|in|cm)\b", value)
    if not m:
        return None
    v, u = float(m.group(1)), m.group(2).lower()
    return round(v * {"mm": 1, "cm": 10, "m": 1000, "in": 25.4}[u])


def _first_kg(value: str):
    value = value.replace(",", "")
    m = re.search(r"\{\{\s*convert\s*\|\s*([\d.]+)\s*\|\s*(kg|lb)\b", value, re.I) or re.search(r"([\d.]+)\s*(kg|lb)\b", value)
    if not m:
        return None
    v, u = float(m.group(1)), m.group(2).lower()
    return round(v if u == "kg" else v * 0.4536)


def parse_infobox(wikitext: str) -> dict:
    out = {}
    for key, fn in [("length", _first_mm), ("width", _first_mm), ("height", _first_mm), ("wheelbase", _first_mm), ("weight", _first_kg)]:
        m = re.search(rf"^\s*\|\s*{key}\s*=\s*(.+)$", wikitext, re.M | re.I)
        if m:
            v = fn(m.group(1))
            if v:
                out[key] = v
    return out


# ---------- 일괄 조회 (요청 수 줄이기) ----------
def _chunks(items: list, n: int):
    for i in range(0, len(items), n):
        yield items[i:i + n]


def _title_map(query: dict):
    """요청한 제목 → 최종 제목 (정규화·넘겨주기 반영)."""
    norm = {x["from"]: x["to"] for x in query.get("normalized", [])}
    red = {x["from"]: x["to"] for x in query.get("redirects", [])}
    return lambda t: red.get(norm.get(t, t), norm.get(t, t))


def batch_resolve(cars: list[dict], recs: dict) -> None:
    """문서 제목 확인 + 한국어 문서 연결 + 대표 사진 이름을 40대씩 한 번에."""
    by_id = {c["id"]: c for c in cars}
    pending = {c["id"]: list(c["wikiTitles"]) for c in cars}
    while pending:
        tried = {cid: titles.pop(0) for cid, titles in pending.items() if titles}
        if not tried:
            break
        for group in _chunks(list(tried.items()), 40):
            r = api("en", action="query", titles="|".join(t for _, t in group), redirects=1,
                    prop="pageimages|langlinks", piprop="name", pilimit="max", lllang="ko", lllimit="max")
            q = r.get("query", {})
            final = _title_map(q)
            pages = {pg["title"]: pg for pg in q.get("pages", [])}
            for cid, t in group:
                pg = pages.get(final(t))
                if not pg or pg.get("missing"):
                    continue
                rec = recs[cid]
                rec["en"] = {"title": pg["title"]}
                if pg.get("langlinks"):
                    rec["ko"] = {"title": pg["langlinks"][0]["title"]}
                img = by_id[cid].get("imageFile") or pg.get("pageimage")
                rec["image"] = {"file": img} if img else None
                pending.pop(cid, None)
        pending = {cid: t for cid, t in pending.items() if t}


def batch_infobox(recs: dict) -> None:
    items = [(cid, r["en"]["title"]) for cid, r in recs.items() if r.get("en")]
    for group in _chunks(items, 10):
        r = api("en", action="query", titles="|".join(t for _, t in group), prop="revisions",
                rvprop="content", rvslots="main", redirects=1)
        q = r.get("query", {})
        final = _title_map(q)
        pages = {pg["title"]: pg for pg in q.get("pages", [])}
        for cid, t in group:
            pg = pages.get(final(t)) or {}
            revs = pg.get("revisions") or [{}]
            text = revs[0].get("slots", {}).get("main", {}).get("content", "")
            box = text[: text.find("\n==")] if "\n==" in text else text   # 첫 단락(인포박스)만
            recs[cid]["infobox"] = parse_infobox(box)


def batch_imageinfo(recs: dict) -> None:
    items = [(cid, "File:" + r["image"]["file"]) for cid, r in recs.items() if r.get("image")]
    for group in _chunks(items, 40):
        r = api("en", action="query", titles="|".join(t for _, t in group), prop="imageinfo",
                iiprop="url|extmetadata", iiurlwidth=IMG_WIDTH)
        q = r.get("query", {})
        final = _title_map(q)
        pages = {pg["title"]: pg for pg in q.get("pages", [])}
        for cid, t in group:
            ii = (pages.get(final(t)) or {}).get("imageinfo", [{}])[0]
            meta = ii.get("extmetadata", {})
            if not ii.get("url"):
                recs[cid]["image"] = None
                continue
            recs[cid]["image"].update({
                "thumb": ii.get("thumburl") or ii.get("url"),
                "page": ii.get("descriptionurl"),
                "artist": strip_html(meta.get("Artist", {}).get("value", "")) or "Unknown",
                "license": strip_html(meta.get("LicenseShortName", {}).get("value", "")),
                "licenseUrl": meta.get("LicenseUrl", {}).get("value", ""),
            })


def collect_all(cars: list[dict], refresh: bool) -> dict:
    """캐시에 없는 차량만 일괄 조회하고, 본문은 차량별로 받는다."""
    recs, todo = {}, []
    for car in cars:
        f = CACHE / f"{car['id']}.json"
        if f.exists() and not refresh:
            recs[car["id"]] = json.loads(f.read_text(encoding="utf-8"))
        else:
            todo.append(car)
    if not todo:
        return recs
    print(f"새로 수집할 차량 {len(todo)}대 (캐시 {len(recs)}대)", flush=True)
    new = {c["id"]: {"en": None, "ko": None, "image": None, "infobox": {}} for c in todo}
    t0 = time.time()
    batch_resolve(todo, new)
    batch_infobox(new)
    batch_imageinfo(new)
    print(f"  일괄 조회 완료 ({time.time() - t0:.0f}s)", flush=True)
    for i, car in enumerate(todo, 1):
        t1 = time.time()
        rec = new[car["id"]]
        if not rec["en"]:
            print(f"  [{i}/{len(todo)}] ! 문서 없음: {car['nameEn']}", flush=True)
        for lang, limit in (("en", TEXT_LIMIT_EN), ("ko", TEXT_LIMIT_KO)):
            if rec.get(lang):
                r = api(lang, action="query", titles=rec[lang]["title"], prop="extracts", explaintext=1, exsectionformat="wiki")
                pages = r.get("query", {}).get("pages", [{}])
                rec[lang]["text"] = clean_extract(pages[0].get("extract", ""), limit)
                rec[lang]["url"] = wiki_url(lang, rec[lang]["title"])
        (CACHE / f"{car['id']}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        recs[car["id"]] = rec
        print(f"  [{i}/{len(todo)}] {car['year']} {car['nameEn']} · {time.time() - t1:.1f}s", flush=True)
    return recs


def download_image(car_id: str, img: dict, refresh: bool) -> str | None:
    if not img or not img.get("thumb"):
        return None
    ext = Path(urllib.parse.urlparse(img["thumb"]).path).suffix.lower() or ".jpg"
    if ext not in (".jpg", ".jpeg", ".png", ".webp"):
        ext = ".jpg"
    path = IMG_DIR / f"{car_id}{ext}"
    if not path.exists() or refresh:
        path.write_bytes(get(img["thumb"], binary=True))
    return f"assets/cars/{path.name}"


def main():
    refresh = "--refresh" in sys.argv
    CACHE.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    cars = json.loads(SRC.read_text(encoding="utf-8"))

    recs = collect_all(cars, refresh)
    out_cars, report, credits = [], [], []
    for i, car in enumerate(cars, 1):
        rec = recs[car["id"]]
        c = {k: v for k, v in car.items() if k not in ("wikiTitles", "imageFile")}

        docs = []
        for lang in ("ko", "en"):
            d = rec.get(lang)
            if d and d.get("text"):
                docs.append({"id": f"wiki-{lang}", "type": "wiki", "lang": lang, "title": d["title"], "url": d["url"], "text": d["text"]})
        c["docs"] = docs

        img = rec.get("image")
        t1 = time.time()
        src = download_image(car["id"], img, refresh) if img and img.get("thumb") else None
        if time.time() - t1 > 3:
            print(f"  사진 [{i}/{len(cars)}] {car['nameEn']} · {time.time() - t1:.1f}s", flush=True)
        c["image"] = {"src": src, "artist": img["artist"], "license": img["license"], "licenseUrl": img["licenseUrl"], "page": img["page"]} if src else None
        if src:
            credits.append(f"| {car['year']} {car['name']} | [{img['file']}]({img['page']}) | {img['artist']} | {img['license']} |")

        # 제원 대조: 1.5% 넘게 차이 나면 보고
        diffs = []
        for k, v in rec.get("infobox", {}).items():
            mine = car.get(k)
            if mine is None:   # 비어 있으면 위키 인포박스 값으로 채운다
                c[k] = v
                c.setdefault("filledFromWiki", []).append(k)
                diffs.append(f"{k}: 비어 있음 → 위키 값 {v}로 채움")
            elif abs(mine - v) / v > 0.015:
                diffs.append(f"{k}: {mine} ≠ 위키 {v}")
        report.append((car, rec, diffs))
        out_cars.append(c)

    meta = {"generatedAt": date.today().isoformat(), "carCount": len(out_cars), "docCount": sum(len(c["docs"]) for c in out_cars)}
    OUT_JSON.write_text(json.dumps({"meta": meta, "cars": out_cars}, ensure_ascii=False, indent=1), encoding="utf-8")

    lines = ["# 제원 대조 결과 (영문 위키백과 인포박스 기준)", "", f"생성일: {meta['generatedAt']}", ""]
    for car, rec, diffs in report:
        flag = "✅" if not any("≠" in d for d in diffs) else "⚠️"
        en = rec.get("en") or {}
        lines.append(f"- {flag} **{car['year']} {car['name']}** — 문서: {en.get('title', '없음')}, 한국어 문서: {'있음' if rec.get('ko') else '없음'}, 사진: {'있음' if rec.get('image') else '없음'}")
        lines += [f"    - {d}" for d in diffs]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    SOURCES.write_text("\n".join([
        "# 데이터 출처와 이용 조건", "",
        "## 차량 메타데이터", "`data/cars_source.json` — 제조사 공개 제원과 위키백과를 참고해 직접 정리. 트림(`trim`) 기준 값이며 연식·시장에 따라 다를 수 있음. 비어 있던 치수·중량은 영문 위키백과 인포박스 값으로 채우고 `filledFromWiki`에 기록.", "",
        "## 외부 문서", "한국어·영어 위키백과 본문 — CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/). 원문 URL은 `cars_enriched.json`의 각 문서 `url`과 Chroma 청크 메타데이터에 기록.", "",
        "## 차량 사진 (Wikimedia Commons)", "각 사진의 저작자와 라이선스를 화면에 함께 표시한다.", "",
        "| 차량 | 파일 | 저작자 | 라이선스 |", "|---|---|---|---|", *credits, "",
    ]), encoding="utf-8")

    print(f"\n완료: 차량 {meta['carCount']}대 · 문서 {meta['docCount']}건 · 사진 {len(credits)}장")
    print(f"→ {OUT_JSON.relative_to(ROOT)}\n→ {REPORT.relative_to(ROOT)}\n→ {SOURCES.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
