"use strict";

const DATA_URL = "data/xian.json";
const DEFAULT_CHAPTER_ID = "ch01-ground-before-time";

const categoryLabels = {
  history: { zh: "历史", ja: "歴史", en: "History" },
  food: { zh: "饮食", ja: "食", en: "Food" },
  attractions: { zh: "景点", ja: "見どころ", en: "Attractions" },
  transport: { zh: "交通", ja: "交通", en: "Transport" },
  hotels: { zh: "住宿", ja: "宿", en: "Hotels" },
  itineraries: { zh: "行程", ja: "旅程", en: "Itineraries" },
  "cultural-context": { zh: "文化脉络", ja: "文化背景", en: "Context" },
  practical: { zh: "实用方位", ja: "実用案内", en: "Field notes" },
  maps: { zh: "地图", ja: "地図", en: "Map" },
};

const languageNames = { zh: "中文", ja: "日本語", en: "ENGLISH" };
const assetLabels = {
  "asset-xian-before-walls-map": "XI'AN BEFORE THE WALLS",
  "asset-xian-yongning-gate-arrival": "YONGNING GATE · CITY THRESHOLD",
  "asset-xian-capital-layers-map": "SUCCESSIVE CAPITALS, DIFFERENT SITES",
  "asset-xian-daming-site-impression": "DAMING PALACE · SITE-SCALE IMPRESSION",
  "asset-xian-qin-mausoleum-pits-map": "QIN MAUSOLEUM · MOUND AND VISITOR PITS",
  "asset-xian-terracotta-pit-one-visit": "TERRACOTTA ARMY · PIT 1 AT FIRST SIGHT",
  "asset-xian-terracotta-conservation-impression": "TERRACOTTA · CONSERVATION WORK",
  "asset-xian-written-word-route-map": "PAGODAS TO BEILIN · WRITTEN-WORD ROUTE",
  "asset-xian-rubbing-replica-demonstration": "RUBBING ON A MODERN REPLICA",
  "asset-xian-big-wild-goose-pagoda-visit": "BIG WILD GOOSE PAGODA · COURTYARD VIEW",
  "asset-xian-inside-wall-route-map": "INSIDE THE WALL · CROSSROADS AND LANES",
  "asset-xian-city-wall-walk": "XI'AN CITY WALL · WIDTH AND DISTANCE",
  "asset-xian-bell-tower-orientation": "BELL TOWER · FOUR-AVENUE CENTRE",
  "asset-xian-lane-courtyard-threshold": "LANE TO COURTYARD · THE THRESHOLD",
  "asset-xian-food-contexts-map": "XI'AN FOOD · FOUR CONTEXTS",
  "asset-xian-breaking-mo-table": "PAOMO · BREAKING THE MO",
  "asset-xian-nearby-day-choices-map": "XI'AN AROUND · FIVE ONE-DAY CHOICES",
  "asset-xian-managed-mountain-day": "MOUNTAIN DAY · MANAGED TRAIL",
  "asset-xian-arrival-hubs-map": "ARRIVING IN XI'AN · FOUR HUBS",
  "asset-xian-north-interchange": "XI'AN NORTH · CHOOSE THE NEXT LEG",
  "asset-xian-stay-areas-map": "WHERE TO STAY · FIVE ITINERARY ANCHORS",
  "asset-xian-south-gate-hotel-arrival": "SOUTH GATE · FIND THE ACTUAL ENTRANCE",
  "asset-xian-itinerary-days-map": "TWO, THREE OR FIVE DAYS · ONE COHERENT ROUTE",
  "asset-xian-small-wild-goose-route-morning": "SMALL WILD GOOSE PAGODA · ONE MORNING GROUP",
  "asset-xian-before-departure-four-guides": "BEFORE DEPARTURE · FOUR EVIDENCE CHECKS",
};
const state = {
  document: null,
  chapter: null,
  citationNumbers: new Map(),
  mode: "parallel",
};

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function storedPreference(key, fallback) {
  try {
    return window.localStorage.getItem(key) || fallback;
  } catch {
    return fallback;
  }
}

