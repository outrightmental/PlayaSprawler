# 13 — Caveats (read before building)

1. **The 50 lb margin is 0.19 kg (0.8 %).** The mass budget is a target. Real parts will be weighed;
   expect to need PS-Lite wheels or the two-bag pack on the first prototypes.
2. **Axle steel is assumed.** SF 2.1 at PS-125 assumes a 785 MPa yield 40Cr axle. Verify per motor
   model; if unverifiable, the carrier must support the axle on both sides (costs ~60 g and 20 mm of width).
3. **The truss model is idealised**: pin joints, tension-only cords, seat modelled as five straight
   fabric members, no joint compliance. Deflections are lower bounds; forces are reasonable; joint
   bearing is checked separately and conservatively.
4. **Printed-part allowables** use a 0.5 knock-down on datasheet strength. That is an engineering
   guess until T-2/T-5 data exist for the chosen filament and printer.
5. **Range figures** assume drive efficiency 0.70 at low speed and textbook rolling-resistance
   coefficients (hard playa 0.02, soft 0.06, wet sand 0.05, dry loose sand 0.20). Dry sand range
   (2.5 km) is a warning, not a feature.
6. **Deflated-tire packing** is the only way the 16 × 3.0 wheel fits the section. Tubeless
   reseating on the playa with a mini pump must be proven (T-11).
7. **Regulatory**: the vehicle is only legal in BRC as an Accessibility Vehicle for riders with a
   documented need; on Ocean Beach only as an OPDMD under ADA. Nothing here is a permit.
8. **Hot-swap while rolling** is a demonstrated protocol behaviour, not an invitation; the procedure
   says stop first.
9. **Single supplier risk**: the mini geared hub motor class is commodity, but axle flats, wire
   exits and gear ratios vary by vendor. The carrier is parametric for that reason.
10. **No prototype exists yet.** Everything here is analysis, CAD and simulation. Stage 0 of the
    rollout is a single wheel module on a test rig.
