# 10 — Test protocols

Each test records: part IDs, class, date, tester, instrument, result, pass/fail. Results go in the
rating record; failures go in an issue with the part quarantined.

| ID | Test | Method | Pass |
|---|---|---|---|
| T-1 | Tube 3-point bend | 25 × 22 CF sample, 300 mm span, load to failure ×3 per batch | ultimate ≥ 450 MPa flexural; stiffness within 15 % of E = 80 GPa |
| T-2 | Socket pull-out and bearing | joiner socket + bonded tube stub, axial pull and 90° prying | ≥ 2 × LC2 member force for the class, no crack |
| T-3 | Latch / dock pull-out | module on dock, pull along rail and vertical lift, 1.5 × LC2 wheel load | pin holds; shoe strain recovers |
| T-4 | Cord and seat-edge tensile | 5 mm cord with spliced eye ×3; seat edge webbing sample ×3 | cord ≥ 9 kN with eyes (0.5 knocked), edge ≥ 6 kN |
| T-5 | Static proof | assembled frame + seat, 1.5 × class payload on the seat for 60 s; each joiner also individually | no damage, permanent set ≤ 0.5 mm, deflection within 10 % of prediction |
| T-6 | Drop | class payload dummy, 150 mm drop onto hard playa-equivalent, ×10 | no damage; wheel status shows no fault |
| T-7 | Dyno and range | module on roller, 8 km/h at loads for each CRR row; full-vehicle loop on hard playa | drive efficiency ≥ 0.70; range ≥ 15 km |
| T-8 | Brake and hold | 8 km/h stop on level and 10 % downgrade; hold on 10 % for 5 min | stop ≤ 1.5 m; no roll-back |
| T-9 | Comms fail-safe | pull each cable in turn while rolling; kill the B node; flood the bus with malformed packets | affected wheels stop ≤ 0.5 s; vehicle never accelerates |
| T-10 | Hot-swap timing | rider seated; swap each module in turn; swap a control module; swap in a lower-rated module | ≤ 60 s each; `crawl` on the low part; `run` after replacement |
| T-11 | Pack / unpack | one person, no tools, from bag to rolling and back, ×3 | ≤ 15 min each way; bag ≤ 50 lb on a checked scale |
| T-12 | Dust and water | IP5X dust chamber on a module; IPX4 spray | no ingress at connectors or battery bay |
| T-13 | Thermal | soft-playa 10 % grade equivalent for 20 min at 40 °C ambient | motor < 95 °C, controller < 85 °C |
| T-14 | Stability | tilt table with class dummy | lift-off ≥ 24° side slope (0.45 g) |
