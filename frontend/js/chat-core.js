/* =========================================================
   MOTORLAB — 질의응답 공통 로직 (F2006 ~ F2009, F2012, F2015)
   메인 페이지의 Q&A 탭과 질의응답 전용 페이지가 같은 코드를 쓴다.
   차량별 대화 기록은 sessionStorage에 저장해 두 페이지가 이어서 쓴다.
   ========================================================= */
window.ChatCore = (function () {
  "use strict";
  const { esc, modelLabel, renderRich, sourcesHTML, warnBox, settings, toast } = window.UI;
  const STEP_LABELS = ["검색어 추출", "후보 문서 선별", "문서 수집 · 색인", "근거 검색", "답변 생성"];
  const STORE_KEY = "motorlab.histories";
  const MAX_PER_CAR = 40;

  /* ---------------- 대화 기록 저장 ---------------- */
  let histories = {};
  try { histories = JSON.parse(sessionStorage.getItem(STORE_KEY) || "{}"); } catch { histories = {}; }
  for (const id of Object.keys(histories)) histories[id] = histories[id].filter((m) => m.role === "user" || m.status !== "pending");

  function persist() {
    try {
      const plain = {};
      for (const [id, hist] of Object.entries(histories)) {
        plain[id] = hist.filter((m) => m.status !== "pending").slice(-MAX_PER_CAR).map(({ _el, ...m }) => m);
      }
      sessionStorage.setItem(STORE_KEY, JSON.stringify(plain));
    } catch { /* 저장소가 가득 차거나 막혀 있으면 이번 화면에서만 유지 */ }
  }
  const historyOf = (id) => (histories[id] ||= []);

  /* ---------------- 렌더링 ---------------- */
  function stepsHTML(entry) {
    const done = entry.status !== "pending";
    let head;
    if (!done) head = `<span class="spinner"></span>${STEP_LABELS[entry.cur] || "준비 중"}…`;
    else if (entry.status === "error") head = `<svg style="stroke:var(--bad)"><use href="#ico-alert"/></svg>처리 중단`;
    else {
      const c = entry.res.collect || {};
      const what = c.selected?.length ? `새 문서 ${c.selected.length}건 수집` : c.cache_hits?.length ? "이미 수집된 문서 사용" : "색인된 문서 사용";
      head = `<svg><use href="#ico-check"/></svg>${what} · 근거 ${entry.res.retrieved.length}건 검색 · ${esc(modelLabel(entry.res.model))}`;
    }
    return `
      <div class="steps ${done ? "is-done" : ""} ${entry.open ? "is-open" : ""}">
        <div class="steps__head">${head}${done ? `<button class="steps__toggle" type="button">${entry.open ? "접기" : "처리 과정"}</button>` : ""}</div>
        <ol class="steps__list">
          ${STEP_LABELS.map((l, i) => {
            const st = entry.steps[i];
            const cls = !st ? "" : st.state === "run" ? "is-run" : "is-done";
            return `<li class="step ${cls}"><span class="step__dot"></span><span>${l}${st?.detail ? ` <span class="step__detail">— ${esc(st.detail)}</span>` : ""}</span></li>`;
          }).join("")}
        </ol>
      </div>`;
  }

  function botHTML(entry) {
    let body = stepsHTML(entry);
    if (entry.status === "error") body += warnBox(entry.error);
    else if (entry.status === "done") {
      const r = entry.res;
      const rag = `<div class="msg__text">${renderRich(r.answer, r.citations)}</div>`;
      body += r.norag_answer
        ? `<div class="rag-compare"><div class="is-norag"><h5>RAG 미사용</h5>${renderRich(r.norag_answer, [])}</div><div><h5>RAG 사용 · 근거 기반</h5>${rag}</div></div>`
        : rag;
      body += sourcesHTML(r.citations);
      if (settings.show_retrieved) {
        const unused = r.retrieved.filter((x) => !r.citations.some((c) => c.n === x.n));
        if (unused.length) body += sourcesHTML(unused, "검색됐지만 인용되지 않은 근거", "sources--retrieved");
      }
    }
    return `<div class="msg msg--bot"><span class="msg__avatar" aria-hidden="true"></span><div class="msg__body">${body}</div></div>`;
  }

  /* ---------------- 대화창 하나 ---------------- */
  /**
   * opts: { log, composer, textarea, suggest?, clearBtn?, getCar(), emptyHTML(car), onAnswered?(car, res) }
   */
  function create(opts) {
    const { log, composer, textarea } = opts;

    function mount(entry) {
      const tmp = document.createElement("div");
      tmp.innerHTML = botHTML(entry);
      const el = tmp.firstElementChild;
      if (entry._el?.isConnected) entry._el.replaceWith(el);
      entry._el = el;
      return el;
    }

    const scrollEnd = () => { log.scrollTop = log.scrollHeight; };

    function render() {
      const car = opts.getCar();
      if (!car) return;
      const hist = historyOf(car.id);
      if (!hist.length) { log.innerHTML = opts.emptyHTML(car); return; }
      log.innerHTML = "";
      hist.forEach((m) => {
        if (m.role === "user") log.insertAdjacentHTML("beforeend", `<div class="msg msg--user"><div class="msg__bubble">${esc(m.text)}</div></div>`);
        else { m._el = null; log.appendChild(mount(m)); }
      });
      scrollEnd();
    }

    async function ask(question) {
      const car = opts.getCar();
      if (!car) { toast("먼저 차량을 선택하세요"); return; }
      question = question.trim();
      if (!question) return;
      const hist = historyOf(car.id);
      if (hist.some((m) => m.status === "pending")) { toast("이전 답변을 생성하는 중입니다"); return; }

      hist.push({ role: "user", text: question });
      const entry = { role: "bot", status: "pending", cur: 0, steps: [], open: false };
      hist.push(entry);
      render();
      composer.classList.add("is-busy");
      const refresh = () => { if (entry._el?.isConnected) { mount(entry); scrollEnd(); } };
      try {
        entry.res = await API.chatStream(
          { car_id: car.id, question, top_k: settings.top_k, search_type: settings.search_type, compare_rag: settings.compare_rag, model: settings.model },
          (ev) => {
            if (ev.type !== "progress") return;
            for (let i = 0; i < ev.step; i++) {
              entry.steps[i] ||= { state: "done", detail: "" };
              entry.steps[i].state = "done";
            }
            entry.steps[ev.step] = { state: "run", detail: ev.detail };
            entry.cur = ev.step;
            refresh();
          }
        );
        entry.steps.forEach((x) => x && (x.state = "done"));
        entry.status = "done";
        opts.onAnswered?.(car, entry.res);
      } catch (err) {
        entry.status = "error";
        entry.error = err.code || "UPSTREAM";
      }
      composer.classList.remove("is-busy");
      persist();
      refresh();
    }

    function clear() {
      const car = opts.getCar();
      if (!car) return;
      histories[car.id] = [];
      persist();
      render();
      toast("이 차량의 대화를 지웠습니다");
    }

    // 입력창: Enter 전송 · Shift+Enter 줄바꿈 · 한글 조합 중에는 전송하지 않음
    const resize = () => { textarea.style.height = "auto"; textarea.style.height = Math.min(textarea.scrollHeight, 200) + "px"; };
    textarea.addEventListener("input", resize);
    textarea.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey && !e.isComposing) { e.preventDefault(); composer.requestSubmit(); }
    });
    composer.addEventListener("submit", (e) => {
      e.preventDefault();
      const q = textarea.value;
      textarea.value = "";
      resize();
      ask(q);
    });
    opts.suggest?.addEventListener("click", (e) => { const b = e.target.closest(".chip"); if (b) ask(b.dataset.q || b.textContent); });
    opts.clearBtn?.addEventListener("click", clear);
    log.addEventListener("click", (e) => {
      const tog = e.target.closest(".steps__toggle");
      if (!tog) return;
      const car = opts.getCar();
      const entry = car && historyOf(car.id).find((m) => m._el && m._el.contains(tog));
      if (entry) { entry.open = !entry.open; mount(entry); }
    });

    return { render, ask, clear };
  }

  const SUGGESTIONS = ["엔진과 변속기, 출력과 토크 알려줘", "전장·전폭·전고·휠베이스는?", "제로백과 최고속도는?", "서스펜션 구성과 승차감은 어때?", "공인 연비는 어떻게 돼?", "어떤 역사를 가진 차야?"];
  const suggestHTML = () => SUGGESTIONS.map((q) => `<button class="chip" type="button">${q}</button>`).join("");

  return { create, suggestHTML, historyOf };
})();
