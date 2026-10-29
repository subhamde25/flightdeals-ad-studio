// Shared SVG icons, flags and a deterministic QR-style matrix.
(function () {
  const I = {};
  const sw = (w = 2) => `fill="none" stroke="currentColor" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"`;
  I.passport = (w = 2) => `<svg viewBox="0 0 24 24" ${sw(w)}><rect x="4.5" y="2.5" width="15" height="19" rx="2.2"/><circle cx="12" cy="10" r="3.6"/><path d="M8.4 10h7.2M12 6.4c1.2 1.1 1.2 6.1 0 7.2M12 6.4c-1.2 1.1-1.2 6.1 0 7.2"/><path d="M8.5 17.5h7"/></svg>`;
  I.sim = (w = 2) => `<svg viewBox="0 0 24 24" ${sw(w)}><path d="M7 2.5h7.5l4.5 4.5v12.5a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-15a2 2 0 0 1 2-2z"/><rect x="8.2" y="10.5" width="7.6" height="7" rx="1.2"/><path d="M12 10.5v7M8.2 14h7.6"/></svg>`;
  I.bed = (w = 2) => `<svg viewBox="0 0 24 24" ${sw(w)}><path d="M2.5 19V5.5M2.5 13.5h19V19M21.5 13.5v-2.5a3 3 0 0 0-3-3H11v5.5"/><circle cx="6.8" cy="10" r="2"/></svg>`;
  I.check = (w = 3) => `<svg viewBox="0 0 24 24" ${sw(w)}><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>`;
  I.x = (w = 3) => `<svg viewBox="0 0 24 24" ${sw(w)}><path d="M6 6l12 12M18 6L6 18"/></svg>`;
  I.stamp = (w = 2) => `<svg viewBox="0 0 24 24" ${sw(w)}><path d="M5 21h14M6 17.5h12v-3a1.5 1.5 0 0 0-1.5-1.5h-2.3l-.7-3.2a3 3 0 1 0-3 0L9.8 13H7.5A1.5 1.5 0 0 0 6 14.5z"/></svg>`;
  I.clock = (w = 2) => `<svg viewBox="0 0 24 24" ${sw(w)}><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>`;
  I.info = (w = 2) => `<svg viewBox="0 0 24 24" ${sw(w)}><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/></svg>`;
  I.shield = (w = 2) => `<svg viewBox="0 0 24 24" ${sw(w)}><path d="M12 2.5l7.5 3v6c0 4.5-3.2 8.3-7.5 10-4.3-1.7-7.5-5.5-7.5-10v-6z"/><path d="M8.5 12l2.5 2.5 4.5-4.5"/></svg>`;
  I.doc = (w = 2) => `<svg viewBox="0 0 24 24" ${sw(w)}><path d="M14 2.5H6.5a2 2 0 0 0-2 2v15a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V8z"/><path d="M14 2.5V8h5.5M8.5 13h7M8.5 17h7"/></svg>`;
  I.wifi = (w = 2) => `<svg viewBox="0 0 24 24" ${sw(w)}><path d="M2.5 8.8a14 14 0 0 1 19 0M5.5 12.3a9.5 9.5 0 0 1 13 0M8.6 15.7a5 5 0 0 1 6.8 0"/><circle cx="12" cy="19" r="1" fill="currentColor"/></svg>`;
  I.pin = (w = 2) => `<svg viewBox="0 0 24 24" ${sw(w)}><path d="M12 21.5s-7-6.2-7-11.5a7 7 0 0 1 14 0c0 5.3-7 11.5-7 11.5z"/><circle cx="12" cy="10" r="2.6"/></svg>`;
  I.search = (w = 2.2) => `<svg viewBox="0 0 24 24" ${sw(w)}><circle cx="11" cy="11" r="7"/><path d="M20.5 20.5l-4.5-4.5"/></svg>`;
  I.ext = (w = 2.2) => `<svg viewBox="0 0 24 24" ${sw(w)}><path d="M14 4h6v6M20 4l-9 9M18 14v5a1.5 1.5 0 0 1-1.5 1.5h-11A1.5 1.5 0 0 1 4 19V7.5A1.5 1.5 0 0 1 5.5 6H10"/></svg>`;
  I.arrow = (w = 2.6) => `<svg viewBox="0 0 24 24" ${sw(w)}><path d="M5 12h14M13 6l6 6-6 6"/></svg>`;
  I.chev = (w = 2.2) => `<svg viewBox="0 0 24 24" ${sw(w)}><path d="M6 9l6 6 6-6"/></svg>`;
  I.globe = (w = 2) => `<svg viewBox="0 0 24 24" ${sw(w)}><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.6 2.6 15.4 0 18M12 3c-2.6 2.6-2.6 15.4 0 18"/></svg>`;
  I.bolt = (w = 2) => `<svg viewBox="0 0 24 24" ${sw(w)}><path d="M13 2.5L4.5 13.5H11l-1 8 8.5-11H12z"/></svg>`;
  I.cal = (w = 2) => `<svg viewBox="0 0 24 24" ${sw(w)}><rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg>`;
  I.coffee = (w = 2) => `<svg viewBox="0 0 24 24" ${sw(w)}><path d="M4 9h13v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5zM17 10h1.5a2.5 2.5 0 0 1 0 5H17M7 3.5v2.5M10.5 3.5v2.5M14 3.5v2.5"/></svg>`;
  I.heart = (w = 2) => `<svg viewBox="0 0 24 24" ${sw(w)}><path d="M12 20s-7.5-4.6-7.5-10A4.3 4.3 0 0 1 12 7.4 4.3 4.3 0 0 1 19.5 10c0 5.4-7.5 10-7.5 10z"/></svg>`;
  I.map = (w = 2) => `<svg viewBox="0 0 24 24" ${sw(w)}><path d="M9 4.5L3.5 6.5v13l5.5-2 6 2 5.5-2v-13l-5.5 2z"/><path d="M9 4.5v13M15 6.5v13"/></svg>`;
  I.list = (w = 2) => `<svg viewBox="0 0 24 24" ${sw(w)}><path d="M8 6h12M8 12h12M8 18h12M4 6h.01M4 12h.01M4 18h.01"/></svg>`;
  I.sparkle = (w = 2) => `<svg viewBox="0 0 24 24" ${sw(w)}><path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/></svg>`;
  I.plane = () => `<svg viewBox="0 0 24 24"><path fill="currentColor" d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/></svg>`;
  I.star = () => `<svg viewBox="0 0 24 24"><path fill="currentColor" d="M12 2.8l2.8 5.8 6.3.9-4.6 4.4 1.1 6.3L12 17.2l-5.6 3 1.1-6.3L2.9 9.5l6.3-.9z"/></svg>`;
  I.signal = () => `<svg viewBox="0 0 34 22"><rect class="b0" x="0" y="15" width="6" height="7" rx="1.5" fill="currentColor"/><rect class="b1" x="9" y="10" width="6" height="12" rx="1.5" fill="currentColor"/><rect class="b2" x="18" y="5" width="6" height="17" rx="1.5" fill="currentColor"/><rect class="b3" x="27" y="0" width="6" height="22" rx="1.5" fill="currentColor"/></svg>`;
  I.cursor = () => `<svg viewBox="0 0 32 40"><path d="M3 2.5v29.5l7.6-7.2 5 11.5 5.2-2.3-5-11.2H26z" fill="#0b0f1a" stroke="#fff" stroke-width="2.6" stroke-linejoin="round"/></svg>`;

  // flags
  I.flagIN = () => `<svg viewBox="0 0 30 20"><rect width="30" height="20" rx="3" fill="#fff"/><path d="M0 3a3 3 0 0 1 3-3h24a3 3 0 0 1 3 3v3.67H0z" fill="#FF9933"/><path d="M0 13.33h30V17a3 3 0 0 1-3 3H3a3 3 0 0 1-3-3z" fill="#138808"/><circle cx="15" cy="10" r="2.6" fill="none" stroke="#000080" stroke-width=".8"/><circle cx="15" cy="10" r=".6" fill="#000080"/></svg>`;
  I.flagTH = () => `<svg viewBox="0 0 30 20"><rect width="30" height="20" rx="3" fill="#A51931"/><rect y="3.33" width="30" height="13.34" fill="#F4F5F8"/><rect y="6.67" width="30" height="6.66" fill="#2D2A4A"/></svg>`;

  // deterministic QR-like matrix as SVG
  I.qr = (n = 29, seed = 7, fg = '#0C1E45') => {
    const cells = [];
    const finder = (x, y) => (x < 7 && y < 7) || (x >= n - 7 && y < 7) || (x < 7 && y >= n - 7);
    for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) {
      if (finder(x, y)) continue;
      let a = (x * 73856093) ^ (y * 19349663) ^ (seed * 83492791);
      a = Math.imul(a ^ (a >>> 16), 2246822507); a = Math.imul(a ^ (a >>> 13), 3266489909); a ^= a >>> 16;
      if (((a >>> 0) % 1000) / 1000 > 0.5) cells.push(`<rect x="${x}" y="${y}" width="1.02" height="1.02"/>`);
    }
    const fp = (x, y) => `<rect x="${x}" y="${y}" width="7" height="7" rx="1.4" fill="${fg}"/><rect x="${x + 1}" y="${y + 1}" width="5" height="5" rx="1" fill="#fff"/><rect x="${x + 2}" y="${y + 2}" width="3" height="3" rx=".7" fill="${fg}"/>`;
    return `<svg viewBox="-1 -1 ${n + 2} ${n + 2}" shape-rendering="crispEdges"><rect x="-1" y="-1" width="${n + 2}" height="${n + 2}" fill="#fff"/><g fill="${fg}">${cells.join('')}</g>${fp(0, 0)}${fp(n - 7, 0)}${fp(0, n - 7)}</svg>`;
  };

  window.I = I;
})();
