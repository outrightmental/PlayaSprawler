"""One-bag pack: geometry fit and the 50 lb mass budget — the binding constraint of the whole design."""
import math
import ps_params as P

def tube_segments():
    """Longest members are shock-corded into two segments so nothing exceeds the bag cross-section."""
    import numpy as np
    nodes = P.frame_nodes()
    segs = []
    for name, a, b, kind in P.frame_members():
        if kind != "tube":
            continue
        L = float(np.linalg.norm(np.array(nodes[a]) - np.array(nodes[b])))
        n = math.ceil(L / (P.BAG_OUTER_MM[1] - 2 * P.BAG_WALL_MM - 10))
        segs.append((name, L, n, L / n))
    return segs

def run():
    Lb, Wb, Hb = (x - 2 * P.BAG_WALL_MM for x in P.BAG_OUTER_MM)
    linear_in = sum(P.BAG_OUTER_MM) / 25.4
    stack_len = 4 * P.MODULE_WIDTH_MM
    wheel_fits_inflated = P.WHEEL_OD_MM <= min(Wb, Hb)
    wheel_fits_deflated = P.WHEEL_OD_DEFLATED_MM <= min(Wb, Hb)
    leftover_len = Lb - stack_len
    segs = tube_segments()
    longest = max(s[3] for s in segs)
    tubes_fit = longest <= max(Wb, Hb) - 10
    # corner voids beside the wheel stack (square section minus circle), usable for small parts
    void_mm3 = (Wb * Hb - math.pi * (P.WHEEL_OD_DEFLATED_MM / 2) ** 2) * stack_len
    total = sum(P.MASS_BUDGET.values())
    margin = P.BAG_MASS_MAX_KG - total
    return {"bag_inner": (Lb, Wb, Hb), "linear_in": linear_in, "stack_len": stack_len,
            "wheel_fits_inflated": wheel_fits_inflated, "wheel_fits_deflated": wheel_fits_deflated,
            "leftover_len": leftover_len, "segments": segs, "longest_segment": longest, "tubes_fit": tubes_fit,
            "void_L": void_mm3 / 1e6, "total_kg": total, "limit_kg": P.BAG_MASS_MAX_KG, "margin_kg": margin,
            "margin_pct": margin / P.BAG_MASS_MAX_KG * 100, "ok": margin >= 0 and wheel_fits_deflated and tubes_fit and leftover_len > 60}

def to_markdown(r):
    Lb, Wb, Hb = r["bag_inner"]
    L = [f"### One-bag pack ({P.BAG_OUTER_MM[0]:.0f} × {P.BAG_OUTER_MM[1]:.0f} × {P.BAG_OUTER_MM[2]:.0f} mm duffel = {r['linear_in']:.1f} linear inches, limit {P.BAG_LINEAR_IN_MAX:.0f})\n",
         f"- Four wheel modules stacked axially: {r['stack_len']:.0f} mm of the {Lb:.0f} mm bag length; {r['leftover_len']:.0f} mm slab remains for tubes, seat, controls and bus node.",
         f"- Wheel OD {P.WHEEL_OD_MM:.0f} mm inflated: fits the {Wb:.0f} × {Hb:.0f} mm section? **{'yes' if r['wheel_fits_inflated'] else 'no'}** → pack with tires deflated ({P.WHEEL_OD_DEFLATED_MM:.0f} mm): **{'yes' if r['wheel_fits_deflated'] else 'no'}**.",
         f"- Longest tube segment {r['longest_segment']:.0f} mm (shock-corded splits below): fits crosswise? **{'yes' if r['tubes_fit'] else 'no'}**.",
         f"- Corner voids beside the wheel stack: ~{r['void_L']:.0f} L for control modules, bus node, harness, cords.",
         f"- Mass: **{r['total_kg']:.2f} kg of {r['limit_kg']:.2f} kg** ({P.BAG_MASS_MAX_LB:.0f} lb) → margin {r['margin_kg']:+.2f} kg ({r['margin_pct']:+.1f}%).\n",
         "| Mass budget item | Target (kg) |", "|---|---|"]
    for k, v in P.MASS_BUDGET.items():
        L.append(f"| {k} | {v:.2f} |")
    L.append(f"| **Total** | **{r['total_kg']:.2f}** |")
    L.append("\n| Wheel module breakdown | kg |\n|---|---|")
    for k, v in P.WHEEL_MODULE_BREAKDOWN.items():
        L.append(f"| {k} | {v:.2f} |")
    L.append(f"| **Module total** | **{sum(P.WHEEL_MODULE_BREAKDOWN.values()):.2f}** |")
    L.append("\n| Tube member | Length (mm) | Segments | Segment length (mm) |\n|---|---|---|---|")
    for name, ln, n, sl in r["segments"]:
        L.append(f"| {name} | {ln:.0f} | {n} | {sl:.0f} |")
    return "\n".join(L)

if __name__ == "__main__":
    print(to_markdown(run()))
