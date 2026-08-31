/* The floor — an interactive 2D office the walkthrough plays over.

   It is a VIEW. Every number it draws is read out of `<episode>.floor.json`, which
   sits beside the script in `walkthrough/`, and every one of those numbers is in a
   Markdown document that GitHub also renders. The floor computes nothing: it will not
   take a headcount and hand you an access-point count, because that would make the
   viewer the place a fact first appeared. See docs/adr/0011.

   Three registers, because the material has three. Far out is occupancy, coverage and
   the four segments. In the middle is placement. Close in is the path from an access
   port to an uplink. Distance carries meaning here rather than just magnification.

   Browsing is the default mode and works in silence: three audiences each lack a
   different thing, and the one on a podcast has no screen at all. */

import { getLang } from "./i18n.js";

const TILE = 16;
const REGISTER = { floor: 1.0, room: 3.0, rack: 6.0 };
const REGISTER_ORDER = ["floor", "room", "rack"];

/* One palette, fixed, and it does not follow the reader's theme (ADR-0013). These are
   the brass skin's values dimmed to interior light — a game scene has its own. */
const C = {
  void: "#1b1a17", ground: "#2a2823", ink: "#26262b", wall: "#4a463d",
  soft: "#8a8479", bone: "#c9c2b4", brass: "#a8763e", bright: "#c99a5b",
  patina: "#5e7a9b", sage: "#7c8f6f", mustard: "#b8915a", glass: "#33414a",
};
const TONE = { staff: C.patina, guest: C.sage, unpatchable: C.mustard, management: C.brass };
const SKIN = ["#8f7a63", "#6f5b47", "#b39b7d", "#5a4a3c", "#a3846a"];
const HAIR = ["#2e2620", "#4a3a2c", "#6b4a2f", "#8a6a45", "#1f1b18", "#5a4636"];
const SHIRT = [C.patina, C.sage, C.mustard, C.bone, "#7a6f8f", "#8f6f6f"];

const T = {
  floor:  { zh: "楼面", en: "Floor" },
  room:   { zh: "房间", en: "Room" },
  rack:   { zh: "机柜", en: "Rack" },
  browse: { zh: "自由浏览", en: "Browse" },
  play:   { zh: "播放", en: "Play" },
  pause:  { zh: "暂停", en: "Pause" },
  prev:   { zh: "上一拍", en: "Back" },
  next:   { zh: "下一拍", en: "Next" },
  reset:  { zh: "回到全景", en: "Reset view" },
  hint:   { zh: "拖动平移 · 滚轮缩放 · 点一个东西看它为什么在那里",
            en: "Drag to pan · scroll to zoom · click a thing to see why it is there" },
  noVoice:{ zh: "这个浏览器没有语音合成，按下一拍手动走。",
            en: "No speech synthesis in this browser — step through with Next." },
  criteria:{ zh: "要指定什么", en: "What to specify" },
  read:   { zh: "读下去", en: "Read on" },
  hands:  { zh: "亲手做过", en: "hands-on" },
  ramp:   { zh: "验证过的 ramp", en: "verified ramp" },
  noConfig:{ zh: "这里没有配置片段。这个仓库不持有设备配置，也不会为了填一个面板去长一份。",
             en: "No configuration here. This repo holds no device configurations and does not grow one to fill a panel." },
};
const t = (k) => T[k][getLang() === "zh" ? "zh" : "en"] ?? T[k].en;
const pick = (v) => (v && typeof v === "object" ? (v[getLang() === "zh" ? "zh" : "en"] ?? v.en) : v);

/** The hand-drawn sheet from tools/floor/tiles.tiles, derived by build-tiles.py.
    If it fails to load the floor still draws — every sprite has a flat fallback —
    because a missing decoration should not take the argument down with it. */
async function loadTiles() {
  try {
    const index = await (await fetch("assets/floor/tiles.json")).json();
    const image = await new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = "assets/floor/tiles.png";
    });
    return { image, ...index };
  } catch { return null; }
}

function rng(seed) {
  let s = (seed >>> 0) || 1;
  return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
}

/* ── scene geometry ───────────────────────────────────────────────────────── */

/** Every desk position, expanded from the pods. Three across, two rows, a gap between
    so the aisles read. The count is asserted against `total` by build-walkthrough.py. */
function deskSeats(scene) {
  const seats = [];
  for (const pod of scene.stage.desks.pods) {
    const [px, py] = pod.at;
    const perSide = Math.ceil(pod.seats / 2);
    for (let i = 0; i < pod.seats; i += 1) {
      const north = i < perSide;
      seats.push({
        x: px + (north ? i : i - perSide),
        desk: py + (north ? 1 : 2),      // the two desk rows meet at the spine
        chair: py + (north ? 0 : 3),     // people sit on the outside, facing in
        side: north ? "n" : "s",
      });
    }
  }
  return seats;
}

/** Seats around a meeting table, for the one beat that fills the large room. */
function roomSeats(room) {
  const [rx, ry, rw, rh] = room.rect;
  const seats = [];
  for (let x = rx + 1; x < rx + rw - 1; x += 1) seats.push([x, ry + 2], [x, ry + rh - 3]);
  for (let y = ry + 4; y < ry + rh - 4; y += 2) seats.push([rx + 1, y], [rx + rw - 2, y]);
  return seats.slice(0, room.seats);
}

