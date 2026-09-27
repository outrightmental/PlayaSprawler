# Contributing

1. Change a number in `analysis/ps_params.py`, not in a doc. Run `python analysis/run_all.py`,
   `python cad/ps_cad.py`, `python firmware/sim/psbus_sim.py --check`, `python scripts/build_site.py`.
   CI runs the same four commands on every pull request.
2. Interface changes (dock, PS-Bus messages, seat pockets) need an ADR and a new interface version.
3. Every part design that goes into a fleet needs its proof-test record (`docs/10`) attached to the PR.
4. Hardware is CERN-OHL-S v2, software Apache-2.0, documentation CC-BY-SA-4.0 (see `LICENSE.md`).
