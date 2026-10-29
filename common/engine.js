// Shared, deterministic motion engine. Every visual value is a pure function of t.
(function () {
  const E = {};
  E.clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  E.lerp = (a, b, k) => a + (b - a) * k;
  // progress of t through [a,b], clamped 0..1
  E.p = (t, a, b) => E.clamp((t - a) / (b - a));
  E.mix = (a, b, k) => a + (b - a) * k;

  // easings
  E.outCubic = k => 1 - Math.pow(1 - k, 3);
  E.outQuart = k => 1 - Math.pow(1 - k, 4);
  E.outQuint = k => 1 - Math.pow(1 - k, 5);
  E.outExpo = k => (k >= 1 ? 1 : 1 - Math.pow(2, -10 * k));
  E.inExpo = k => (k <= 0 ? 0 : Math.pow(2, 10 * k - 10));
  E.inCubic = k => k * k * k;
  E.inQuart = k => k * k * k * k;
  E.inOutCubic = k => (k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2);
  E.inOutQuart = k => (k < 0.5 ? 8 * k ** 4 : 1 - Math.pow(-2 * k + 2, 4) / 2);
  E.inOutExpo = k => (k <= 0 ? 0 : k >= 1 ? 1 : k < 0.5 ? Math.pow(2, 20 * k - 10) / 2 : (2 - Math.pow(2, -20 * k + 10)) / 2);
  E.outBack = (k, s = 1.70158) => 1 + (s + 1) * Math.pow(k - 1, 3) + s * Math.pow(k - 1, 2);
  E.inBack = (k, s = 1.70158) => (s + 1) * k * k * k - s * k * k;
  E.linear = k => k;

  // closed-form damped spring step response: 0 -> 1 (overshoots when damp < 1)
  E.spring = (t, freq = 2.4, damp = 0.45) => {
    if (t <= 0) return 0;
    const w = 2 * Math.PI * freq, z = damp;
    if (z >= 1) return 1 - Math.exp(-w * t) * (1 + w * t);
    const wd = w * Math.sqrt(1 - z * z);
    return 1 - Math.exp(-z * w * t) * (Math.cos(wd * t) + (z * w / wd) * Math.sin(wd * t));
  };
  // spring that starts at time a
  E.sp = (t, a, freq, damp) => E.spring(t - a, freq, damp);

  // keyframes: kf(t, [[t0, v0], [t1, v1, ease], ...]) — ease applies to the segment ending at that key
  E.kf = (t, keys, defEase = E.inOutCubic) => {
    if (t <= keys[0][0]) return keys[0][1];
    for (let i = 1; i < keys.length; i++) {
      const [t1, v1, ez] = keys[i];
      if (t <= t1) {
        const [t0, v0] = keys[i - 1];
        const k = (ez || defEase)((t - t0) / (t1 - t0));
        return v0 + (v1 - v0) * k;
      }
    }
    return keys[keys.length - 1][1];
  };

  // seeded hash -> [0,1)
  E.hash = (n) => { let x = Math.sin(n * 127.1 + 311.7) * 43758.5453123; return x - Math.floor(x); };

  // DOM helpers
  const cache = {};
  E.$ = id => cache[id] || (cache[id] = document.getElementById(id));
  // T(el, {x, y, s, sx, sy, r, o, blur, bx, by, z}) — sets transform/opacity/filter
  E.T = (el, o) => {
    if (typeof el === 'string') el = E.$(el);
    if (!el) return;
    const x = o.x || 0, y = o.y || 0;
    const sx = (o.s ?? 1) * (o.sx ?? 1), sy = (o.s ?? 1) * (o.sy ?? 1);
    let tf = `translate3d(${x.toFixed(2)}px,${y.toFixed(2)}px,0)`;
    if (o.c) tf += ' translate(-50%,-50%)';
    if (o.r) tf += ` rotate(${o.r.toFixed(3)}deg)`;
    if (o.skx) tf += ` skewX(${o.skx.toFixed(3)}deg)`;
    if (sx !== 1 || sy !== 1) tf += ` scale(${sx.toFixed(4)},${sy.toFixed(4)})`;
    el.style.transform = tf;
    if (o.o !== undefined) {
      const op = E.clamp(o.o);
      el.style.opacity = op.toFixed(3);
      el.style.visibility = op <= 0.001 ? 'hidden' : 'visible';
    }
    const b = o.blur || 0;
    let f = '';
    if (b > 0.05) f += `blur(${b.toFixed(2)}px)`;
    if (o.bright !== undefined && o.bright !== 1) f += ` brightness(${o.bright.toFixed(3)})`;
    if (o.sat !== undefined && o.sat !== 1) f += ` saturate(${o.sat.toFixed(3)})`;
    el.style.filter = f || 'none';
  };
  E.show = (el, on) => { if (typeof el === 'string') el = E.$(el); if (el) el.style.display = on ? '' : 'none'; };
  E.vis = (el, on) => { if (typeof el === 'string') el = E.$(el); if (el) el.style.visibility = on ? 'visible' : 'hidden'; };

  // velocity-based blur: magnitude of change of fn over dt
  E.vblur = (fn, t, k = 1, dt = 1 / 60, max = 30) => Math.min(max, Math.abs(fn(t) - fn(t - dt)) * k);

  // split element text into per-char spans (keeps spaces)
  E.split = (el) => {
    if (typeof el === 'string') el = E.$(el);
    const txt = el.textContent; el.textContent = '';
    const spans = [];
    for (const ch of txt) {
      const s = document.createElement('span');
      s.className = 'ch'; s.textContent = ch === ' ' ? ' ' : ch;
      s.style.display = 'inline-block'; s.style.willChange = 'transform';
      el.appendChild(s); spans.push(s);
    }
    return spans;
  };

  // typed text: returns substring for typing effect at given chars/sec
  E.typed = (str, t, a, cps = 22) => str.slice(0, Math.max(0, Math.floor((t - a) * cps)));

  // number roll
  E.fmtINR = (n) => {
    n = Math.round(n); const s = String(n);
    if (s.length <= 3) return s;
    const last3 = s.slice(-3); let rest = s.slice(0, -3);
    rest = rest.replace(/\B(?=(\d{2})+(?!\d))/g, ',');
    return rest + ',' + last3;
  };

  // starfield on a canvas, deterministic
  E.Stars = class {
    constructor(canvas, n = 220, seed = 1) {
      this.c = canvas; this.ctx = canvas.getContext('2d');
      this.s = [];
      for (let i = 0; i < n; i++) {
        const h = k => E.hash(seed * 1000 + i * 7.31 + k);
        this.s.push({ x: h(1), y: h(2), r: 0.6 + h(3) * 1.8, ph: h(4) * 6.28, sp: 0.6 + h(5) * 2.2, d: 0.2 + h(6) * 0.8 });
      }
    }
    draw(t, driftX = 0, driftY = 0, alpha = 1) {
      const { ctx, c } = this; ctx.clearRect(0, 0, c.width, c.height);
      if (alpha <= 0) return;
      for (const s of this.s) {
        const tw = 0.55 + 0.45 * Math.sin(t * s.sp + s.ph);
        let x = (s.x * c.width + driftX * s.d) % c.width; if (x < 0) x += c.width;
        let y = (s.y * c.height + driftY * s.d) % c.height; if (y < 0) y += c.height;
        ctx.globalAlpha = alpha * tw * (0.35 + 0.65 * s.d);
        ctx.fillStyle = '#ffffff';
        ctx.beginPath(); ctx.arc(x, y, s.r, 0, 6.283); ctx.fill();
      }
      ctx.globalAlpha = 1;
    }
  };

  // film grain: a few pre-baked noise tiles, picked deterministically per frame
  E.Grain = class {
    constructor(canvas, amt = 18) {
      this.c = canvas; this.ctx = canvas.getContext('2d'); this.tiles = [];
      const S = 256;
      for (let k = 0; k < 6; k++) {
        const tc = document.createElement('canvas'); tc.width = tc.height = S;
        const tx = tc.getContext('2d'); const img = tx.createImageData(S, S);
        for (let i = 0; i < S * S; i++) {
          const v = 128 + (E.hash(k * 99991 + i * 1.7) - 0.5) * 2 * amt * 3;
          img.data[i * 4] = img.data[i * 4 + 1] = img.data[i * 4 + 2] = v; img.data[i * 4 + 3] = 255;
        }
        tx.putImageData(img, 0, 0); this.tiles.push(tc);
      }
    }
    draw(t) {
      const k = Math.floor(t * 24) % this.tiles.length;
      const pat = this.ctx.createPattern(this.tiles[k], 'repeat');
      this.ctx.fillStyle = pat; this.ctx.fillRect(0, 0, this.c.width, this.c.height);
    }
  };

  // wait for fonts + images
  E.ready = async (extraFonts = []) => {
    const fams = ["700 100px 'Space Grotesk'", "500 100px 'Space Grotesk'", "800 100px Manrope", "600 100px Manrope", "500 100px Manrope", "700 100px Manrope", ...extraFonts];
    await Promise.all(fams.map(f => document.fonts.load(f, 'A₹')));
    await document.fonts.ready;
    const imgs = [...document.images];
    await Promise.all(imgs.map(i => i.complete ? (i.decode ? i.decode().catch(() => { }) : 0) : new Promise(r => { i.onload = i.onerror = r; })));
    await Promise.all(imgs.map(i => i.decode ? i.decode().catch(() => { }) : 0));
  };

  window.E = E;
})();
