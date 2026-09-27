# Playa Sprawler — analysis results (v0.1.0, generated 2026-09-08)

Everything below is computed by `analysis/run_all.py` from `analysis/ps_params.py`. Re-run after any parameter change. Idealisations are stated in each script's docstring.

### One-bag pack (660 × 450 × 450 mm duffel = 61.4 linear inches, limit 62)

- Four wheel modules stacked axially: 540 mm of the 640 mm bag length; 100 mm slab remains for tubes, seat, controls and bus node.
- Wheel OD 457 mm inflated: fits the 430 × 430 mm section? **no** → pack with tires deflated (400 mm): **yes**.
- Longest tube segment 376 mm (shock-corded splits below): fits crosswise? **yes**.
- Corner voids beside the wheel stack: ~32 L for control modules, bus node, harness, cords.
- Mass: **22.49 kg of 22.68 kg** (50 lb) → margin +0.19 kg (+0.8%).

| Mass budget item | Target (kg) |
|---|---|
| Wheel module (x4) | 17.40 |
| Frame tubes (carbon) | 0.74 |
| Joiners (printed) + hardware | 0.90 |
| Cords + tensioners | 0.15 |
| Seat canvas | 0.70 |
| Control modules (x2) | 0.60 |
| Bus node (switch + supervisor + power) | 0.55 |
| Harness (M12 data + power) | 0.65 |
| Bag | 0.80 |
| **Total** | **22.49** |

| Wheel module breakdown | kg |
|---|---|
| hub motor | 1.90 |
| rim + spokes | 0.62 |
| tire (tubeless) + sealant | 0.80 |
| battery pack | 0.41 |
| controller + node board | 0.15 |
| carrier (printed + Al torque plates) | 0.35 |
| connectors + fasteners | 0.10 |
| **Module total** | **4.33** |

| Tube member | Length (mm) | Segments | Segment length (mm) |
|---|---|---|---|
| SEAT_RAIL | 360 | 1 | 360 |
| CTRL_RAIL | 560 | 2 | 280 |
| TOP_RAIL | 460 | 2 | 230 |
| LEG_FL | 376 | 1 | 376 |
| LEG_RL | 376 | 1 | 376 |
| POLE_L | 491 | 2 | 245 |
| POST_L | 162 | 1 | 162 |
| LEG_FR | 376 | 1 | 376 |
| LEG_RR | 376 | 1 | 376 |
| POLE_R | 491 | 2 | 245 |
| POST_R | 162 | 1 | 162 |

---

## Rating class PS-100 (payload 100 kg)

### Frame truss — payload 100 kg

| Case | Kind | Max displacement (mm) | Worst tube SF (buckling) | Worst tube SF (strength) | Worst cord SF | Worst seat-edge SF | Slack tension members | Mechanism? |
|---|---|---|---|---|---|---|---|---|
| LC1 Static seated | deflection | 12.4 (RTIP_R) | 34.7 | 40.3 | 11.7 | 11.4 | XF_1, BACKSTAY_L, AFTSTAY_R | no |
| LC2 Dynamic vertical (bump/drop) | ultimate | 31.0 (RTIP_R) | 13.9 | 16.1 | 4.7 | 4.6 | XF_1, BACKSTAY_L, AFTSTAY_R | no |
| LC3 Lateral skid / turn | ultimate | 42.4 (RTIP_L) | 15.7 | 18.3 | 6.0 | 7.1 | XF_1, XR_1, XR_2, AFTSTAY_L, BACKSTAY_R | no |
| LC5 Backrest lean | ultimate | 26.6 (RTIP_R) | 22.9 | 26.6 | 8.2 | 8.7 | XF_2, AFTSTAY_R, BACKSTAY_R | no |

#### LC2 member forces (ultimate case, 2.5 g)

