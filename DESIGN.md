# DESIGN.md — bentov-kuramoto v0.1.0

## Why this expansion exists

The previous step compared Bentov's chain to a Kuramoto ring in prose.
Prose can hide an assumption. Code cannot, if the assumption is a
parameter. So this prototype turns each step of Bentov's argument into
a parameter, and adds the control that separates "the drive did it"
from "the system was already doing it".

## Choices, and what was falsified along the way

- **Frequencies in Hz, coupling in Hz.** The first build mixed rad/s
  coupling with Hz frequencies, and coherence collapsed. Fixed by
  converting coupling to rad/s internally (2π factor), documented in
  `ring.py`. The earlier chat table used rad/s units throughout; the
  numbers here are therefore not directly comparable to it — the
  pattern (coherence rises with coupling, falls with spread) is.
- **Local vs global coherence are both reported, always.** A ring can
  be locally smooth and globally twisted. Reporting only one number
  is how "synchronized" becomes a slogan. Both are in every row.
- **Tube test threshold corrected, not fudged.** The standing-wave
  envelope spread is analytically ~0.485 for k=1, not >0.5 as first
  guessed. The test now uses 0.4, with that calculation in the comment.
  The travelling envelope is exactly flat (0.000) over a full period.
- **Twisted sensor test needs equal frequencies.** A twist imposed on
  a heterogeneous ring washes out before the sensor reads it, giving a
  nonsense k_est (−12.26 in the first run). With equal frequencies the
  twist persists and the sensor reads k_est 1.00. That failure is
  informative: a pattern must be *maintained* to be readable, and
  Bentov's standing wave would need a maintaining mechanism too.
- **Chain meditation is deliberately circular.** Meditation ON does
  not model "meditation"; it models "all frequencies forced to ~7 Hz".
  If the chain locked without that forcing, the test would be a
  discovery. It does not lock without it (OFF spread 0.994). The
  circularity is documented, not hidden, because it is the finding.

## What was NOT built, on purpose

- No "consciousness" variable. There is nothing in a phase oscillator
  that could stand for awareness, and inventing one would be the exact
  error this prototype is meant to expose.
- No Earth field physics. The driver is a sine at 7.83 Hz. It does not
  radiate, decay, or interact with anything except the phases it is
  wired to.
- No medical or therapeutic claim. Nothing here should be used to
  guide breathing, treatment, or diagnosis.

## Falsified designs (kept in the record)

1. "A weak Earth drive alone orders the ring." Falsified: drive alone
   at strength 0.3 gives local coherence −0.082; with coupling it is
   0.661.
2. "Global order and local order are the same thing." Falsified:
   spread 0.5, K=3.0 gives local 0.839 with global 0.045.
3. "Standing and travelling waves are interchangeable descriptions."
   Falsified: envelopes 0.000 flat vs 0.485 with true nodes.
4. "The chain locks under meditation in general." Falsified as stated:
   it locks only when frequencies are forced together first.
