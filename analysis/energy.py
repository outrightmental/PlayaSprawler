"""Traction power, torque and range on the four surfaces the vehicle is built for."""
import ps_params as P

def run(payload_kg):
    vehicle_kg = sum(P.MASS_BUDGET.values()) - P.MASS_BUDGET["Bag"]
    m = payload_kg + vehicle_kg
    v = P.V_MAX_KMH / 3.6
    e_usable = 4 * P.BATTERY["wh"] * P.BATTERY["usable_frac"]
    rows = []
    for name, crr in P.CRR.items():
        for grade in (0.0, P.GRADE_MAX):
            F = m * P.G * (crr + grade)
            p_mech = F * v
            p_el = p_mech / P.DRIVE_EFF + P.AUX_W
            per_wheel_W = p_mech / 4 / P.DRIVE_EFF
            torque = F / 4 * (P.WHEEL_R_MM / 1000)
            hours = e_usable / p_el
            rows.append({"surface": name, "grade": grade, "F_N": F, "p_el_W": p_el,
                         "per_wheel_W": per_wheel_W, "torque_Nm": torque,
                         "range_km": hours * P.V_MAX_KMH, "hours": hours,
                         "torque_ok": torque <= P.MOTOR["torque_rated_Nm"],
                         "power_ok": per_wheel_W <= P.MOTOR["nominal_W"]})
    return {"gross_kg": m, "e_usable_wh": e_usable, "rows": rows}

def to_markdown(r):
    L = [f"### Traction, torque and range (gross mass {r['gross_kg']:.0f} kg, usable energy {r['e_usable_wh']:.0f} Wh, {P.V_MAX_KMH:.0f} km/h)\n",
         "| Surface | Grade | Drawbar force (N) | Electrical power (W) | Per-wheel motor load (W) | Per-wheel torque (N·m) | Range (km) | Within motor rating? |",
         "|---|---|---|---|---|---|---|---|"]
    for x in r["rows"]:
        ok = "yes" if (x["torque_ok"] and x["power_ok"]) else ("torque" if not x["torque_ok"] else "power") + " limit — derate speed"
        L.append(f"| {x['surface']} | {x['grade']*100:.0f}% | {x['F_N']:.0f} | {x['p_el_W']:.0f} | {x['per_wheel_W']:.0f} | {x['torque_Nm']:.1f} | {x['range_km']:.1f} | {ok} |")
    L.append(f"\nMotor basis: {P.MOTOR['type']}, {P.MOTOR['nominal_W']:.0f} W nominal / {P.MOTOR['peak_W']:.0f} W peak, {P.MOTOR['torque_rated_Nm']:.0f} N·m rated / {P.MOTOR['torque_peak_Nm']:.0f} N·m peak. Drive efficiency {P.DRIVE_EFF:.2f} assumed at low speed; verify on the dynamometer test.")
    return "\n".join(L)

if __name__ == "__main__":
    print(to_markdown(run(P.RATING_CLASSES[P.DEFAULT_CLASS])))