| Member | Type | Length (mm) | Axial (N, + tension) | SF buckling | SF strength/cord |
|---|---|---|---|---|---|
| SEAT_RAIL | tube | 360 | -1614 | 29.0 | 30.9 |
| CTRL_RAIL | tube | 560 | +529 | inf | 94.2 |
| TOP_RAIL | tube | 460 | +26 | inf | 1950.7 |
| SEAT_CROSS | fabric | 410 | +0 | nan | 17322670070.7 |
| SEAT_FRONT_EDGE | fabric | 360 | +438 | nan | 13.7 |
| REAR_CORD | cord | 560 | +557 | — | 16.2 |
| XF_1 | cord | 586 | +0 | — | inf |
| XF_2 | cord | 586 | +0 | — | 198986624.5 |
| XR_1 | cord | 586 | +41 | — | 220.0 |
| XR_2 | cord | 586 | +41 | — | 220.0 |
| LEG_FL | tube | 376 | -3092 | 13.9 | 16.1 |
| LEG_RL | tube | 376 | -2215 | 19.3 | 22.5 |
| POLE_L | tube | 491 | -1671 | 15.1 | 29.8 |
| POST_L | tube | 162 | -985 | 235.8 | 50.6 |
| SIDE_CORD_L | cord | 660 | +1921 | — | 4.7 |
| FORESTAY_L | cord | 416 | +1220 | — | 7.4 |
| AFTSTAY_L | cord | 502 | -0 | — | inf |
| BACKSTAY_L | cord | 714 | +0 | — | inf |
| SIDE_STRAP_L | fabric | 450 | +383 | nan | 15.7 |
| SLING_FL | fabric | 208 | +849 | nan | 7.1 |
| SLING_RL | fabric | 321 | +1313 | nan | 4.6 |
| LEG_FR | tube | 376 | -3092 | 13.9 | 16.1 |
| LEG_RR | tube | 376 | -2215 | 19.3 | 22.5 |
| POLE_R | tube | 491 | -1671 | 15.1 | 29.8 |
| POST_R | tube | 162 | -985 | 235.8 | 50.6 |
| SIDE_CORD_R | cord | 660 | +1921 | — | 4.7 |
| FORESTAY_R | cord | 416 | +1220 | — | 7.4 |
| AFTSTAY_R | cord | 502 | +0 | — | inf |
| BACKSTAY_R | cord | 714 | -0 | — | inf |
| SIDE_STRAP_R | fabric | 450 | +383 | nan | 15.7 |
| SLING_FR | fabric | 208 | +849 | nan | 7.1 |
| SLING_RR | fabric | 321 | +1313 | nan | 4.6 |

Front seat post, bounding case with the forestay slack (pure cantilever, LC2): moment 29.6 N·m, tube stress 48 MPa (SF 9.3), socket bearing 1.6 MPa (SF 25.3 on knocked-down printed strength).

### Stability and turn-rate limiter

Combined CG height 694 mm; track 691 mm; wheelbase 660 mm.
Quasi-static tipping threshold: 0.50 g lateral (26° side slope), 0.48 g longitudinal.
Firmware limiter target: 0.25 g lateral (margin 2.0x on the geometric threshold); rule `|omega| * |v| <= a_lat_max, omega = (vR - vL) / track`.
At the 8 km/h cap the tightest permitted radius is 2.0 m; stopping distance at 0.30 g is 0.8 m.

| Turn radius (m) | Speed allowed (km/h) |
|---|---|
| 0.5 | 4.0 |
| 1.0 | 5.6 |
| 1.5 | 6.9 |
| 2.0 | 8.0 |
| 3.0 | 8.0 |
| 5.0 | 8.0 |

### Traction, torque and range (gross mass 122 kg, usable energy 291 Wh, 8 km/h)

| Surface | Grade | Drawbar force (N) | Electrical power (W) | Per-wheel motor load (W) | Per-wheel torque (N·m) | Range (km) | Within motor rating? |
|---|---|---|---|---|---|---|---|
| playa, hard | 0% | 24 | 86 | 19 | 1.4 | 27.2 | yes |
| playa, hard | 10% | 143 | 465 | 114 | 8.2 | 5.0 | yes |
| playa, soft/dusty | 0% | 72 | 237 | 57 | 4.1 | 9.8 | yes |
| playa, soft/dusty | 10% | 191 | 616 | 152 | 10.9 | 3.8 | yes |
| beach, wet firm | 0% | 60 | 199 | 47 | 3.4 | 11.7 | yes |
| beach, wet firm | 10% | 179 | 578 | 142 | 10.2 | 4.0 | yes |
| beach, dry loose | 0% | 239 | 768 | 189 | 13.6 | 3.0 | yes |
| beach, dry loose | 10% | 358 | 1147 | 284 | 20.5 | 2.0 | torque limit — derate speed |

