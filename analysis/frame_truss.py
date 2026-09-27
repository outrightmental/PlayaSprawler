"""
Frame structural analysis — 3D pin-jointed truss with tension-only cords.

Idealisation (stated so it can be challenged):
  * Tubes and cords carry axial load only; joint eccentricity moments are
    covered by the printed-joiner socket check and by the proof test.
  * Cords are tension-only. If the linear solve puts a cord in compression it
    is removed and the system re-solved (iterated to convergence). A cord that
    must carry compression signals a mechanism: the script flags it.
  * The wheel-module docks are supported in x, y, z (the wheel contact reacts
    the frame); the module carrier reacts the moment from the contact patch.
  * Seated load enters at the four seat tips: vertical share plus the
    horizontal pull of the fabric sling (parabolic-sag approximation).
"""
import math
import numpy as np
import ps_params as P


def _unit(a, b):
    v = np.array(b) - np.array(a)
    L = float(np.linalg.norm(v))
    return v / L, L


def member_props(kind):
    if kind == "tube":
        A = math.pi / 4 * (P.TUBE["od"] ** 2 - P.TUBE["id"] ** 2)
        return P.TUBE["E_MPa"], A
    if kind == "fabric":
        return P.FABRIC["E_MPa"], P.FABRIC["area_mm2"]
    return P.CORD["E_MPa"], P.CORD["area_mm2"]


def tip_loads(payload_kg, lc):
    """Return {node: [Fx, Fy, Fz]} in N for a load case.
    Seated weight is applied at the two sling low points (the canvas carries it
    to the tips as a real member). Lateral and backrest loads are applied where
    the fabric delivers them: at the tips."""
    W = payload_kg * P.G
    nodes = P.frame_nodes()
    loads = {k: np.zeros(3) for k in nodes}
    for s in ("L", "R"):
        loads[f"SEAT_{s}"] += np.array([0, 0, -lc["vert"] * W / 2])
        # front lateral share reaches the hub through the short post (post bending checked in stub_check)
        loads[f"HUB_{s}"] += np.array([0, lc["lat"] * W * P.FRONT_SHARE / 2, 0])
        loads[f"RTIP_{s}"] += np.array([0, lc["lat"] * W * (1 - P.FRONT_SHARE) / 2, 0])
        loads[f"RTIP_{s}"] += np.array([-lc["back"] * W / 2, 0, 0])
    return loads


