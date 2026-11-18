"""PDE, quadrature and martingale schemes for Lecture 13 (NumPy only).

Run with Python 3.12+ and NumPy. Writes pricing_schemes_results.json.
The examples are model calculations, without a market calibration.
MC intervals quantify sampling error, not a discretization or model error.
Executable Monte Carlo covers all five product families. Full Asian,
lookback and five-state correlation PDE grids remain slide pseudocode.
"""
from pathlib import Path
import json
import math
import numpy as np

HERE = Path(__file__).resolve().parent


def statistics(values):
    values = np.asarray(values, dtype=float)
    mean = float(values.mean())
    se = float(values.std(ddof=1) / math.sqrt(values.size))
    return {"mean": mean, "se": se, "ci95": [mean - 1.96*se, mean + 1.96*se],
            "paths": int(values.size)}


def bs_paths(rng, M, dt, s0, r, sigma, z=None):
    """Exact BS endpoints, including S0; dt contains positive year fractions.

    Rows are paths, columns are dates. Supply z and -z to form antithetic
    paths. Exact endpoints do not make integral/maximum monitoring exact.
    """
    dt = np.asarray(dt, dtype=float)
    if dt.ndim != 1 or not dt.size or np.any(dt <= 0):
        raise ValueError("dt must contain positive time increments.")
    if z is None:
        z = rng.standard_normal((M, dt.size))
    if np.shape(z) != (M, dt.size):
        raise ValueError("The normal array must have one row per path.")
    increments = (r-.5*sigma**2)*dt + sigma*np.sqrt(dt)*z
    logs = np.c_[np.zeros(M), np.cumsum(increments, axis=1)]
    return s0*np.exp(logs)


def normal_cdf(x):
    """Standard normal CDF, using the standard-library erfc."""
    x = np.asarray(x, dtype=float)
    return np.vectorize(lambda u: .5*math.erfc(-u/math.sqrt(2)),
                        otypes=[float])(x)


def geometric_call(s0, K, r, sigma, times):
    """Exact geometric Asian call on the specified future fixing dates.

    Time-zero valuation, equally weighted fixings, excluding S0.
    """
    times = np.asarray(times, dtype=float)
    if times.ndim != 1 or not times.size or np.any(np.diff(np.r_[0., times]) <= 0):
        raise ValueError("Fixing dates must be positive and strictly increasing.")
    T = times[-1]
    mu = math.log(s0)+(r-.5*sigma**2)*times.mean()
    var = sigma**2*np.minimum.outer(times, times).mean()
    if var == 0:
        return math.exp(-r*T)*max(math.exp(mu)-K, 0.)
    nu = math.sqrt(var)
    d2 = (mu-math.log(K))/nu
    return float(math.exp(-r*T)*(math.exp(mu+.5*var)*normal_cdf(d2+nu)
                                -K*normal_cdf(d2)))


def asian_payoffs(S, K, r, T):
    """Discounted arithmetic/geometric payoffs; columns 1..N are fixings."""
    future = S[:, 1:]
    A = future.mean(axis=1)
    G = np.exp(np.log(future).mean(axis=1))
    discount = math.exp(-r*T)
    return discount*np.maximum(A-K, 0.), discount*np.maximum(G-K, 0.)


def pilot_beta(target, control):
    """Fit only on independent pilot observations; zero variance -> no control."""
    variance = np.var(control, ddof=1)
    return float(np.cov(target, control, ddof=1)[0, 1]/variance) if variance > 0 else 0.


def variance_ratio(raw_variance, new_variance):
    """Undefined when the new observation is deterministic; JSON uses null."""
    return float(raw_variance/new_variance) if new_variance > 0 else None