Motor basis: mini geared hub motor, no-clutch (regen-capable) variant preferred, 250 W nominal / 500 W peak, 20 N·m rated / 35 N·m peak. Drive efficiency 0.70 assumed at low speed; verify on the dynamometer test.

### Flotation (per-wheel load 298 N, dry-sand target ≤ 40 kPa)

| Tire | Ground pressure (kPa / psi) | Contact area (cm²) | Patch length (mm) | Tire deflection (mm) | Deflection acceptable (≤ 22% of section)? |
|---|---|---|---|---|---|
| 16 x 3.0 (baseline) | 30 / 4.3 | 99 | 187 | 19 | no — rim-out risk |
| 16 x 3.0 (baseline) | 40 / 5.8 | 75 | 140 | 11 | yes |
| 16 x 3.0 (baseline) | 55 / 8.0 | 54 | 102 | 6 | yes |
| 16 x 2.4 (PS-Lite) | 30 / 4.3 | 99 | 233 | 32 | no — rim-out risk |
| 16 x 2.4 (PS-Lite) | 40 / 5.8 | 75 | 175 | 18 | no — rim-out risk |
| 16 x 2.4 (PS-Lite) | 55 / 8.0 | 54 | 127 | 9 | yes |
| 20 x 4.0 (PS-Sand, two-bag pack) | 30 / 4.3 | 99 | 142 | 10 | yes |
| 20 x 4.0 (PS-Sand, two-bag pack) | 40 / 5.8 | 75 | 107 | 6 | yes |
| 20 x 4.0 (PS-Sand, two-bag pack) | 55 / 8.0 | 54 | 78 | 3 | yes |

Model: contact pressure ≈ inflation pressure; patch width ≈ 0.7 × section width; deflection ≈ L²/8R. Beach wheelchairs run 20–30 kPa; the 16 x 3.0 baseline lands at ~40 kPa, which is workable on dry sand at crawl speed and excellent on playa. The 20 x 4.0 variant buys real dry-sand flotation at the cost of the one-bag pack.

### Wheel-module axle, cantilever check (LC2, 2.5 g)

Sprung load per wheel 639 N at 45 mm cantilever → bending 28.8 N·m plus peak motor torque 35 N·m.
Bending stress 226 MPa, shear 138 MPa, von Mises 328 MPa on a 12 mm axle with 10 mm flats.
Safety factor 2.39 against an assumed yield of 785 MPa (target 1.5). **The axle steel grade must be verified per motor model; if it cannot be, the module carrier must support the axle on both sides.**

---

## Rating class PS-125 (payload 125 kg)

### Frame truss — payload 125 kg

| Case | Kind | Max displacement (mm) | Worst tube SF (buckling) | Worst tube SF (strength) | Worst cord SF | Worst seat-edge SF | Slack tension members | Mechanism? |
|---|---|---|---|---|---|---|---|---|
| LC1 Static seated | deflection | 15.5 (RTIP_R) | 27.7 | 32.2 | 9.4 | 9.1 | XF_1, BACKSTAY_L, AFTSTAY_R | no |
| LC2 Dynamic vertical (bump/drop) | ultimate | 38.8 (RTIP_R) | 11.1 | 12.9 | 3.7 | 3.7 | XF_1, BACKSTAY_L, AFTSTAY_R | no |
| LC3 Lateral skid / turn | ultimate | 53.0 (RTIP_L) | 12.6 | 14.6 | 4.8 | 5.7 | XF_1, XR_1, XR_2, AFTSTAY_L, BACKSTAY_R | no |
| LC5 Backrest lean | ultimate | 33.2 (RTIP_R) | 18.3 | 21.3 | 6.6 | 7.0 | XF_2, AFTSTAY_R, BACKSTAY_R | no |