def solve(payload_kg, lc, verbose=False):
    nodes = P.frame_nodes()
    members = P.frame_members()
    names = list(nodes)
    idx = {n: i for i, n in enumerate(names)}
    ndof = 3 * len(names)
    active = {m[0]: True for m in members}
    docks = [f"DOCK_{p}" for p in ("FL", "FR", "RL", "RR")]
    # Wheels react vertical load everywhere. Horizontal restraint is deliberately
    # minimal (a free-rolling wheel cannot hold longitudinal thrust): x at the two
    # front docks, y at one dock. Lateral (LC3) and braking (LC5) cases add the
    # tire friction restraint that physically exists for those loads.
    fixed = {d: {2} for d in docks}
    fixed["DOCK_FL"] |= {0, 1}; fixed["DOCK_FR"] |= {0}
    if lc["lat"] > 0:
        for d in docks: fixed[d] |= {1}
    if lc["back"] > 0:
        for d in docks: fixed[d] |= {0}
    supports = docks
    loads = tip_loads(payload_kg, lc)
    F = np.zeros(ndof)
    for n, f in loads.items():
        if n in idx:
            F[3 * idx[n]:3 * idx[n] + 3] = f

    forces = {}
    tension_only = [m[0] for m in members if m[3] in ("cord", "fabric")]
    history = []
    for it in range(60):
        K = np.zeros((ndof, ndof))
        for name, a, b, kind in members:
            if not active[name]:
                continue
            E, A = member_props(kind)
            u, L = _unit(nodes[a], nodes[b])
            k = E * A / L
            T = np.outer(u, u) * k
            ia, ib = 3 * idx[a], 3 * idx[b]
            K[ia:ia + 3, ia:ia + 3] += T; K[ib:ib + 3, ib:ib + 3] += T
            K[ia:ia + 3, ib:ib + 3] -= T; K[ib:ib + 3, ia:ia + 3] -= T
        free = np.ones(ndof, dtype=bool)
        for s, dofs in fixed.items():
            for k in dofs:
                free[3 * idx[s] + k] = False
        Kff = K[np.ix_(free, free)]
        d = np.zeros(ndof)
        Kff += np.eye(Kff.shape[0]) * 1e-6   # numerical guard; a mechanism shows up as a huge displacement
        d[free] = np.linalg.solve(Kff, F[free])
        forces = {}
        elong = {}
        for name, a, b, kind in members:
            E, A = member_props(kind)
            u, L = _unit(nodes[a], nodes[b])
            da, db = d[3 * idx[a]:3 * idx[a] + 3], d[3 * idx[b]:3 * idx[b] + 3]
            e_m = float(np.dot(u, db - da))
            elong[name] = e_m
            forces[name] = E * A / L * e_m if active[name] else 0.0
        # tension-only fixed point: a member is active iff it would be stretched
        want = {m: (elong[m] > -1e-4) for m in tension_only}
        changes = [m for m in tension_only if want[m] != active[m]]
        if not changes:
            break
        # change one member per iteration (most violated first) to avoid oscillation
        changes.sort(key=lambda m: abs(elong[m]), reverse=True)
        m = changes[0]
        active[m] = want[m]
        key = tuple(sorted(k for k, v in active.items() if v))
        if key in history:      # cycling: accept current state
            break
        history.append(key)
    reactions = K @ d - F
    react = {s: reactions[3 * idx[s]:3 * idx[s] + 3] for s in supports}
    disp = {n: d[3 * idx[n]:3 * idx[n] + 3] for n in names}
    removed = [k for k, v in active.items() if not v]
    return forces, react, disp, removed


def tube_checks(force_N, length_mm):
    """Return (buckling SF, strength SF) for a tube member carrying axial force."""
    E, A = member_props("tube")
    I = math.pi / 64 * (P.TUBE["od"] ** 4 - P.TUBE["id"] ** 4)
    p_cr = math.pi ** 2 * E * I / length_mm ** 2        # pinned-pinned Euler
    sf_b = float("inf") if force_N >= 0 else p_cr / abs(force_N)
    sf_s = float("inf") if abs(force_N) < 1e-9 else P.TUBE["sigma_ult_MPa"] * A / abs(force_N)
    return sf_b, sf_s


def cord_check(force_N, kind="cord"):
    cap = P.CORD["mbl_N"] * P.CORD["knot_knockdown"] if kind == "cord" else P.FABRIC["edge_strength_N"]
    return float("inf") if force_N <= 1e-9 else cap / force_N


def stub_check(payload_kg, factor):
    """Front seat post: cantilever stub in the hub socket. Returns moment, tube stress SF, socket bearing SF."""
    nodes = P.frame_nodes()
    W = payload_kg * P.G * factor
    Vf = W * P.FRONT_SHARE / 2
    slope = 4 * P.SLING_SAG_RATIO
    H = Vf / slope
    stub = np.array(nodes["FTIP_L"]) - np.array(nodes["HUB_L"])
    L = float(np.linalg.norm(stub))
    Fv = np.array([-H, 0, -Vf])
    # moment at socket mouth = |r x F| with r = stub vector
    M = float(np.linalg.norm(np.cross(stub, Fv)))          # N mm
    I = math.pi / 64 * (P.TUBE["od"] ** 4 - P.TUBE["id"] ** 4)
    sigma = M * (P.TUBE["od"] / 2) / I
    sf_tube = P.TUBE["sigma_ult_MPa"] / sigma
    socket_depth = 50.0
    bearing = M / (socket_depth * 0.6) / (P.TUBE["od"] * socket_depth / 2)  # couple over 60% of depth on half-socket area
    allow = P.PRINT["sigma_ult_datasheet_MPa"] * P.PRINT["knockdown"]
    return {"stub_len_mm": L, "moment_Nm": M / 1000, "tube_sigma_MPa": sigma, "sf_tube": sf_tube,
            "socket_bearing_MPa": bearing, "sf_socket": allow / bearing}


