# 02 — Architecture

The sketch that started the project drew a box (battery · motor · gearbox · brake · electronics,
"4× redundant unit"), a camp-chair frame, two foot controls, a signal bus and a network
`W W W W — B — C C — I 1..n — L 1..n`. The architecture keeps exactly that shape.

```
            ┌────────────── PS-Bus (100BASE-TX, UDP multicast) ──────────────┐
            │                                                                 │
   W(FL) ───┤   W(FR) ───┤   W(RL) ───┤   W(RR) ───┤   C(CL) ──┤  C(CR) ──┤   I 1..n  L 1..n
     │            │           │            │            │           │          │       │
   ══╪════════════╪═══════════╪════════════╪════════════╪═══════════╪══════════╪═══════╪══  power bus (SELV 21–29.4 V)
                                        ┌───┴───┐
                                        │   B   │  unmanaged switch + supervisor + charge input
                                        └───────┘
```

## Node types

| Node | Count | Role | Publishes | Subscribes |
|---|---|---|---|---|
| **W** wheel module | 4 | traction, braking, battery, node | `wheel/<pos>/status` 10 Hz, `node/<serial>/hello` 1 Hz | `ctrl/tread/<side>`, `veh/mode`, `veh/estop` |
| **C** control module | 2 | rider input → normalised tread command | `ctrl/tread/<side>` 50 Hz, hello | `veh/mode` (for haptics/LED) |
| **B** bus node | 1 | 8-port unmanaged switch, supervisor MCU, power distribution, charge input, e-stop button | `veh/mode`, `veh/estop`, `veh/log` | everything |
| **I** input | 0..n | horn, lights switch, phone app, spare inputs | `input/<n>/event` | — |
| **L** load | 0..n | lights, sound, whatever the seat decorator wants | — | `light/<n>/cmd`, `veh/mode` |

Every port on the vehicle is the same port: **DATA** (M12 D-coded, Ethernet) + **POWER/ID**
(M12 A-coded, 4 pins: bus +, bus −, ID, spare). The ID pin is a resistor to bus − inside the dock;
its value tells the node which dock it is in: FL, FR, RL, RR, CL, CR, AUX1..n.

## Skid steer

There is no steering mechanism. The left tread command drives both left wheels, the right tread
command both right wheels. Turning = differential speed. This is what makes the four modules
identical: no module knows anything about steering geometry, only which side it is on
(and left-side nodes invert their motor sign).

## Power

Each wheel module carries a 7s1p pack (25.2 V nominal). The vehicle power bus runs at pack
voltage. Each module connects to the bus through an ideal-diode discharge path (so the highest
pack feeds the bus, never back-feeds another pack) and a current-limited charge path (≤ 3–5 A).
Consequences:

* one charger on the B node charges and balances all four packs;
* control modules, lights and the switch buck-convert from the bus; no PoE hardware needed;
* traction current stays inside the module — the dock connector only carries ≤ 5 A.

## Safety chain (what stops the wheels)

1. Rider releases input → command goes to 0 → wheels ramp down at 0.30 g.
2. Any control message stops arriving → wheel stops itself within 200 ms + 300 ms ramp.
3. Supervisor sees a missing wheel (status silent > 250 ms) → `veh/mode = stop`.
4. Any part reports a rating below the rider class → `veh/mode = crawl` (2 km/h).
5. E-stop button on B, or any node publishing `veh/estop` → all stop.
6. B node dies → no switch → no messages → every wheel stops by rule 2.

## Structure

The frame is a tensegrity-flavoured camp chair: two printed hubs joined by the seat rail, four
carbon legs down to the four docks, two carbon poles up to the backrest tips, two short posts to
the front seat tips, and Dyneema cords (side, rear, X-braces, forestays, aftstays, crossed
backstays) that close the truss. The canvas seat is a structural member: its side straps and edge
webbing carry real load, which is why it is rated like everything else (`docs/08`).

## Where things live

```
analysis/   parameters + all calculations → results/
cad/        CadQuery generator → exports/ (STEP, STL, SVG)
firmware/   PS-Bus reference simulator + message schemas
docs/       this folder, ADRs, sources
seat/       seat pattern
site/       playasprawler.outright.io
```