#### LC2 member forces (ultimate case, 2.5 g)

| Member | Type | Length (mm) | Axial (N, + tension) | SF buckling | SF strength/cord |
|---|---|---|---|---|---|
| SEAT_RAIL | tube | 360 | -2017 | 23.2 | 24.7 |
| CTRL_RAIL | tube | 560 | +661 | inf | 75.4 |
| TOP_RAIL | tube | 460 | +32 | inf | 1560.5 |
| SEAT_CROSS | fabric | 410 | +0 | nan | 13858136251.6 |
| SEAT_FRONT_EDGE | fabric | 360 | +548 | nan | 11.0 |
| REAR_CORD | cord | 560 | +696 | — | 12.9 |
| XF_1 | cord | 586 | +0 | — | inf |
| XF_2 | cord | 586 | +0 | — | 159189319.8 |
| XR_1 | cord | 586 | +51 | — | 176.0 |
| XR_2 | cord | 586 | +51 | — | 176.0 |
| LEG_FL | tube | 376 | -3865 | 11.1 | 12.9 |
| LEG_RL | tube | 376 | -2769 | 15.5 | 18.0 |
| POLE_L | tube | 491 | -2088 | 12.1 | 23.9 |
| POST_L | tube | 162 | -1231 | 188.6 | 40.5 |
| SIDE_CORD_L | cord | 660 | +2401 | — | 3.7 |
| FORESTAY_L | cord | 416 | +1525 | — | 5.9 |
| AFTSTAY_L | cord | 502 | -0 | — | inf |
| BACKSTAY_L | cord | 714 | +0 | — | inf |
| SIDE_STRAP_L | fabric | 450 | +479 | nan | 12.5 |
| SLING_FL | fabric | 208 | +1061 | nan | 5.7 |
| SLING_RL | fabric | 321 | +1641 | nan | 3.7 |
| LEG_FR | tube | 376 | -3865 | 11.1 | 12.9 |
| LEG_RR | tube | 376 | -2769 | 15.5 | 18.0 |
| POLE_R | tube | 491 | -2088 | 12.1 | 23.9 |
| POST_R | tube | 162 | -1231 | 188.6 | 40.5 |
| SIDE_CORD_R | cord | 660 | +2401 | — | 3.7 |
| FORESTAY_R | cord | 416 | +1525 | — | 5.9 |
| AFTSTAY_R | cord | 502 | +0 | — | inf |
| BACKSTAY_R | cord | 714 | -0 | — | inf |
| SIDE_STRAP_R | fabric | 450 | +479 | nan | 12.5 |
| SLING_FR | fabric | 208 | +1061 | nan | 5.7 |
| SLING_RR | fabric | 321 | +1641 | nan | 3.7 |

Front seat post, bounding case with the forestay slack (pure cantilever, LC2): moment 37.0 N·m, tube stress 60 MPa (SF 7.5), socket bearing 2.0 MPa (SF 20.3 on knocked-down printed strength).

### Stability and turn-rate limiter

Combined CG height 709 mm; track 691 mm; wheelbase 660 mm.
Quasi-static tipping threshold: 0.49 g lateral (26° side slope), 0.47 g longitudinal.
Firmware limiter target: 0.25 g lateral (margin 1.9x on the geometric threshold); rule `|omega| * |v| <= a_lat_max, omega = (vR - vL) / track`.
At the 8 km/h cap the tightest permitted radius is 2.0 m; stopping distance at 0.30 g is 0.8 m.

| Turn radius (m) | Speed allowed (km/h) |
|---|---|
| 0.5 | 4.0 |
| 1.0 | 5.6 |
| 1.5 | 6.9 |
| 2.0 | 8.0 |
| 3.0 | 8.0 |
| 5.0 | 8.0 |

### Traction, torque and range (gross mass 147 kg, usable energy 291 Wh, 8 km/h)

