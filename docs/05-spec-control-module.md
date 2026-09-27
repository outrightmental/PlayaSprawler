# 05 — Control module spec (interface v1)

**Two per vehicle: CL and CR. Any input form. Same message.**

## Interface (frozen)

| Item | Spec |
|---|---|
| Mechanical | 25 mm tube clamp onto the front control rail (CTRL_RAIL) or the seat rail; one lever bolt. Position is adjustable along the rail. |
| Data / Power-ID | the same M12 D-coded + M12 A-coded pair as every port. The dock ID says CL or CR. |
| Message | `ctrl/tread/<side>` at 50 Hz: `{ "v": -1.0..1.0, "seq": n, "src": serial, "input": "lever|pedal|..." }` |
| Zero | mechanical return-to-centre; firmware dead-band ≥ 5 %. |
| Mass | ≤ 0.30 kg. |

## Input forms (all valid)

| Form | Who | Notes |
|---|---|---|
| Hand lever (fore/aft) | most riders | spring-centred, 30° travel |
| Foot pedal (rocker) | riders without the use of one hand | heel-toe rocker, 20° travel |
| Joystick half (one axis) | one-handed riders using two stacked modules | two modules on one rail clamp |
| Sip-puff / switch pairs | as needed | publishes ±0.6 steps with ramping |

The sketch's example — a rider missing the left leg and the right arm — uses a **left lever** and a
**right pedal**. The wheels cannot tell. The simulator (`firmware/sim/psbus_sim.py`) runs exactly
this configuration.

## Behaviour

* Publish at 50 Hz regardless of change (the wheels use the stream as a heartbeat).
* `seq` increments; wheels ignore out-of-order messages.
* If the module's own sensor faults, it publishes `v = 0` with `"fault": true` rather than going silent, so the vehicle stops smoothly instead of by timeout.
* Optional haptic/LED shows `veh/mode` (run / crawl / stop).

## Turn-rate limiter (lives in the wheels, fed by both controls)

Each wheel knows both sides' commands (both are on the bus). Before applying its own target it
scales both symmetrically so that `|ω|·|v| ≤ 0.25 g` with `ω = (vR − vL)/track`. Result at 8 km/h:
minimum radius 2.0 m; at 1 m radius the cap is 5.6 km/h.
