"""Tests for bentov-kuramoto v0.1.0.  Run: python3 -m unittest tests -v"""
import math
import unittest

from ring import Ring
from chain import Chain
from tube import (travelling, standing, amplitude_profile,
                  profile_spread)
from sensor import sample


class TestRing(unittest.TestCase):
    def test_coherence_rises_with_coupling(self):
        low = Ring(spread=0.5, coupling=0.2, seed=42).run().local_coherence()
        high = Ring(spread=0.5, coupling=3.0, seed=42).run().local_coherence()
        self.assertGreater(high, low)

    def test_coherence_rises_when_spread_narrows(self):
        wide = Ring(spread=2.0, coupling=1.0, seed=42).run().local_coherence()
        narrow = Ring(spread=0.05, coupling=1.0, seed=42).run().local_coherence()
        self.assertGreater(narrow, wide)

    def test_drive_alone_beats_nothing_but_coupling_beats_drive_alone(self):
        alone = Ring(drive_hz=7.83, drive_strength=0.3, coupling=0.0,
                     seed=42).run().local_coherence()
        both = Ring(drive_hz=7.83, drive_strength=0.3, coupling=1.0,
                    seed=42).run().local_coherence()
        self.assertGreater(both, alone)

    def test_global_order_can_stay_low_while_local_coherence_is_high(self):
        # Strong coupling, moderate spread: locally smooth, globally
        # twisted, so the global order parameter stays near zero.
        r = Ring(spread=0.5, coupling=3.0, seed=42).run()
        self.assertGreater(r.local_coherence(), 0.8)
        self.assertLess(r.global_order(), 0.2)


class TestChain(unittest.TestCase):
    def test_meditation_locks_chain_and_off_does_not(self):
        off = Chain(meditation=False, coupling=1.0, seed=42).run()
        on = Chain(meditation=True, coupling=1.0, seed=42).run()
        self.assertLess(on.phase_diff_spread(), off.phase_diff_spread())
        self.assertLess(on.phase_diff_spread(), 0.5)


class TestTube(unittest.TestCase):
    def test_travelling_envelope_is_flat_and_standing_is_not(self):
        # One full period, so the travelling envelope is measured fairly.
        times = [2.0 * math.pi * j / 63 for j in range(63)]
        trav = profile_spread(amplitude_profile(
            [travelling(t=t) for t in times]))
        stand = profile_spread(amplitude_profile(
            [standing(t=t) for t in times]))
        self.assertLess(trav, 0.05)
        # Analytic value for a k=1 standing wave is ~0.485; 0.4 is the
        # honest threshold, not a guessed 0.5.
        self.assertGreater(stand, 0.4)


class TestSensor(unittest.TestCase):
    def test_sensor_is_read_only(self):
        r = Ring(twisted=True, coupling=1.0).run(steps=500)
        before = list(r.theta)
        sample(r, 10)
        self.assertEqual(r.theta, before)

    def test_sensor_reads_twist_without_any_drive(self):
        # Equal frequencies, so the imposed twist is not washed out by
        # heterogeneous natural frequencies before the sensor reads it.
        r = Ring(twisted=True, spread=0.0, coupling=1.0).run(steps=500)
        s = sample(r, 10)
        self.assertAlmostEqual(s["k_est"], 1.0, places=1)


if __name__ == "__main__":
    unittest.main()