/* ── drawing ──────────────────────────────────────────────────────────────── */

class Floor {
  constructor(host, scene, beats, sheet) {
    this.sheet = sheet;
    this.scene = scene;
    this.beats = beats;                       // [{id, text}] in script order
    this.seats = deskSeats(scene);
    this.order = this.shuffled(this.seats.length);
    this.state = { zoom: "floor", cast: "empty", focus: null, highlight: [], overlay: null, marker: null };
    this.view = { x: 0, y: 0, scale: REGISTER.floor, user: false };
    this.selected = null;
    this.index = -1;
    this.speaking = false;
    this.build(host);
  }

  shuffled(n) {
    const r = rng(20260831), a = [...Array(n).keys()];
    for (let i = n - 1; i > 0; i -= 1) {
      const j = Math.floor(r() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  prop(id) {
    const p = this.scene.props.find((q) => q.id === id);
    if (!p) return null;
    return p.sameAs ? { ...this.prop(p.sameAs), ...p, id: p.id, label: p.label } : p;
  }

  /* ── DOM ── */

  build(host) {
    host.className = "floor";
    host.innerHTML = `
      <div class="floor-bar">
        <div class="floor-registers" role="group">
          ${REGISTER_ORDER.map((r) => `<button data-reg="${r}">${t(r)}</button>`).join("")}
        </div>
        <div class="floor-days" role="group">
          ${["empty", "fri", "mon", "tue"].map((d) => `<button data-day="${d}">${
            pick(this.scene.stage.occupancy.label) ? this.scene.stage.occupancy.label[getLang() === "zh" ? "zh" : "en"][d] : d
          }</button>`).join("")}
        </div>
        <div class="floor-transport">
          <button data-act="prev">${t("prev")}</button>
          <button data-act="play" class="accent">${t("play")}</button>
          <button data-act="next">${t("next")}</button>
          <button data-act="reset">${t("reset")}</button>
        </div>
      </div>
      <div class="floor-stage">
        <canvas class="floor-canvas"></canvas>
        <div class="floor-marker" hidden></div>
        <div class="floor-caption" hidden></div>
        <aside class="floor-panel" hidden></aside>
      </div>
      <p class="floor-hint">${t("hint")}</p>`;

    this.canvas = host.querySelector(".floor-canvas");
    this.ctx = this.canvas.getContext("2d");
    this.panel = host.querySelector(".floor-panel");
    this.caption = host.querySelector(".floor-caption");
    this.markerEl = host.querySelector(".floor-marker");
    this.host = host;

    host.addEventListener("click", (e) => {
      const reg = e.target.closest("[data-reg]");
      const day = e.target.closest("[data-day]");
      const act = e.target.closest("[data-act]");
      if (reg) { this.state.zoom = reg.dataset.reg; this.view.user = false; this.frame(); }
      if (day) { this.state.cast = day.dataset.day; this.frame(); }
      if (act) this.transport(act.dataset.act);
      if (e.target.closest(".floor-panel-close")) this.select(null);
    });

    let drag = null;
    this.canvas.addEventListener("pointerdown", (e) => {
      drag = { x: e.clientX, y: e.clientY, vx: this.view.x, vy: this.view.y, moved: false };
      this.canvas.setPointerCapture(e.pointerId);
    });
    this.canvas.addEventListener("pointermove", (e) => {
      if (!drag) return;
      const dx = e.clientX - drag.x, dy = e.clientY - drag.y;
      if (Math.abs(dx) + Math.abs(dy) > 3) drag.moved = true;
      this.view.x = drag.vx + dx; this.view.y = drag.vy + dy; this.view.user = true;
      this.draw();
    });
    this.canvas.addEventListener("pointerup", (e) => {
      if (drag && !drag.moved) this.click(e);
      drag = null;
    });
    this.canvas.addEventListener("wheel", (e) => {
      e.preventDefault();
      const before = this.view.scale;
      const lo = (this.base || 0.2) * 0.7, hi = (this.base || 0.2) * 9;
      this.view.scale = Math.min(hi, Math.max(lo, before * (e.deltaY < 0 ? 1.12 : 0.89)));
      const rect = this.canvas.getBoundingClientRect();
      const mx = e.clientX - rect.left, my = e.clientY - rect.top;
      this.view.x = mx - (mx - this.view.x) * (this.view.scale / before);
      this.view.y = my - (my - this.view.y) * (this.view.scale / before);
      this.view.user = true;
      const rel = this.view.scale / (this.base || 1);
      this.state.zoom = rel < 1.7 ? "floor" : rel < 3.5 ? "room" : "rack";
      this.syncBar();
      this.draw();
    }, { passive: false });

    new ResizeObserver(() => this.resize()).observe(host.querySelector(".floor-stage"));
    this.resize();
  }

  resize() {
    const stage = this.host.querySelector(".floor-stage");
    const dpr = Math.min(2, globalThis.devicePixelRatio || 1);
    this.canvas.width = Math.max(320, stage.clientWidth) * dpr;
    this.canvas.height = Math.max(280, stage.clientHeight) * dpr;
    this.canvas.style.width = `${this.canvas.width / dpr}px`;
    this.canvas.style.height = `${this.canvas.height / dpr}px`;
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    this.dpr = dpr;
    // Re-derive from the beat rather than re-framing what is already on screen. A
    // resize that only recentres lets the register drift out of step with the
    // narration — the camera stays where it was while the words have moved on, and
    // nothing looks broken enough to notice.
    if (this.index >= 0) this.goto(this.index); else this.frame();
  }

  /** Put the current focus in the middle at the current register, unless the reader
      has taken the view over by dragging or scrolling. */
  frame() {
    if (!this.view.user) {
      const g = this.scene.stage.grid;
      const w = this.canvas.width / this.dpr, h = this.canvas.height / this.dpr;
      this.base = Math.min(w / (g.w * TILE), h / (g.h * TILE));
      this.view.scale = REGISTER[this.state.zoom] * this.base;
      const target = this.focusPoint();
      this.view.x = w / 2 - target[0] * TILE * this.view.scale;
      this.view.y = h / 2 - target[1] * TILE * this.view.scale;
    }
    this.syncBar();
    this.draw();
  }

  focusPoint() {
    const g = this.scene.stage.grid;
    const id = this.state.focus;
    if (!id) return [g.w / 2, g.h / 2];
    const p = this.prop(id);
    if (p && p.at) return p.at;
    for (const key of ["rooms", "booths", "spaces"]) {
      const hit = (this.scene.stage[key] || []).find((r) => r.id === id);
      if (hit) return [hit.rect[0] + hit.rect[2] / 2, hit.rect[1] + hit.rect[3] / 2];
    }
    return [g.w / 2, g.h / 2];
  }

  syncBar() {
    for (const b of this.host.querySelectorAll("[data-reg]")) b.classList.toggle("on", b.dataset.reg === this.state.zoom);
    for (const b of this.host.querySelectorAll("[data-day]")) b.classList.toggle("on", b.dataset.day === this.state.cast);
    const play = this.host.querySelector('[data-act="play"]');
    if (play) play.textContent = this.speaking ? t("pause") : t("play");
  }

  world(x, y) { return [this.view.x + x * TILE * this.view.scale, this.view.y + y * TILE * this.view.scale]; }
  unit() { return TILE * this.view.scale; }

  /** One hand-drawn tile at a grid position. Returns false when there is no sheet,
      so every caller can fall back to a flat rectangle. */
  sprite(name, gx, gy, w = 1, h = 1) {
    const s = this.sheet;
    if (!s || !(name in s.columns)) return false;
    const [x, y] = this.world(gx, gy);
    const u = this.unit();
    this.ctx.drawImage(s.image, s.columns[name] * s.tile, 0, s.tile, s.tile,
                       Math.round(x), Math.round(y), Math.ceil(w * u), Math.ceil(h * u));
    return true;
  }

  draw() {
    const ctx = this.ctx, u = this.unit();
    const w = this.canvas.width / this.dpr, h = this.canvas.height / this.dpr;
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = C.void;
    ctx.fillRect(0, 0, w, h);
    ctx.imageSmoothingEnabled = false;

    const g = this.scene.stage.grid;
    const [ox, oy] = this.world(0, 0);
    ctx.fillStyle = C.ground;
    ctx.fillRect(ox, oy, g.w * u, g.h * u);

    if (!this.walls) this.buildWalls();
    this.drawFloors(g, u);
    this.drawFurniture(u);
    this.drawWalls(u);
    this.drawCast(u);
    this.drawProps(u);
    this.drawOverlay(u);
    this.drawHighlights(u);
    this.drawLabels(u);
  }

  /** Every cell that is wall, and every cell that is a doorway. Built once per scene
      from the plate: an enclosure's perimeter, plus the shell. */
  buildWalls() {
    const g = this.scene.stage.grid;
    const wall = new Set(), door = new Set(), key = (x, y) => `${x},${y}`;
    const enclosed = [...this.scene.stage.rooms, ...this.scene.stage.spaces,
                      ...this.scene.stage.booths];
    for (const o of enclosed) {
      const [rx, ry, rw, rh] = o.rect;
      for (let x = rx; x < rx + rw; x += 1) { wall.add(key(x, ry)); wall.add(key(x, ry + rh - 1)); }
      for (let y = ry; y < ry + rh; y += 1) { wall.add(key(rx, y)); wall.add(key(rx + rw - 1, y)); }
      const d = o.door;
      if (d) {
        const at = { n: [d.at, ry], s: [d.at, ry + rh - 1],
                     w: [rx, d.at], e: [rx + rw - 1, d.at] }[d.side];
        if (at) door.add(key(at[0], at[1]));
      }
    }
    for (let x = 0; x < g.w; x += 1) { wall.add(key(x, 0)); wall.add(key(x, g.h - 1)); }
    for (let y = 0; y < g.h; y += 1) { wall.add(key(0, y)); wall.add(key(g.w - 1, y)); }
    this.walls = wall;
    this.doors = door;
  }

  /** Draw a wall cell as a band with an arm toward each neighbouring wall. Sixteen
      cases fall out of four booleans, so corners, tees, crosses and ends are all right
      by construction — which sixteen hand-drawn tiles of pure geometry would not be. */
  drawWalls(u) {
    const ctx = this.ctx;
    const g = this.scene.stage.grid;
    const has = (x, y) => this.walls.has(`${x},${y}`);
    const A = 5 / 16, B = 11 / 16;                       // the band, in tile fractions
    for (const cell of this.walls) {
      const [x, y] = cell.split(",").map(Number);
      const [px, py] = this.world(x, y);
      const isDoor = this.doors.has(cell);
      const arms = [];
      arms.push([A, A, B - A, B - A]);                   // the core, always
      if (has(x, y - 1)) arms.push([A, 0, B - A, A]);
      if (has(x, y + 1)) arms.push([A, B, B - A, 1 - B]);
      if (has(x - 1, y)) arms.push([0, A, A, B - A]);
      if (has(x + 1, y)) arms.push([B, A, 1 - B, B - A]);
      for (const [ax, ay, aw, ah] of arms) {
        const rx = Math.round(px + ax * u), ry = Math.round(py + ay * u);
        const rw = Math.ceil(aw * u) + 1, rh = Math.ceil(ah * u) + 1;
        if (isDoor) {
          // A doorway is the frame without the leaf: brass jambs, no infill.
          ctx.fillStyle = "#a8763e";
          ctx.fillRect(rx, ry, rw, Math.max(1, Math.round(u / 16)));
          ctx.fillRect(rx, ry + rh - Math.max(1, Math.round(u / 16)), rw,
                       Math.max(1, Math.round(u / 16)));
          continue;
        }
        ctx.fillStyle = "#e0dacb";
        ctx.fillRect(rx, ry, rw, rh);
        ctx.fillStyle = "#a99f8a";                       // the face, along the bottom
        ctx.fillRect(rx, ry + rh - Math.max(1, Math.round(u * 2 / 16)), rw,
                     Math.max(1, Math.round(u * 2 / 16)));
        ctx.fillStyle = "#6e6455";
        ctx.fillRect(rx, ry + rh - Math.max(1, Math.round(u / 16)), rw,
                     Math.max(1, Math.round(u / 16)));
      }
    }
    // Glazing along the north shell, which is where the light in the opening beat is.
    for (let x = 3; x < g.w - 3; x += 1) {
      if (x % 3 === 0) continue;
      const [px, py] = this.world(x, 0);
      ctx.fillStyle = "#8fb6cc";
      ctx.fillRect(Math.round(px + u * 0.12), Math.round(py + u * 7 / 16),
                   Math.ceil(u * 0.76), Math.ceil(u * 2 / 16));
    }
  }

  /** Floors: carpet everywhere, a warmer floor inside enclosures, and circulation
      drawn as itself because the plate states it rather than implying it. */
  drawFloors(g, u) {
    for (let y = 0; y < g.h; y += 1) {
      for (let x = 0; x < g.w; x += 1) {
        if (!this.sprite((x + y) % 3 === 0 ? "carpet" : "carpet-plain", x, y)) {
          const [px, py] = this.world(x, y);
          this.ctx.fillStyle = C.ground;
          this.ctx.fillRect(px, py, u + 1, u + 1);
        }
      }
    }
    for (const o of [...this.scene.stage.rooms, ...this.scene.stage.spaces]) {
      const [rx, ry, rw, rh] = o.rect;
      for (let y = ry + 1; y < ry + rh - 1; y += 1) {
        for (let x = rx + 1; x < rx + rw - 1; x += 1) this.sprite("floor-room", x, y);
      }
    }
    const ctx = this.ctx;
    for (const leg of this.scene.circulation) {
      const [x, y, w, h] = this.rect(leg.rect, u);
      ctx.fillStyle = "rgba(224,218,203,0.10)";
      ctx.fillRect(x, y, w, h);
    }
  }

  rect(r, u) { const [a, b] = this.world(r[0], r[1]); return [a, b, r[2] * u, r[3] * u]; }

  drawFurniture(u) {
    const ctx = this.ctx;

    for (const s of this.seats) {
      if (!this.sprite(s.side === "n" ? "desk-n" : "desk-s", s.x, s.desk)) {
        const [px, py] = this.world(s.x, s.desk);
        ctx.fillStyle = "#c9a06a";
        ctx.fillRect(px + u * 0.1, py + u * 0.4, u * 0.8, u * 0.5);
      }
      this.sprite(s.side === "n" ? "chair-n" : "chair-s", s.x, s.chair);
    }

    for (const room of this.scene.stage.rooms) {
      const [rx, ry, rw, rh] = room.rect;
      const ty = ry + Math.floor(rh / 2) - 1;
      const left = rx + 2, right = rx + rw - 3;
      for (let x = left; x <= right; x += 1) {
        const tile = x === left ? "table-l" : x === right ? "table-r" : "table-m";
        if (!this.sprite(tile, x, ty)) {
          const [px, py] = this.world(x, ty);
          ctx.fillStyle = "#c9a06a"; ctx.fillRect(px, py + u * 0.15, u + 1, u * 0.7);
        }
        if (x > left && x < right) {
          this.sprite("chair-meet", x, ty - 1);
          this.sprite("chair-meet", x, ty + 1);
        }
      }
      this.sprite("plant-tall", rx + rw - 2, ry + 1);
    }

    for (const space of this.scene.stage.spaces) this.furnish(space, u);

    for (const booth of this.scene.stage.booths) {
      const [bx, by, bw, bh] = booth.rect;
      this.sprite("booth", bx + Math.floor(bw / 2) - 1, by + Math.floor(bh / 2) - 1);
    }

    for (const [x, y] of [[15, 14], [29, 14], [21, 19]]) this.sprite("printer", x, y);

    // The pocket below the service desk: lockers along the wall and soft seating, which
    // is what the space beside a walk-up point is actually used for.
    for (let x = 2; x <= 7; x += 1) this.sprite("locker", x, 25);
    this.sprite("sofa", 2, 27);
    this.sprite("low-table", 4, 27);
    this.sprite("sofa", 6, 27);
    // And the short bench's leftover, between the last pod and the east leg.
    for (const [x, y] of [[34, 20], [34, 22]]) this.sprite("locker", x, y);
    for (const [x, y] of [[8, 28], [33, 28], [35, 14], [13, 19], [28, 14]])
      this.sprite("plant-small", x, y);
    this.sprite("plant-tall", 7, 28);
  }

  /** Each support space is furnished for what it is for. A store with a couple of desks
      in it is not a store, and a service desk in a back office is not a service desk. */
  furnish(space, u) {
    const ctx = this.ctx;
    const [rx, ry, rw, rh] = space.rect;
    if (space.kind === "idf") {
      // Three racks, because the port count lands on three access switches.
      for (let n = 0; n < 3; n += 1) {
        if (!this.sprite("rack", rx + 2 + n, ry + 2)) {
          const [px, py] = this.world(rx + 2 + n, ry + 2);
          ctx.fillStyle = C.ink; ctx.fillRect(px, py, u + 1, u + 1);
        }
      }
    } else if (space.kind === "store") {
      // Shelving down both walls, an aisle between: stock, not desk space.
      for (let y = ry + 1; y < ry + rh - 1; y += 1) {
        this.sprite("shelving", rx + 1, y);
        this.sprite("shelving", rx + rw - 2, y);
      }
    } else if (space.kind === "service") {
      // A counter facing the open plan, with the staffed side behind it.
      for (let x = rx + 1; x < rx + rw - 1; x += 1) this.sprite("desk-counter", x, ry + rh - 3);
      for (let x = rx + 2; x < rx + rw - 2; x += 1) this.sprite("chair-n", x, ry + rh - 4);
      this.sprite("shelving", rx + 1, ry + 1);
      this.sprite("plant-small", rx + rw - 2, ry + 1);
    } else if (space.kind === "pantry") {
      for (let x = rx + 1; x < rx + rw - 2; x += 1) this.sprite("counter", x, ry + 1);
      this.sprite("fridge", rx + rw - 2, ry + 1);
      // Two canteen tables, four seats each. Somewhere to eat, not just somewhere to
      // boil a kettle — otherwise the floor's occupancy walks out at lunchtime.
      for (const [tx, ty] of [[rx + 2, ry + 4], [rx + 5, ry + 4], [rx + 2, ry + 7], [rx + 5, ry + 7]]) {
        if (ty >= ry + rh - 1) continue;
        this.sprite("table-dine", tx, ty);
        this.sprite("chair-n", tx, ty - 1);
        this.sprite("chair-s", tx, ty + 1);
        this.sprite("chair-n", tx + 1, ty - 1);
        this.sprite("chair-s", tx + 1, ty + 1);
      }
      this.sprite("plant-tall", rx + rw - 2, ry + rh - 2);
    } else {                                   // the lobby
      this.sprite("sofa", rx + 1, ry + rh - 3);
      this.sprite("coffee", rx + rw - 3, ry + 1);
      this.sprite("shelf", rx + 1, ry + 1);
      for (let x = rx + 3; x < rx + rw - 3; x += 1) this.sprite("desk-counter", x, ry + 4);
      this.sprite("plant-tall", rx + rw - 2, ry + rh - 2);
    }
  }

  drawCast(u) {
    const ctx = this.ctx;
    const n = this.scene.stage.occupancy[this.state.cast] ?? 0;
    const px = u / 16;
    /** A seated person, built from parts: hair, head, shoulders, arms. Sixty-five
        figures need variation nobody is going to draw sixty-five times (ADR-0013). */
    const figure = (gx, gy, i) => {
      const [ox, oy] = this.world(gx + 0.5, gy + 0.42);
      const box = (cx, cy, w, h, fill) => {
        ctx.fillStyle = fill;
        ctx.fillRect(Math.round(ox + cx * px), Math.round(oy + cy * px),
                     Math.max(1, Math.round(w * px)), Math.max(1, Math.round(h * px)));
      };
      const shirt = SHIRT[i % SHIRT.length], hair = HAIR[i % HAIR.length];
      box(-4, 0, 8, 6, shirt);            // shoulders
      box(-6, 1, 2, 4, shirt);            // arms
      box(4, 1, 2, 4, shirt);
      box(-3, -6, 6, 7, SKIN[i % SKIN.length]);
      box(-3, -7, 6, 4, hair);            // hair, over the crown and down the sides
      box(-4, -6, 1, 4, hair);
      box(3, -6, 1, 4, hair);
    };
    for (let i = 0; i < Math.min(n, this.seats.length); i += 1) {
      const s = this.seats[this.order[i]];
      figure(s.x, s.chair, this.order[i]);        // on the chair, not on the desk
    }
    if (this.state.overlay === "room-full") {
      const room = this.scene.stage.rooms.find((r) => r.id === "room-large");
      roomSeats(room).forEach(([gx, gy], i) => figure(gx, gy, i + 40));
    }
  }

  drawProps(u) {
    const ctx = this.ctx;
    for (const p of this.scene.props) {
      if (!p.at) continue;
      const full = this.prop(p.id);
      const [x, y] = this.world(p.at[0] + 0.5, p.at[1] + 0.5);
      if (p.kind === "ap") {
        ctx.fillStyle = p.id === "ap-large-room" ? C.bright : C.brass;
        ctx.beginPath(); ctx.arc(x, y, Math.max(3, u * 0.36), 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = C.void; ctx.lineWidth = Math.max(1, u * 0.08); ctx.stroke();
      } else if (p.kind === "segment") {
        ctx.fillStyle = TONE[full.segment?.replace("seg-", "")] ?? C.soft;
        ctx.globalAlpha = 0.9;
        ctx.fillRect(x - u * 0.3, y - u * 0.3, u * 0.6, u * 0.6);
        ctx.globalAlpha = 1;
      } else if (["idf", "uplink", "plan"].includes(p.kind)) {
        ctx.strokeStyle = C.bone; ctx.lineWidth = Math.max(1, u * 0.09);
        ctx.strokeRect(x - u * 0.34, y - u * 0.34, u * 0.68, u * 0.68);
      }
    }
  }

  drawOverlay(u) {
    const ctx = this.ctx, o = this.state.overlay;
    if (!o) return;
    if (o === "coverage") {
      for (const p of this.scene.props.filter((q) => q.kind === "ap")) {
        const [x, y] = this.world(p.at[0] + 0.5, p.at[1] + 0.5);
        const radius = (p.id === "ap-large-room" ? 5.5 : 8.5) * u;
        const grad = ctx.createRadialGradient(x, y, 0, x, y, radius);
        grad.addColorStop(0, "rgba(168,118,62,0.20)");
        grad.addColorStop(1, "rgba(168,118,62,0)");
        ctx.fillStyle = grad;
        ctx.beginPath(); ctx.arc(x, y, radius, 0, Math.PI * 2); ctx.fill();
      }
    }
    if (o === "segments") {
      const tint = (r, tone) => {
        const [x, y, w, h] = this.rect(r, u);
        ctx.fillStyle = tone; ctx.globalAlpha = 0.22; ctx.fillRect(x, y, w, h); ctx.globalAlpha = 1;
      };
      const space = (id) => this.scene.stage.spaces.find((s) => s.id === id);
      const TINT = { lobby: TONE.guest, idf: TONE.management, store: TONE.unpatchable,
                     service: TONE.staff, pantry: TONE.staff };
      for (const s of this.scene.stage.spaces) tint(s.rect, TINT[s.id] ?? TONE.staff);
      for (const room of this.scene.stage.rooms) tint(room.rect, TONE.staff);
      for (const booth of this.scene.stage.booths) tint(booth.rect, TONE.unpatchable);
      void space;
    }
    if (o === "collision" || o === "addressing") {
      const g = this.scene.stage.grid;
      const [x, y] = this.world(0, 0);
      ctx.strokeStyle = o === "collision" ? "#b8915a" : "rgba(94,122,155,0.5)";
      ctx.setLineDash([u * 0.4, u * 0.4]);
      ctx.lineWidth = Math.max(1, u * 0.1);
      ctx.strokeRect(x, y, g.w * u, g.h * u);
      ctx.setLineDash([]);
    }
    if (o === "tiers" || o === "ports" || o === "poe" || o === "devices" || o === "rooms" || o === "payroll") {
      this.legend(o);
    }
  }

  legend(kind) {
    const zh = getLang() === "zh";
    const rows = {
      tiers:   zh ? ["桌面口 · 千兆 · 最不饿", "AP 上联 · 多千兆 · 真正在动", "接入到核心 · 万兆 · 按总和"]
                  : ["Desk · 1GbE · least starved", "AP uplink · multi-gig · the tier that moves", "Access to core · 10GbE · sized on the sum"],
      ports:   zh ? ["桌面 70 · 会议室 14 · 电话亭 6", "AP 6 · 打印 3 · 门禁 3 · 备用 8", "在用 ≈ 110 · 含增长 ≈ 135"]
                  : ["Desks 70 · rooms 14 · booths 6", "APs 6 · printers 3 · doors 3 · spares 8", "Active ≈ 110 · with growth ≈ 135"],
      poe:     zh ? ["同时负载 ≈ 500 W", "同口数机型可差一倍以上", "写瓦数，不要只写口数"]
                  : ["≈ 500 W simultaneous draw", "Same port count, over 2× the budget apart", "Specify watts, not just ports"],
      devices: zh ? ["65 人 × 2 台 = 130", "+ 7 会议室 + 6 亭 + 打印门禁", "≈ 145 台关联设备"]
                  : ["65 people × 2 devices = 130", "+ 7 rooms + 6 booths + printers, doors", "≈ 145 associated devices"],
      rooms:   zh ? ["1 大 · 2 中 · 4 小", "八成会议 ≤ 6 人", "大会议室利用率 12%"]
                  : ["1 large · 2 medium · 4 small", "80% of meetings seat 6 or fewer", "The large room sits at 12% utilisation"],
      payroll: zh ? ["工资单 100", "星期二 65 · 星期一 52 · 星期五 38", "按星期二定尺寸"]
                  : ["Payroll 100", "Tue 65 · Mon 52 · Fri 38", "Size for Tuesday"],
    }[kind] ?? [];
    const ctx = this.ctx;
    ctx.font = "12px ui-monospace, SFMono-Regular, Menlo, monospace";
    ctx.textBaseline = "top";
    const pad = 10, lh = 18;
    const width = Math.max(...rows.map((r) => ctx.measureText(r).width)) + pad * 2;
    ctx.fillStyle = "rgba(27,26,23,0.88)";
    ctx.fillRect(12, 12, width, rows.length * lh + pad * 2 - 4);
    ctx.strokeStyle = "rgba(168,118,62,0.5)";
    ctx.strokeRect(12.5, 12.5, width - 1, rows.length * lh + pad * 2 - 5);
    rows.forEach((r, i) => {
      ctx.fillStyle = i === rows.length - 1 ? C.bright : C.bone;
      ctx.fillText(r, 12 + pad, 12 + pad + i * lh);
    });
  }

  drawHighlights(u) {
    const ctx = this.ctx;
    const ids = new Set(this.state.highlight || []);
    if (this.selected) ids.add(this.selected);
    if (!ids.size) return;
    ctx.save();
    ctx.strokeStyle = C.bright;
    ctx.lineWidth = Math.max(1.5, u * 0.12);
    ctx.shadowColor = C.bright;
    ctx.shadowBlur = 12;
    for (const id of ids) {
      const room = [...this.scene.stage.rooms, ...this.scene.stage.booths,
                    ...this.scene.stage.spaces].find((r) => r.id === id);
      if (room) {
        const [x, y, w, h] = this.rect(room.rect, u);
        ctx.strokeRect(x, y, w, h);
        continue;
      }
      if (id === "desks") {
        for (const s of this.seats) {
          const [x, y] = this.world(s.x, s.desk);
          ctx.strokeRect(x + u * 0.1, y + u * 0.15, u * 0.8, u * 0.6);
        }
        continue;
      }
      const p = this.scene.props.find((q) => q.id === id);
      if (p && p.at) {
        const [x, y] = this.world(p.at[0] + 0.5, p.at[1] + 0.5);
        ctx.beginPath(); ctx.arc(x, y, Math.max(6, u * 0.7), 0, Math.PI * 2); ctx.stroke();
      }
    }
    ctx.restore();
  }

  drawLabels(u) {
    if (u < 9) return;
    const ctx = this.ctx;
    ctx.font = `${Math.max(9, Math.min(15, u * 0.55))}px ui-sans-serif, system-ui, sans-serif`;
    ctx.fillStyle = "rgba(201,194,180,0.75)";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    for (const room of this.scene.stage.rooms) {
      const [x, y, w, h] = this.rect(room.rect, u);
      ctx.fillText(pick(room.label), x + w / 2, y + h - Math.min(18, u));
    }
    ctx.fillStyle = C.bright;
    for (const space of this.scene.stage.spaces) {
      const [x, y, w, h] = this.rect(space.rect, u);
      ctx.fillText(pick(space.label), x + w / 2, y + h - Math.min(18, u));
    }
    ctx.textAlign = "start";
  }

  /* ── interaction ── */

  click(event) {
    const rect = this.canvas.getBoundingClientRect();
    const mx = event.clientX - rect.left, my = event.clientY - rect.top;
    const u = this.unit();
    let best = null, bestD = Infinity;
    for (const p of this.scene.props) {
      if (!p.at) continue;
      const [x, y] = this.world(p.at[0] + 0.5, p.at[1] + 0.5);
      const d = Math.hypot(mx - x, my - y);
      if (d < Math.max(14, u * 0.9) && d < bestD) { best = p.id; bestD = d; }
    }
    if (!best) {
      for (const room of [...this.scene.stage.rooms, ...this.scene.stage.booths,
                          ...this.scene.stage.spaces]) {
        const [x, y, w, h] = this.rect(room.rect, u);
        if (mx >= x && mx <= x + w && my >= y && my <= y + h) {
          best = this.scene.props.some((q) => q.id === room.id) ? room.id : "room-large";
          break;
        }
      }
    }
    if (!best) {
      for (const s of this.seats) {
        const [x, y] = this.world(s.x, s.desk);
        if (mx >= x && mx <= x + u && my >= y - u && my <= y + u * 2) { best = "desks"; break; }
      }
    }
    this.select(best);
  }

  select(id) {
    this.selected = id;
    if (!id) { this.panel.hidden = true; this.draw(); return; }
    const p = this.prop(id);
    if (!p) { this.panel.hidden = true; this.draw(); return; }
    if (this.speaking) this.stop();
    const marks = new Set((p.anchors || []).map((a) => a.marker).filter(Boolean));
    this.panel.hidden = false;
    this.panel.innerHTML = `
      <button class="floor-panel-close" aria-label="close">×</button>
      <h4>${pick(p.label)}</h4>
      <p class="floor-marks">${[...marks].map((m) =>
        `<span class="mark">${m} ${m === "🔨" ? t("hands") : t("ramp")}</span>`).join("")}</p>
      <p class="floor-why">${pick(p.why)}</p>
      <p class="floor-sub">${t("criteria")}</p>
      <ul>${(pick(p.criteria) || []).map((c) => `<li>${c}</li>`).join("")}</ul>
      <p class="floor-sub">${t("read")}</p>
      <ul class="floor-anchors">${(p.anchors || []).map((a) =>
        `<li><a href="#/${a.path}#${a.frag}">${a.marker ?? ""} ${
          a.frag.replace(/-+/g, " ").trim()}</a><span class="floor-path">${a.path}</span></li>`).join("")}</ul>
      <p class="floor-noconfig">${t("noConfig")}</p>`;
    this.draw();
  }

  /* ── the narration line ── */

  transport(act) {
    if (act === "reset") { this.view.user = false; this.state.zoom = "floor"; this.frame(); return; }
    if (act === "next") { this.goto(this.index + 1); return; }
    if (act === "prev") { this.goto(this.index - 1); return; }
    if (act === "play") { this.speaking ? this.stop() : this.play(); }
  }

  /** Accumulate every beat state from the first up to `i`: a beat with no entry of its
      own inherits the one before it, which is why only changes are written down. */
  goto(i) {
    if (!this.beats.length) return;
    this.index = Math.max(0, Math.min(this.beats.length - 1, i));
    const state = { zoom: "floor", cast: "empty", focus: null, highlight: [], overlay: null, marker: null };
    for (let n = 0; n <= this.index; n += 1) {
      Object.assign(state, this.scene.beats[this.beats[n].id] || {});
    }
    const moved = state.zoom !== this.state.zoom || state.focus !== this.state.focus;
    this.state = state;
    if (moved) this.view.user = false;
    this.caption.hidden = false;
    this.caption.textContent = this.beats[this.index].text;
    this.markerEl.hidden = !state.marker;
    this.markerEl.textContent = state.marker
      ? `${state.marker} ${state.marker === "🔨" ? t("hands") : t("ramp")}` : "";
    this.markerEl.className = `floor-marker ${state.marker === "🧭" ? "ramp" : "hands"}`;
    this.frame();
  }

  play() {
    const synth = globalThis.speechSynthesis;
    if (!synth) { this.caption.hidden = false; this.caption.textContent = t("noVoice"); return; }
    this.speaking = true;
    this.syncBar();
    const speak = () => {
      if (!this.speaking) return;
      if (this.index >= this.beats.length - 1 && this.index !== -1) { this.stop(); return; }
      this.goto(this.index + 1);
      const utter = new SpeechSynthesisUtterance(this.beats[this.index].text);
      utter.lang = getLang() === "zh" ? "zh-CN" : "en-US";
      utter.rate = 0.95;
      utter.onend = () => speak();
      utter.onerror = () => this.stop();
      synth.speak(utter);
    };
    synth.cancel();
    speak();
  }

  stop() {
    this.speaking = false;
    globalThis.speechSynthesis?.cancel();
    this.syncBar();
  }
}

/* ── mount ────────────────────────────────────────────────────────────────── */

const BEAT_RE = /<!--\s*beat:\s*([a-z0-9][a-z0-9-]*)\s*-->\s*\n+([^\n]+)/g;

/** Beat ids and the paragraph each one carries, in script order. The comments are
    invisible on the page and never reach a speech engine, which is the point. */
export function readBeats(markdown) {
  const beats = [];
  for (const m of markdown.matchAll(BEAT_RE)) beats.push({ id: m[1], text: m[2].trim() });
  return beats;
}

let live = null;

/** Mount the floor above a walkthrough script. Returns false when the document is not
    a walkthrough or its scene data is not there, and the page renders as prose. */
export async function mountFloor(host, path, markdown) {
  if (!/^walkthrough\/.+\.(zh|en)\.md$/.test(path)) return false;
  const scenePath = `${path.replace(/\.(zh|en)\.md$/, "")}.floor.json`;
  let scene;
  try {
    const response = await fetch(`/doc/${scenePath}`);
    if (!response.ok) throw new Error(`${response.status} for ${scenePath}`);
    const episode = await response.json();
    // Geometry is shared by every episode; panels and cues belong to this one.
    const platePath = `walkthrough/${episode.plate}`;
    const plateResponse = await fetch(`/doc/${platePath}`);
    if (!plateResponse.ok) throw new Error(`${plateResponse.status} for ${platePath}`);
    const plate = await plateResponse.json();
    scene = {
      stage: { grid: plate.grid, rooms: plate.rooms, spaces: plate.spaces,
               booths: plate.booths, desks: plate.desks, segments: plate.segments,
               occupancy: plate.occupancy },
      circulation: plate.circulation, core: plate.core, entry: plate.entry,
      topology: plate.topology, props: episode.props, beats: episode.beats,
    };
  } catch (err) {
    // A walkthrough always has a floor. Rendering nothing here is how a reader
    // concludes there was never meant to be one — and the likeliest cause is a viewer
    // process older than the floor, which reloading the page will never fix, because
    // serve.py re-reads the index per request but loads its own code once at startup.
    host.className = "floor-absent";
    host.innerHTML = `<p class="floor-absent-head">${t("floorMissing")}</p>
      <p>${t("floorMissingWhy")}</p>
      <pre><code>python3 site/serve.py</code></pre>
      <p class="floor-absent-detail">${scenePath} — ${String(err.message ?? err)}</p>`;
    return true;                       // keep the host: the notice is the mount
  }

  live?.stop();
  live = new Floor(host, scene, readBeats(markdown), await loadTiles());
  live.goto(0);
  return true;
}

export function unmountFloor() { live?.stop(); live = null; }