function savePreference(key, value) {
  try {
    window.localStorage.setItem(key, value);
  } catch {
    // Preferences are optional when storage is unavailable.
  }
}

function localizedValue(values) {
  if (state.mode === "zh" || state.mode === "ja" || state.mode === "en") {
    return values[state.mode];
  }
  return values.en;
}

function availableChapters(documentData) {
  return documentData.chapters.filter((chapter) => chapter.blocks.length > 0);
}

function chapterIdFromLocation(documentData) {
  const requested = new URL(window.location.href).searchParams.get("chapter");
  const availableIds = new Set(availableChapters(documentData).map((chapter) => chapter.id));
  return availableIds.has(requested) ? requested : DEFAULT_CHAPTER_ID;
}

function renderLanguageSet(values, className) {
  const wrapper = element("div", className);
  for (const language of ["zh", "ja", "en"]) {
    const item = element("span", "", values[language]);
    item.dataset.lang = language;
    item.lang = language === "zh" ? "zh-Hans" : language;
    wrapper.append(item);
  }
  return wrapper;
}

function renderTokens(layer, language) {
  const fragment = document.createDocumentFragment();
  for (const token of layer.tokens) {
    if (!token.reading) {
      fragment.append(document.createTextNode(token.text));
      continue;
    }
    const ruby = document.createElement("ruby");
    ruby.lang = language === "zh" ? "zh-Hans" : "ja";
    ruby.append(document.createTextNode(token.text));
    const reading = element("rt", "", token.reading);
    reading.lang = language === "zh" ? "zh-Latn-pinyin" : "ja-Hira";
    ruby.append(reading);
    fragment.append(ruby);
  }
  return fragment;
}

function citationOrder(chapter) {
  const seen = new Set();
  const ordered = [];
  for (const block of chapter.blocks) {
    for (const citationId of block.citation_ids) {
      if (!seen.has(citationId)) {
        seen.add(citationId);
        ordered.push(citationId);
      }
    }
  }
  return ordered;
}

function buildCitationNumbers(chapter) {
  return new Map(citationOrder(chapter).map((citationId, index) => [citationId, index + 1]));
}

function renderBlockCitations(block) {
  const wrapper = element("div", "block-citations");
  wrapper.append(element("span", "", "SOURCES"));
  for (const citationId of block.citation_ids) {
    const number = state.citationNumbers.get(citationId);
    const link = element("a", "", `[${number}]`);
    link.href = `#source-${number}`;
    link.setAttribute("aria-label", `Source ${number}`);
    wrapper.append(link);
  }
  return wrapper;
}

function mapButton(label, text, action) {
  const button = element("button", "", text);
  button.type = "button";
  button.title = label;
  button.setAttribute("aria-label", label);
  button.addEventListener("click", action);
  return button;
}

function renderVisualCaption(asset, className) {
  const caption = element("figcaption", className);
  const captions = element("div", "caption-grid");
  for (const language of ["zh", "ja", "en"]) {
    const paragraph = element("p", "", asset.captions[language]);
    paragraph.dataset.lang = language;
    paragraph.lang = language === "zh" ? "zh-Hans" : language;
    captions.append(paragraph);
  }
  caption.append(captions);
  if (asset.provenance?.method !== "generated") {
    caption.append(element("p", "visual-rights", asset.rights));
  }
  return caption;
}

