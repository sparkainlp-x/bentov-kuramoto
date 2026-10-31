"""Bentov's chain as four coupled macro-oscillators.

Nodes, in Bentov's order: heart, aorta, breath, brain.
Plus an optional Earth driver at drive_hz.

Meditation ON is modelled exactly as Bentov describes it, and no more:
the four natural frequencies are pulled toward a common ~7 Hz and the
coupling is raised.  Meditation OFF keeps the nodes at their natural,
far-apart frequencies with weak coupling.

That is the hidden assumption made visible: entrainment in this model
does NOT follow from meditation in general.  It follows from forcing
all four frequencies to be nearly equal first.  If you remove that
forcing, the same coupling does not lock the chain (see tests).
"""
import math
import random

NAMES = ("heart", "aorta", "breath", "brain")
# Natural frequencies in Hz, deliberately far apart: a resting heart
# beats ~1 Hz, breathing ~0.25 Hz, brain alpha ~10 Hz.  The aorta's
# claimed vibration is ~7 Hz.  These are illustrative, not measurements.
NATURAL_HZ = {"heart": 1.2, "aorta": 7.0, "breath": 0.25, "brain": 10.0}


class Chain:
    def __init__(self, meditation=False, coupling=1.0, drive_hz=None,
                 drive_strength=0.0, seed=42):
        rng = random.Random(seed)
        self.theta = {k: rng.uniform(0.0, 2.0 * math.pi) for k in NAMES}
        if meditation:
            # Frequencies pulled to a common ~7 Hz, small spread.
            self.omega = {k: 2.0 * math.pi * rng.gauss(7.0, 0.2)
                          for k in NAMES}
            self.coupling = max(coupling, 1.0)
        else:
            self.omega = {k: 2.0 * math.pi * NATURAL_HZ[k] for k in NAMES}
            self.coupling = coupling
        self.drive_hz = drive_hz
        self.drive_strength = drive_strength
        self.drive_phase = 0.0
        self.history = []  # snapshots of phase differences, for variance

    def step(self, dt=0.01):
        new = {}
        for k in NAMES:
            c = sum(math.sin(self.theta[j] - self.theta[k])
                    for j in NAMES if j != k)
            c *= self.coupling / (len(NAMES) - 1)
            d = 0.0
            if self.drive_hz is not None and self.drive_strength:
                d = self.drive_strength * math.sin(
                    self.drive_phase - self.theta[k])
            new[k] = self.theta[k] + dt * (self.omega[k] + c + d)
        self.theta = new
        if self.drive_hz is not None:
            self.drive_phase += dt * 2.0 * math.pi * self.drive_hz
        # Record heart-brain phase difference, wrapped to (-pi, pi].
        d = self.theta["heart"] - self.theta["brain"]
        while d > math.pi:
            d -= 2.0 * math.pi
        while d <= -math.pi:
            d += 2.0 * math.pi
        self.history.append(d)

    def run(self, steps=3000, dt=0.01, record_from=2000):
        for s in range(steps):
            self.step(dt)
            if s < record_from:
                self.history.pop() if self.history else None
        return self

    def phase_diff_spread(self):
        """Circular spread of the recorded heart-brain phase differences.

        0 = phase difference perfectly stable (locked), ~1 = drifting.
        Computed as 1 - |mean unit vector|.
        """
        if not self.history:
            return 1.0
        s = sum(complex(math.cos(d), math.sin(d)) for d in self.history)
        return 1.0 - abs(s) / len(self.history)