| Surface | Grade | Drawbar force (N) | Electrical power (W) | Per-wheel motor load (W) | Per-wheel torque (N·m) | Range (km) | Within motor rating? |
|---|---|---|---|---|---|---|---|
| playa, hard | 0% | 29 | 101 | 23 | 1.6 | 23.0 | yes |
| playa, hard | 10% | 173 | 558 | 137 | 9.9 | 4.2 | yes |
| playa, soft/dusty | 0% | 86 | 284 | 69 | 4.9 | 8.2 | yes |
| playa, soft/dusty | 10% | 230 | 741 | 183 | 13.2 | 3.1 | yes |
| beach, wet firm | 0% | 72 | 238 | 57 | 4.1 | 9.8 | yes |
| beach, wet firm | 10% | 216 | 695 | 171 | 12.3 | 3.4 | yes |
| beach, dry loose | 0% | 288 | 924 | 228 | 16.4 | 2.5 | yes |
| beach, dry loose | 10% | 432 | 1381 | 343 | 24.7 | 1.7 | torque limit — derate speed |

Motor basis: mini geared hub motor, no-clutch (regen-capable) variant preferred, 250 W nominal / 500 W peak, 20 N·m rated / 35 N·m peak. Drive efficiency 0.70 assumed at low speed; verify on the dynamometer test.

### Flotation (per-wheel load 360 N, dry-sand target ≤ 40 kPa)

| Tire | Ground pressure (kPa / psi) | Contact area (cm²) | Patch length (mm) | Tire deflection (mm) | Deflection acceptable (≤ 22% of section)? |
|---|---|---|---|---|---|
| 16 x 3.0 (baseline) | 30 / 4.3 | 120 | 225 | 28 | no — rim-out risk |
| 16 x 3.0 (baseline) | 40 / 5.8 | 90 | 169 | 16 | yes |
| 16 x 3.0 (baseline) | 55 / 8.0 | 65 | 123 | 8 | yes |
| 16 x 2.4 (PS-Lite) | 30 / 4.3 | 120 | 281 | 46 | no — rim-out risk |
| 16 x 2.4 (PS-Lite) | 40 / 5.8 | 90 | 211 | 26 | no — rim-out risk |
| 16 x 2.4 (PS-Lite) | 55 / 8.0 | 65 | 153 | 14 | no — rim-out risk |
| 20 x 4.0 (PS-Sand, two-bag pack) | 30 / 4.3 | 120 | 171 | 14 | yes |
| 20 x 4.0 (PS-Sand, two-bag pack) | 40 / 5.8 | 90 | 128 | 8 | yes |
| 20 x 4.0 (PS-Sand, two-bag pack) | 55 / 8.0 | 65 | 93 | 4 | yes |

Model: contact pressure ≈ inflation pressure; patch width ≈ 0.7 × section width; deflection ≈ L²/8R. Beach wheelchairs run 20–30 kPa; the 16 x 3.0 baseline lands at ~40 kPa, which is workable on dry sand at crawl speed and excellent on playa. The 20 x 4.0 variant buys real dry-sand flotation at the cost of the one-bag pack.

### Wheel-module axle, cantilever check (LC2, 2.5 g)

Sprung load per wheel 793 N at 45 mm cantilever → bending 35.7 N·m plus peak motor torque 35 N·m.
Bending stress 280 MPa, shear 138 MPa, von Mises 368 MPa on a 12 mm axle with 10 mm flats.
Safety factor 2.13 against an assumed yield of 785 MPa (target 1.5). **The axle steel grade must be verified per motor model; if it cannot be, the module carrier must support the axle on both sides.**

---

## Rating class PS-150 (payload 150 kg)

### Frame truss — payload 150 kg

