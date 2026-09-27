# 04 — Wheel module spec (interface v1)

**One part number. Four per vehicle. Any dock.**

## Interface (frozen)

| Item | Spec |
|---|---|
| Mechanical | fore/aft-symmetric T-rail on top of the carrier (stem 12 × 8 mm, head 24 × 8 mm, 120 mm long) sliding into the dock shoe; one Ø8 mm spring drop-pin captures it. Rail top = dock plane 300 mm above ground. |
| Load path | rail → shoe → printed dock joiner → legs/cords. Rated per class like every other load-path part. |
| Data | M12 D-coded female, 100BASE-TX. |
| Power/ID | M12 A-coded 4-pin female: 1 bus +, 2 bus −, 3 ID (reads dock resistor), 4 spare. Port fuse 5 A. |
| Module envelope | 135 mm wide (45 carrier + 5 gap + 76 tire + 9 nut), 457 mm OD inflated, 400 mm deflated. |
| Mass | ≤ 4.35 kg. |
| Ingress | IP54 module, IP65 connectors, mated or capped. |

## Internals (free to improve within the envelope)

| Sub-part | Baseline |
|---|---|
| Wheel | 16 × 3.0 (ISO 76-305) folding-bead tubeless tire on a 20-hole rim laced to the hub motor; sealant. |
| Motor | mini geared hub motor, 250 W nominal / 500 W peak, 20 N·m rated / 35 N·m peak, no-clutch (regen-capable) variant preferred so regen braking and hold-on-slope work. |
| Brake | regen + the gearbox's holding torque for service; a friction parking brake is not required at 8 km/h (T-8 verifies the 1.5 m stop on 10 % grade). |
| Battery | 7s1p 18650 3.4 Ah (25.2 V, 85.7 Wh, 0.41 kg) with BMS, on the inboard carrier. Fuel gauge LED. |
| Controller | FOC controller with hall + current sensing; speed control with torque limit; limits from `veh/mode`. |
| Node | small MCU with 100BASE-TX PHY (or an ESP32-class MCU + external PHY); runs the PS-Bus reference behaviour. |
| Carrier | printed "brick" 45 mm thick inboard of the wheel; aluminium torque plates clamp the axle flats; single-sided axle clamp (see caveat). |

## Behaviour

* On power-up: read ID pin → role (FL/FR/RL/RR) → side (left inverts motor sign) → subscribe.
* `ctrl/tread/<side>` at 50 Hz: `v ∈ [−1, 1]` → target speed `v × cap(mode)`; accel ≤ 0.25 g, decel ≤ 0.30 g.
* No valid command for 200 ms → ramp to zero in 300 ms and hold.
* Publish `wheel/<pos>/status` at 10 Hz (speed, SoC, temperature, fault, stop reason) and `hello` at 1 Hz (serial, rating, firmware).
* Thermal derate above 80 °C winding; cut at 95 °C.

## Analysis summary (PS-125)

| Quantity | Value |
|---|---|
| Per-wheel torque, hard playa flat / soft 10 % | 1.6 / 13.2 N·m |
| Per-wheel torque, dry loose sand 10 % | 24.7 N·m → above rated: derate speed |
| Axle bending + torque, LC2 | 368 MPa von Mises, SF 2.1 on assumed 785 MPa yield |
| Ground pressure 16 × 3.0 at 40 kPa | 90 cm² patch, 16 mm deflection — OK |

## Variants

* **PS-Lite**: 16 × 2.4 tire, −0.2 kg per module (mass margin ~5 %), poorer sand flotation.
* **PS-Sand**: 20 × 4.0 tire, 30 kPa at 30 psi-equivalent; does not fit the one-bag pack (two bags, both allowed on one ticket).

## Charging

The fleet charger is a dock: same rail, same two M12 connectors. Any module docks to charge. The
charger publishes `charger/<slot>/status` on the fleet LAN so stewards see the shelf.