function renderMap(asset, number) {
  const figure = element("figure", "map-figure");
  const bar = element("div", "map-bar");
  const visualLabel = assetLabels[asset.id] || asset.id.replace(/^asset-/, "").toUpperCase();
  bar.append(
    element("span", "map-label", `MAP ${String(number).padStart(2, "0")} · ${visualLabel}`),
  );

  const tools = element("div", "map-tools");
  const viewport = element("div", "map-viewport");
  viewport.tabIndex = 0;
  viewport.setAttribute("aria-label", `Scrollable map: ${visualLabel}`);
  const stage = element("div", "map-stage");
  const image = document.createElement("img");
  image.src = asset.variants.web;
  image.alt = asset.captions.en;
  image.width = 1600;
  image.height = 1050;
  stage.append(image);
  viewport.append(stage);

  let zoom = 1;
  let minus;
  let plus;
  const defaultScrollLeft = () => {
    if (!window.matchMedia("(max-width: 480px)").matches) return 0;
    const focus = ["asset-xian-before-walls-map", "asset-xian-inside-wall-route-map"].includes(
      asset.id,
    )
      ? 0.7
      : 0.5;
    return Math.max(0, (stage.scrollWidth - viewport.clientWidth) * focus);
  };
  const centerMobileMap = (behavior = "auto") => {
    viewport.scrollTo({ top: 0, left: defaultScrollLeft(), behavior });
  };
  const applyZoom = () => {
    const minimumWidth = window.matchMedia("(max-width: 480px)").matches ? 760 : 720;
    stage.style.width = `${Math.round(zoom * 100)}%`;
    stage.style.minWidth = `${Math.round(minimumWidth * zoom)}px`;
    minus.disabled = zoom <= 1;
    plus.disabled = zoom >= 2.5;
  };
  minus = mapButton("Zoom out", "−", () => {
    zoom = Math.max(1, zoom - 0.25);
    applyZoom();
  });
  plus = mapButton("Zoom in", "+", () => {
    zoom = Math.min(2.5, zoom + 0.25);
    applyZoom();
  });
  const reset = mapButton("Reset map", "↺", () => {
    zoom = 1;
    applyZoom();
    centerMobileMap("smooth");
  });
  tools.append(minus, plus, reset);
  bar.append(tools);
  figure.append(bar, viewport);

  figure.append(renderVisualCaption(asset, "map-caption"));
  applyZoom();
  image.addEventListener("load", () => requestAnimationFrame(() => centerMobileMap()));
  return figure;
}

function renderFigure(asset, number) {
  const figure = element("figure", "editorial-figure");
  const label = assetLabels[asset.id] || asset.id.replace(/^asset-/, "").toUpperCase();
  const bar = element("div", "figure-bar");
  bar.append(element("span", "figure-label", `FIGURE ${String(number).padStart(2, "0")} · ${label}`));
  const image = document.createElement("img");
  image.className = "figure-image";
  image.src = asset.variants?.web || asset.variants?.fallback || asset.path;
  image.alt = asset.captions.en;
  image.loading = "lazy";
  figure.append(bar, image, renderVisualCaption(asset, "figure-caption"));
  return figure;
}

function renderBlock(block, index, assetById, visualNumber) {
  const section = element("section", "reading-block");
  section.classList.add(`kind-${block.kind}`);
  section.id = block.id;
  section.dataset.category = block.category;

  const header = element("header", "block-header");
  const meta = element("div", "block-meta");
  meta.append(
    element("span", "block-index", String(index + 1).padStart(2, "0")),
    renderLanguageSet(categoryLabels[block.category], "block-category"),
  );
  header.append(meta);
  if (block.temporal_scope === "time-sensitive") {
    header.append(element("time", "time-label", `CHECKED ${block.checked_at}`));
  }
  section.append(header);
  if (block.heading) {
    section.append(renderLanguageSet(block.heading, "block-heading"));
  }

  const grid = element("div", "language-grid");
  for (const language of ["zh", "ja", "en"]) {
    const panel = element("div", "language-panel");
    panel.dataset.lang = language;
    panel.lang = language === "zh" ? "zh-Hans" : language;
    panel.append(element("span", "language-label", languageNames[language]));
    const paragraph = document.createElement("p");
    if (language === "en") {
      paragraph.textContent = block.text.en;
    } else {
      paragraph.append(renderTokens(block.readings[language], language));
    }
    panel.append(paragraph);
    grid.append(panel);
  }
  section.append(grid, renderBlockCitations(block));

  if (block.kind === "map") {
    const asset = assetById.get(block.asset_ids[0]);
    section.append(renderMap(asset, visualNumber));
  } else if (block.kind === "figure") {
    const asset = assetById.get(block.asset_ids[0]);
    section.append(renderFigure(asset, visualNumber));
  }
  return section;
}