| Case | Kind | Max displacement (mm) | Worst tube SF (buckling) | Worst tube SF (strength) | Worst cord SF | Worst seat-edge SF | Slack tension members | Mechanism? |
|---|---|---|---|---|---|---|---|---|
| LC1 Static seated | deflection | 18.6 (RTIP_R) | 23.1 | 26.9 | 7.8 | 7.6 | XF_1, BACKSTAY_L, AFTSTAY_R | no |
| LC2 Dynamic vertical (bump/drop) | ultimate | 46.5 (RTIP_R) | 9.2 | 10.7 | 3.1 | 3.0 | XF_1, BACKSTAY_L, AFTSTAY_R | no |
| LC3 Lateral skid / turn | ultimate | 63.7 (RTIP_L) | 10.5 | 12.2 | 4.0 | 4.7 | XF_1, XR_1, XR_2, AFTSTAY_L, BACKSTAY_R | no |
| LC5 Backrest lean | ultimate | 39.9 (RTIP_R) | 15.2 | 17.7 | 5.5 | 5.8 | XF_2, AFTSTAY_R, BACKSTAY_R | no |

#### LC2 member forces (ultimate case, 2.5 g)

| Member | Type | Length (mm) | Axial (N, + tension) | SF buckling | SF strength/cord |
|---|---|---|---|---|---|
| SEAT_RAIL | tube | 360 | -2421 | 19.3 | 20.6 |
| CTRL_RAIL | tube | 560 | +793 | inf | 62.8 |
| TOP_RAIL | tube | 460 | +38 | inf | 1300.4 |
| SEAT_CROSS | fabric | 410 | +0 | nan | 11548446804.1 |
| SEAT_FRONT_EDGE | fabric | 360 | +657 | nan | 9.1 |
| REAR_CORD | cord | 560 | +836 | — | 10.8 |
| XF_1 | cord | 586 | +0 | — | inf |
| XF_2 | cord | 586 | +0 | — | 132657761.9 |
| XR_1 | cord | 586 | +61 | — | 146.7 |
| XR_2 | cord | 586 | +61 | — | 146.7 |
| LEG_FL | tube | 376 | -4638 | 9.2 | 10.7 |
| LEG_RL | tube | 376 | -3323 | 12.9 | 15.0 |
| POLE_L | tube | 491 | -2506 | 10.1 | 19.9 |
| POST_L | tube | 162 | -1477 | 157.2 | 33.7 |
| SIDE_CORD_L | cord | 660 | +2882 | — | 3.1 |
| FORESTAY_L | cord | 416 | +1830 | — | 4.9 |
| AFTSTAY_L | cord | 502 | -0 | — | inf |
| BACKSTAY_L | cord | 714 | +0 | — | inf |
| SIDE_STRAP_L | fabric | 450 | +575 | nan | 10.4 |
| SLING_FL | fabric | 208 | +1273 | nan | 4.7 |
| SLING_RL | fabric | 321 | +1969 | nan | 3.0 |
| LEG_FR | tube | 376 | -4638 | 9.2 | 10.7 |
| LEG_RR | tube | 376 | -3323 | 12.9 | 15.0 |
| POLE_R | tube | 491 | -2506 | 10.1 | 19.9 |
| POST_R | tube | 162 | -1477 | 157.2 | 33.7 |
| SIDE_CORD_R | cord | 660 | +2882 | — | 3.1 |
| FORESTAY_R | cord | 416 | +1830 | — | 4.9 |
| AFTSTAY_R | cord | 502 | +0 | — | inf |
| BACKSTAY_R | cord | 714 | -0 | — | inf |
| SIDE_STRAP_R | fabric | 450 | +575 | nan | 10.4 |
| SLING_FR | fabric | 208 | +1273 | nan | 4.7 |
| SLING_RR | fabric | 321 | +1969 | nan | 3.0 |

Front seat post, bounding case with the forestay slack (pure cantilever, LC2): moment 44.4 N·m, tube stress 72 MPa (SF 6.2), socket bearing 2.4 MPa (SF 16.9 on knocked-down printed strength).

### Stability and turn-rate limiter

Combined CG height 719 mm; track 691 mm; wheelbase 660 mm.
Quasi-static tipping threshold: 0.48 g lateral (26° side slope), 0.46 g longitudinal.
Firmware limiter target: 0.25 g lateral (margin 1.9x on the geometric threshold); rule `|omega| * |v| <= a_lat_max, omega = (vR - vL) / track`.
At the 8 km/h cap the tightest permitted radius is 2.0 m; stopping distance at 0.30 g is 0.8 m.

