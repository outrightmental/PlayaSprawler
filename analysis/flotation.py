"""Tire ground pressure — the flotation question that separates a beach vehicle from a playa toy."""
import math
import ps_params as P

def patch(load_N, pressure_kPa, tire_w_mm, wheel_r_mm):
    area_mm2 = load_N / (pressure_kPa * 1e-3)
    width = 0.7 * tire_w_mm
    length = area_mm2 / width
    deflection = length ** 2 / (8 * wheel_r_mm)
    return area_mm2, length, deflection

def run(payload_kg):
    vehicle_kg = sum(P.MASS_BUDGET.values()) - P.MASS_BUDGET["Bag"]
    per_wheel = (payload_kg + vehicle_kg) * P.G / 4
    rows = []
    for name, w, r in (("16 x 3.0 (baseline)", 76.0, 228.5), ("16 x 2.4 (PS-Lite)", 61.0, 213.0), ("20 x 4.0 (PS-Sand, two-bag pack)", 100.0, 254.0)):
        for p in (30.0, 40.0, 55.0):
            a, ln, d = patch(per_wheel, p, w, r)
            rows.append({"tire": name, "kPa": p, "psi": p * 0.145, "area_cm2": a / 100, "length_mm": ln, "deflection_mm": d,
                         "ok": d <= 0.22 * w})
    return {"per_wheel_N": per_wheel, "rows": rows, "target_kPa": P.SAND_PRESSURE_DRY_KPA}

def to_markdown(r):
    L = [f"### Flotation (per-wheel load {r['per_wheel_N']:.0f} N, dry-sand target ≤ {r['target_kPa']:.0f} kPa)\n",
         "| Tire | Ground pressure (kPa / psi) | Contact area (cm²) | Patch length (mm) | Tire deflection (mm) | Deflection acceptable (≤ 22% of section)? |",
         "|---|---|---|---|---|---|"]
    for x in r["rows"]:
        L.append(f"| {x['tire']} | {x['kPa']:.0f} / {x['psi']:.1f} | {x['area_cm2']:.0f} | {x['length_mm']:.0f} | {x['deflection_mm']:.0f} | {'yes' if x['ok'] else 'no — rim-out risk'} |")
    L.append("\nModel: contact pressure ≈ inflation pressure; patch width ≈ 0.7 × section width; deflection ≈ L²/8R. Beach wheelchairs run 20–30 kPa; the 16 x 3.0 baseline lands at ~40 kPa, which is workable on dry sand at crawl speed and excellent on playa. The 20 x 4.0 variant buys real dry-sand flotation at the cost of the one-bag pack.")
    return "\n".join(L)

if __name__ == "__main__":
    print(to_markdown(run(P.RATING_CLASSES[P.DEFAULT_CLASS])))
