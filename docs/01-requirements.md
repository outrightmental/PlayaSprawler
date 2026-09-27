# 01 — Requirements

Verification: **A** analysis · **T** test · **I** inspection · **D** demonstration. Numbers in
parentheses are the current design values from `analysis/results/results.md`.

## 1. Transport — one bag on the Burner Express

| ID | Requirement | V |
|---|---|---|
| REQ-010 | The complete vehicle, disassembled, fits in one soft bag ≤ 62 linear inches (chosen 660 × 450 × 450 mm = 61.4 in). | I |
| REQ-011 | Bag mass including the bag ≤ 50 lb / 22.68 kg (budget 22.49 kg, +0.19 kg margin). | T |
| REQ-012 | Packing and unpacking each take ≤ 15 min by one person without tools. | D |
| REQ-013 | Lithium cells travel inside the wheel modules; packs are ≤ 100 Wh each (85.7 Wh) and carry a state-of-charge indicator. | I |

## 2. Wheel module

| ID | Requirement | V |
|---|---|---|
| REQ-020 | All four wheel modules are identical and interchangeable in any dock without adjustment or configuration. | D |
| REQ-021 | A module can be exchanged in ≤ 60 s with the rider seated (one latch, no tools). | T |
| REQ-022 | Each module contains motor, gearbox, brake, controller, battery and network node; traction current never crosses the dock. | I |
| REQ-023 | Continuous drawbar per module ≥ 60 N at 8 km/h (soft playa 10 % grade needs 230 N total). | A/T |
| REQ-024 | Module mass ≤ 4.35 kg. | T |

## 3. Control module

| ID | Requirement | V |
|---|---|---|
| REQ-030 | Two control modules, one per side (CL, CR). Each publishes one normalised tread command `v ∈ [−1, +1]` at 50 Hz. | D |
| REQ-031 | Any input form (lever, pedal, joystick axis, sip-puff…) is a valid control module; the vehicle cannot tell them apart. | D |
| REQ-032 | A control module is hot-swappable; loss of one side stops that side within 200 ms + 300 ms ramp. | T |
| REQ-033 | Inputs have a mechanical or firmware dead-band ≥ 5 % around zero and return to zero when released. | T |

## 4. Network and power

| ID | Requirement | V |
|---|---|---|
| REQ-040 | Signals travel only over 100BASE-TX Ethernet on M12 D-coded connectors; no other signal wiring exists. | I |
| REQ-041 | Every node is a UDP-multicast pub/sub peer; there is no master for control messages. | D |
| REQ-042 | A node learns its role from the dock ID pin (geographic addressing); no per-node configuration. | D |
| REQ-043 | Primary power is a separate SELV bus (21–29.4 V) on M12 A-coded connectors, per-port limited to 5 A. | I/T |
| REQ-044 | Wheel nodes stop if no valid command arrives within 200 ms; all nodes stop on `veh/estop`. | T |
| REQ-045 | Losing the bus node (switch) is a safe state: all wheels stop. | T |

## 5. Structure and rating

| ID | Requirement | V |
|---|---|---|
| REQ-050 | Every vehicle carries a rating class PS-100 / PS-125 / PS-150 (payload kg). | I |
| REQ-051 | Every load-path part is rated and marked; vehicle rating = min(part ratings). | I |
| REQ-052 | Load cases LC1 (1.0 g static), LC2 (2.5 g vertical), LC3 (1.0 g + 0.6 g lateral), LC5 (0.5 W backrest) with SF tube 2.0, cord 3.0, fabric 3.0, print 1.5 on knocked-down allowables. | A |
| REQ-053 | Every load-path part passes a 1.5 × static proof load before marking. | T |
| REQ-054 | Static seated deflection at the rear tips ≤ 20 mm at class payload (15.5 mm at PS-125). | A/T |
| REQ-055 | No mechanism: the frame is kinematically stable in every load case with the seat installed. | A |
| REQ-056 | Printed parts use CF-filled nylon or PET with 100 % infill in load regions; datasheet strength knocked down by 0.5. | I |

## 6. Mobility and terrain

| ID | Requirement | V |
|---|---|---|
| REQ-060 | Speed cap 8 km/h (BRC 5 mph) in `run`; 2 km/h in `crawl`. | T |
| REQ-061 | Firmware turn-rate limiter `|ω|·|v| ≤ 0.25 g` (tip threshold 0.49 g). | A/T |
| REQ-062 | Range ≥ 15 km on hard playa at class payload (23 km predicted). | A/T |
| REQ-063 | Ground pressure ≤ 40 kPa at class payload for dry sand; 20 × 4.0 variant ≤ 30 kPa. | A/T |

## 7. Fleet

| ID | Requirement | V |
|---|---|---|
| REQ-070 | A fleet charger accepts any wheel module through the standard dock connector. | D |
| REQ-071 | Every part carries a QR label: class · part · batch · maker · proof date. | I |
| REQ-072 | The supervisor logs hello/rating records so a fleet steward can audit what was on which vehicle. | D |

## 8. Regulatory

| ID | Requirement | V |
|---|---|---|
| REQ-080 | The vehicle is designed and documented as a powered mobility device (ISO 7176 / EN 12184 reference); it is not a scooter or golf cart. | I |
| REQ-081 | Lights: white front, red rear, side marker at night per BRC vehicle policy. | I |
| REQ-082 | Riders check current BRC Accessibility Vehicle and GGNRA Ocean Beach rules before use (see `docs/12`). | I |
