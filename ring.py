"""Kuramoto ring: the expanded prototype's membrane.

A ring of N phase oscillators with local (nearest-neighbour) coupling.
An optional external driver (the 'Earth' field in Bentov's language)
advances at drive_hz and pulls each oscillator with strength E.

All frequencies are in Hz, converted to rad/s internally.  This is a
classical toy, not a body, not a planet, not a measurement.
"""
import math
import random


class Ring:
    def __init__(self, n=64, base_hz=7.0, spread=0.5, coupling=1.0,
                 drive_hz=None, drive_strength=0.0, noise=0.0, seed=42,
                 twisted=False):
        self.n = n
        # Coupling is given in Hz, like the frequencies, and converted
        # to rad/s here.  Passing K=1 therefore means a coupling of the
        # same order as a 1 Hz frequency spread, not 1 rad/s.
        self.coupling = coupling * 2.0 * math.pi
        self.drive_hz = drive_hz
        self.drive_strength = drive_strength
        self.noise = noise
        rng = random.Random(seed)
        self.theta = [rng.uniform(0.0, 2.0 * math.pi) for _ in range(n)]
        if twisted:
            # Winding number +1: phase winds once around the ring.
            self.theta = [2.0 * math.pi * i / n for i in range(n)]
        self.omega = [2.0 * math.pi * rng.gauss(base_hz, spread)
                      for _ in range(n)]
        self.drive_phase = 0.0
        self._rng = rng
        self._prev_theta = list(self.theta)

    def step(self, dt=0.01):
        n = self.n
        new = []
        for i in range(n):
            c = 0.5 * self.coupling * (
                math.sin(self.theta[(i - 1) % n] - self.theta[i])
                + math.sin(self.theta[(i + 1) % n] - self.theta[i]))
            d = 0.0
            if self.drive_hz is not None and self.drive_strength:
                d = self.drive_strength * math.sin(
                    self.drive_phase - self.theta[i])
            nz = self._rng.gauss(0.0, self.noise) if self.noise else 0.0
            new.append(self.theta[i] + dt * (self.omega[i] + c + d + nz))
        self._prev_theta = list(self.theta)
        self.theta = new
        if self.drive_hz is not None:
            self.drive_phase += dt * 2.0 * math.pi * self.drive_hz

    def run(self, steps=3000, dt=0.01):
        for _ in range(steps):
            self.step(dt)
        return self

    def global_order(self):
        """r: 1 = all phases identical, 0 = phases spread around the circle."""
        s = sum(complex(math.cos(t), math.sin(t)) for t in self.theta)
        return abs(s) / self.n

    def local_coherence(self):
        """Mean cos(neighbour phase difference): 1 = locally smooth."""
        return sum(math.cos(self.theta[(i + 1) % self.n] - self.theta[i])
                   for i in range(self.n)) / self.n

    def mean_hz(self, dt=0.01):
        """Mean instantaneous frequency in Hz, from the last step."""
        diffs = []
        for i in range(self.n):
            d = self.theta[i] - self._prev_theta[i]
            # Wrap to (-pi, pi] so a full turn is not mistaken for a jump.
            while d > math.pi:
                d -= 2.0 * math.pi
            while d <= -math.pi:
                d += 2.0 * math.pi
            diffs.append(d / dt / (2.0 * math.pi))
        return sum(diffs) / self.n
