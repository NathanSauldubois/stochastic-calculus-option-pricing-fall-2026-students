# Numerical schemes for Lecture 13

The slides present the formulas and numerical methods without Python or
pseudocode blocks. This directory keeps the executable examples separately.
The lecture opens with SDE simulation, Monte Carlo, variance reduction and
finite differences, then covers Asians, barriers, lookbacks and correlation
swaps. VIX futures and numerical examples are in the appendix.

Run `python3 pricing_schemes.py` with NumPy to regenerate
`pricing_schemes_results.json`. The current version was run with Python
3.12 and NumPy 2.2.5. All inputs are illustrative pricing-model parameters.

| Product | Executable Python | Additional methods |
| --- | --- | --- |
| Discrete arithmetic Asian | Exact BS fixing samples; geometric-call control with independent pilot; antithetic pairs; exact geometric control price on irregular dates | Continuous-average split PDE; discrete fixing updates |
| Continuous down-and-out call | Implicit log-grid PDE; reflection quadrature; bridge-survival MC; conditional weighting versus Bernoulli survival | Tridiagonal matrix assembly |
| Continuous fixed-strike lookback | Exact BS bridge maxima; independent reflection-tail quadrature, retaining the past record | Triangular PDE matrix and fixed-spot maximum-boundary rows |
| Pairwise correlation swap | Continuous log-covariation ratio; centered sampled-return correlation on a fixed observation schedule | Five-state PDE propagation using Gaussian quadrature and interpolation |
| Model VIX future (optional appendix) | CIR-generator PDE; exact CIR terminal samples; known-mean terminal-variance control; independent Laplace quadrature | Tridiagonal assembly and noncentral-chi-square density quadrature |

The full Asian, lookback and five-state correlation PDE grids are not
implemented by this script. The slides give the pricing equations and contract conditions.

The shared `bs_paths` kernel returns one path per row, including time
zero. A discrete Asian uses columns 1 onward as future fixings; a
trapezoidal stock integral describes a different, continuously averaged
contract and retains quadrature bias.

For the correlation example, the default sampled contract has 16 fixed
future observation dates, excluding inception. Both the 32-step and
64-step internal simulations retain these dates. Internal steps update
the stock and continuous covariation; sampled-return totals are updated
only at contractual dates. The continuous and sampled statistics are
separate contracts, even with constant coefficients.

The VIX calculation uses a continuous-diffusion Heston proxy for a
30/365-year forward window, rather than the exchange's SPX-option auction
settlement. Its futures quotation is not discounted. The inner expected
variance is analytic; simulating realized future volatility would change
the payoff. The remote upper variance boundary is checked by moving it.

Variance-reduction conventions:

- Controls use the same paths as the target payoff, an exact known mean,
  and a coefficient estimated on an independent pilot. Main-path SE is
  computed from the controlled observations.
- An antithetic observation is one pair average. There are `M` independent
  pairs and `2M` path evaluations. The reported antithetic variance ratio
  compares equal numbers of path evaluations, not equal numbers of pairs.
- For barriers, conditional weighting and Bernoulli survival target the
  same continuous payoff. Their comparison isolates variance reduction.
  Endpoint-only monitoring targets a different contract.
- Exact bridge maxima remove BS grid-maximum bias. That correction alone
  is not a claim of reduced variance.

JSON confidence intervals measure MC sampling error only. Refine time,
state grids, quadrature and artificial boundaries separately. Variance
ratios for deterministic observations are reported as `null`.

Run `python3 numerical_lab.py` to regenerate the original
`numerical_results.json`. Its parameters, seeds and optional slide
tables have been preserved. The geometric-control derivation is in the slide appendix; its code stays here. The PDFs compile without executing Python.
Lecture 14 and final-review scope remain Lectures 1-11 only.
