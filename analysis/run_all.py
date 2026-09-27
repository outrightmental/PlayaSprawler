"""Run every analysis for every rating class and write results/ (markdown + JSON) for docs and the site."""
import json, os, math, datetime
import ps_params as P
import frame_truss, stability, energy, flotation, axle, packing

os.makedirs("results", exist_ok=True)
summary = {"project": P.PROJECT, "version": P.VERSION, "generated": datetime.date.today().isoformat(), "classes": {}}
md = [f"# {P.PROJECT} — analysis results (v{P.VERSION}, generated {summary['generated']})\n",
      "Everything below is computed by `analysis/run_all.py` from `analysis/ps_params.py`. "
      "Re-run after any parameter change. Idealisations are stated in each script's docstring.\n"]

pk = packing.run()
md.append(packing.to_markdown(pk))
summary["packing"] = {k: v for k, v in pk.items() if k != "segments"}
summary["packing"]["segments"] = [list(s) for s in pk["segments"]]

for cls, kg in P.RATING_CLASSES.items():
    md.append(f"\n---\n\n## Rating class {cls} (payload {kg:.0f} kg)\n")
    ft = frame_truss.run(kg); md.append(frame_truss.to_markdown(ft))
    st = stability.run(kg); md.append("\n" + stability.to_markdown(st))
    en = energy.run(kg); md.append("\n" + energy.to_markdown(en))
    fl = flotation.run(kg); md.append("\n" + flotation.to_markdown(fl))
    ax = axle.run(kg); md.append("\n" + axle.to_markdown(ax))
    worst = {lc: c["worst"] for lc, c in ft["cases"].items()}
    summary["classes"][cls] = {
        "payload_kg": kg,
        "frame": {lc: {"worst": {k: (None if math.isinf(v) else round(v, 2)) for k, v in c["worst"].items()},
                       "max_d_mm": round(c["max_d_mm"], 1), "mechanism": c["mechanism"],
                       "members": {row[0]: round(row[3]) for row in c["rows"]}} for lc, c in ft["cases"].items()},
        "stability": {k: v for k, v in st.items() if k != "v_by_radius"},
        "v_by_radius": st["v_by_radius"],
        "energy": en["rows"], "axle": ax,
    }

open("results/results.md", "w").write("\n".join(md) + "\n")
json.dump(summary, open("results/results.json", "w"), indent=1, default=float)
print("\n".join(md))
