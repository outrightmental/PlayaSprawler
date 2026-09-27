# 11 — Fleet operations

The reason for all the standardisation: a camp keeps a rack of modules, not a row of vehicles.

## Inventory model

| Pool | Unit | Typical camp of 8 vehicles |
|---|---|---|
| Wheel modules | identical | 32 on vehicles + 8 charging/spare |
| Control modules | identical interface, various inputs | 16 + 4 |
| Bus nodes | identical | 8 + 2 |
| Frames | class-marked kits | 8 + spare tubes/joiners/cords |
| Seats | personal, never pooled | one per rider |

## Charging rack

A row of docks (same rail, same connectors) on a bus bar fed by the camp's power. Modules charge
at ≤ 3 A each; a 32-module night uses ~2.7 kWh. Rack publishes each slot's SoC on the camp LAN.

## Swap procedure (any module, rider seated)

1. Rider releases controls → `stop`.
2. Pull the dock pin, slide the module aft off the rail (front dock) or forward (rear dock).
3. Slide the spare in, pin clicks. Node reads the dock, hellos with its rating.
4. Supervisor: `run` if the rating meets the rider class, otherwise `crawl` — the rider sees it on the control LED.
5. Log auto-records serial in / serial out.

Target ≤ 60 s. The simulator shows the timing.

## Lifecycle states

`new → proof-tested → in service → flagged (fault/status) → inspected → in service | retired`.
A flagged module never goes back on a vehicle without an inspection entry.

## Sign-out

Rider mass + gear → rider class. Steward assigns a vehicle whose rating ≥ rider class; the B node
is set to the rider class so firmware enforces it for the rest of the day.

## Records

The supervisor logs every `hello` (serial, dock, rating) with a timestamp; the fleet steward pulls
logs at charge time. Combined with QR labels this answers "which parts were on the vehicle that
had the incident" in one query.
