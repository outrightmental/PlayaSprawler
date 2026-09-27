# 12 — Regulatory framing

**This is a powered mobility device, not a scooter.** That is a design decision with consequences,
not a label.

## Black Rock City

* City speed limit 5 mph → firmware cap 8 km/h.
* Seated electric scooters, e-motorcycles and golf carts are disallowed personal transport.
* Four-wheeled seated electric vehicles are permitted only as **Accessibility Vehicles** (electric
  wheelchairs and 3–4-wheel mobility scooters) for people with documented mobility needs, with the
  DMV process that goes with it; otherwise a vehicle needs a Mutant Vehicle licence.
* Lights at night: white front, red rear, sides visible.

Design consequences: seat height and controls follow the mobility-device pattern; speed and
turn-rate limits are firmware-enforced, not optional; the documentation set references ISO 7176
(wheelchairs) and EN 12184 (electrically powered wheelchairs) test families so a rider can show an
inspector what the vehicle is.

## Ocean Beach, San Francisco (GGNRA / National Park Service)

Motor vehicles are prohibited on the beach. Wheelchairs and other power-driven mobility devices
(OPDMDs) used by people with mobility disabilities are the ADA exception, subject to the park's
current assessment. Riders must check current GGNRA policy before use; the project does not claim
a right of access.

## Batteries in transit

Burner Express accepts e-bikes and their batteries in luggage. Packs here are ≤ 100 Wh each (the
airline threshold used as a conservative design limit), with SoC indicators and terminal caps.

## What the project does not do

It does not certify anything. Rating labels are a community practice, not a legal mark. See
`docs/13`.
