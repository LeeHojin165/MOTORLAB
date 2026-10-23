"""ChromaDB 색인 스크립트

  python -m scripts.build_index                 차량 메타데이터 색인 (F2001 · F2002)
  python -m scripts.build_index --bundle        + 차량 자체 위키 문서 묶음 색인 (F2005, 오프라인 대비)
  python -m scripts.build_index --pdf           + data/pdfs/{차량 ID}/*.pdf 색인 (F2016)
  python -m scripts.build_index --reset ...     컬렉션과 수집 캐시를 비우고 다시 (청크 설정을 바꾼 뒤)
  python -m scripts.build_index --show bmw-ix3-2026   항목 1건의 색인 텍스트 출력 (검증 4.1)

같은 명령을 여러 번 실행해도 청크 ID가 고정되어 있어 개수가 늘지 않는다.
"""
from __future__ import annotations

import argparse
import sys

from backend.config import settings
from backend.domain.cars import get_car, index_text, load_cars


def index_pdfs() -> int:
    from pypdf import PdfReader
    from backend.store import vectorstore as vs

    total = 0
    for folder in sorted(p for p in (settings.data_dir / "pdfs").glob("*") if p.is_dir()):
        car = get_car(folder.name)
        if car is None:
            print(f"  ! 알 수 없는 차량 폴더: {folder.name}")
            continue
        for pdf in sorted(folder.glob("*.pdf")):
            # PDF는 쪽 단위로 먼저 나눈 뒤 청킹한다 — 근거에 '파일명 p.쪽'을 표시하기 위해
            for page_no, page in enumerate(PdfReader(pdf).pages, start=1):
                text = (page.extract_text() or "").strip()
                if text:
                    total += vs.index_document(car, source_type="pdf", lang="ko", title=pdf.name, text=text, page=page_no,
                                               query="(PDF)")
            print(f"  · {car['name']} ← {pdf.name}")
    return total


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", action="store_true")
    ap.add_argument("--pdf", action="store_true")
    ap.add_argument("--reset", action="store_true")
    ap.add_argument("--show")
    args = ap.parse_args()

    if args.show:
        car = get_car(args.show)
        print(index_text(car) if car else f"차량 없음: {args.show}")
        return
    if not settings.has_api_key:
        sys.exit("OPENAI_API_KEY가 없습니다. .env 파일을 먼저 설정하세요 (.env.example 참고).")

    from backend.collect import collector
    from backend.store import vectorstore as vs

    if args.reset:
        for name in (vs.META, vs.DOCS):
            try:
                vs._client().delete_collection(name)
            except Exception:
                pass
        vs.store.cache_clear()
        collector.CACHE_FILE.unlink(missing_ok=True)
        print("컬렉션과 수집 캐시를 비웠습니다.")

    cars = load_cars()
    print(f"차량 {len(cars)}대 로드 · 청크 {settings.chunk_size}자 / 중복 {settings.chunk_overlap}자 · DB 위치 {settings.chroma_dir}")
    print(f"car_meta 색인: {vs.index_meta(cars)}건")
    removed = vs.prune({c["id"] for c in cars})
    if removed:
        print(f"목록에 없는 차량 청크 {removed}개 정리")

    if args.bundle:
        for car in cars:
            added = collector.ensure_own_docs(car)
            if added:
                print(f"  · {car['name']}: {', '.join(added)}")
    if args.pdf:
        print(f"PDF 청크: {index_pdfs()}개")

    c = vs.counts()
    print(f"\n현재 색인 — 메타데이터 {c['meta_count']}건 · 문서 {c['doc_count']}건 · 문서 청크 {c['chunk_count']}개")


if __name__ == "__main__":
    main()