def run(payload_kg):
    nodes = P.frame_nodes()
    members = P.frame_members()
    out = {"payload_kg": payload_kg, "cases": {}}
    for lc_id, lc in P.LOAD_CASES.items():
        forces, react, disp, removed = solve(payload_kg, lc)
        rows = []
        worst = {"tube_sf_b": float("inf"), "tube_sf_s": float("inf"), "cord_sf": float("inf"), "fabric_sf": float("inf")}
        worst_node = max(disp, key=lambda k: float(np.linalg.norm(disp[k])))
        for name, a, b, kind in members:
            u, L = _unit(nodes[a], nodes[b])
            f = forces[name]
            if kind == "tube":
                sf_b, sf_s = tube_checks(f, L)
                worst["tube_sf_b"] = min(worst["tube_sf_b"], sf_b)
                worst["tube_sf_s"] = min(worst["tube_sf_s"], sf_s)
                rows.append((name, kind, L, f, sf_b, sf_s))
            else:
                sf = cord_check(f, kind)
                key = "cord_sf" if kind == "cord" else "fabric_sf"
                worst[key] = min(worst[key], sf)
                rows.append((name, kind, L, f, float("nan"), sf))
        dz = max(abs(v[2]) for v in disp.values())
        dmax = max(float(np.linalg.norm(v)) for v in disp.values())
        out["cases"][lc_id] = {
            "name": lc["name"], "kind": lc["kind"], "rows": rows, "removed_cords": removed,
            "max_dz_mm": dz, "max_d_mm": dmax, "mechanism": dmax > 100.0, "worst_node": worst_node,
            "reactions": {k: v.tolist() for k, v in react.items()}, "worst": worst,
        }
    out["stub_static"] = stub_check(payload_kg, 1.0)
    out["stub_dynamic"] = stub_check(payload_kg, P.LOAD_CASES["LC2"]["vert"])
    return out


def to_markdown(res):
    L = [f"### Frame truss — payload {res['payload_kg']:.0f} kg\n"]
    L.append("| Case | Kind | Max displacement (mm) | Worst tube SF (buckling) | Worst tube SF (strength) | Worst cord SF | Worst seat-edge SF | Slack tension members | Mechanism? |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for lc_id, c in res["cases"].items():
        w = c["worst"]
        L.append(f"| {lc_id} {c['name']} | {c['kind']} | {c['max_d_mm']:.1f} ({c['worst_node']}) | {w['tube_sf_b']:.1f} | {w['tube_sf_s']:.1f} | {w['cord_sf']:.1f} | {w['fabric_sf']:.1f} | {', '.join(c['removed_cords']) or '—'} | {'YES' if c['mechanism'] else 'no'} |")
    lc2 = res["cases"]["LC2"]
    L.append(f"\n#### LC2 member forces (ultimate case, {P.LOAD_CASES['LC2']['vert']} g)\n")
    L.append("| Member | Type | Length (mm) | Axial (N, + tension) | SF buckling | SF strength/cord |")
    L.append("|---|---|---|---|---|---|")
    for name, kind, ln, f, sfb, sfs in lc2["rows"]:
        sfb_s = "—" if kind == "cord" else f"{sfb:.1f}"
        L.append(f"| {name} | {kind} | {ln:.0f} | {f:+.0f} | {sfb_s} | {sfs:.1f} |")
    s = res["stub_dynamic"]
    L.append(f"\nFront seat post, bounding case with the forestay slack (pure cantilever, LC2): moment {s['moment_Nm']:.1f} N·m, tube stress {s['tube_sigma_MPa']:.0f} MPa (SF {s['sf_tube']:.1f}), socket bearing {s['socket_bearing_MPa']:.1f} MPa (SF {s['sf_socket']:.1f} on knocked-down printed strength).")
    return "\n".join(L)


if __name__ == "__main__":
    res = run(P.RATING_CLASSES[P.DEFAULT_CLASS])
    print(to_markdown(res))