function renderSources(documentData, chapter) {
  const citationById = new Map(documentData.citations.map((citation) => [citation.id, citation]));
  const section = element("section", "sources");
  section.id = "sources";
  section.append(
    element("h2", "", "资料来源 · 出典 · Sources"),
    element(
      "p",
      "sources-note",
      "Only sources cited in this chapter · Each source shows its checked date",
    ),
  );
  const list = element("ol", "source-list");
  for (const citationId of citationOrder(chapter)) {
    const citation = citationById.get(citationId);
    const number = state.citationNumbers.get(citationId);
    const item = element("li", "source-item");
    item.id = `source-${number}`;
    item.append(element("span", "source-number", `[${number}]`));
    const body = element("div", "");
    const title = element("p", "source-title");
    if (citation.url) {
      const link = element("a", "", citation.title);
      link.href = citation.url;
      link.target = "_blank";
      link.rel = "noreferrer";
      title.append(link);
    } else {
      title.textContent = citation.title;
    }
    const details = [citation.locator, `Checked ${citation.accessed_at}`];
    if (citation.license) details.push(citation.license);
    body.append(title, element("p", "source-detail", details.join(" · ")));
    item.append(body);
    list.append(item);
  }
  section.append(list);
  return section;
}

function renderFooter(book) {
  const footer = element("footer", "book-footer");
  const brand = element("div", "");
  brand.append(
    element("strong", "", book.branding.brand),
    element("p", "", `${book.branding.studio} · ${book.edition}`),
  );
  const link = element("a", "", "GitHub");
  link.href = book.branding.repository;
  footer.append(brand, link);
  return footer;
}

function renderChapter(documentData, chapter) {
  const article = document.getElementById("chapter");
  article.replaceChildren();

  const masthead = element("header", "chapter-masthead");
  const chapterNumber = String(chapter.order).padStart(2, "0");
  const coverage = chapter.coverage.map(
    (category) => categoryLabels[category]?.en || category.replaceAll("-", " "),
  );
  masthead.append(
    element(
      "div",
      "chapter-kicker",
      `CHAPTER ${chapterNumber} · ${coverage.slice(0, 3).join(" · ").toUpperCase()}`,
    ),
  );
  const title = renderLanguageSet(chapter.titles, "chapter-title");
  masthead.append(title);
  const deck = element("div", "chapter-deck");
  coverage.forEach((label) => deck.append(element("span", "", label.toUpperCase())));
  masthead.append(deck);
  article.append(masthead);

  const assetById = new Map(documentData.assets.map((asset) => [asset.id, asset]));
  let mapNumber = 0;
  let figureNumber = 0;
  chapter.blocks.forEach((block, index) => {
    let visualNumber = 0;
    if (block.kind === "map") {
      mapNumber += 1;
      visualNumber = mapNumber;
    } else if (block.kind === "figure") {
      figureNumber += 1;
      visualNumber = figureNumber;
    }
    article.append(renderBlock(block, index, assetById, visualNumber));
  });
  article.append(renderSources(documentData, chapter), renderFooter(documentData.book));
  article.hidden = false;
  document.getElementById("loading").hidden = true;
}

function renderNavigation(documentData, chapter) {
  const chapterOutline = document.getElementById("chapter-outline");
  const chapterSelect = document.getElementById("chapter-select");
  chapterOutline.replaceChildren();
  chapterSelect.replaceChildren();
  for (const item of documentData.chapters) {
    const available = item.blocks.length > 0;
    const className = item.id === chapter.id ? "active" : available ? "available" : "future";
    const listItem = element("li", className);
    const content = available ? document.createElement("a") : element("span", "future");
    if (available) {
      content.href = `?chapter=${encodeURIComponent(item.id)}#reading`;
      content.dataset.chapterId = item.id;
      content.addEventListener("click", (event) => {
        event.preventDefault();
        activateChapter(item.id, { updateUrl: true, scroll: true });
      });
    }
    content.append(
      element("span", "", String(item.order).padStart(2, "0")),
      renderLanguageSet(item.titles, "outline-title"),
    );
    listItem.append(content);
    chapterOutline.append(listItem);

    if (available) {
      const option = document.createElement("option");
      option.value = item.id;
      option.textContent = `${String(item.order).padStart(2, "0")} · ${localizedValue(item.titles)}`;
      option.selected = item.id === chapter.id;
      chapterSelect.append(option);
    }
  }

  const sectionOutline = document.getElementById("section-outline");
  const select = document.getElementById("section-select");
  sectionOutline.replaceChildren();
  select.replaceChildren();
  chapter.blocks.forEach((block, index) => {
    const number = String(index + 1).padStart(2, "0");
    const label = localizedValue(categoryLabels[block.category]);
    const listItem = document.createElement("li");
    const link = element("a", "");
    link.href = `#${block.id}`;
    link.append(element("span", "", number), element("span", "", label));
    listItem.append(link);
    sectionOutline.append(listItem);

    const option = document.createElement("option");
    option.value = block.id;
    option.textContent = `${number} · ${label}`;
    select.append(option);
  });
}

