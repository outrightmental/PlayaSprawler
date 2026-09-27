"""Rollover geometry and the turn-rate limiter the wheel firmware must enforce."""
import math
import ps_params as P

def run(payload_kg):
    vehicle_kg = sum(P.MASS_BUDGET.values()) - P.MASS_BUDGET["Bag"]
    cg_rider = P.SEAT_PAN_Z_MM + P.RIDER_CG_ABOVE_SEAT_MM
    cg_z = (payload_kg * cg_rider + vehicle_kg * P.VEHICLE_CG_Z_MM) / (payload_kg + vehicle_kg)
    half_track = P.TRACK_MM / 2
    half_wb = P.WHEELBASE_MM / 2
    tip_lat_g = half_track / cg_z          # quasi-static lateral acceleration that lifts the inside wheels
    tip_long_g = half_wb / cg_z
    side_slope_deg = math.degrees(math.atan(tip_lat_g))
    v_max = P.V_MAX_KMH / 3.6
    a_lat = P.A_LAT_MAX_G * P.G
    r_min_at_vmax = v_max ** 2 / a_lat
    # speed allowed for a given turn radius: v = sqrt(a_lat * r)
    table = [(r, min(v_max, math.sqrt(a_lat * r))) for r in (0.5, 1.0, 1.5, 2.0, 3.0, 5.0)]
    return {
        "vehicle_kg": vehicle_kg, "cg_z_mm": cg_z, "tip_lat_g": tip_lat_g, "tip_long_g": tip_long_g,
        "side_slope_deg": side_slope_deg, "a_lat_limit_g": P.A_LAT_MAX_G,
        "margin_vs_tip": tip_lat_g / P.A_LAT_MAX_G, "r_min_at_vmax_m": r_min_at_vmax,
        "v_by_radius": table, "stop_dist_m": v_max ** 2 / (2 * P.DECEL_MAX_G * P.G),
        "yaw_rate_rule": "|omega| * |v| <= a_lat_max, omega = (vR - vL) / track",
    }

def to_markdown(r):
    L = ["### Stability and turn-rate limiter\n",
         f"Combined CG height {r['cg_z_mm']:.0f} mm; track {P.TRACK_MM:.0f} mm; wheelbase {P.WHEELBASE_MM:.0f} mm.",
         f"Quasi-static tipping threshold: {r['tip_lat_g']:.2f} g lateral ({r['side_slope_deg']:.0f}° side slope), {r['tip_long_g']:.2f} g longitudinal.",
         f"Firmware limiter target: {r['a_lat_limit_g']:.2f} g lateral (margin {r['margin_vs_tip']:.1f}x on the geometric threshold); rule `{r['yaw_rate_rule']}`.",
         f"At the {P.V_MAX_KMH:.0f} km/h cap the tightest permitted radius is {r['r_min_at_vmax_m']:.1f} m; stopping distance at {P.DECEL_MAX_G:.2f} g is {r['stop_dist_m']:.1f} m.\n",
         "| Turn radius (m) | Speed allowed (km/h) |", "|---|---|"]
    for rad, v in r["v_by_radius"]:
        L.append(f"| {rad:.1f} | {v * 3.6:.1f} |")
    return "\n".join(L)

if __name__ == "__main__":
    print(to_markdown(run(P.RATING_CLASSES[P.DEFAULT_CLASS])))
