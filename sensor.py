"""Passive receiver sensor inside the ring.

Same discipline as membrane-propulsion's sensor: sampling changes NO
model state.  It reads phase, local gradient (hence a k estimate),
local frequency (phase derivative) and local coherence over +/-2 sites.

It measures a pattern in the toy.  It does not measure consciousness,
a field, or a body.
"""
import math


def sample(ring, position, dt=0.01):
    """Return a reading dict.  ring.theta is never modified here."""
    n = ring.n
    i = position % n

    def phase_at(j):
        # Circular interpolation is unnecessary here: phases are stored
        # per site, so the sensor reads the site directly.
        return ring.theta[j % n]

    phase = phase_at(i)
    # Local gradient: wrapped phase difference to the next site.
    grad = phase_at(i + 1) - phase
    while grad > math.pi:
        grad -= 2.0 * math.pi
    while grad <= -math.pi:
        grad += 2.0 * math.pi
    k_est = grad / (2.0 * math.pi / n)
    # Local frequency: phase change since the previous step.
    d = ring.theta[i] - ring._prev_theta[i]
    while d > math.pi:
        d -= 2.0 * math.pi
    while d <= -math.pi:
        d += 2.0 * math.pi
    omega_hz = d / dt / (2.0 * math.pi)
    # Local coherence over +/-2 sites.
    neigh = [phase_at(j) for j in range(i - 2, i + 3)]
    s = sum(complex(math.cos(p), math.sin(p)) for p in neigh)
    coherence = abs(s) / len(neigh)
    return {"phase": phase, "gradient": grad, "k_est": k_est,
            "omega_hz": omega_hz, "coherence": coherence,
            "signal_cos": math.cos(phase) * coherence}
