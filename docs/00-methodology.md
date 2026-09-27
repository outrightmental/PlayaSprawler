# 00 — Methodology

Playa Sprawler is run as an engineering project, not a maker sketch. The method is a small V-model
with one hard rule: **no number appears in a spec, a drawing or the website unless a script in
`analysis/` produced it from `analysis/ps_params.py`.**

## The V

| Left side (definition) | Right side (proof) |
|---|---|
| **Requirements** `docs/01` — numbered `REQ-xxx`, each with a verification method (A = analysis, T = test, I = inspection, D = demonstration). | **Acceptance** — every `REQ` is closed by the named method and logged in the rating record. |
| **Architecture** `docs/02` — modules and the interfaces between them (dock, PS-Bus, power bus, seat pockets). | **Integration tests** `docs/10 §T-9..T-11` — hot-swap timing, comms fail-safe, packing. |
| **Module specs** `docs/04..08` — one file per swappable unit; interface first, internals second. | **Module tests** `docs/10 §T-1..T-8` — bend, socket, latch, cord, proof load, drop, brake, dust. |
| **Analysis** `analysis/*.py` — truss, stability, energy, flotation, axle, packing. | **Test correlation** — measured vs predicted; the parameter file is corrected, never the spec. |

## Rules of the project

1. **Single source of truth.** `analysis/ps_params.py` holds every design parameter. CAD (`cad/ps_cad.py`),
   analysis, the docs tables and the site read from it or from `analysis/results/results.json`.
2. **Ratings are computed, then proven.** A part's class (PS-100/125/150, `docs/03`) is first set by
   analysis with the stated knock-downs and safety factors, then confirmed by a proof test on *every*
   load-path part before the part is marked. Analysis alone never rates a part.
3. **Vehicle rating = min(part ratings).** Enforced twice: on the label (QR) and in firmware
   (`veh/mode` drops to `crawl` if any live node reports a rating below the rider class).
4. **Interfaces are frozen before internals.** The dock (rail + pin + two M12 connectors), the PS-Bus
   message set and the seat-pocket geometry are versioned interfaces (`v1`). Anyone may redesign the
   inside of a wheel module; nobody may change the dock without a new interface version.
5. **Decisions are recorded** as ADRs in `docs/adr/` with the alternatives that lost.
6. **Caveats are first-class.** `docs/13` lists what is idealised, unverified or marginal. The site
   repeats them; hiding them would defeat the point of a safety code.
7. **Traceability.** Requirement → analysis script → result → test → rating record. The table below is
   the index.

## Traceability index

| REQ | Where analysed | Where tested |
|---|---|---|
| REQ-010..013 (one bag) | `analysis/packing.py` | T-11 |
| REQ-020..024 (wheel module) | `energy.py`, `flotation.py`, `axle.py` | T-6, T-7, T-8, T-10 |
| REQ-030..033 (controls) | `firmware/sim/psbus_sim.py` | T-9, T-10 |
| REQ-040..045 (network + power) | `psbus_sim.py` | T-9 |
| REQ-050..056 (structure + rating) | `frame_truss.py` | T-1..T-5 |
| REQ-060..063 (mobility + terrain) | `stability.py`, `energy.py`, `flotation.py` | T-7, field trials |
| REQ-070..072 (fleet) | `docs/11` | fleet drills |
| REQ-080..082 (regulatory) | `docs/12` | inspection |

## Toolchain

* Python 3.12 + numpy for analysis; CadQuery 2.8 for parametric CAD (STEP/STL/SVG exports).
* Everything runs in CI on every pull request (`.github/workflows/pr.yml`): analysis, CAD export,
  simulator self-checks, site build. A red build blocks the merge — the same way a failed proof test
  blocks a part.
