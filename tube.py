"""Standing wave vs travelling wave, in a 1-D tube.

This is the geometry Bentov actually invokes (a tube with a reflecting
end, the aortic bifurcation) and the geometry the ring does NOT have.

- Travelling:  y(x, t) = sin(kx - wt).  Amplitude is constant in space,
  phase moves in time.
- Standing:    y(x, t) = sin(kx - wt) + sin(kx + wt).  Amplitude varies
  in space with fixed nodes (near zero) and antinodes, phase flips at
  nodes and does not travel.

Both are sums of sines.  Calling one by the other's name is an error,
not a poetic licence, because a sensor that measures amplitude alone
cannot tell them apart, while a sensor that measures phase can.
"""
import math


def travelling(n=64, k=1, w=1.0, t=0.0):
    return [math.sin(2.0 * math.pi * k * i / n - w * t) for i in range(n)]


def standing(n=64, k=1, w=1.0, t=0.0):
    return [math.sin(2.0 * math.pi * k * i / n - w * t)
            + math.sin(2.0 * math.pi * k * i / n + w * t)
            for i in range(n)]


def amplitude_profile(samples):
    """Envelope over time at each site: max - min across snapshots."""
    n = len(samples[0])
    return [max(s[i] for s in samples) - min(s[i] for s in samples)
            for i in range(n)]


def profile_spread(profile):
    """0 = every site has the same envelope (travelling-like),
    large = envelope varies strongly in space (standing-like, nodes)."""
    mean = sum(profile) / len(profile)
    var = sum((p - mean) ** 2 for p in profile) / len(profile)
    return math.sqrt(var) / mean if mean else 0.0
