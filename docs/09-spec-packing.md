# 09 — Packing spec (one bag, 50 lb)

**Constraint** (Burner Express, verified 2026-09): 62 linear inches and 50 lb per luggage item;
two items plus a small carry-on per ticket. E-bike batteries are accepted inside the luggage.

## Bag

660 × 450 × 450 mm soft duffel (61.4 in), padded ends, internal 640 × 430 × 430 mm.

## Layout

```
 ┌──────────────────────────────────── 640 ────────────────────────────────────┐
 │ W │ W │ W │ W │  tubes (≤376 mm, shock-corded), cords, seat, B node, controls │
 │135│135│135│135│                          100 mm slab                         │
 └────────────────────────────────────────────────────────────────────────────┘
   four wheel modules stacked axially, TIRES DEFLATED (Ø400 mm) — inflated Ø457 does not fit
   corner voids beside the stack (~32 L) take the two control modules, harness and pump
```

* Tires deflated to pack: tubeless with sealant reseats with a mini pump on site (T-11 times it).
* Longest tube segment 376 mm (legs); rails and poles split with internal shock cord.
* Seat rolled around the cords; B node in its own padded pouch.

## Mass budget (target, kg)

| Item | kg |
|---|---|
| Wheel modules × 4 | 17.40 |
| Frame tubes | 0.74 |
| Joiners + hardware | 0.90 |
| Cords + tensioners | 0.15 |
| Seat | 0.70 |
| Control modules × 2 | 0.60 |
| Bus node | 0.55 |
| Harness | 0.65 |
| Bag | 0.80 |
| **Total** | **22.49** of 22.68 (50 lb) — **+0.19 kg, +0.8 %** |

This is the binding constraint of the whole design and the margin is thin. Mitigations, in order:

1. Weigh every prototype part; the budget is a target, not a measurement.
2. PS-Lite wheels (16 × 2.4) recover ~0.8 kg.
3. Two-bag pack (allowed on one ticket): modules in one bag, everything else in the other. PS-Sand (20 × 4.0) needs this anyway.
4. Carry the B node and controls in the carry-on (9 × 10 × 17 in).