def asian_mc(paths=32768, fixings=64, pilot_paths=4096, seed=2026111401,
             spot=100., strike=100., rate=.02, sigma=.2, maturity=1.):
    """Discrete arithmetic Asian: plain, geometric control and antithetic pairs.

    There are exactly 'fixings' equally spaced future observations.
    The antithetic standard error uses one independent PAIR per row.
    The control uses a separate pilot, not a fitted coefficient on the main run.
    """
    dt = np.full(fixings, maturity/fixings)
    rng = np.random.default_rng(seed)
    pilot_rng = np.random.default_rng(seed+1)
    pilot = bs_paths(pilot_rng, pilot_paths, dt, spot, rate, sigma)
    xp, zp = asian_payoffs(pilot, strike, rate, maturity)
    beta = pilot_beta(xp, zp)
    exact = geometric_call(spot, strike, rate, sigma, np.cumsum(dt))
    z = rng.standard_normal((paths, fixings))
    plus = bs_paths(rng, paths, dt, spot, rate, sigma, z)
    x, control = asian_payoffs(plus, strike, rate, maturity)
    minus = bs_paths(rng, paths, dt, spot, rate, sigma, -z)
    x_minus, _ = asian_payoffs(minus, strike, rate, maturity)
    pair = .5*(x+x_minus)
    controlled = x-beta*(control-exact)
    raw_variance = np.var(x, ddof=1)
    return {"fixings": fixings, "geometric_exact": exact, "pilot_paths": pilot_paths,
            "beta": beta, "plain": statistics(x), "geometric_control": statistics(control),
            "control": statistics(controlled), "antithetic": statistics(pair),
            "antithetic_independent_pairs": paths, "antithetic_path_evaluations": 2*paths,
            "control_variance_ratio": variance_ratio(raw_variance, np.var(controlled, ddof=1)),
            "antithetic_equal_cost_variance_ratio": variance_ratio(raw_variance, 2*np.var(pair, ddof=1)),
            "pathwise_arithmetic_ge_geometric": bool(np.all(x >= control-1e-12))}


def barrier_payoffs(rng, S, dt, K, b, r, sigma, T):
    """Continuous BS barrier: conditional weights and an unbiased Bernoulli hit.

    The endpoint-only observation targets a different, discretely monitored
    contract. All three observations share their exact BS endpoints.
    """
    x = np.log(S/b)
    valid = (x[:, :-1] > 0) & (x[:, 1:] > 0)
    left, right = np.maximum(x[:, :-1], 0.), np.maximum(x[:, 1:], 0.)
    survival = -np.expm1(-2*left*right/(sigma**2*dt))
    weight = np.prod(np.where(valid, survival, 0.), axis=1)
    vanilla = math.exp(-r*T)*np.maximum(S[:, -1]-K, 0.)
    conditional = vanilla*weight
    bernoulli = vanilla*(rng.random(S.shape[0]) < weight)
    endpoint = vanilla*np.all(x > 0, axis=1)
    return conditional, bernoulli, endpoint


def lookback_payoffs(rng, S, dt, K, r, sigma, T, m0):
    """Exact continuous-BS maximum conditional on all sampled endpoints."""
    x, y = np.log(S[:, :-1]), np.log(S[:, 1:])
    U = np.maximum(rng.random(x.shape), np.finfo(float).tiny)
    peak = .5*(x+y+np.sqrt((x-y)**2-2*sigma**2*dt*np.log(U)))
    maximum = np.maximum(m0, np.exp(peak.max(axis=1)))
    endpoint_maximum = np.maximum(m0, S.max(axis=1))
    discount = math.exp(-r*T)
    return (discount*np.maximum(maximum-K, 0.),
            discount*np.maximum(endpoint_maximum-K, 0.))


def lookback_mc(paths=65536, steps=32, seed=2026111402, spot=100., strike=100.,
                rate=.02, sigma=.2, maturity=1., past_maximum=100.):
    """Continuous fixed-strike lookback; past record must be at least spot."""
    if past_maximum < spot:
        raise ValueError("The past maximum cannot be below current spot.")
    rng = np.random.default_rng(seed)
    dt = np.full(steps, maturity/steps)
    S = bs_paths(rng, paths, dt, spot, rate, sigma)
    exact, endpoint = lookback_payoffs(rng, S, dt, strike, rate, sigma,
                                     maturity, past_maximum)
    vanilla = math.exp(-rate*maturity)*np.maximum(S[:, -1]-strike, 0.)
    return {"bridge": statistics(exact), "endpoint_only": statistics(endpoint),
            "pathwise_bridge_ge_grid": bool(np.all(exact >= endpoint-1e-12)),
            "pathwise_bridge_ge_vanilla": bool(np.all(exact >= vanilla-1e-12))}


