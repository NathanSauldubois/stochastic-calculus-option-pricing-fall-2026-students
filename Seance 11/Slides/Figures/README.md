# Heston parameter comparisons for Lecture 11

These are calculated model prices, with no market observations. Each slide
changes one parameter, holding all other risk-neutral parameters fixed.
The two maturities are 0.25 and 2 years. Both panels on each slide use the
same vertical scale.

Baseline: S0 = 100, r = 0, V0 = 0.04, kappa = 2, theta = 0.04,
eta = 0.4, rho = -0.6. There are no dividends.

| Parameter | Lower value | Baseline | Higher value |
| --- | ---: | ---: | ---: |
| rho | -0.85 | -0.6 | 0 |
| eta | 0.2 | 0.4 | 0.8 |
| V0 | 0.02 | 0.04 | 0.08 |
| theta | 0.02 | 0.04 | 0.08 |
| kappa | 0.5 | 2 | 4 |

`heston_smiles.csv` contains Black-Scholes implied volatilities in percent
for 41 strikes between 70 and 130. They are obtained from European Heston
call prices using characteristic-function probability inversion, composite
Simpson quadrature, and bisection of the Black-Scholes formula.

The calculation uses an integration cutoff of 400 and 4096 intervals.
Checks include call bounds, monotonicity, convexity, BS repricing,
the deterministic-variance Black-Scholes limit, and the small-eta limit.
For every curve, five strikes are checked again with cutoff 600 and 12288
intervals. The maximum difference in call price in this refinement check
was below 4.1e-12; this is a numerical comparison, not an error bound.

Instructor-side reproduction, from `Mon Repo/Preparation_fin_semestre/`:

```sh
python3 heston_smiles.py
```

This uses only the Python standard library and regenerates the CSV,
the embedded Heston plots and data in `../Slides.tex`, and the numerical
check report. Compiling the lecture requires only `Slides.tex`; its plot
data are embedded, so neither the CSV nor Python is needed.

Reference: [S. Heston (1993), A Closed-Form Solution for Options with
Stochastic Volatility](https://finance.martinsewell.com/stylized-facts/volatility/Heston1993.pdf).
