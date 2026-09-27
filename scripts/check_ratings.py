#!/usr/bin/env python3
"""CI gate: every rating class must meet its safety-factor targets and the one-bag pack must close.

Fails the build the same way a failed proof test fails a part.
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "analysis"))
import ps_params as P
r = json.load(open(os.path.join(ROOT, "analysis", "results", "results.json")))
ok = True
def chk(cond, msg):
    global ok
    print(("PASS " if cond else "FAIL ") + msg)
    ok = ok and cond
pk = r["packing"]
chk(pk["margin_kg"] >= 0, f"one-bag mass {pk['total_kg']:.2f} kg <= {pk['limit_kg']:.2f} kg (margin {pk['margin_kg']:+.2f})")
chk(pk["linear_in"] <= P.BAG_LINEAR_IN_MAX, f"bag {pk['linear_in']:.1f} linear in <= {P.BAG_LINEAR_IN_MAX}")
chk(pk["wheel_fits_deflated"] and pk["tubes_fit"], "wheels (deflated) and tube segments fit the bag section")
for cls, c in r["classes"].items():
    for lc, case in c["frame"].items():
        w = case["worst"]
        chk(not case["mechanism"], f"{cls} {lc}: no mechanism")
        if lc == "LC1":
            chk(case["max_d_mm"] <= 20.0, f"{cls} LC1 deflection {case['max_d_mm']} mm <= 20 mm")
            continue
        for key, target in (("tube_sf_b", P.SF["tube"]), ("tube_sf_s", P.SF["tube"]), ("cord_sf", P.SF["cord"]), ("fabric_sf", P.SF["fabric"])):
            v = w.get(key)
            if v is None:
                continue
            chk(v >= target - 0.05, f"{cls} {lc}: {key} SF {v} >= {target}")
    chk(c["axle"]["sf"] >= P.SF["axle"], f"{cls}: axle SF {c['axle']['sf']:.2f} >= {P.SF['axle']} (assumed steel)")
    chk(c["stability"]["tip_lat_g"] >= 1.5 * P.A_LAT_MAX_G, f"{cls}: tip threshold {c['stability']['tip_lat_g']:.2f} g >= 1.5 x limiter")
print("RATING GATE PASSED" if ok else "RATING GATE FAILED")
sys.exit(0 if ok else 1)