def lookback_quadrature(spot=100., strike=100., rate=.02, sigma=.2, maturity=1.,
                        past_maximum=100., points=16385):
    """Independent reflection-tail quadrature, in log-record coordinates."""
    if past_maximum < spot:
        raise ValueError("The past maximum cannot be below current spot.")
    if maturity == 0:
        return max(past_maximum-strike, 0.)
    alpha = rate-.5*sigma**2
    scale = sigma*math.sqrt(maturity)
    if scale == 0:
        maximum = max(past_maximum, spot*math.exp(max(rate*maturity, 0.)))
        return math.exp(-rate*maturity)*max(maximum-strike, 0.)
    lower = math.log(max(past_maximum, strike)/spot)
    upper = max(lower+1., abs(alpha)*maturity+12*scale+1.)
    a = np.linspace(lower, upper, points)
    tail = normal_cdf((alpha*maturity-a)/scale)
    tail += np.exp(2*alpha*a/sigma**2)*normal_cdf((-alpha*maturity-a)/scale)
    integral = np.trapezoid(spot*np.exp(a)*tail, a)
    return float(math.exp(-rate*maturity)*(max(past_maximum-strike, 0.)+integral))


def factor_tridiagonal(lower, diagonal, upper):
    """LU factors; lower/upper have length n-1. No dense inverse."""
    pivots = np.array(diagonal, dtype=float, copy=True)
    multipliers = np.empty_like(lower)
    for i in range(1, pivots.size):
        multipliers[i-1] = lower[i-1] / pivots[i-1]
        pivots[i] -= multipliers[i-1] * upper[i-1]
    if np.any(pivots <= 0):
        raise ArithmeticError("The implicit generator system lost positive pivots.")
    return multipliers, pivots, np.array(upper, copy=True)


def solve_factored(factors, rhs):
    multipliers, pivots, upper = factors
    value = np.array(rhs, dtype=float, copy=True)
    for i in range(1, value.size):
        value[i] -= multipliers[i-1] * value[i-1]
    value[-1] /= pivots[-1]
    for i in range(value.size-2, -1, -1):
        value[i] = (value[i] - upper[i]*value[i+1]) / pivots[i]
    return value


def barrier_pde(nodes=640, time_steps=640, spot=100., strike=100., barrier=90.,
                rate=.02, sigma=.2, maturity=1., upper_spot=600.):
    """Implicit log-grid PDE for a continuous no-rebate down-and-out call."""
    if spot <= barrier:
        return 0.
    xmax = math.log(upper_spot/barrier)
    x = np.linspace(0., xmax, nodes+1)
    dx, h = xmax/nodes, maturity/time_steps
    drift = rate - sigma*sigma/2
    up = .5*sigma*sigma/(dx*dx) + max(drift, 0.)/dx
    down = .5*sigma*sigma/(dx*dx) + max(-drift, 0.)/dx
    n = nodes-1
    factors = factor_tridiagonal(
        np.full(n-1, -h*down), np.full(n, 1+h*(up+down+rate)),
        np.full(n-1, -h*up))
    values = np.maximum(barrier*np.exp(x[1:-1])-strike, 0.)
    for k in range(1, time_steps+1):
        # Boundary at the newly solved backward time; large-spot call asymptote.
        upper_value = upper_spot - strike*math.exp(-rate*k*h)
        rhs = values.copy()
        rhs[-1] += h*up*upper_value
        values = solve_factored(factors, rhs)
    values = np.r_[0., values, upper_spot-strike*math.exp(-rate*maturity)]
    return float(np.interp(math.log(spot/barrier), x, values))


