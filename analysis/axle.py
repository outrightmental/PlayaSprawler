"""Hub-motor axle in single-sided (cantilever) mounting — the wheel module's most-loaded metal part."""
import math
import ps_params as P

def run(payload_kg):
    vehicle_kg = sum(P.MASS_BUDGET.values()) - P.MASS_BUDGET["Bag"]
    F = P.LOAD_CASES["LC2"]["vert"] * (payload_kg + vehicle_kg - 4 * 4.35) * P.G / 4  # sprung share per wheel
    M = F * P.AXLE_CANTILEVER_MM                     # N mm at the clamp edge
    d, f = P.AXLE_DIAM_MM, P.AXLE_FLAT_MM
    # section modulus of a circle with two flats, bending about the axis parallel to the flats (worst case)
    # approximate by a rectangle-capped circle: use conservative 0.75 factor on the full-circle modulus
    Z = 0.75 * math.pi * d ** 3 / 32
    sigma = M / Z
    T = P.MOTOR["torque_peak_Nm"] * 1000
    tau = T / (0.75 * math.pi * d ** 3 / 16)
    vm = math.sqrt(sigma ** 2 + 3 * tau ** 2)
    return {"F_N": F, "M_Nm": M / 1000, "sigma_MPa": sigma, "tau_MPa": tau, "vm_MPa": vm,
            "sf": P.AXLE_YIELD_MPA / vm, "sf_target": P.SF["axle"]}

def to_markdown(r):
    L = ["### Wheel-module axle, cantilever check (LC2, 2.5 g)\n",
         f"Sprung load per wheel {r['F_N']:.0f} N at {P.AXLE_CANTILEVER_MM:.0f} mm cantilever → bending {r['M_Nm']:.1f} N·m plus peak motor torque {P.MOTOR['torque_peak_Nm']:.0f} N·m.",
         f"Bending stress {r['sigma_MPa']:.0f} MPa, shear {r['tau_MPa']:.0f} MPa, von Mises {r['vm_MPa']:.0f} MPa on a {P.AXLE_DIAM_MM:.0f} mm axle with {P.AXLE_FLAT_MM:.0f} mm flats.",
         f"Safety factor {r['sf']:.2f} against an assumed yield of {P.AXLE_YIELD_MPA:.0f} MPa (target {r['sf_target']:.1f}). **The axle steel grade must be verified per motor model; if it cannot be, the module carrier must support the axle on both sides.**"]
    return "\n".join(L)

if __name__ == "__main__":
    print(to_markdown(run(P.RATING_CLASSES[P.DEFAULT_CLASS])))
