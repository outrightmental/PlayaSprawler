#!/usr/bin/env python3
"""Build site/index.html from site/src/index.template.html + analysis results + CAD views.

Inlines analysis/results/results.json and cad/exports/geometry so the page works from a file://
URL and on S3 without any fetch. Copies the CAD SVG views into site/assets/.
"""
import json, os, shutil, sys, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "analysis"))
import ps_params as P

res = json.load(open(os.path.join(ROOT, "analysis", "results", "results.json")))
nodes = P.frame_nodes()
members = [{"n": m, "a": a, "b": b, "k": k} for (m, a, b, k) in P.frame_members()]
data = {
    "results": res,
    "nodes": nodes, "members": members,
    "params": {
        "version": P.VERSION, "classes": P.RATING_CLASSES, "default_class": P.DEFAULT_CLASS,
        "bag_mm": P.BAG_OUTER_MM, "bag_in": P.BAG_LINEAR_IN_MAX, "bag_lb": P.BAG_MASS_MAX_LB, "bag_kg": P.BAG_MASS_MAX_KG,
        "v_max_kmh": P.V_MAX_KMH, "wheel_od": P.WHEEL_OD_MM, "wheel_od_deflated": P.WHEEL_OD_DEFLATED_MM,
        "tire": P.TIRE_SPEC, "module_width": P.MODULE_WIDTH_MM, "track": P.TRACK_MM, "wheelbase": P.WHEELBASE_MM,
        "battery": P.BATTERY, "motor": P.MOTOR, "mass_budget": P.MASS_BUDGET, "module_breakdown": P.WHEEL_MODULE_BREAKDOWN,
        "sf": P.SF, "load_cases": P.LOAD_CASES, "comms_timeout_ms": P.COMMS_TIMEOUT_MS, "a_lat_g": P.A_LAT_MAX_G,
        "tube": P.TUBE["spec"], "cord": P.CORD["spec"], "crr": P.CRR,
    },
}
tpl = open(os.path.join(ROOT, "site", "src", "index.template.html")).read()
out = tpl.replace("/*__PS_DATA__*/null", json.dumps(data, separators=(",", ":"), default=float))
out = out.replace("/*__SCRIPT__*/", open(os.path.join(ROOT, "site", "src", "app.js")).read())
assert "/*__PS_DATA__*/" not in out and "/*__SCRIPT__*/" not in out
os.makedirs(os.path.join(ROOT, "site", "assets"), exist_ok=True)
# CadQuery's SVGs are 0.7-1.2 MB each; rasterise them for the page (SVGs stay in cad/exports)
try:
    import cairosvg
except ImportError:
    cairosvg = None
for v in ("iso", "side", "top", "front", "wheel_module"):
    src = os.path.join(ROOT, "cad", "exports", f"view_{v}.svg")
    if not os.path.exists(src):
        continue
    if cairosvg:
        cairosvg.svg2png(url=src, write_to=os.path.join(ROOT, "site", "assets", f"view_{v}.png"), output_width=1400, background_color="white")
    else:
        shutil.copy(src, os.path.join(ROOT, "site", "assets", f"view_{v}.svg"))
open(os.path.join(ROOT, "site", "index.html"), "w").write(out)
print("site/index.html built,", len(out) // 1024, "kB")