def barrier_reflection(spot=100., strike=100., barrier=90., rate=.02,
                       sigma=.2, maturity=1., points=16385):
    """Independent quadrature of the killed log-transition density."""
    x = math.log(spot/barrier)
    alpha = rate-sigma*sigma/2
    scale = sigma*math.sqrt(maturity)
    y = np.linspace(0., x+abs(alpha)*maturity+12*scale+1., points)
    z1 = (y-x-alpha*maturity)/scale
    z2 = (y+x-alpha*maturity)/scale
    density = (np.exp(-z1*z1/2) -
               math.exp(-2*alpha*x/(sigma*sigma))*np.exp(-z2*z2/2))
    density /= scale*math.sqrt(2*math.pi)
    payoff = np.maximum(barrier*np.exp(y)-strike, 0.)
    return float(math.exp(-rate*maturity)*np.trapezoid(payoff*density, y))


def barrier_mc(paths=131072, steps=32, seed=2026111313, spot=100., strike=100.,
               barrier=90., rate=.02, sigma=.2, maturity=1.):
    """Exact BS endpoints: compare two unbiased continuous-barrier estimators.

    Conditional bridge weighting integrates out the Bernoulli knockout draw.
    Endpoint-only monitoring targets a different contract and has monitoring bias
    relative to the continuous contract. It is not a variance-reduction control.
    """
    rng = np.random.default_rng(seed)
    dt = np.full(steps, maturity/steps)
    S = bs_paths(rng, paths, dt, spot, rate, sigma)
    conditional, bernoulli, endpoint = barrier_payoffs(
        rng, S, dt, strike, barrier, rate, sigma, maturity)
    return {"bridge": statistics(conditional), "bernoulli_bridge": statistics(bernoulli),
            "endpoint_only": statistics(endpoint),
            "conditioning_variance_ratio": variance_ratio(np.var(bernoulli, ddof=1),
                                                         np.var(conditional, ddof=1)),
            "pathwise_grid_ge_bridge": bool(np.all(endpoint >= conditional-1e-12))}


def vix_window(kappa, theta, window=30/365):
    b = -math.expm1(-kappa*window)/(kappa*window)
    return theta*(1-b), b


def vix_pde(nodes=2000, time_steps=2000, vmax=.8, v0=.04, maturity=.5,
            kappa=2., theta=.04, eta=.35, window=30/365):
    """Implicit monotone CIR-generator scheme for a futures QUOTATION.

    At zero keep the inward CIR drift. At the remote upper node suppress
    outward jumps; vmax refinement measures this artificial boundary error.
    There is no discount term in the generator.
    """
    variance = np.linspace(0., vmax, nodes+1)
    dv, h = vmax/nodes, maturity/time_steps
    mu = kappa*(theta-variance)
    diffusion = eta*eta*variance/(2*dv*dv)
    up = diffusion + np.maximum(mu, 0.)/dv
    down = diffusion + np.maximum(-mu, 0.)/dv
    down[0] = 0.
    up[-1] = 0.
    factors = factor_tridiagonal(-h*down[1:], 1+h*(up+down), -h*up[:-1])
    a, b = vix_window(kappa, theta, window)
    values = 100*np.sqrt(a+b*variance)
    for _ in range(time_steps):
        values = solve_factored(factors, values)
    return float(np.interp(v0, variance, values))


def cir_terminal(rng, M, v, tau, kappa, theta, eta):
    """Exact CIR transition, including zero time and deterministic limits."""
    if tau == 0:
        return np.full(M, v)
    if eta == 0:
        return np.full(M, theta+(v-theta)*math.exp(-kappa*tau))
    c = eta**2*(-math.expm1(-kappa*tau))/(4*kappa)
    degrees = 4*kappa*theta/eta**2
    noncentrality = math.exp(-kappa*tau)*v/c
    return c*rng.noncentral_chisquare(degrees, noncentrality, M)


