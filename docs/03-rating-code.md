# 03 — Rating code (the safety DNA)

## Classes

| Class | Payload (rider + carried gear) | Typical use |
|---|---|---|
| PS-100 | 100 kg | lighter riders, PS-Lite wheels |
| PS-125 | 125 kg | **default** fleet build |
| PS-150 | 150 kg | heavier riders; seat-edge SF sits exactly at the 3.0 target |

A **rider class** is chosen at sign-out (rider mass + gear, rounded up). The **vehicle rating** is
the minimum class marked on any load-path part installed. Rider class ≤ vehicle rating, or the
vehicle runs in `crawl`.

## Load cases (multiples of payload weight W)

| Case | Vertical | Lateral | Backrest | Kind |
|---|---|---|---|---|
| LC1 static seated | 1.0 W | — | — | deflection check |
| LC2 dynamic vertical (bump / 150 mm drop) | 2.5 W | — | — | ultimate |
| LC3 lateral skid / turn | 1.0 W | 0.6 W | — | ultimate |
| LC5 backrest lean | 1.0 W | — | 0.5 W | ultimate |

## Allowables and safety factors

| Material | Allowable basis | Knock-down | SF |
|---|---|---|---|
| Roll-wrapped CF tube 25 × 22 | 450 MPa ultimate; Euler buckling with E = 80 GPa | — | 2.0 |
| Dyneema SK78 5 mm | MBL 18 kN | 0.5 for knots (spliced eyes preferred) | 3.0 |
| Seat fabric edge (1000D + 25 mm webbing) | 6 kN pull test | — | 3.0 |
| Printed joiner (PA12-CF / PET-CF, 100 % infill) | 80 MPa datasheet | 0.5 | 1.5 |
| Hub-motor axle (12 mm, flats) | 785 MPa yield **assumed** | verify per motor | 1.5 |

Knock-downs are applied first, then SF. Printed parts get the harshest treatment on purpose:
anisotropy, moisture, printer variance and UV are all real on the playa.

## Proof test

Before a part is marked, it is loaded to **1.5 × the LC1 load of its class** for 60 s with no
visible damage and no permanent set > 0.5 mm (`docs/10 T-5`). Proof-tested parts get a QR label:

```
PS-125 · JOINER-HUB-L · batch 2026-09-A · maker <id> · proof 2026-09-14
```

## What is a load-path part

Tubes, joiners, cords, seat canvas, wheel-module carrier, axle clamp, dock pins, control-module
mounts. Batteries, boards and lights are not — but they carry the same label format for fleet logs.

## Firmware enforcement

Every node's `hello` carries its rating. The supervisor computes
`vehicle_rating = min(rating of every live node)` and publishes it in `veh/mode`.
If `vehicle_rating < rider_class`, mode is `crawl` (2 km/h). This catches the case the label cannot:
someone swapping a PS-100 wheel module onto a PS-150 rider's vehicle in the dark. The frame's
rating (which has no node) is entered once on the B node at assembly and included in the min.

## Current margins (from `analysis/results/results.md`)

| Class | Worst tube SF (buckling) | Worst cord SF | Worst seat-edge SF | Axle SF (assumed steel) | Status |
|---|---|---|---|---|---|
| PS-100 | 13.9 | 4.7 | 4.6 | 2.4 | passes |
| PS-125 | 11.1 | 3.7 | 3.7 | 2.1 | passes |
| PS-150 | 9.2 | 3.1 | 3.0 | 1.9 | passes at the target |

Tubes are deliberately oversize (their size is set by joint bearing and stiffness, not by strength);
cords and the seat edge are the governing parts.
