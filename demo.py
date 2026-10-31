"""Demo: Bentov chain vs Kuramoto ring, side by side, with controls.

Run:  python3 demo.py
Prints the table that the comparison in chat was built from.  Every
number is reproducible from its seed; change a seed and the table
changes a little, the pattern does not.
"""
import math

from ring import Ring
from chain import Chain
from tube import travelling, standing, amplitude_profile, profile_spread
from sensor import sample


def ring_row(label, **kw):
    r = Ring(**kw).run()
    print(f"{label:38s} local={r.local_coherence():.3f} "
          f"global r={r.global_order():.3f} mean Hz={r.mean_hz():.3f}")
    return r


def main():
    print("== Ring: coupling and spread (5-seed means in the chat table; "
          "here seed 42) ==")
    ring_row("spread 0.5, K=0.2", spread=0.5, coupling=0.2)
    ring_row("spread 0.5, K=1.0", spread=0.5, coupling=1.0)
    ring_row("spread 0.5, K=3.0", spread=0.5, coupling=3.0)
    ring_row("spread 0.05, K=1.0", spread=0.05, coupling=1.0)
    ring_row("spread 2.0, K=1.0", spread=2.0, coupling=1.0)
    print()
    print("== Ring: Earth drive, with and without coupling ==")
    ring_row("drive 7.83 Hz, E=0.3, K=0 (drive alone)",
             drive_hz=7.83, drive_strength=0.3, coupling=0.0)
    ring_row("drive 7.83 Hz, E=0.3, K=1.0 (drive + coupling)",
             drive_hz=7.83, drive_strength=0.3, coupling=1.0)
    print()
    print("== Chain: meditation off vs on (heart-brain phase spread) ==")
    for med in (False, True):
        c = Chain(meditation=med, coupling=1.0).run()
        print(f"meditation={'ON ' if med else 'OFF'}  "
              f"phase-diff spread={c.phase_diff_spread():.3f} "
              f"(0 = locked, ~1 = drifting)")
    print()
    print("== Tube: travelling vs standing envelope ==")
    times = [2.0 * math.pi * j / 63 for j in range(63)]
    for name, fn in (("travelling", travelling), ("standing", standing)):
        prof = amplitude_profile([fn(t=t) for t in times])
        print(f"{name:12s} envelope spread={profile_spread(prof):.3f} "
              f"min envelope={min(prof):.3f} max={max(prof):.3f}")
    print()
    print("== Sensor on a twisted ring, no drive (the no-drive control) ==")
    r = Ring(twisted=True, spread=0.0, coupling=1.0).run(steps=500)
    s = sample(r, 10)
    print(f"position 10: k_est={s['k_est']:.2f} omega={s['omega_hz']:.3f} Hz "
          f"coherence={s['coherence']:.3f}")
    print("A twist already in the ring is readable by the sensor, "
          "with no Earth drive at all.")


if __name__ == "__main__":
    main()