def vix_mc(paths=524288, seed=2026111314, v0=.04, maturity=.5,
           kappa=2., theta=.04, eta=.35, window=30/365, pilot_paths=16384):
    """Exact CIR terminal samples and a known-mean terminal-variance control.

    The inner expected forward variance is analytic; averaging a simulated
    realized volatility would change the target. Both raw and controlled
    observations price an undiscounted futures quotation.
    """
    rng = np.random.default_rng(seed)
    pilot_rng = np.random.default_rng(seed+1)
    a, b = vix_window(kappa, theta, window)
    mean_variance = theta+(v0-theta)*math.exp(-kappa*maturity)
    terminal = cir_terminal(rng, paths, v0, maturity, kappa, theta, eta)
    values = 100*np.sqrt(a+b*terminal)
    pilot_v = cir_terminal(pilot_rng, pilot_paths, v0, maturity, kappa, theta, eta)
    beta = pilot_beta(100*np.sqrt(a+b*pilot_v), pilot_v)
    controlled = values-beta*(terminal-mean_variance)
    quote = statistics(values)
    exact_variance = (v0*eta*eta*math.exp(-kappa*maturity)*
                      (1-math.exp(-kappa*maturity))/kappa +
                      theta*eta*eta*(1-math.exp(-kappa*maturity))**2/(2*kappa))
    return {"futures_quote": quote,
            "variance_control": statistics(controlled), "control_beta": beta,
            "control_pilot_paths": pilot_paths,
            "jensen_upper_bound": float(100*math.sqrt(a+b*mean_variance)),
            "terminal_variance": statistics(terminal),
            "exact_terminal_variance_mean": mean_variance,
            "exact_terminal_variance_variance": exact_variance}


def vix_laplace_quadrature(v0=.04, maturity=.5, kappa=2., theta=.04,
                           eta=.35, window=30/365, nodes=256):
    """Independent square-root Laplace integral, with Gaussian quadrature.

    E[sqrt(Y)] = (2 sqrt(pi))^-1 int_0^inf (1-E[e^-uY]) u^-3/2 du.
    Substitutions u=x^2, x=tan(pi*t/2) give a smooth finite-interval
    integrand. The CIR Laplace transform is used, rather than an FD grid
    or random terminal draws. This check requires eta>0 and maturity>0.
    """
    a, b = vix_window(kappa, theta, window)
    c = eta*eta*(-math.expm1(-kappa*maturity))/(4*kappa)
    degrees = 4*kappa*theta/(eta*eta)
    noncentrality = math.exp(-kappa*maturity)*v0/c
    z, weights = np.polynomial.legendre.leggauss(nodes)
    t = (z+1)/2
    angle = math.pi*t/2
    x = np.tan(angle)
    q = c*b*x*x
    log_transform = -a*x*x - .5*degrees*np.log1p(2*q) - noncentrality*q/(1+2*q)
    integrand = -np.expm1(log_transform)/(x*x) * (math.pi/2)/np.cos(angle)**2
    return float(100/math.sqrt(math.pi)*np.dot(weights/2, integrand))


