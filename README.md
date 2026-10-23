# MOTORLAB — 근거로 답하는 자동차 백과

1886년 벤츠 파텐트 모토르바겐부터 2026년형 전기차까지, **차량 메타데이터와 위키백과 문서를 근거로** 질문에 답하는 RAG 서비스입니다.
답변에는 근거 번호가 붙고, 실제로 인용된 문서의 제목과 원문 출처가 함께 표시됩니다.

- Python · FastAPI · LangGraph(retrieve → generate) · ChromaDB · OpenAI 호환 GPT API
- 화면: HTML · CSS · JavaScript (서버가 같은 주소에서 제공)

## 사용 모델 (SSAFY GMS 경유)

| 역할 | 모델 | 설정 |
|---|---|---|
| 답변 생성(프롬프트 3) · 비교 · 사실 확인 · 조건 탐색 | **GPT-4o** (기본) / GPT-4o mini / Claude Sonnet 4.5 — 화면 설정에서 선택 | `ANSWER_MODEL`, `MODELS` |
| 검색어 추출(프롬프트 1) · 후보 선별(프롬프트 2) | GPT-4o mini | `UTILITY_MODEL` |
| 임베딩 | text-embedding-3-small | `EMBEDDING_MODEL` |

Claude 3.5 Sonnet은 GMS에서 제공하지 않아(퇴역 모델) 후속인 `claude-sonnet-4-5-20250929`를 씁니다.
Claude는 Anthropic Messages API(`ANTHROPIC_BASE_URL`)로, GPT는 OpenAI 호환 API(`OPENAI_BASE_URL`)로 호출하며 GMS 키 하나로 둘 다 동작합니다.

## 실행

```bash
# 0) 가상환경 + 라이브러리 (요구사항정의서 고정 버전)
python -m venv .venv
.venv\Scripts\activate            # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

# 1) 환경변수 — .env.example 을 .env 로 복사하고 OPENAI_API_KEY 입력
#    SSAFY GMS 사용 시 OPENAI_BASE_URL 주석 해제
copy .env.example .env

# 2) (선택) 사진·문서 묶음 다시 만들기 — 결과물(data/cars_enriched.json, frontend/assets)은 이미 포함
python scripts/build_data.py

# 3) ChromaDB 색인
python -m scripts.build_index --bundle
#    ※ ChromaDB 1.5.x는 경로에 한글이 있으면 인덱스를 다시 읽지 못합니다.
#      프로젝트 경로에 한글이 있으면 DB는 자동으로 ~/.motorlab/chroma 에 저장됩니다 (.env의 CHROMA_DIR로 변경 가능).

# 4) 서버 실행 → http://localhost:8000
uvicorn backend.server:app --reload
```

## 구조 (NF2005 모듈 분리)

```
motorlab/
  backend/
    config.py              실행 설정 (.env)
    llm.py                 LLM·임베딩 생성, 공통 오류, JSON 파싱
    domain/                ← 데이터 준비 영역: 도메인에 묶인 부분은 여기에만
      cars.py              차량 데이터 로드, 색인 텍스트 구성 (F2001)
      prompts.py           프롬프트 1·2·3 + 특화 기능 프롬프트
    collect/               수집
      wikipedia.py         위키백과 API (간격·재시도·User-Agent, NF2006)
      collector.py         검색어 추출(프롬프트1) → 후보 선별(프롬프트2) → 본문 수집, 질문·검색어 캐시 (F2003·F2004·NF2002)
    store/vectorstore.py   색인: Chroma 컬렉션 2개, 청킹, 청크 ID 규칙 (F2002·F2005)
    rag/graph.py           검색·생성: LangGraph retrieve → generate, 근거 병합·중복 제거·인용 추출 (F2006~F2008)
    services/              서비스 기능
      chat.py              질의응답 + 진행 상태 스트리밍 (F2009·F2012·F2015)
      features.py          조건 탐색(F2011), 제원 비교·사실 확인(F2010)
    server.py              FastAPI (F2013)
  scripts/
    build_data.py          위키 문서 묶음·사진 수집 → data/cars_enriched.json
    build_index.py         ChromaDB 색인 (--bundle, --pdf, --reset, --show)
    show_graph.py          LangGraph 구조 출력
  data/
    cars_source.json       직접 정리한 차량 제원 200대 (항목 메타데이터 원본)
    cars_enriched.json     제원 + 사진 정보 + 차량 자체 위키 문서 묶음
    pdfs/{차량 ID}/*.pdf   (선택) PDF 문서 출처 (F2016)
    verify_report.md       영문 위키 인포박스와 치수 대조 결과
    SOURCES.md             데이터·문서·사진 출처와 이용 조건 (NF2007)
  frontend/                index.html · css · js(api.js, app.js) · assets/cars
```

