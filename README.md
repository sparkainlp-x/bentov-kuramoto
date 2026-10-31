# bentov-kuramoto v0.2.0

**SYNTHETIC toy: Bentov's chain, rebuilt as coupled oscillators, with
the controls Bentov never ran. Classical simulation only. Not a body,
not a planet, not a measurement of consciousness, not a medical device,
not a validation of Bentov — and not a refutation of meditation as a
practice. It tests one specific claim: that resonance follows from the
oscillator maths alone.**

## What it is

An expansion of the Kuramoto-ring prototype, in four parts:

1. **`ring.py`** — 64 phase oscillators, local ring coupling, optional
   external driver at a set Hz (the "Earth" field in Bentov's language).
   Frequencies and coupling are in Hz.
2. **`chain.py`** — Bentov's chain as four macro-oscillators: heart,
   aorta, breath, brain, plus an optional Earth driver. Meditation OFF
   keeps their natural, far-apart frequencies (heart ~1.2 Hz, breath
   ~0.25 Hz, aorta ~7 Hz, brain ~10 Hz) with weak coupling. Meditation
   ON pulls all four toward a common ~7 Hz and raises the coupling —
   exactly the hidden assumption in Bentov's argument, made explicit.
3. **`tube.py`** — standing wave vs travelling wave in a 1-D tube, the
   geometry Bentov actually invokes (a tube with a reflecting end)
   versus the geometry a ring has (a closed loop).
4. **`sensor.py`** — a passive, read-only receiver inside the ring:
   phase, local gradient (k estimate), local frequency, local coherence
   over ±2 sites. Sampling changes no model state, test-pinned.

## Measured (seed 42, unless stated)

Ring, 3,000 steps:

| condition | local coherence | global r | mean Hz |
|---|---|---|---|
| spread 0.5, K=0.2 | 0.118 | 0.167 | 7.065 |
| spread 0.5, K=1.0 | 0.697 | 0.278 | 7.065 |
| spread 0.5, K=3.0 | 0.839 | 0.045 | 7.065 |
| spread 0.05, K=1.0 | 0.988 | 0.749 | 7.006 |
| spread 2.0, K=1.0 | 0.201 | 0.188 | 7.259 |

Earth drive (7.83 Hz, strength 0.3): drive alone, K=0 → local −0.082;
drive + coupling, K=1.0 → local 0.661. A weak external field does not
order the ring by itself; coupling does the work.

Chain, heart–brain phase-difference spread (0 = locked, ~1 = drifting):
meditation OFF → 0.994; meditation ON → 0.000.

Tube, one full period: travelling envelope spread 0.000 (flat, 2.000
everywhere); standing envelope spread 0.485, min 0.000 (nodes), max
3.998 (antinodes).

Sensor, twisted ring with equal frequencies, no drive at all:
position 10 → k_est 1.00, ω 7.000 Hz, coherence 0.990. A twist already
in the ring is readable with no Earth drive.

## What this shows, and what it does not

Shows: entrainment really does need close frequencies *and* sufficient
coupling; local coherence and global phase alignment are different
measurements (spread 0.5, K=3.0: local 0.839, global 0.045); a standing
wave and a travelling wave are distinguishable by their envelope, not
by amplitude alone; a sensor can read a pattern that was already there.

Does not show: that a human aorta forms a 7 Hz standing wave, that
such a wave couples to the brain or to the Earth, that consciousness
expands, or that any of this is a treatment. Those are Bentov's claims,
not this toy's results. The chain's meditation-ON result is circular by
design — it locks *because* the frequencies were forced to ~7 Hz first —
and that circularity is the point: it is the assumption Bentov's
argument needs, and it is not supplied by meditation in general.

## v0.2.0 addition: tick times — predictions, and past between rings

`tick.py` + `tick_demo.py` + `test_tick.py`. A tick is one full turn
of a tracked site's phase. Predictions use only that ring's own past
intervals; the past between rings is measured two ways, and the
difference matters:

- Wrapped lag (to the most recent tick of A) folds into one period and
  cannot show drift — it is kept only for phase, never for drift.
- Index-aligned lag (t_B[k] − t_A[k]) is unwrapped: a faster ring
  gains a fixed amount per tick.

Measured, 1,000-step warmup discarded, then 3,000 steps at dt=0.01:

| ring | ticks | mean interval | implied Hz | mean \|pred error\| |
|---|---|---|---|---|
| A 7.00 Hz, spread 0.05 | 210 | 0.1427 s | 7.009 | 0.0040 s |
| B 7.00 Hz, spread 0.05 | 210 | 0.1430 s | 6.995 | 0.0042 s |
| C 7.83 Hz, spread 0.05 | 235 | 0.1276 s | 7.839 | 0.0038 s |

Prediction error is under one step (dt=0.01 s) for every ring — even
for C, which ticks at a different rate. Predicting your own next tick
does not require agreeing with the other ring.

Index-aligned past, clean controls (spread 0): same exact rate
(7 vs 7 Hz) → lag drift +0.030 s over 210 ticks, std 0.0095 s, i.e.
stable within 3 steps; faster rate (7.83 vs 7 Hz) → drift −3.150 s
over 210 ticks. And the realistic warning: A and B above are both
nominally 7 Hz, yet their tracked sites tick at 7.009 vs 6.995 Hz, so
their cross-ring lag slowly walks. Nominal rate is not tick rate, for
a single site.

## Run it

```
python3 -m unittest tests test_tick -v   # 12/12
python3 demo.py
python3 tick_demo.py
```

## Honest limits

- Stdlib only, Python 3.10+. AGPL-3.0-only.
- All numbers are synthetic, seed-dependent, and specific to these
  parameters. Change a seed and the table moves a little; the pattern
  (coupling + narrow spread → local order) does not.
- No energy, metabolism, blood flow, cerebrospinal fluid, or
  electromagnetic field is modelled. "Earth driver" is a sine wave in
  code, not the Schumann resonance.
- The chain's natural frequencies are illustrative, not measurements
  of any person.

## Credits

Authors: Jean-François Brisson and Mun Seok Lee.
Lee, author of the Digital to Wave paradigm (Zenodo 21947036,
21947108), is the inspiration friend behind this wave and
membrane work. This package's code was built by Brisson with
AI assistance, except where a file already credits Lee as
author; the joint credit here is for the shared programme,
not a claim that Lee wrote every line of this package.
