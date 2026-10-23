/* =========================================================
   MOTORLAB — 공통 UI (메인 페이지 · 질의응답 페이지가 함께 사용)
   렌더링 함수, 검색 설정 저장, 설정 드로어, 근거 목록 연동
   ========================================================= */
window.UI = (function () {
  "use strict";

  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (ch) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch]));
  const fmt = (n) => (n == null ? null : Number(n).toLocaleString("ko-KR"));

  const FUEL = { gasoline: "가솔린", diesel: "디젤", electric: "전기", hybrid: "하이브리드", hydrogen: "수소전기" };
  const FUEL_FILTER = [["all", "전체"], ["gasoline", "가솔린"], ["diesel", "디젤"], ["hybrid", "하이브리드"], ["electric", "전기"], ["hydrogen", "수소"]];
  const SRC_LABEL = { meta: "메타데이터", wiki: "위키백과", pdf: "PDF" };
  const MODEL_LABEL = { "gpt-4o": "GPT-4o", "gpt-4o-mini": "GPT-4o mini" };
  const modelLabel = (m) => MODEL_LABEL[m] || (m || "").replace(/^claude-(\w+)-(\d)-(\d)-\d+$/, (_, n, a, b) => `Claude ${n[0].toUpperCase() + n.slice(1)} ${a}.${b}`);

  /* ---------------- 사진 ---------------- */
  function credit(img) {
    if (!img) return "";
    const by = img.artist.length > 40 ? img.artist.slice(0, 38) + "…" : img.artist;
    return `사진: <a href="${esc(img.page)}" target="_blank" rel="noopener">${esc(by)}</a> · ${esc(img.license || "Wikimedia Commons")}`;
  }
  function photo(c, { eager = false, showCredit = true } = {}) {
    if (!c.image) return `<figure class="photo photo--fallback"><svg aria-hidden="true"><use href="#sil-sedan"/></svg></figure>`;
    return `<figure class="photo">
      <img src="${esc(c.image.src)}" alt="${esc(c.name)} 사진" loading="${eager ? "eager" : "lazy"}" decoding="async" data-loading onload="this.removeAttribute('data-loading')" onerror="this.closest('figure').classList.add('photo--fallback');this.remove()">
      ${showCredit ? `<figcaption class="photo__credit">${credit(c.image)}</figcaption>` : ""}
    </figure>`;
  }

  /* ---------------- toast ---------------- */
  let toastTimer;
  function toast(msg) {
    const t = $("#toast");
    if (!t) return;
    t.textContent = msg;
    t.classList.add("is-show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => t.classList.remove("is-show"), 2400);
  }

  /* ---------------- 오류 문구 (NF2004: 서버 오류 원문은 보여주지 않음) ---------------- */
  const ERR_MSG = {
    NO_API_KEY: "API 키가 설정되지 않아 답변을 생성할 수 없습니다. 서버의 <code>.env</code>에 <code>OPENAI_API_KEY</code>를 넣고 서버를 다시 시작하세요.",
    NO_INDEX: "색인된 데이터가 없습니다. <code>python -m scripts.build_index --bundle</code>을 먼저 실행하세요.",
    NO_RESULT: "해당 차량을 찾지 못했습니다.",
    NETWORK: "서버에 연결할 수 없습니다. <code>uvicorn backend.server:app</code>이 실행 중인지 확인하세요.",
    BAD_REQUEST: "입력값을 확인해 주세요.",
    UPSTREAM: "일시적인 오류로 답변하지 못했습니다. 잠시 후 다시 시도해 주세요.",
  };
  const errMsg = (code) => ERR_MSG[code] || ERR_MSG.UPSTREAM;
  const warnBox = (code, extra = "") => `<div class="notice notice--warn" ${extra}><svg><use href="#ico-alert"/></svg><span>${errMsg(code)}</span></div>`;

  /* ---------------- 본문 · 근거 렌더링 (F2008 / F2016) ---------------- */
  // "[근거 n]" → 인용 칩, "- " → 목록, **굵게**
  function renderRich(text, citations) {
    const typeOf = (n) => citations.find((x) => x.n === n)?.type || "meta";
    const inline = (s) => esc(s)
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      .replace(/\[근거\s*(\d+)\]/g, (_, n) => `<span class="cite" data-n="${n}" data-type="${typeOf(+n)}" role="button" tabindex="0" title="근거 ${n} 보기">${n}</span>`);
    const out = [];
    let list = [];
    const flush = () => { if (list.length) { out.push(`<ul>${list.join("")}</ul>`); list = []; } };
    text.split("\n").forEach((line) => {
      if (/^\s*[-*•]\s+/.test(line)) list.push(`<li>${inline(line.replace(/^\s*[-*•]\s+/, ""))}</li>`);
      else { flush(); if (line.trim()) out.push(`<p>${inline(line.replace(/^#+\s*/, ""))}</p>`); }
    });
    flush();
    return out.join("");
  }

  function sourceRow(s) {
    const label = s.type === "wiki" ? `위키백과 ${String(s.lang || "").toUpperCase()}` : SRC_LABEL[s.type] || s.type;
    const where = s.page ? ` · p.${s.page}` : "";
    return `
      <li class="source" data-n="${s.n}">
        <span class="source__no">[${s.n}]</span>
        <div>
          <div class="source__title"><span class="src-badge" data-type="${s.type}" data-lang="${s.lang || ""}">${label}</span>${esc(s.title)}${where}</div>
          ${s.snippet ? `<div class="source__snippet">${esc(s.snippet)}</div>` : ""}
          ${s.chunk_id ? `<span class="source__id">${esc(s.chunk_id)}${s.score != null ? ` · 유사도 ${s.score.toFixed(3)}` : s.type === "meta" ? " · 항상 포함" : " · MMR 선택"}</span>` : ""}
        </div>
        ${s.url ? `<a class="source__link" href="${esc(s.url)}" target="_blank" rel="noopener">원문 ↗</a>` : `<span class="source__link source__link--plain">${s.type === "pdf" ? "PDF" : "메타데이터"}</span>`}
      </li>`;
  }

  function sourcesHTML(citations, title = "답변에 사용한 근거", extraCls = "") {
    if (!citations.length) {
      return `<div class="notice"><svg><use href="#ico-info"/></svg><span>답변에 인용된 근거가 없습니다. 색인된 문서에서 확인되지 않는 내용일 수 있습니다.</span></div>`;
    }
    return `
      <div class="sources is-open ${extraCls}">
        <button class="sources__head" type="button">${title} ${citations.length}건</button>
        <ul class="sources__list">${citations.map(sourceRow).join("")}</ul>
      </div>`;
  }

  /* ---------------- 제원표 ---------------- */
  function specRow(k, v, unit = "") {
    const na = v == null || v === "";
    return `<div class="spec-row"><dt>${k}</dt><dd class="${na ? "is-na" : ""}">${na ? "확인되지 않음" : esc(v) + unit}</dd></div>`;
  }

  function specHTML(c) {
    const kpi = (v, unit, k) => `<div class="spec-kpi"><div class="spec-kpi__v">${v == null ? "—" : v}${v == null ? "" : `<small>${unit}</small>`}</div><div class="spec-kpi__k">${k}</div></div>`;
    const s = c.suspension || {};
    return `
      <div class="spec-hero">
        <div class="spec-hero__tags">
          <span class="tag tag--fuel-${c.fuel}">${FUEL[c.fuel]}</span>
          <span class="tag">${esc(c.driveCode)}</span>
          <span class="tag">${esc(c.bodyType)}</span>
        </div>
        ${photo(c, { eager: true })}
        <div class="spec-kpis">
          ${kpi(c.powerPs != null ? fmt(c.powerPs) : null, "PS", "최고출력")}
          ${kpi(c.torqueNm != null ? fmt(c.torqueNm) : null, "N·m", "최대토크")}
          ${kpi(c.zeroTo100, "s", "0–100 km/h")}
        </div>
      </div>
      <div class="spec-group"><h4>Powertrain</h4><dl>
        ${specRow("기준 트림", c.trim)}
        ${specRow("동력원", FUEL[c.fuel])}
        ${specRow("엔진 · 모터", c.engine)}
        ${specRow("변속기", c.transmission)}
        ${specRow("구동방식", c.drive)}
        ${specRow("최고출력", c.powerText)}
        ${specRow("최대토크", c.torqueNm != null ? fmt(c.torqueNm) : null, " N·m")}
      </dl></div>
      <div class="spec-group"><h4>Performance · Efficiency</h4><dl>
        ${specRow("0–100 km/h", c.zeroTo100, " 초")}
        ${specRow("최고속도", c.topSpeed, " km/h")}
        ${specRow("공인 연비", c.efficiency)}
      </dl></div>
      <div class="spec-group"><h4>Body</h4><dl>
        ${specRow("차종", c.bodyType)}
        ${specRow("전장", fmt(c.length), " mm")}
        ${specRow("전폭", fmt(c.width), " mm")}
        ${specRow("전고", fmt(c.height), " mm")}
        ${specRow("휠베이스", fmt(c.wheelbase), " mm")}
        ${specRow("공차중량", fmt(c.weight), " kg")}
      </dl></div>
      <div class="spec-group"><h4>Chassis</h4><dl>
        ${specRow("앞 서스펜션", s.front)}
        ${specRow("뒤 서스펜션", s.rear)}
        ${specRow("승차감", c.ride)}
      </dl></div>`;
  }

  /* ---------------- 차량 목록 항목 ---------------- */
  function carItemHTML(c, active) {
    return `
      <li><button class="car-item ${active ? "is-active" : ""}" data-car="${c.id}">
        ${c.image ? `<img class="car-item__thumb" src="${esc(c.image.src)}" alt="" loading="lazy">` : `<span class="car-item__thumb"></span>`}
        <span><span class="car-item__name">${esc(c.name)}</span><span class="car-item__meta">${c.year} · ${esc(c.maker)} · ${FUEL[c.fuel]}</span></span>
      </button></li>`;
  }

  const matchCar = (c, q, fuel) => (fuel === "all" || c.fuel === fuel) &&
    (!q || [c.name, c.nameEn, c.maker, c.trim, String(c.year)].join(" ").toLowerCase().includes(q));

  /* ---------------- 검색 설정 (두 페이지가 localStorage로 공유) ---------------- */
  const SETTINGS_KEY = "motorlab.settings";
  const settings = { top_k: 6, search_type: "similarity", compare_rag: false, show_retrieved: false, model: null };
  let savedSettings = false;
  try {
    const raw = localStorage.getItem(SETTINGS_KEY);
    if (raw) { Object.assign(settings, JSON.parse(raw)); savedSettings = true; }
  } catch { /* 저장소를 못 쓰면 기본값 사용 */ }
  function saveSettings() {
    try { localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings)); } catch { /* 무시 */ }
  }

  function segmented(sel, attr, onChange) {
    const root = $(sel);
    if (!root) return;
    root.addEventListener("click", (e) => {
      const b = e.target.closest("button");
      if (!b || b.classList.contains("is-active")) return;
      $$("button", root).forEach((x) => x.classList.toggle("is-active", x === b));
      onChange(b.dataset[attr]);
    });
  }
  const setSegment = (sel, attr, value) => $$(`${sel} button`).forEach((b) => b.classList.toggle("is-active", b.dataset[attr] === value));

  /** 설정 드로어 연결. onChange(key)는 설정이 바뀔 때 호출된다. */
  function bindDrawer(onChange = () => {}) {
    const drawer = $("#settingsDrawer"), scrim = $("#scrim");
    const open = () => { drawer.classList.add("is-open"); drawer.setAttribute("aria-hidden", "false"); scrim.hidden = false; };
    const close = () => { drawer.classList.remove("is-open"); drawer.setAttribute("aria-hidden", "true"); scrim.hidden = true; };
    $("#openSettings").addEventListener("click", open);
    $("#closeSettings").addEventListener("click", close);
    scrim.addEventListener("click", close);
    document.addEventListener("keydown", (e) => e.key === "Escape" && close());

    const topk = $("#setTopK");
    topk.addEventListener("input", () => { settings.top_k = +topk.value; $("#outTopK").textContent = topk.value; saveSettings(); onChange("top_k"); });
    segmented("#setModel", "model", (v) => { settings.model = v; saveSettings(); toast(`답변 모델: ${modelLabel(v)}`); onChange("model"); });
    segmented("#setMode", "mode", (v) => { settings.search_type = v; saveSettings(); toast(v === "mmr" ? "MMR 검색으로 전환했습니다" : "유사도 검색으로 전환했습니다"); onChange("search_type"); });
    $("#setCompareRag").addEventListener("change", (e) => { settings.compare_rag = e.target.checked; saveSettings(); toast(e.target.checked ? "다음 질문부터 RAG 미사용 답변을 함께 표시합니다" : "RAG 전후 비교를 껐습니다"); onChange("compare_rag"); });
    $("#setShowRetrieved").addEventListener("change", (e) => { settings.show_retrieved = e.target.checked; saveSettings(); onChange("show_retrieved"); });
  }

  /** 서버 상태를 받아 드로어 내용과 설정 초기값을 채운다. */
  function applyServerStatus(st) {
    const cfg = st.settings;
    if (!savedSettings) {   // 저장된 설정이 없으면 서버 기본값
      settings.top_k = cfg.top_k;
      settings.search_type = cfg.search_type;
      settings.model = cfg.answer_model;
    }
    if (!cfg.models.includes(settings.model)) settings.model = cfg.answer_model;
    $("#setModel").innerHTML = cfg.models.map((m) => `<button type="button" data-model="${esc(m)}" class="${m === settings.model ? "is-active" : ""}">${esc(modelLabel(m))}</button>`).join("");
    $("#utilityModel").textContent = modelLabel(cfg.utility_model);
    $("#setTopK").value = settings.top_k;
    $("#outTopK").textContent = settings.top_k;
    setSegment("#setMode", "mode", settings.search_type);
    $("#setCompareRag").checked = settings.compare_rag;
    $("#setShowRetrieved").checked = settings.show_retrieved;
    $("#serverInfo").innerHTML = [
      ["청크 크기", `${fmt(cfg.chunk_size)}자`], ["중복 길이", `${fmt(cfg.chunk_overlap)}자`], ["MMR 후보 수", fmt(cfg.mmr_fetch_k)],
      ["답변 기본 모델", modelLabel(cfg.answer_model)], ["프롬프트 1·2 모델", modelLabel(cfg.utility_model)], ["임베딩 모델", cfg.embedding_model],
      ["문서 수집", cfg.offline_collect ? "제공 묶음만" : "위키백과 실시간"],
      ["색인", `메타 ${fmt(st.meta_count)} · 문서 ${fmt(st.doc_count)} · 청크 ${fmt(st.chunk_count)}`],
    ].map(([k, v]) => `<div><dt>${k}</dt><dd>${esc(v)}</dd></div>`).join("");
  }

  /** 상단 상태 표시와 경고 상자 (F2012). 실패 시 null 반환 */
  async function loadStatus({ pill, alerts }) {
    const items = [];
    let st = null;
    try {
      st = await API.status();
      pill.className = "status-pill";
      if (!st.api_key_ok) { pill.classList.add("is-bad"); $(".status-pill__text", pill).textContent = "API 키 누락"; }
      else if (!st.meta_count) { pill.classList.add("is-warn"); $(".status-pill__text", pill).textContent = "색인 없음"; }
      else { pill.classList.add("is-ok"); $(".status-pill__text", pill).textContent = `색인 ${fmt(st.meta_count)}건 · 정상`; }
      if (!st.api_key_ok) items.push(["bad", "API 키가 설정되지 않았습니다", ERR_MSG.NO_API_KEY + " 키는 화면에 표시되지 않습니다."]);
      if (!st.meta_count) items.push(["warn", "색인된 차량 데이터가 없습니다", ERR_MSG.NO_INDEX]);
    } catch {
      pill.className = "status-pill is-bad";
      $(".status-pill__text", pill).textContent = "서버 연결 실패";
      items.push(["bad", "서버에 연결할 수 없습니다", ERR_MSG.NETWORK + " 접속 주소는 <code>http://localhost:8000</code>입니다."]);
    }
    if (alerts) alerts.innerHTML = items.map(([lv, t, d]) => `
      <div class="alert ${lv === "bad" ? "alert--bad" : ""}" role="alert">
        <svg><use href="#ico-alert"/></svg>
        <div><strong>${t}</strong><p>${d}</p></div>
      </div>`).join("");
    return st;
  }

  /* ---------------- 근거 목록 접기 · 인용 칩 연동 (페이지 전체) ---------------- */
  document.addEventListener("click", (e) => {
    const head = e.target.closest(".sources__head");
    if (head) { head.parentElement.classList.toggle("is-open"); return; }
    const cite = e.target.closest(".cite");
    if (!cite) return;
    const scope = cite.closest(".msg__body, .ai-card, .verdict__body");
    const src = scope && scope.querySelector(`.source[data-n="${cite.dataset.n}"]`);
    if (!src) return;
    src.closest(".sources").classList.add("is-open");
    src.classList.add("is-hot");
    cite.classList.add("is-hot");
    src.scrollIntoView({ behavior: "smooth", block: "nearest" });
    setTimeout(() => { src.classList.remove("is-hot"); cite.classList.remove("is-hot"); }, 1600);
  });

  return {
    $, $$, esc, fmt, FUEL, FUEL_FILTER, modelLabel, credit, photo, toast, ERR_MSG, errMsg, warnBox,
    renderRich, sourcesHTML, specHTML, carItemHTML, matchCar,
    settings, saveSettings, segmented, setSegment, bindDrawer, applyServerStatus, loadStatus,
  };
})();
