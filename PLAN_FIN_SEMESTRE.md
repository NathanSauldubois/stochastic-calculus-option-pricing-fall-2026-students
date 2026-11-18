# End-of-semester course plan

Updated November 18, 2026. Each session has a 150-minute plan, including a
10-minute break. The teaching materials are in English. Sessions 12–14
use slides only; no separate course notes are provided.

| Session | Topic | Core content |
| --- | --- | --- |
| 11 | Beyond Black–Scholes | Local volatility, Dupire, Heston, pricing dynamics and variance hedging |
| 12 | Change of Numeraire and Fixed-Income Basics | Stochastic-rate foundations, numeraire changes, dated cash flows, bootstrapping, duration, forward loans, FRAs, swaps, caplets and a multicurve introduction |
| 13 | Exotic Option Pricing | Asian, barrier and lookback options, correlation swaps and VIX futures; replication/PDE, martingale pricing and numerical schemes for each product |
| 14 | Course Review: Lectures 1–11 | 26 worked exercises: Itô, martingales, Girsanov, replication, arbitrage, American exercise, simulation, implied volatility and Heston |

**Review scope: Sessions 1–11 only. The new material in Sessions 12–13 is
excluded from Session 14's review.**

## Session 12 — 150 minutes

| Minutes | Topic |
| --- | --- |
| 0–10 | Familiar pricing formula, short rate, bank account and random discount factor |
| 10–30 | Numeraire as a traded unit, density, conditional Bayes and the stock example |
| 30–65 | Zero-coupon and coupon cash flows, discount curve, bootstrapping as inverse pricing, and duration as a specified rate sensitivity |
| 65–75 | Break |
| 75–105 | Simple loan rate, forward agreement, end-paid FRA replication, swap payments, annuity and par rate |
| 105–125 | Payment-date measure, caplet payoff, Black distribution and cap–floor parity |
| 125–145 | Multicurve introduction: collateral discounting, index projection, FRA and swap valuation |
| 145–150 | Summary, checks and questions |

The Brownian drift calculation, swaption and annuity measure, quotation
conversions and Gaussian short-rate calculation are optional appendices
outside this timing. Each new instrument is introduced through its cash
flows before valuation; notation is defined before it is used. Rate
examples first use a default-free single-curve teaching framework. The
closing multicurve block assumes full continuous same-currency cash
collateral and distinguishes the collateral discount curve from the
contractual index-projection inputs. Standalone numerical pricing applications
have been removed. Small cash-flow illustrations introduce coupon conventions;
pricing, bootstrapping and duration are developed symbolically.

## Session 13 — 150 minutes

| Minutes | Topic |
| --- | --- |
| 0–15 | Pricing arguments, MC precision, antithetic pairs, controls and conditioning |
| 15–40 | Asian: replication/PDE, expectation, grid pseudocode, MC and geometric control |
| 40–65 | Barrier: replication/PDE, reflection quadrature, Brownian bridge and conditional MC |
| 65–75 | Break |
| 75–100 | Lookback: record boundary, supremum law, grid pseudocode and bridge-maximum code |
| 100–122 | Correlation swap: two-stock replication, five-state grid and fixed-observation simulation |
| 122–145 | VIX future: spanning, CIR PDE/code, exact transition, control and quadrature |
| 145–150 | Diagnosis and summary |

Each of the five product sections has three subsections: Replication and
PDE pricing; Martingale pricing; Numerical schemes for both approaches.
The correlation block distinguishes continuous log covariation from a
sampled centered-return correlation. The VIX block distinguishes the
exchange's special opening settlement from a continuous-diffusion Heston
proxy, and the futures quotation from a funded terminal-payment claim.
Stock/cash replication is not claimed for unspanned variance risk.

Every product includes Python or labeled pseudocode for the PDE and
martingale schemes. Introduce variance reduction before the geometric
control, and define the Brownian bridge before the crossing/maximum laws.
Walk through selected code blocks in class; the remaining details serve
as reference within the 150-minute session.

`Seance 13/Workshop/pricing_schemes.py` implements MC for all five families,
the barrier and VIX PDEs, and geometric/reflection/integral benchmarks.
It adds independent-pilot Asian and VIX controls, antithetic Asian pairs
and a conditional-versus-Bernoulli barrier comparison. Antithetic SE uses
independent pair averages. Sampled correlations retain the same 16
contractual future observations when the internal time grid is refined.
The full Asian/lookback and five-state correlation grids remain pseudocode.
The geometric derivation/code and earlier numerical experiments remain
optional appendices, with the original experiment seeds preserved.
Both workshop scripts require NumPy; the lecture PDF compiles without them.

## Session 14 — 150 minutes, Sessions 1–11 only

| Minutes | Review problem |
| --- | --- |
| 0–5 | Route map, conventions and solution checks |
| 5–30 | 1–6. Itô, martingales, stopping times and representation |
| 30–60 | 7–13. Girsanov, replication, Black–Scholes and Greeks |
| 60–70 | Break |
| 70–100 | 14–18. Executable arbitrage and American exercise |
| 100–125 | 19–22. Monte Carlo and implied volatility |
| 125–145 | 23–26. Heston: spanning, pricing drift and variance |
| 145–150 | Exit check and questions |

The review contains 26 worked exercises on 30 static pages, with each
question and its answer shown together. Problems 15 and 23 each use two
pages to keep their derivations legible. Section title cards and
progressive overlays are absent. No new material from Sessions 12–13 is
added to the review.

## Materials and compilation

The current PDFs and their standalone LaTeX sources for Sessions 12–14
are in each session's `Slides/` directory. All 14 student slide decks use
Beamer `handout` mode and display their full content without pauses. Separate notes and worksheets
12–14 have been archived. The synthesis, the 44-exercise core booklet,
and the 36-problem optional booklet cover Sessions 1–11 only. Their teacher
solutions follow the same scope and numbering.

Compile from the directory of the relevant `.tex` file, for example:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error Slides.tex
```

Use the existing section syllabus for calendar and administrative information.
This plan records the revised teaching topics and review scope.