def correlation_mc(paths=32768, steps=64, seed=2026111315, local=True,
                   rate=.02, maturity=1., fixings=16):
    """Pairwise continuous covariation ratio and a DIFFERENT sampled statistic.

    Positive bounded local volatilities and a bounded local correlation;
    both risks are stock-driven. No extra variance factor is introduced.
    Sampled correlations use centered log returns on a FIXED fixing schedule.
    Refining the internal integration grid does not add contractual fixings.
    """
    if fixings < 2 or steps < fixings or steps % fixings:
        raise ValueError("Use at least two fixings and a multiple of that many internal steps.")
    rng = np.random.default_rng(seed)
    h = maturity/steps
    log_s1 = np.zeros(paths)
    log_s2 = np.zeros(paths)
    a1 = np.zeros(paths)
    a2 = np.zeros(paths)
    cov = np.zeros(paths)
    l1 = np.zeros(paths)
    l2 = np.zeros(paths)
    q1 = np.zeros(paths)
    q2 = np.zeros(paths)
    q12 = np.zeros(paths)
    previous1 = np.zeros(paths)
    previous2 = np.zeros(paths)
    stride = steps//fixings
    for j in range(steps):
        if local:
            sigma1 = .2*(1+.25*np.tanh(log_s1))
            sigma2 = .3*(1-.20*np.tanh(log_s2))
            rho = .35+.20*np.tanh(log_s1-log_s2)
        else:
            sigma1, sigma2, rho = .2, .3, .4
        z1 = rng.standard_normal(paths)
        z2 = rho*z1+np.sqrt(1-rho*rho)*rng.standard_normal(paths)
        r1 = (rate-sigma1*sigma1/2)*h+sigma1*math.sqrt(h)*z1
        r2 = (rate-sigma2*sigma2/2)*h+sigma2*math.sqrt(h)*z2
        a1 += sigma1*sigma1*h
        a2 += sigma2*sigma2*h
        cov += rho*sigma1*sigma2*h
        log_s1 += r1
        log_s2 += r2
        if (j+1) % stride == 0:
            obs1, obs2 = log_s1-previous1, log_s2-previous2
            l1 += obs1
            l2 += obs2
            q1 += obs1*obs1
            q2 += obs2*obs2
            q12 += obs1*obs2
            previous1, previous2 = log_s1.copy(), log_s2.copy()
    continuous = cov/np.sqrt(a1*a2)
    var1, var2 = q1-l1*l1/fixings, q2-l2*l2/fixings
    if np.any(var1 <= 0) or np.any(var2 <= 0):
        raise ArithmeticError("Apply the contract's zero-sample-variance rule.")
    sample = (q12-l1*l2/fixings)/np.sqrt(var1*var2)
    if np.max(np.abs(continuous)) > 1+1e-12 or np.max(np.abs(sample)) > 1+1e-12:
        raise ArithmeticError("The correlation statistic left its feasible range.")
    return {"steps": steps, "contractual_fixings": fixings,
            "fixing_dates": [float(maturity*j/fixings) for j in range(1, fixings+1)],
            "continuous_fair_strike": statistics(continuous),
            "sampled_centered_fair_strike": statistics(sample),
            "continuous_range": [float(continuous.min()), float(continuous.max())],
            "model": "bounded two-stock local diffusion" if local else "constant coefficients"}


def run_examples():
    asian = asian_mc()
    lookback = {"tail_quadrature": lookback_quadrature(), "mc": lookback_mc()}
    barrier = {
        "reflection": barrier_reflection(),
        "pde_coarse": barrier_pde(nodes=320, time_steps=320),
        "pde_fine": barrier_pde(),
        "mc": barrier_mc(),
    }
    vix = {
        "pde_coarse": vix_pde(nodes=500, time_steps=500),
        "pde_medium": vix_pde(nodes=1000, time_steps=1000),
        "pde_fine": vix_pde(),
        # Same variance spacing, a more distant artificial upper boundary.
        "pde_larger_domain": vix_pde(nodes=3000, vmax=1.2),
        "laplace_quadrature": vix_laplace_quadrature(),
        "mc": vix_mc(),
    }
    constant = correlation_mc(paths=4096, steps=32, local=False)
    correlations = {"constant_coefficient_check": constant,
                    "local_32_steps": correlation_mc(steps=32),
                    "local_64_steps": correlation_mc(steps=64)}
    return {"conventions": {
        "data": "illustrative pricing-model simulations, not market observations",
        "barrier": "continuous down-and-out call, no rebate, BS, expiry cash payment",
        "vix": "Heston continuous-diffusion 30/365-window proxy; idealized futures quotation",
        "correlation": "pairwise continuous log covariation ratio; centered sample statistic on 16 fixed future dates separately labeled",
        "error_intervals": "MC sampling error only",
        "asian": "equally weighted discrete arithmetic average; 64 future fixings, excluding S0",
        "lookback": "continuous fixed-strike BS call on the running maximum, including the past record",
        "variance_reduction": "independent pilot controls; antithetic SE from independent pair averages",
    }, "asian": asian, "barrier": barrier, "lookback": lookback,
       "vix": vix, "correlation": correlations}


if __name__ == "__main__":
    results = run_examples()
    destination = HERE / "pricing_schemes_results.json"
    destination.write_text(json.dumps(results, indent=2, allow_nan=False)+"\n")
    print(f"Wrote {destination.name}")
