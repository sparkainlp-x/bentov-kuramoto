"""Tick times: predictions, and the past between rings.

A 'tick' is one full turn of a phase oscillator: the moment its
unbounded phase crosses a multiple of 2*pi upward.  This is the toy
version of a pendulum tick, a heartbeat, a ring's cycle — nothing more.

Two things are measured here, and they are different:

1. PREDICTION, inside one ring: from the ring's own past intervals,
   predict its next tick time.  Prediction error = predicted - actual.
   A stable ring predicts well; a noisy or drifting ring does not.
   Prediction is per-ring, from its own past only — never from the
   other ring, and never from the future.

2. PAST, between two rings: for every tick of ring B, the lag to the
   most recent tick of ring A, and the history of those lags.
   - Lag stable (small spread)  -> the two rings are ticking together,
     whatever their absolute phase offset.
   - Lag drifting linearly    -> the rings tick at different rates;
     the slope of the lag history is the frequency difference.
   - Lag scattered              -> no stable tick relationship.

Tick times are detected at step granularity (dt), so every interval
carries a quantisation error of up to one dt.  That error is reported,
not hidden: prediction errors smaller than dt are meaningless.
"""
import math


class TickTracker:
    """Tracks ticks of one site of one ring (default: site 0)."""

    def __init__(self, site=0, window=None):
        self.site = site
        self.window = window  # if set, mean interval uses only last N
        self.ticks = []       # tick times, in seconds
        self.predictions = []  # (predicted_time, actual_time, error)
        self._next_threshold = None
        self._pending_prediction = None

    def update(self, theta_value, time):
        """Call once per step, after the ring has stepped."""
        if self._next_threshold is None:
            # First sight: the next tick is the next multiple of 2*pi.
            self._next_threshold = (math.floor(theta_value / (2.0 * math.pi))
                                    + 1) * 2.0 * math.pi
        while theta_value >= self._next_threshold:
            self.ticks.append(time)
            if self._pending_prediction is not None:
                pred = self._pending_prediction
                self.predictions.append((pred, time, pred - time))
                self._pending_prediction = None
            self._next_threshold += 2.0 * math.pi
            # Predict the next tick from past intervals, if any.
            if len(self.ticks) >= 2:
                intervals = self.intervals()
                if self.window:
                    intervals = intervals[-self.window:]
                self._pending_prediction = (
                    self.ticks[-1] + sum(intervals) / len(intervals))

    def intervals(self):
        return [b - a for a, b in zip(self.ticks, self.ticks[1:])]

    def mean_interval(self):
        iv = self.intervals()
        return sum(iv) / len(iv) if iv else None

    def mean_hz_from_ticks(self):
        """Frequency implied by past ticks alone: 1 / mean interval."""
        m = self.mean_interval()
        return 1.0 / m if m else None

    def next_prediction(self):
        return self._pending_prediction

    def prediction_errors(self):
        return [e for (_, _, e) in self.predictions]

    def mean_abs_prediction_error(self):
        errs = self.prediction_errors()
        return sum(abs(e) for e in errs) / len(errs) if errs else None


def lags_between(tracker_a, tracker_b):
    """For each tick of B, lag to the most recent tick of A.

    Returns a list of (t_b, lag).  Ticks of B before A's first tick
    have no past in A and are skipped, not invented.
    """
    out = []
    a_ticks = tracker_a.ticks
    for t_b in tracker_b.ticks:
        past_a = [t for t in a_ticks if t <= t_b]
        if past_a:
            out.append((t_b, t_b - past_a[-1]))
    return out


def lags_by_index(tracker_a, tracker_b):
    """Lag by tick number: t_b[k] - t_a[k], for k in common.

    Unlike lags_between (lag to the most recent A tick, which wraps
    into one period and therefore cannot drift), this one is unwrapped:
    a faster B gains a fixed amount per tick, so its index lag drifts
    linearly with k.  That drift, divided by the number of ticks, is
    exactly the mean-interval difference between the rings.
    """
    return [(k, tb - ta) for k, (ta, tb) in
            enumerate(zip(tracker_a.ticks, tracker_b.ticks))]


def lag_summary(lags):
    """Mean lag, spread (std), and drift (last lag - first lag).

    Drift ~ 0 with small spread = rings ticking together.
    Drift large and roughly linear = different tick rates.
    """
    if not lags:
        return {"n": 0, "mean_lag": None, "std_lag": None, "drift": None}
    vals = [lag for (_, lag) in lags]
    mean = sum(vals) / len(vals)
    var = sum((v - mean) ** 2 for v in vals) / len(vals)
    return {"n": len(vals), "mean_lag": mean,
            "std_lag": math.sqrt(var), "drift": vals[-1] - vals[0]}
