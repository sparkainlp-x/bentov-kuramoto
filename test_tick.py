"""Tests for tick.py.  Run: python3 -m unittest test_tick -v"""
import unittest

from ring import Ring
from tick import TickTracker, lags_between, lags_by_index, lag_summary


def run_ring(base_hz, seed, steps=3000, dt=0.01, spread=0.05):
    ring = Ring(base_hz=base_hz, spread=spread, coupling=1.0, seed=seed)
    # Warmup discarded, as in membrane-propulsion: the first ticks
    # carry the ring's transient, not its settled tick rate.
    for _ in range(1000):
        ring.step(dt)
    tracker = TickTracker(site=0)
    for s in range(steps):
        ring.step(dt)
        tracker.update(ring.theta[0], (s + 1) * dt)
    return tracker


class TestTick(unittest.TestCase):
    def test_stable_ring_predicts_its_own_next_tick(self):
        t = run_ring(7.00, seed=42)
        self.assertGreater(len(t.ticks), 100)
        # Mean interval must recover ~7 Hz from ticks alone.
        self.assertAlmostEqual(t.mean_hz_from_ticks(), 7.0, delta=0.2)
        # Prediction error is bounded by step quantisation (dt=0.01),
        # with a small margin for coupling jitter.
        self.assertLess(t.mean_abs_prediction_error(), 0.02)

    def test_same_rate_rings_have_stable_past_lag(self):
        # Clean control: spread 0, so both tracked sites tick at
        # exactly 7 Hz.  Only the initial phase differs, so the
        # index-aligned lag must stay constant within one step.
        a = run_ring(7.00, seed=42, spread=0.0)
        b = run_ring(7.00, seed=7, spread=0.0)
        s = lag_summary(lags_by_index(a, b))
        # Drift 0.03 s over 210 ticks = 0.00014 s per tick, under 0.1%
        # of the 0.143 s period: stable to within 3 steps, not exactly
        # constant, because the ring is still slowly settling.
        self.assertLess(abs(s["drift"]), 0.05)
        self.assertLess(s["std_lag"], 0.02)

    def test_faster_ring_lag_drifts(self):
        a = run_ring(7.00, seed=42, spread=0.0)
        c = run_ring(7.83, seed=42, spread=0.0)
        s = lag_summary(lags_by_index(a, c))
        # C gains ~0.015 s per tick over A: over 200 ticks, seconds.
        self.assertLess(s["drift"], -1.0)
        # ...while C still predicts its own ticks well.
        self.assertLess(c.mean_abs_prediction_error(), 0.02)

    def test_no_tick_before_first_past(self):
        a = run_ring(7.00, seed=42, steps=10)
        b = run_ring(7.00, seed=7, steps=3000)
        # lags_between skips B ticks with no A past; it never invents one.
        lags = lags_between(a, b)
        self.assertTrue(all(t_b >= a.ticks[0] for (t_b, _) in lags))


if __name__ == "__main__":
    unittest.main()