function activateChapter(chapterId, options = {}) {
  const { updateUrl = false, scroll = false } = options;
  const chapter = availableChapters(state.document).find((item) => item.id === chapterId);
  if (!chapter) return;
  state.chapter = chapter;
  state.citationNumbers = buildCitationNumbers(chapter);
  renderChapter(state.document, chapter);
  renderNavigation(state.document, chapter);
  document.title = `${chapter.titles.en} · ${state.document.book.titles.en} | LazyTravel`;

  if (updateUrl) {
    const url = new URL(window.location.href);
    url.searchParams.set("chapter", chapter.id);
    url.hash = "reading";
    window.history.pushState({ chapterId: chapter.id }, "", url);
  }
  if (scroll) document.getElementById("reading").scrollIntoView({ block: "start" });
}

function setMode(mode) {
  const allowed = new Set(["parallel", "zh", "ja", "en"]);
  state.mode = allowed.has(mode) ? mode : "parallel";
  document.documentElement.dataset.mode = state.mode;
  for (const button of document.querySelectorAll("[data-mode-button]")) {
    button.setAttribute("aria-pressed", String(button.dataset.modeButton === state.mode));
  }
  if (state.document && state.chapter) renderNavigation(state.document, state.chapter);
  savePreference("lazytravel-language", state.mode);
}

function bindControls() {
  for (const button of document.querySelectorAll("[data-mode-button]")) {
    button.addEventListener("click", () => setMode(button.dataset.modeButton));
  }

  const rubyToggle = document.getElementById("ruby-toggle");
  rubyToggle.checked = storedPreference("lazytravel-ruby", "on") !== "off";
  const applyRuby = () => {
    document.documentElement.classList.toggle("hide-ruby", !rubyToggle.checked);
    savePreference("lazytravel-ruby", rubyToggle.checked ? "on" : "off");
  };
  rubyToggle.addEventListener("change", applyRuby);
  applyRuby();

  document.getElementById("section-select").addEventListener("change", (event) => {
    const target = document.getElementById(event.target.value);
    if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
  });

  document.getElementById("chapter-select").addEventListener("change", (event) => {
    activateChapter(event.target.value, { updateUrl: true, scroll: true });
  });

  window.addEventListener("popstate", () => {
    if (state.document) activateChapter(chapterIdFromLocation(state.document));
  });
}

async function initialize() {
  bindControls();
  setMode(storedPreference("lazytravel-language", "parallel"));
  try {
    const response = await fetch(DATA_URL, { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const documentData = await response.json();
    state.document = documentData;
    document.getElementById("github-link").href = documentData.book.branding.repository;
    const editionDate = documentData.book.edition.match(/\d{4}-\d{2}-\d{2}$/)?.[0];
    document.getElementById("edition-short").textContent =
      `XI'AN · ${editionDate?.slice(0, 4) || documentData.book.edition}`;
    document.getElementById("edition-label").textContent = editionDate
      ? `Research edition · ${editionDate}`
      : documentData.book.edition;
    activateChapter(chapterIdFromLocation(documentData));
    setMode(state.mode);
  } catch (error) {
    const loading = document.getElementById("loading");
    loading.textContent = `Unable to load the Xi'an edition: ${error.message}`;
    loading.setAttribute("role", "alert");
  }
}

initialize();
