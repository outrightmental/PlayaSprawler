(function () {
  'use strict';
  const P = PS.params, R = PS.results, C = R.classes, PK = R.packing;
  const DEF = P.default_class, D = C[DEF];
  const $ = (s, el) => (el || document).querySelector(s);
  const fmt = (x, d) => Number(x).toLocaleString('en-US', { maximumFractionDigits: d == null ? 1 : d, minimumFractionDigits: d == null ? 0 : d });
  const moduleMass = Object.values(P.module_breakdown).reduce((a, b) => a + b, 0);
  const eUsable = 4 * P.battery.wh * P.battery.usable_frac;

  // ---------- simple value binding
  const V = {
    version: P.version, bag_lb: fmt(P.bag_lb, 0), timeout: P.comms_timeout_ms,
    bag_dims: P.bag_mm.map(x => fmt(x, 0)).join(' × '), bag_in: fmt(PK.linear_in, 1),
    mass_total: fmt(PK.total_kg, 2), mass_limit: fmt(PK.limit_kg, 2), mass_margin: (PK.margin_kg >= 0 ? '+' : '') + fmt(PK.margin_kg, 2) + ' kg (' + fmt(PK.margin_pct, 1) + ' %)',
    mass_margin_kg: fmt(PK.margin_kg, 2), vmax: fmt(P.v_max_kmh, 0), wh: fmt(P.battery.wh, 1), alat: P.a_lat_g,
    tire: P.tire, wheel_od: fmt(P.wheel_od, 0), wheel_od_deflated: fmt(P.wheel_od_deflated, 0), module_width: fmt(P.module_width, 0),
    module_mass: fmt(moduleMass, 2), tube: P.tube, cord: P.cord, e_usable: fmt(eUsable, 0),
    stack: fmt(PK.stack_len, 0), longest: fmt(PK.longest_segment, 0),
  };
  document.querySelectorAll('[data-v]').forEach(el => { const k = el.getAttribute('data-v'); if (k in V) el.textContent = V[k]; });
  $('#built').textContent = R.generated;

  // ---------- hero: side view generated from the frame nodes
  (function hero() {
    const svg = $('#hero-svg'), N = PS.nodes;
    const k = 0.36, ox = 300, oy = 335;
    const X = x => ox + x * k, Z = z => oy - z * k;
    const r = P.wheel_od / 2;
    let out = [];
    out.push(`<line x1="0" y1="${Z(0)}" x2="560" y2="${Z(0)}" stroke="#d9d6cc" stroke-width="1.5"/>`);
    const wheel = (x, extra) => `<g class="${extra || ''}">
      <circle class="tire" cx="${X(x)}" cy="${Z(r)}" r="${r * k}"/>
      <circle class="rim" cx="${X(x)}" cy="${Z(r)}" r="${r * k * 0.66}"/>
      <rect class="brick" x="${X(x) - 100 * k}" y="${Z(284)}" width="${200 * k}" height="${96 * k}" rx="5"/>
      <rect x="${X(x) - 60 * k}" y="${Z(300)}" width="${120 * k}" height="${16 * k}" fill="#15171c"/>
      <circle cx="${X(x)}" cy="${Z(r)}" r="5" fill="#15171c"/></g>`;
    // rear-right module is the one that gets swapped (drawn twice: out and in)
    out.push(wheel(N.DOCK_FL[0]));
    out.push(wheel(N.DOCK_RL[0], 'swap-out'));
    out.push(wheel(N.DOCK_RL[0], 'swap-in'));
    for (const m of PS.members) {
      const a = N[m.a], b = N[m.b];
      if (!(m.a.endsWith('_L') || m.a.endsWith('L')) || !(m.b.endsWith('_L') || m.b.endsWith('L'))) continue; // left side only
      if (m.a === m.b) continue;
      if (m.k === 'fabric') continue;
      const cls = m.k === 'tube' ? 'tube' : 'cord';
      if (Math.abs(a[0] - b[0]) < 1 && Math.abs(a[2] - b[2]) < 1) continue; // rails: seen end-on
      out.push(`<line class="${cls}" x1="${X(a[0])}" y1="${Z(a[2])}" x2="${X(b[0])}" y2="${Z(b[2])}"/>`);
    }
    // seat sling: front tip -> low point -> rear tip
    const f = N.FTIP_L, s = N.SEAT_L, rt = N.RTIP_L;
    out.push(`<path class="fab" d="M${X(f[0])},${Z(f[2])} Q${X(s[0] + 40)},${Z(s[2] - 60)} ${X(rt[0])},${Z(rt[2])}"/>`);
    for (const nm of ['HUB_L', 'DOCK_FL', 'DOCK_RL', 'FTIP_L', 'RTIP_L']) {
      const p = N[nm]; out.push(`<circle class="joint" cx="${X(p[0])}" cy="${Z(p[2])}" r="6"/>`);
    }
    out.push(`<text x="12" y="${Z(0) + 18}" font-family="JetBrains Mono,monospace" font-size="11" fill="#8a8f9a">RR module: out, spare in — pin, rail, two M12s</text>`);
    out.push(`<text x="548" y="20" text-anchor="end" font-family="JetBrains Mono,monospace" font-size="11" fill="#8a8f9a">side view · generated from ps_params.py · x → forward</text>`);
    svg.innerHTML = out.join('');
    // ticker + mode badge synced to the 9 s CSS loop
    const tick = $('#hero-ticker'), badge = $('#hero-mode');
    let seq = 1200, t0 = performance.now(), lines = [];
    function push(html) { lines.push(html); if (lines.length > 4) lines.shift(); tick.innerHTML = lines.map(l => `<div>${l}</div>`).join(''); }
    setInterval(() => {
      const t = ((performance.now() - t0) / 1000) % 9; seq += 5;
      const phase = t < 3.4 ? 'run' : t < 4.6 ? 'pulled' : t < 5.9 ? 'stop' : 'run2';
      if (phase === 'run' || phase === 'run2') { badge.textContent = 'RUN'; badge.className = 'modebadge'; }
      else { badge.textContent = 'STOP'; badge.className = 'modebadge stop'; }
      const v = (0.55 + 0.1 * Math.sin(t * 2)).toFixed(2);
      if (phase === 'run') push(`<b>ctrl/tread/left</b> {v: ${v}, seq: ${seq}} · <b>wheel/RR/status</b> {v_kmh: ${(v * 8).toFixed(1)}, soc: 0.86}`);
      else if (phase === 'pulled') push(`<i>wheel/RR/status silent 250 ms</i> → <b>veh/mode</b> {mode: "stop"} — every wheel ramps to 0 in 300 ms`);
      else if (phase === 'stop') push(`<b>node/W-0042/hello</b> {dock: "RR", rating: "PS-125"} · read from the dock ID pin, no configuration`);
      else push(`<b>veh/mode</b> {mode: "run", rating: "PS-125"} · <b>ctrl/tread/right</b> {v: ${v}, seq: ${seq + 1}}`);
    }, 700);
  })();

  // ---------- evidence tables
  (function evidence() {
    const lcName = { LC1: 'LC1 static seated', LC2: 'LC2 2.5 g vertical', LC3: 'LC3 lateral skid', LC5: 'LC5 backrest lean' };
    let h = `<tr><th>Case</th>${Object.keys(C).map(c => `<th colspan="4">${c}</th>`).join('')}</tr><tr><th></th>${Object.keys(C).map(() => '<th class="n">defl. mm</th><th class="n">tube SF</th><th class="n">cord SF</th><th class="n">seat SF</th>').join('')}</tr>`;
    for (const lc of Object.keys(D.frame)) {
      h += `<tr><td>${lcName[lc] || lc}</td>`;
      for (const c of Object.keys(C)) {
        const w = C[c].frame[lc].worst, ult = lc !== 'LC1';
        const cell = (v, t) => v == null ? '<td class="n">—</td>' : `<td class="n ${ult ? (v >= t ? 'pass' : 'fail') : ''}">${fmt(v, 1)}</td>`;
        h += `<td class="n">${fmt(C[c].frame[lc].max_d_mm, 1)}</td>${cell(w.tube_sf_b, P.sf.tube)}${cell(w.cord_sf, P.sf.cord)}${cell(w.fabric_sf, P.sf.fabric)}`;
      }
      h += '</tr>';
    }
    $('#frame-table').innerHTML = h;
    const s = D.stability;
    $('#stab-text').innerHTML = `Combined CG ${fmt(s.cg_z_mm, 0)} mm high on a ${fmt(P.track, 0)} mm track and ${fmt(P.wheelbase, 0)} mm wheelbase. Quasi-static tip at <b>${fmt(s.tip_lat_g, 2)} g</b> lateral (${fmt(s.side_slope_deg, 0)}° side slope), ${fmt(s.tip_long_g, 2)} g longitudinal. The limiter runs at ${P.a_lat_g} g — ${fmt(s.margin_vs_tip, 1)}× under the threshold. Stop from 8 km/h in ${fmt(s.stop_dist_m, 1)} m at 0.30 g.`;
    $('#turn-table').innerHTML = `<tr><th class="n">radius m</th><th class="n">cap km/h</th></tr>` + D.v_by_radius.map(([r, v]) => `<tr><td class="n">${fmt(r, 1)}</td><td class="n">${fmt(v * 3.6, 1)}</td></tr>`).join('');
    const a = D.axle;
    $('#axle-text').innerHTML = `At 2.5 g the wheel carries ${fmt(a.F_N, 0)} N on a 45 mm cantilever: ${fmt(a.M_Nm, 1)} N·m bending plus 35 N·m peak torque → ${fmt(a.vm_MPa, 0)} MPa von Mises on the 12 mm axle. <b>SF ${fmt(a.sf, 2)}</b> against an <em>assumed</em> 785 MPa yield (target ${a.sf_target}). Verify per motor or clamp both sides.`;
    const maxR = Math.max(...D.energy.map(e => e.range_km));
    $('#range-bars').innerHTML = D.energy.map(e => `<div class="row"><span>${e.surface} · ${fmt(e.grade * 100, 0)} %</span><div class="b"><i class="${e.torque_ok && e.power_ok ? '' : 'flag'}" style="width:${(e.range_km / maxR * 100).toFixed(1)}%"></i></div><span class="n">${fmt(e.range_km, 1)} km</span></div>`).join('');
  })();

  // ---------- rating calculator
  (function rating() {
    const rc = $('#rc'), sw = $('#swap'), out = $('#rating-out');
    const kg = c => P.classes[c];
    function render() {
      const cls = rc.value, cl = C[cls];
      let parts = [['Frame tubes', cls], ['Joiners', cls], ['Cords', cls], ['Seat', cls], ['Wheel FL', cls], ['Wheel FR', cls], ['Wheel RL', cls], ['Wheel RR', sw.value || cls]];
      const veh = parts.reduce((m, p) => kg(p[1]) < kg(m) ? p[1] : m, 'PS-150');
      const mode = kg(veh) < kg(cls) ? 'crawl' : 'run';
      const w2 = cl.frame.LC2.worst, w3 = cl.frame.LC3.worst;
      let h = `<table><tr><th>Check at ${cls} (${kg(cls)} kg payload)</th><th class="n">SF</th><th class="n">target</th><th></th></tr>`;
      const row = (n, v, t) => `<tr><td>${n}</td><td class="n">${fmt(v, 2)}</td><td class="n">${t}</td><td class="${v >= t ? 'pass' : 'fail'}">${v >= t ? 'pass' : 'FAIL'}</td></tr>`;
      h += row('Tube buckling, LC2', w2.tube_sf_b, P.sf.tube) + row('Cord, LC2', w2.cord_sf, P.sf.cord) + row('Seat edge, LC2', w2.fabric_sf, P.sf.fabric) + row('Cord, LC3 lateral', w3.cord_sf, P.sf.cord) + row('Axle (assumed steel)', cl.axle.sf, P.sf.axle);
      h += `<tr><td>Static deflection, LC1</td><td class="n">${fmt(cl.frame.LC1.max_d_mm, 1)} mm</td><td class="n">≤ 20</td><td class="${cl.frame.LC1.max_d_mm <= 20 ? 'pass' : 'fail'}">${cl.frame.LC1.max_d_mm <= 20 ? 'pass' : 'FAIL'}</td></tr></table>`;
      h += `<p style="margin-top:12px">Parts on the vehicle: ${parts.map(p => `<span class="tag ${kg(p[1]) < kg(cls) ? 'flag' : ''}">${p[0]} ${p[1]}</span>`).join(' ')}</p>`;
      h += `<p><b>Vehicle rating = min(parts) = ${veh}.</b> Rider class ${cls} → firmware mode <span class="tag ${mode === 'run' ? 'ok' : 'flag'}">${mode}</span>${mode === 'crawl' ? ' (2 km/h cap until the low-rated part is replaced)' : ''}.</p>`;
      out.innerHTML = h;
    }
    rc.onchange = sw.onchange = render; render();
  })();

  // ---------- module and mass bars, segments
  (function bars() {
    const mb = P.module_breakdown, mx = Math.max(...Object.values(mb));
    $('#module-breakdown').innerHTML = Object.entries(mb).map(([k, v]) => `<div class="row"><span>${k}</span><div class="b"><i style="width:${(v / mx * 100).toFixed(1)}%"></i></div><span class="n">${fmt(v, 2)} kg</span></div>`).join('');
    const m = P.mass_budget, lim = PK.limit_kg;
    let cum = 0, h = '';
    for (const [k, v] of Object.entries(m)) { cum += v; h += `<div class="row"><span>${k}</span><div class="b"><i style="width:${(v / lim * 100).toFixed(1)}%"></i></div><span class="n">${fmt(v, 2)}</span></div>`; }
    h += `<div class="row" style="margin-top:6px;font-weight:700"><span>total</span><div class="b"><i class="flag" style="width:${(cum / lim * 100).toFixed(1)}%"></i></div><span class="n">${fmt(cum, 2)}</span></div>`;
    h += `<div class="row"><span>limit (50 lb)</span><div class="b" style="background:transparent;border:1px dashed var(--ink-3)"></div><span class="n">${fmt(lim, 2)}</span></div>`;
    $('#mass-bars').innerHTML = h;
    $('#seg-table').innerHTML = '<tr><th>Tube</th><th class="n">length</th><th class="n">segments</th></tr>' + PK.segments.map(s => `<tr><td>${s[0]}</td><td class="n">${fmt(s[1], 0)} mm</td><td class="n">${s[2]} × ${fmt(s[3], 0)}</td></tr>`).join('');
  })();

  // ---------- PS-Bus simulator (port of firmware/sim/psbus_sim.py)
  (function sim() {
    const TIMEOUT = P.comms_timeout_ms / 1000, RAMP = 0.3, CAP = { run: P.v_max_kmh, crawl: 2, stop: 0 }, KG = P.classes;
    const DT = 0.02; let now = 0;
    const log = $('#sim-log'), logs = [];
    function L(msg, cls) { logs.push(`<div><span class="t">${now.toFixed(2)}s</span> <span class="${cls || ''}">${msg}</span></div>`); if (logs.length > 200) logs.shift(); log.innerHTML = logs.join(''); log.scrollTop = log.scrollHeight; }
    const bus = { subs: [], pub(t, m) { for (const [p, cb] of this.subs) if (match(p, t)) cb({ t, ts: now, ...m }); }, sub(p, cb) { this.subs.push([p, cb]); return cb; }, unsub(cbs) { this.subs = this.subs.filter(([p, cb]) => !cbs.includes(cb)); } };
    const match = (p, t) => { const a = p.split('/'), b = t.split('/'); return a.length === b.length && a.every((x, i) => x === '+' || x === b[i]); };
    const SIDE = { FL: 'left', RL: 'left', FR: 'right', RR: 'right', CL: 'left', CR: 'right' };
    let serialN = 1;
    class Wheel {
      constructor(rating) { this.serial = 'W-' + String(serialN++).padStart(4, '0'); this.rating = rating; this.cmd = 0; this.cmdTs = -1e9; this.seq = -1; this.v = 0; this.mode = 'stop'; this.estop = false; this.nextStatus = 0; this.nextHello = 0; this.alive = false; this.cbs = []; this.stopReason = null; }
      plug(dock) { this.dock = dock; this.alive = true; this.side = SIDE[dock]; this.cmdTs = -1e9; this.nextHello = now;
        this.cbs = [bus.sub('ctrl/tread/' + this.side, m => { if (typeof m.v !== 'number' || m.v < -1 || m.v > 1) return; this.cmd = m.v; this.cmdTs = m.ts; }),
          bus.sub('veh/mode', m => this.mode = m.mode), bus.sub('veh/estop', m => this.estop = m.active)]; }
      unplug() { this.alive = false; bus.unsub(this.cbs); this.cbs = []; this.dock = null; }
      tick() { if (!this.alive) return;
        if (now >= this.nextHello) { bus.pub(`node/${this.serial}/hello`, { kind: 'wheel', dock: this.dock, rating: this.rating }); this.nextHello = now + 1; }
        const cap = CAP[this.mode] || 0, timedOut = now - this.cmdTs > TIMEOUT;
        let target = 0; this.stopReason = null;
        if (this.estop) this.stopReason = 'estop'; else if (timedOut) this.stopReason = 'timeout'; else if (cap === 0) this.stopReason = 'mode'; else target = this.cmd * cap;
        const step = 8 * DT / (Math.abs(target) < Math.abs(this.v) ? RAMP : 0.5);
        this.v += Math.max(-step, Math.min(step, target - this.v)); if (Math.abs(this.v) < 1e-3) this.v = 0;
        if (now >= this.nextStatus) { bus.pub(`wheel/${this.dock}/status`, { serial: this.serial, v_kmh: this.v, stop: this.stopReason }); this.nextStatus = now + 0.1; } }
    }
    class Control {
      constructor(serial, input, fn) { this.serial = serial; this.input = input; this.fn = fn; this.seq = 0; this.next = 0; this.alive = false; this.nextHello = 0; }
      plug(dock) { this.dock = dock; this.side = SIDE[dock]; this.alive = true; this.nextHello = now; }
      unplug() { this.alive = false; }
      tick() { if (!this.alive) return; if (now >= this.nextHello) { bus.pub(`node/${this.serial}/hello`, { kind: 'control', dock: this.dock, rating: 'PS-150' }); this.nextHello = now + 1; }
        if (now >= this.next) { bus.pub('ctrl/tread/' + this.side, { v: this.fn(), seq: ++this.seq, src: this.serial, input: this.input }); this.next = now + DT; } }
    }
    const sup = { rider: 'PS-125', parts: {}, status: {}, mode: 'stop', estop: false, frameRating: 'PS-125',
      init() { bus.sub('node/+/hello', m => { const s = m.t.split('/')[1]; for (const k of Object.keys(this.parts)) if (this.parts[k].dock === m.dock && k !== s) delete this.parts[k]; this.parts[s] = { kind: m.kind, dock: m.dock, rating: m.rating, ts: m.ts }; });
        bus.sub('wheel/+/status', m => this.status[m.t.split('/')[1]] = m.ts); },
      tick() { const live = Object.values(this.parts).filter(p => now - p.ts <= 2.5); const wheels = new Set(live.filter(p => p.kind === 'wheel').map(p => p.dock));
        const ok = ['FL', 'FR', 'RL', 'RR'].every(d => wheels.has(d) && now - (this.status[d] ?? -1e9) <= 0.25);
        let rating = live.concat([{ rating: this.frameRating }]).reduce((m, p) => KG[p.rating] < KG[m] ? p.rating : m, 'PS-150');
        const mode = this.estop ? 'stop' : !ok ? 'stop' : KG[rating] < KG[this.rider] ? 'crawl' : 'run';
        if (mode !== this.mode) { L(`supervisor: mode ${this.mode} → <b>${mode}</b> (wheels ${[...wheels].sort().join(',') || 'none'}, vehicle rating ${rating}, rider ${this.rider})`, 'm'); this.mode = mode; }
        this.rating = rating; bus.pub('veh/mode', { mode, rating, rider_class: this.rider }); bus.pub('veh/estop', { active: this.estop }); } };
    sup.init();
    const tl = $('#tl'), tr = $('#tr');
    const cl = new Control('C-0007', 'lever', () => tl.value / 100), cr = new Control('C-0011', 'pedal', () => tr.value / 100);
    const wheels = { FL: new Wheel('PS-125'), FR: new Wheel('PS-125'), RL: new Wheel('PS-125'), RR: new Wheel('PS-125') };
    for (const d in wheels) wheels[d].plug(d); cl.plug('CL'); cr.plug('CR');
    let spare = null;
    const wdiv = $('#sim-wheels');
    wdiv.innerHTML = ['FL', 'FR', 'RL', 'RR'].map(d => `<div class="wheel" id="w-${d}"><span class="pos">${d}</span> <span class="ser"></span><div class="bar"><i></i></div><span class="st"></span></div>`).join('');
    L('boot: 4 wheel modules + lever (CL) + pedal (CR) + supervisor; rider class PS-125');
    $('#b-pull').onclick = () => { if (!wheels.RR.alive) return; L(`HOT-SWAP: wheel RR (${wheels.RR.serial}) pulled out`, 'e'); wheels.RR.unplug(); };
    const insert = r => { if (wheels.RR.alive) { L('dock RR is occupied — pull the module first', 'e'); return; } spare = new Wheel(r); spare.plug('RR'); wheels.RR = spare; L(`spare ${spare.serial} rated ${r} pushed into dock RR; it reads the dock ID and becomes RR`); };
    $('#b-ins100').onclick = () => insert('PS-100'); $('#b-ins125').onclick = () => insert('PS-125');
    $('#b-cut').onclick = () => { if (!cl.alive) return; cl.unplug(); L('FAULT: left control cable unplugged (CL goes silent)', 'e'); $('#sim-cl').className = 'tag flag'; $('#sim-cl').textContent = 'CL unplugged'; };
    $('#b-plug').onclick = () => { if (cl.alive) return; cl.plug('CL'); L('left control re-plugged into dock CL'); $('#sim-cl').className = 'tag ok'; $('#sim-cl').textContent = 'CL lever'; };
    $('#b-estop').onclick = () => { sup.estop = !sup.estop; L(`e-stop ${sup.estop ? 'PRESSED' : 'released'}`, 'e'); $('#b-estop').textContent = sup.estop ? 'release e-stop' : 'e-stop'; };
    tl.oninput = () => $('#tlv').textContent = (tl.value / 100).toFixed(2); tr.oninput = () => $('#trv').textContent = (tr.value / 100).toFixed(2);
    let visible = true; const io = new IntersectionObserver(e => visible = e[0].isIntersecting, { rootMargin: '200px' }); io.observe($('#sim'));
    setInterval(() => { if (!visible) return; now += DT; cl.tick(); cr.tick(); for (const d in wheels) wheels[d].tick(); sup.tick();
      for (const d in wheels) { const w = wheels[d], el = $('#w-' + d); el.classList.toggle('gone', !w.alive); $('.ser', el).textContent = w.alive ? `${w.serial} · ${w.rating}` : 'empty dock'; $('.bar i', el).style.width = (Math.abs(w.v) / P.v_max_kmh * 100) + '%'; $('.st', el).textContent = w.alive ? `${w.v.toFixed(1)} km/h${w.stopReason ? ' · stop: ' + w.stopReason : ''}` : '—'; }
      const m = $('#sim-mode'); m.textContent = sup.mode; m.className = 'tag ' + (sup.mode === 'run' ? 'ok' : 'flag'); $('#sim-rating').textContent = sup.rating || '—';
    }, DT * 1000);
  })();
})();