## RAG 파이프라인

| 단계 | 내용 |
|---|---|
| 색인 1 — `car_meta` | 차량 1대 = 청크 1개. 이름·연도·제조사·트림·차종·동력원·엔진·변속기·구동·출력·토크·가속·연비·치수·서스펜션·승차감을 한 텍스트로. 청크 ID = 차량 ID → 재색인해도 개수 불변 |
| 수집 | 차량 자체 문서는 항상 색인 → 이미 받은 (차량, 질문)이면 그때의 검색어를 재사용, 처음이면 프롬프트 1로 검색어 추출(JSON 배열) → 이미 수집한 (차량, 검색어)는 건너뜀 → 위키백과 검색 후보의 **제목·요약만** 프롬프트 2에 보여 선별 → 고른 문서만 본문 수집 |
| 색인 2 — `car_docs` | `CHUNK_SIZE`/`CHUNK_OVERLAP`로 분할. 청크 ID `{차량 ID}:{문서 ID}:{순번}`. 메타데이터: car_id, source_type, lang, title, url, page, doc_id, query, chunk_index, collected_at |
| retrieve | 선택 차량 메타데이터 청크를 항상 [근거 1]로 넣고, `car_docs`를 `car_id` 필터로 좁혀 유사도 또는 MMR(`MMR_FETCH_K` 후보 → Top-k)로 검색 → 청크 ID·본문 해시로 중복 제거 |
| generate | 프롬프트 3: 근거만 사용, 문장마다 [근거 n], 없으면 "확인되지 않습니다". 본문의 [근거 n]을 찾아 **인용된 근거만** 화면에 표시, 없는 번호는 삭제 |

설정값(청크 크기·중복·Top-k·검색 방식)은 `.env`에서 바꾸고, Top-k와 검색 방식은 화면 설정에서도 질문마다 바꿀 수 있습니다.
청크 설정을 바꾼 뒤에는 `python -m scripts.build_index --reset --bundle`로 다시 색인합니다.

## 검증에 쓰는 명령

```bash
python -m scripts.build_index --show bmw-ix3-2026   # 항목 1건의 색인 텍스트 (4.1)
python -m scripts.build_index                       # 두 번 실행해도 car_meta 개수 불변 (4.1)
python -m scripts.show_graph                        # LangGraph 노드 구성 (4.3)
type data\collect_cache.json                        # 질문별 검색어, 검색어별 선별·제외 문서 (4.2, NF2002)
```

검증 스크립트와 실행 로그·화면 캡처는 `docs/evidence/`에 있습니다 (스크립트: `docs/evidence/scripts/`, 프로젝트 루트에서 `PYTHONPATH=.`로 실행).

## 제출 문서 (docs/)

| 문서 | 내용 |
|---|---|
| `요구사항_정의서.md` | 도메인 선택 조건 충족 근거, 기능·비기능 요구사항 표 |
| `RAG_파이프라인_설계문서.md` | 컬렉션·메타데이터, 수집·청킹·색인 흐름, 병합·중복 제거, 프롬프트 3종, 설정값 근거, 근거 표시, 문제 해결 |
| `요구사항_대조표.md` | 요구사항별 구현 위치·확인 결과·증빙, 심화 기능과 필수 구현 비교 |
| `테스트_결과표.md` | 테스트 케이스별 입력·기대·실제 결과 |
| `RAG_전후_비교.md` | 대표 질문 7개의 RAG 사용 전후 비교 (F2015) |
| `셀프_체크리스트.md` | 셀프 점검 결과 27항목 |
| `PORTFOLIO.md`, `motorlab-architecture.png` | 서비스 소개, 아키텍처 그림 |

## 출처와 이용 조건

- 차량 제원: 제조사 공개 자료와 위키백과를 참고해 직접 정리 (트림 기준, 연식·시장별로 다를 수 있음)
- 위키백과 본문: CC BY-SA 4.0 — 청크마다 원문 URL 저장, 화면에 원문 링크 표시
- 차량 사진: Wikimedia Commons — 사진마다 저작자와 라이선스를 화면과 `data/SOURCES.md`에 표기
