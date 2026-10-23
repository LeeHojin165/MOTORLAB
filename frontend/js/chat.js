/* =========================================================
   MOTORLAB — 질의응답 전용 페이지 (chat.html)
   주소: chat.html?car={차량 ID}&q={질문}   q가 있으면 바로 질문한다
   ========================================================= */
(function () {
  "use strict";

  const { $, esc, FUEL_FILTER, photo, specHTML, carItemHTML, matchCar } = window.UI;
  const LAST_CAR_KEY = "motorlab.lastCar";
  const MOBILE = () => window.matchMedia("(max-width: 900px)").matches;

  const state = { cars: [], byId: new Map(), selected: null, fuel: "all" };
  const carById = (id) => state.byId.get(id);

  /* ---------------- 상태 표시 (F2012) ---------------- */
  async function loadStatus() {
    const st = await UI.loadStatus({ pill: $("#statusPill"), alerts: $("#sysAlerts") });
    if (st && !loadStatus.done) { loadStatus.done = true; UI.applyServerStatus(st); }
  }

  /* ---------------- 사이드바 · 제원 패널 열고 닫기 ---------------- */
  const cp = $("#cp"), scrim = $("#cpScrim");
  function setSide(open) {
    cp.classList.toggle("side-open", open);
    cp.classList.toggle("side-closed", !open);
    syncScrim();
  }
  function setSpec(open) {
    cp.classList.toggle("spec-open", open);
    $("#specPanel").setAttribute("aria-hidden", String(!open));
    $("#toggleSpec").setAttribute("aria-expanded", String(open));
    $("#toggleSpec").textContent = open ? "제원 닫기" : "제원 보기";
    syncScrim();
  }
  function syncScrim() {
    scrim.hidden = !(MOBILE() && (cp.classList.contains("side-open") || cp.classList.contains("spec-open")));
  }

  /* ---------------- 차량 목록 ---------------- */
  function renderFuelFilter() {
    const root = $("#fuelFilter");
    root.innerHTML = FUEL_FILTER.map(([v, l]) => `<button class="chip ${v === state.fuel ? "is-active" : ""}" data-fuel="${v}">${l}</button>`).join("");
  }

  function renderCarList() {
    const q = $("#carSearch").value.trim().toLowerCase();
    const list = state.cars.filter((c) => matchCar(c, q, state.fuel));
    const ul = $("#carList");
    if (!state.cars.length) { ul.innerHTML = `<li class="car-list__empty">차량 목록을 불러오지 못했습니다.</li>`; return; }
    if (!list.length) { ul.innerHTML = `<li class="car-list__empty">"${esc(q)}"와 일치하는 차량이 없습니다.</li>`; return; }
    ul.innerHTML = list.map((c) => carItemHTML(c, state.selected?.id === c.id)).join("");
  }

  async function refreshDocs(id) {
    $("#barDocs").textContent = "";
    try {
      const docs = await API.carDocs(id);
      if (state.selected?.id === id) $("#barDocs").textContent = `수집 문서 ${docs.length}건`;
    } catch { /* 상단 안내가 담당 */ }
  }

  let chat;
  function selectCar(id, { closeSide = true } = {}) {
    const c = carById(id);
    if (!c) return;
    state.selected = c;
    renderCarList();
    $("#chatMaker").textContent = `${c.maker} · ${c.country} · ${c.trim} 기준`;
    $("#chatTitle").innerHTML = `${esc(c.name)}<small>${c.year}</small>`;
    $("#barThumb").innerHTML = c.image ? `<img src="${esc(c.image.src)}" alt="">` : "";
    $("#question").placeholder = `${c.name}에 대해 질문하세요 — 엔진, 변속기, 출력, 연비, 치수, 서스펜션, 승차감…`;
    $("#composer").classList.remove("is-disabled");
    $("#specPanel").innerHTML = specHTML(c);
    refreshDocs(id);
    try { localStorage.setItem(LAST_CAR_KEY, id); } catch { /* 무시 */ }
    const url = new URL(location.href);
    url.searchParams.set("car", id);
    url.searchParams.delete("q");
    history.replaceState(null, "", url);
    chat.render();
    if (closeSide && MOBILE()) setSide(false);
  }

  /* ---------------- 대화 ---------------- */
  function bindChat() {
    chat = ChatCore.create({
      log: $("#chatLog"),
      composer: $("#composer"),
      textarea: $("#question"),
      suggest: $("#suggest"),
      clearBtn: $("#clearChat"),
      getCar: () => state.selected,
      emptyHTML: (c) => `
        <div class="cp-welcome">
          ${photo(c, { eager: true })}
          <div class="cp-welcome__text">
            <p class="eyebrow">${esc(c.maker)} · ${c.year}</p>
            <h2>${esc(c.name)}</h2>
            <p>엔진·변속기·출력·토크·구동방식·연비·치수·서스펜션·승차감·역사까지 무엇이든 물어보세요.<br>모든 답변에는 근거 번호와 원문 출처가 붙습니다.</p>
          </div>
        </div>`,
      onAnswered: (c) => { refreshDocs(c.id); loadStatus(); },
    });
    $("#suggest").innerHTML = ChatCore.suggestHTML();
  }

  /* ---------------- 이벤트 ---------------- */
  function bindUI() {
    UI.bindDrawer((key) => { if (key === "show_retrieved" && state.selected) chat.render(); });
    $("#carSearch").addEventListener("input", renderCarList);
    $("#fuelFilter").addEventListener("click", (e) => {
      const b = e.target.closest("[data-fuel]");
      if (!b) return;
      state.fuel = b.dataset.fuel;
      renderFuelFilter();
      renderCarList();
    });
    $("#carList").addEventListener("click", (e) => { const b = e.target.closest("[data-car]"); if (b) selectCar(b.dataset.car); });
    $("#toggleSide").addEventListener("click", () => setSide(!cp.classList.contains("side-open")));
    $("#toggleSpec").addEventListener("click", () => setSpec(!cp.classList.contains("spec-open")));
    scrim.addEventListener("click", () => { setSide(false); setSpec(false); });
    $("#openMenu").addEventListener("click", () => { const m = $("#mobileMenu"); m.hidden = !m.hidden; });
    document.addEventListener("keydown", (e) => {
      if (e.key === "/" && document.activeElement?.tagName !== "TEXTAREA" && document.activeElement?.tagName !== "INPUT") {
        e.preventDefault();
        $("#question").focus();
      }
    });
    window.addEventListener("resize", syncScrim);
  }

  /* ---------------- 시작 ---------------- */
  async function boot() {
    bindUI();
    bindChat();
    renderFuelFilter();
    setSide(!MOBILE());
    $("#composer").classList.add("is-disabled");
    const statusP = loadStatus();
    try { state.cars = await API.cars(); } catch { state.cars = []; }
    state.byId = new Map(state.cars.map((c) => [c.id, c]));
    $("#carCount").textContent = state.cars.length;
    await statusP;
    renderCarList();
    if (!state.cars.length) return;

    const params = new URLSearchParams(location.search);
    let last = null;
    try { last = localStorage.getItem(LAST_CAR_KEY); } catch { /* 무시 */ }
    const id = [params.get("car"), last, "bmw-ix3-2026"].find((x) => x && carById(x)) || state.cars[state.cars.length - 1].id;
    const q = params.get("q");
    selectCar(id, { closeSide: false });
    // 선택된 차량이 목록에서 보이도록
    $(`#carList [data-car="${CSS.escape(id)}"]`)?.scrollIntoView({ block: "center" });
    if (q) chat.ask(q);
    else if (!MOBILE()) $("#question").focus({ preventScroll: true });
  }

  boot();
})();