| Turn radius (m) | Speed allowed (km/h) |
|---|---|
| 0.5 | 4.0 |
| 1.0 | 5.6 |
| 1.5 | 6.9 |
| 2.0 | 8.0 |
| 3.0 | 8.0 |
| 5.0 | 8.0 |

### Traction, torque and range (gross mass 172 kg, usable energy 291 Wh, 8 km/h)

| Surface | Grade | Drawbar force (N) | Electrical power (W) | Per-wheel motor load (W) | Per-wheel torque (N·m) | Range (km) | Within motor rating? |
|---|---|---|---|---|---|---|---|
| playa, hard | 0% | 34 | 117 | 27 | 1.9 | 19.9 | yes |
| playa, hard | 10% | 202 | 652 | 160 | 11.5 | 3.6 | yes |
| playa, soft/dusty | 0% | 101 | 331 | 80 | 5.8 | 7.0 | yes |
| playa, soft/dusty | 10% | 269 | 866 | 214 | 15.4 | 2.7 | yes |
| beach, wet firm | 0% | 84 | 277 | 67 | 4.8 | 8.4 | yes |
| beach, wet firm | 10% | 253 | 812 | 201 | 14.4 | 2.9 | yes |
| beach, dry loose | 0% | 337 | 1079 | 267 | 19.2 | 2.2 | power limit — derate speed |
| beach, dry loose | 10% | 505 | 1614 | 401 | 28.9 | 1.4 | torque limit — derate speed |

Motor basis: mini geared hub motor, no-clutch (regen-capable) variant preferred, 250 W nominal / 500 W peak, 20 N·m rated / 35 N·m peak. Drive efficiency 0.70 assumed at low speed; verify on the dynamometer test.

### Flotation (per-wheel load 421 N, dry-sand target ≤ 40 kPa)

| Tire | Ground pressure (kPa / psi) | Contact area (cm²) | Patch length (mm) | Tire deflection (mm) | Deflection acceptable (≤ 22% of section)? |
|---|---|---|---|---|---|
| 16 x 3.0 (baseline) | 30 / 4.3 | 140 | 264 | 38 | no — rim-out risk |
| 16 x 3.0 (baseline) | 40 / 5.8 | 105 | 198 | 21 | no — rim-out risk |
| 16 x 3.0 (baseline) | 55 / 8.0 | 77 | 144 | 11 | yes |
| 16 x 2.4 (PS-Lite) | 30 / 4.3 | 140 | 329 | 63 | no — rim-out risk |
| 16 x 2.4 (PS-Lite) | 40 / 5.8 | 105 | 247 | 36 | no — rim-out risk |
| 16 x 2.4 (PS-Lite) | 55 / 8.0 | 77 | 179 | 19 | no — rim-out risk |
| 20 x 4.0 (PS-Sand, two-bag pack) | 30 / 4.3 | 140 | 201 | 20 | yes |
| 20 x 4.0 (PS-Sand, two-bag pack) | 40 / 5.8 | 105 | 150 | 11 | yes |
| 20 x 4.0 (PS-Sand, two-bag pack) | 55 / 8.0 | 77 | 109 | 6 | yes |

Model: contact pressure ≈ inflation pressure; patch width ≈ 0.7 × section width; deflection ≈ L²/8R. Beach wheelchairs run 20–30 kPa; the 16 x 3.0 baseline lands at ~40 kPa, which is workable on dry sand at crawl speed and excellent on playa. The 20 x 4.0 variant buys real dry-sand flotation at the cost of the one-bag pack.

### Wheel-module axle, cantilever check (LC2, 2.5 g)

Sprung load per wheel 946 N at 45 mm cantilever → bending 42.6 N·m plus peak motor torque 35 N·m.
Bending stress 335 MPa, shear 138 MPa, von Mises 411 MPa on a 12 mm axle with 10 mm flats.
Safety factor 1.91 against an assumed yield of 785 MPa (target 1.5). **The axle steel grade must be verified per motor model; if it cannot be, the module carrier must support the axle on both sides.**
