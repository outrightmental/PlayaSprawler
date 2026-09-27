# ADR-001 — The wheel module is the battery

Status: accepted · 2026-09

**Context.** The sketch shows one box with battery, motor, gearbox, brake and electronics, "4× redundant unit". A central pack would be lighter per Wh and simpler to charge, but it puts traction current through the docks and makes the module depend on the frame.

**Decision.** Each wheel module carries its own 7s1p pack (85.7 Wh). The vehicle power bus runs at pack voltage; modules feed it through ideal diodes and take charge through a current limit. Traction current never crosses a dock.

**Consequences.** Docks carry ≤ 5 A and can be cheap M12 connectors. A module is a complete, testable, chargeable unit — the fleet rack is just docks. Packs stay under 100 Wh, which simplifies transport. Cost: four BMSs instead of one, ~0.4 kg of extra enclosure, and per-pack imbalance managed by the charge limiter.

**Rejected.** Central pack in the B node (traction over docks, single point of failure); swappable central pack (heavier dock, no per-module test).
