# 08 — Seat spec (the personal part)

The seat is one piece of canvas with **four corner pockets** that slip over the domed pegs on the
two front tips and two rear tips — exactly like the REI camp chair the sketch came from. It is the
only part that is never swapped, so it is the part people decorate. It is also structural.

## Structure

| Element | Spec | Rating role |
|---|---|---|
| Body | 1000D Cordura or 600D polyester, UV-stable; 2 layers in the sling | carries the rider (SLING_F/R, SEAT_CROSS) |
| Side straps | 25 mm tubular nylon webbing sewn full length FTIP→RTIP both sides, bar-tacked at the pockets | SIDE_STRAP (fabric member, 479 N at LC2) |
| Front edge | webbing FTIP→FTIP | SEAT_FRONT_EDGE |
| Corner pockets | double-layer cups, Ø32 mm × 70 mm deep, webbing loop through each | transfer 1.6 kN (rear, LC2) into the pegs |
| Edge strength | ≥ 6 kN pull test on the finished edge (T-4) | SF 3.0 at PS-150 |

The pattern is in `seat/seat-pattern.svg` (flat, with seam allowances). Sew with bonded nylon #92
or #138. Every finished seat is proof-loaded (T-5) and labelled with its class like a joiner.

## Decoration rules (so the art never compromises the rating)

1. Paint, dye, patches, LEDs: anything on the **face** of the body panel is free.
2. Do not cut, burn or sew through the side straps, the front-edge webbing or the pockets.
3. Added mass on the seat counts toward the payload, not the vehicle; keep lights on the L bus with
   an M12 AUX port rather than a separate battery.
4. Dust cover: the seat comes off in 20 s — take it inside at night.

## Geometry

Chord FTIP→RTIP 447 mm at 27° rake; sag ratio 0.33 (150 mm) sets the sling angle and therefore
the horizontal pull on the tips; front share of seated weight 0.45. Changing the sag changes the
loads — re-run `analysis/run_all.py` after any pattern change (`SEAT_SAG_MM`).
