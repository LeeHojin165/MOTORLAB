/* =========================================================
   MOTORLAB — 메인 페이지 (연대기 · Q&A 탭 · 차량 탐색 · 제원 비교 · 사실 확인)
   공통 렌더링은 js/ui.js, 질의응답 로직은 js/chat-core.js
   ========================================================= */
(function () {
  "use strict";

  const { $, $$, esc, fmt, FUEL, FUEL_FILTER, modelLabel, credit, photo, toast, warnBox,
    renderRich, sourcesHTML, specHTML, carItemHTML, matchCar, settings } = window.UI;

  const ERAS = [
    { id: "all", label: "전체", test: () => true },
    { id: "e1", label: "~1945", test: (y) => y <= 1945 },
    { id: "e2", label: "1946–1989", test: (y) => y >= 1946 && y <= 1989 },
    { id: "e3", label: "1990–2009", test: (y) => y >= 1990 && y <= 2009 },
    { id: "e4", label: "2010–2026", test: (y) => y >= 2010 },
  ];
  const HERO_PICKS = ["bmw-ix3-2026", "porsche-taycan-2019", "mercedes-300sl-1954"];

  const state = {
    cars: [],
    byId: new Map(),
    selected: null,
    fuel: "all",
    era: "all",
    compareIds: ["mercedes-300sl-1954", "porsche-911-992-2019", "bmw-ix3-2026"],
  };
  const carById = (id) => state.byId.get(id);
  const chatUrl = (id) => `chat.html?car=${encodeURIComponent(id)}`;

  /* =========================================================
     Navigation / tabs
     ========================================================= */
  function switchView(view) {
    $$(".tab").forEach((t) => { const on = t.dataset.view === view; t.classList.toggle("is-active", on); t.setAttribute("aria-selected", on); });
    $$(".view").forEach((v) => { const on = v.id === "view-" + view; v.hidden = !on; v.classList.toggle("is-active", on); });
  }

  function bindNav() {
    const nav = $("#gnav"), hero = $(".hero");
    const onScroll = () => nav.classList.toggle("is-solid", window.scrollY > hero.offsetHeight - 80);
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
    document.addEventListener("click", (e) => {
      const a = e.target.closest("[data-goto]");
      if (!a) return;
      e.preventDefault();
      switchView(a.dataset.goto);
      $("#mobileMenu").hidden = true;
      $("#workspace").scrollIntoView({ behavior: "smooth" });
    });
    $$(".tab").forEach((t) => t.addEventListener("click", () => switchView(t.dataset.view)));
    $("#openMenu").addEventListener("click", () => { const m = $("#mobileMenu"); m.hidden = !m.hidden; });
    $$("#mobileMenu a[href='#chronicle']").forEach((a) => a.addEventListener("click", () => ($("#mobileMenu").hidden = true)));
  }

  function updateHeroMode() {
    $("#statMode").textContent = `${settings.search_type === "mmr" ? "MMR" : "유사도"} · k${settings.top_k}`;
  }

  /* =========================================================
     Status (F2002, F2012)
     ========================================================= */
  async function loadStatus() {
    const st = await UI.loadStatus({ pill: $("#statusPill"), alerts: $("#sysAlerts") });
    if (!st) return;
    $("#statMeta").textContent = fmt(st.meta_count);
    $("#statDocs").textContent = fmt(st.doc_count);
    $("#statChunks").textContent = fmt(st.chunk_count);
    $("#sideMetaCount").textContent = fmt(st.meta_count) + "건";
    if (!loadStatus.done) { loadStatus.done = true; UI.applyServerStatus(st); updateHeroMode(); }
  }

  function renderHero() {
    const c = HERO_PICKS.map(carById).find((x) => x && x.image);
    if (!c) return;
    const media = $("#heroMedia");
    const img = new Image();
    img.onload = () => { media.style.backgroundImage = `url("${c.image.src}")`; media.classList.add("is-loaded"); };
    img.src = c.image.src;
    $("#heroCredit").innerHTML = `<b>${c.year} ${esc(c.name)}</b><br>${credit(c.image)}`;
  }

  /* =========================================================
     Chronicle
     ========================================================= */
  function renderEraFilter() {
    const root = $("#eraFilter");
    root.innerHTML = ERAS.map((e) => `<button role="tab" data-era="${e.id}" class="${e.id === state.era ? "is-active" : ""}">${e.label}</button>`).join("");
    root.onclick = (ev) => {
      const b = ev.target.closest("button");
      if (!b) return;
      state.era = b.dataset.era;
      renderEraFilter();
      renderChronicle();
    };
  }

  function renderChronicle() {
    const era = ERAS.find((e) => e.id === state.era);
    const list = state.cars.filter((c) => era.test(c.year));
    const track = $("#chronicleTrack");
    if (!list.length) { track.innerHTML = `<div class="car-list__empty">표시할 차량이 없습니다.</div>`; return; }
    track.innerHTML = list.map((c) => `
      <div class="chrono-card" data-car="${c.id}" role="button" tabindex="0">
        <span class="chrono-card__year">${c.year}</span>
        ${photo(c)}
        <span class="chrono-card__name">${esc(c.name)}</span>
        <span class="chrono-card__meta">${esc(c.maker)} · ${esc(c.country)}</span>
        <span class="chrono-card__tag">${FUEL[c.fuel]} · ${esc(c.bodyType)}</span>
      </div>`).join("");
    track.scrollLeft = 0;
    const go = (e) => {
      if (e.target.closest("a")) return;
      const b = e.target.closest("[data-car]");
      if (!b || (e.type === "keydown" && e.key !== "Enter")) return;
      selectCar(b.dataset.car);
      switchView("qa");
      $("#workspace").scrollIntoView({ behavior: "smooth" });
    };
    track.onclick = go;
    track.onkeydown = go;
  }

  /* =========================================================
     Q&A 탭 (F2009) — 넓은 화면은 chat.html
     ========================================================= */
  function renderFuelFilter() {
    const root = $("#fuelFilter");
    root.innerHTML = FUEL_FILTER.map(([v, l]) => `<button class="chip ${v === state.fuel ? "is-active" : ""}" data-fuel="${v}">${l}</button>`).join("");
    root.onclick = (e) => {
      const b = e.target.closest("[data-fuel]");
      if (!b) return;
      state.fuel = b.dataset.fuel;
      renderFuelFilter();
      renderCarList();
    };
  }

  function renderCarList() {
    const q = $("#carSearch").value.trim().toLowerCase();
    const list = state.cars.filter((c) => matchCar(c, q, state.fuel));
    const ul = $("#carList");
    if (!state.cars.length) { ul.innerHTML = `<li class="car-list__empty">차량 목록을 불러오지 못했습니다.</li>`; return; }
    if (!list.length) { ul.innerHTML = `<li class="car-list__empty">"${esc(q)}"와 일치하는 차량이 없습니다.</li>`; return; }
    ul.innerHTML = list.map((c) => carItemHTML(c, state.selected?.id === c.id)).join("");
  }

  function renderSideDocs(docs) {
    $("#sideDocCount").textContent = docs.length + "건";
    $("#sideDocList").innerHTML = docs.map((d) => `<li title="${esc(d.source_type)}">${esc(d.title)}${d.lang ? " · " + d.lang.toUpperCase() : ""}</li>`).join("") || "<li>아직 수집된 문서 없음 — 첫 질문 때 수집</li>";
  }

  async function refreshSideDocs(id) {
    try {
      const docs = await API.carDocs(id);
      if (state.selected?.id === id) renderSideDocs(docs);
    } catch { /* 상태 표시는 상단 안내가 담당 */ }
  }

  let chat;
  function selectCar(id) {
    const c = carById(id);
    if (!c) return;
    state.selected = c;
    renderCarList();
    $("#chatMaker").textContent = `${c.maker} · ${c.country} · ${c.trim} 기준`;
    $("#chatTitle").innerHTML = `${esc(c.name)}<small>${c.year}</small>`;
    $("#openWide").href = chatUrl(c.id);
    $("#composer").classList.remove("is-disabled");
    $("#question").placeholder = `${c.name}에 대해 질문하세요 — 엔진, 변속기, 출력, 연비, 치수, 서스펜션…`;
    $("#sideDocCount").textContent = "—";
    $("#sideDocList").innerHTML = "";
    refreshSideDocs(id);
    $("#specPanel").innerHTML = specHTML(c);
    chat.render();
  }

  function bindChat() {
    chat = ChatCore.create({
      log: $("#chatLog"),
      composer: $("#composer"),
      textarea: $("#question"),
      suggest: $("#suggest"),
      clearBtn: $("#clearChat"),
      getCar: () => state.selected,
      emptyHTML: (c) => `<div class="chat-empty">${photo(c, { showCredit: false })}<p><b>${esc(c.name)}</b>에 대해 무엇이든 물어보세요.<br>모든 답변에는 근거 번호와 원문 출처가 붙습니다.</p></div>`,
      onAnswered: (c, res) => { if (state.selected?.id === c.id) renderSideDocs(res.docs || []); loadStatus(); },
    });
    $("#suggest").innerHTML = ChatCore.suggestHTML();
    $("#carSearch").addEventListener("input", renderCarList);
    $("#carList").addEventListener("click", (e) => { const b = e.target.closest("[data-car]"); if (b) selectCar(b.dataset.car); });
  }

  /* =========================================================
     Explore (F2011)
     ========================================================= */
  function bindExplore() {
    const examples = ["1990년 이전의 후륜구동 수동 스포츠카", "제로백 5초 이하 전기차", "2024년 이후 출시된 한국 전기차", "주행거리 700km 이상 전기차", "승차감이 부드러운 차", "3열 SUV"];
    $("#exploreExamples").innerHTML = examples.map((x) => `<button class="chip" type="button">${x}</button>`).join("");
    $("#exploreExamples").addEventListener("click", (e) => {
      const b = e.target.closest(".chip");
      if (!b) return;
      $("#exploreInput").value = b.textContent;
      $("#exploreForm").requestSubmit();
    });
    $("#exploreForm").addEventListener("submit", async (e) => {
      e.preventDefault();
      const q = $("#exploreInput").value.trim();
      if (!q) return;
      const prog = $("#exploreProgress"), res = $("#exploreResults"), sum = $("#exploreSummary");
      res.innerHTML = ""; sum.innerHTML = "";
      prog.hidden = false;
      prog.innerHTML = `<span class="bar"></span><span class="txt">메타데이터 색인에서 후보를 찾고 조건에 맞는 차량을 고르는 중</span>`;
      try {
        const out = await API.explore(q, settings.model);
        prog.hidden = true;
        sum.innerHTML = `
          <div>
            <h3>조건에 맞는 차량 ${out.results.length}대</h3>
            ${out.conditions.length ? `<div class="parsed-conds">${out.conditions.map((x) => `<span>${esc(x)}</span>`).join("")}</div>` : ""}
          </div>
          <p>메타데이터 후보 ${out.candidates}건 중 조건을 모두 만족하는 차량만 표시</p>`;
        if (!out.results.length) {
          res.innerHTML = `<div class="empty-state" style="grid-column:1/-1"><strong>조건에 맞는 차량이 없습니다</strong>조건을 하나 줄이거나 다른 표현으로 다시 입력해 보세요.</div>`;
          return;
        }
        res.innerHTML = out.results.map(({ car_id, reason }) => {
          const c = carById(car_id);
          if (!c) return "";
          return `
            <a class="car-card" href="${chatUrl(c.id)}" data-car="${c.id}">
              <div class="car-card__top"><span class="car-card__year">${c.year}</span><span class="car-card__match">조건 일치</span></div>
              ${photo(c, { showCredit: false })}
              <span class="car-card__name">${esc(c.name)}</span>
              <span class="car-card__maker">${esc(c.maker)} · ${FUEL[c.fuel]} · ${esc(c.bodyType)}</span>
              <div class="car-card__specs">
                <div><b>${c.powerPs != null ? fmt(c.powerPs) : "—"}</b>PS</div>
                <div><b>${c.zeroTo100 ?? "—"}</b>0–100 s</div>
                <div><b>${esc(c.driveCode)}</b>구동</div>
              </div>
              <div class="car-card__why">${esc(reason)}</div>
              <span class="car-card__cta">이 차량에 질문하기 <svg><use href="#ico-arrow"/></svg></span>
            </a>`;
        }).join("");
      } catch (err) {
        prog.hidden = true;
        res.innerHTML = warnBox(err.code, 'style="grid-column:1/-1"');
      }
    });
  }

  /* =========================================================
     Compare (F2010)
     ========================================================= */
  const CMP_ROWS = [
    ["Powertrain"],
    ["기준 트림", (c) => c.trim],
    ["동력원", (c) => FUEL[c.fuel]],
    ["엔진 · 모터", (c) => c.engine],
    ["변속기", (c) => c.transmission],
    ["구동방식", (c) => c.drive],
    ["최고출력", (c) => c.powerText, (c) => c.powerPs, "max"],
    ["최대토크", (c) => c.torqueNm && `${fmt(c.torqueNm)} N·m`, (c) => c.torqueNm, "max"],
    ["Performance"],
    ["0–100 km/h", (c) => c.zeroTo100 && `${c.zeroTo100} 초`, (c) => c.zeroTo100, "min"],
    ["최고속도", (c) => c.topSpeed && `${c.topSpeed} km/h`, (c) => c.topSpeed, "max"],
    ["공인 연비", (c) => c.efficiency],
    ["Body"],
    ["차종", (c) => c.bodyType],
    ["전장 × 전폭 × 전고", (c) => (c.length && c.width && c.height) ? `${fmt(c.length)} × ${fmt(c.width)} × ${fmt(c.height)} mm` : null],
    ["휠베이스", (c) => c.wheelbase && `${fmt(c.wheelbase)} mm`, (c) => c.wheelbase, "max"],
    ["공차중량", (c) => c.weight && `${fmt(c.weight)} kg`, (c) => c.weight, "min"],
    ["Chassis"],
    ["서스펜션", (c) => (c.suspension?.front || c.suspension?.rear) ? `앞 ${c.suspension.front || "—"} / 뒤 ${c.suspension.rear || "—"}` : null],
    ["승차감", (c) => c.ride],
  ];

  function renderComparePick() {
    const opts = (sel) => `<option value="">— 선택 안 함 —</option>` +
      state.cars.map((c) => `<option value="${c.id}" ${c.id === sel ? "selected" : ""}>${c.year} ${esc(c.name)}</option>`).join("");
    $("#comparePick").innerHTML = [0, 1, 2].map((i) => {
      const c = carById(state.compareIds[i]);
      return `
        <div class="compare-slot">
          <label class="label" for="cmp${i}">차량 ${String.fromCharCode(65 + i)}</label>
          <select id="cmp${i}" class="select" data-slot="${i}">${opts(state.compareIds[i])}</select>
          ${c ? photo(c) : `<figure class="photo is-empty"></figure>`}
        </div>`;
    }).join("");
    $("#comparePick").onchange = (e) => {
      const s = e.target.closest("select");
      if (!s) return;
      state.compareIds[+s.dataset.slot] = s.value || null;
      renderComparePick();
      renderCompare();
    };
  }

  let cmpSeq = 0;
  async function renderCompare() {
    const cs = state.compareIds.map(carById).filter(Boolean);
    const table = $("#compareTable"), box = $("#compareSummary");
    if (cs.length < 2) {
      table.innerHTML = `<tbody><tr><td class="is-na">비교하려면 차량을 2대 이상 선택하세요.</td></tr></tbody>`;
      box.hidden = true;
      return;
    }
    let html = `<thead><tr><th></th>${cs.map((c) => `<th>${esc(c.name)}<small>${c.year} · ${esc(c.maker)}</small></th>`).join("")}</tr></thead><tbody>`;
    CMP_ROWS.forEach(([label, get, num, best]) => {
      if (!get) { html += `<tr class="group-row"><th colspan="${cs.length + 1}">${label}</th></tr>`; return; }
      let bestVal = null;
      if (num) {
        const vals = cs.map(num).filter((v) => v != null);
        if (vals.length > 1) bestVal = best === "max" ? Math.max(...vals) : Math.min(...vals);
      }
      html += `<tr><th>${label}</th>${cs.map((c) => {
        const v = get(c);
        const isBest = bestVal != null && num(c) === bestVal;
        return `<td class="${v == null || v === "" ? "is-na" : ""} ${isBest ? "is-best" : ""}">${v == null || v === "" ? "확인되지 않음" : esc(v)}</td>`;
      }).join("")}</tr>`;
    });
    table.innerHTML = html + "</tbody>";

    const seq = ++cmpSeq;
    box.hidden = false;
    box.innerHTML = `<span class="msg__avatar"></span><div><h4>AI 비교 요약</h4><div class="progress-line" style="margin:0"><span class="bar"></span><span>메타데이터 근거로 요약하는 중</span></div></div>`;
    try {
      const out = await API.compare(cs.map((c) => c.id), settings.model);
      if (seq !== cmpSeq) return;
      box.innerHTML = `<span class="msg__avatar"></span><div class="msg__body"><h4>AI 비교 요약 · ${esc(modelLabel(out.model))}</h4><div class="msg__text">${renderRich(out.summary, out.citations)}</div>${sourcesHTML(out.citations, "비교에 사용한 근거")}</div>`;
    } catch (err) {
      if (seq !== cmpSeq) return;
      box.innerHTML = `<span class="msg__avatar"></span><div><h4>AI 비교 요약</h4>${warnBox(err.code)}</div>`;
    }
  }

  /* =========================================================
     Fact check (F2010)
     ========================================================= */
  function bindFact() {
    const examples = [
      ["audi-quattro-1980", "아우디 콰트로는 5기통 터보 엔진을 얹은 사륜구동 차다"],
      ["tesla-roadster-2008", "테슬라 로드스터는 전륜구동이다"],
      ["bmw-ix3-2026", "BMW iX3는 469마력을 낸다"],
      ["ford-model-t-1908", "모델 T는 조립 라인으로 대량 생산되었다"],
    ];
    $("#factExamples").innerHTML = examples.map(([, t], i) => `<button class="chip" type="button" data-i="${i}">${t}</button>`).join("");
    $("#factExamples").addEventListener("click", (e) => {
      const b = e.target.closest(".chip");
      if (!b) return;
      const [id, t] = examples[+b.dataset.i];
      $("#factCar").value = id;
      $("#factClaim").value = t;
      $("#factForm").requestSubmit();
    });
    $("#factForm").addEventListener("submit", async (e) => {
      e.preventDefault();
      const car_id = $("#factCar").value, claim = $("#factClaim").value.trim();
      if (!car_id || !claim) { toast("차량과 주장을 모두 입력하세요"); return; }
      const prog = $("#factProgress"), out = $("#factResult");
      out.innerHTML = "";
      prog.hidden = false;
      prog.innerHTML = `<span class="bar"></span><span class="txt">근거 문서를 검색해 주장과 대조하는 중</span>`;
      try {
        const r = await API.factcheck(car_id, claim, settings.model);
        prog.hidden = true;
        const word = { true: "사실", false: "사실 아님", unknown: "확인 불가" }[r.verdict];
        out.innerHTML = `
          <div class="verdict">
            <div class="verdict__badge" data-v="${r.verdict}">
              <span class="verdict__label">Verdict</span>
              <span class="verdict__word">${word}</span>
              <span class="verdict__claim">“${esc(claim)}”</span>
            </div>
            <div class="verdict__body msg__body">
              <p class="eyebrow">${esc(carById(car_id).name)} · 판정 근거</p>
              <div class="msg__text">${renderRich(r.explanation, r.citations)}</div>
              ${sourcesHTML(r.citations, "판정에 사용한 근거")}
            </div>
          </div>`;
      } catch (err) {
        prog.hidden = true;
        out.innerHTML = warnBox(err.code);
      }
    });
  }

  function renderFactSelect() {
    $("#factCar").innerHTML = `<option value="">차량 선택</option>` +
      state.cars.map((c) => `<option value="${c.id}">${c.year} ${esc(c.name)}</option>`).join("");
  }

  /* =========================================================
     Boot
     ========================================================= */
  async function boot() {
    bindNav();
    UI.bindDrawer((key) => {
      if (key === "top_k" || key === "search_type") updateHeroMode();
      if (key === "show_retrieved" && state.selected) chat.render();
    });
    bindChat();
    bindExplore();
    bindFact();
    updateHeroMode();
    renderEraFilter();
    $("#composer").classList.add("is-disabled");
    const statusP = loadStatus();
    try { state.cars = await API.cars(); } catch { state.cars = []; }
    state.byId = new Map(state.cars.map((c) => [c.id, c]));
    await statusP;
    renderHero();
    renderChronicle();
    renderFuelFilter();
    renderCarList();
    renderComparePick();
    renderFactSelect();
    // chat.html 등에서 ?view=explore 처럼 들어오면 해당 탭을 연다
    const view = new URLSearchParams(location.search).get("view");
    if (view && $(`#view-${view}`)) { switchView(view); setTimeout(() => $("#workspace").scrollIntoView(), 50); }
    if (state.cars.length) {
      selectCar(carById("bmw-ix3-2026") ? "bmw-ix3-2026" : state.cars[state.cars.length - 1].id);
      renderCompare();
    }
  }

  boot();
})();
