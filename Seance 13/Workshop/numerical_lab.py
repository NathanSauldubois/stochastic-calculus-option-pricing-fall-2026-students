"""Reproducible numerical examples for lectures 11--14 (NumPy only).

Run with Python 3.12+ and NumPy. All prices are per share. Simulated data,
not market observations. Confidence intervals quantify sampling error only.
The JSON is consumed by build_slides.py; seeds and discretizations are fixed.
"""
from pathlib import Path
import json
import math
import numpy as np

HERE = Path(__file__).resolve().parent


def cdf(x):
    x = np.asarray(x, dtype=float)
    # Five-term normal-tail approximation; max absolute error < 8e-8.
    a = np.abs(x)
    t = 1.0 / (1.0 + 0.2316419 * a)
    p = 1.0 - np.exp(-a * a / 2) / np.sqrt(2 * np.pi) * t * (
        0.319381530 + t * (-0.356563782 + t * (1.781477937
        + t * (-1.821255978 + t * 1.330274429))))
    return np.where(x >= 0, p, 1 - p)


def bs_call(s=100., k=100., r=.02, sigma=.2, t=1.):
    if t <= 0:
        return np.maximum(np.asarray(s) - k, 0)
    d1 = (np.log(np.asarray(s) / k) + (r + sigma * sigma / 2) * t) / (sigma * np.sqrt(t))
    return np.asarray(s) * cdf(d1) - k * np.exp(-r * t) * cdf(d1 - sigma * np.sqrt(t))


def implied_vol(price):
    lo, hi = .001, 2.
    for _ in range(70):
        mid = (lo + hi) / 2
        if bs_call(sigma=mid) < price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def stats(x):
    x = np.asarray(x)
    se = x.std(ddof=1) / np.sqrt(x.size)
    return dict(mean=float(x.mean()), se=float(se), low=float(x.mean()-1.96*se),
                high=float(x.mean()+1.96*se), sd=float(x.std(ddof=1)),
                q05=float(np.quantile(x, .05)), q95=float(np.quantile(x, .95)))


def barrier_experiment():
    """Exact GBM grid; coupled refinements; exact conditional bridge weights.

    Endpoint payoffs times the survival weight estimate a continuously
    monitored, constant-volatility down-and-out call without rebate.
    """
    rng = np.random.default_rng(20261112)
    m, fine, grids = 32768, 1024, [16, 64, 256, 1024]
    store = {n: [[], []] for n in grids}
    h, sig, r = 90., .2, .02
    for start in range(0, m, 2048):
        size = min(2048, m-start)
        dw = rng.standard_normal((size, fine)) / np.sqrt(fine)
        for n in grids:
            increments = dw.reshape(size, n, fine//n).sum(axis=2)
            x = np.c_[np.full(size, np.log(100.)),
                         np.log(100.) + np.cumsum((r-sig*sig/2)/n + sig*increments, axis=1)]
            dist = x - np.log(h)
            alive = (dist > 0).all(axis=1)
            p_hit = np.exp(np.minimum(0., -2*dist[:, :-1]*dist[:, 1:]/(sig*sig/n)))
            survival = np.prod(1-p_hit, axis=1)*alive
            vanilla = np.exp(-r)*np.maximum(np.exp(x[:, -1])-100., 0)
            store[n][0].append(vanilla*alive)
            store[n][1].append(vanilla*survival)
    return [dict(n=n, grid=stats(np.concatenate(store[n][0])),
                 bridge=stats(np.concatenate(store[n][1]))) for n in grids]


def asian_experiment():
    rng = np.random.default_rng(20261113)
    m, n = 32768, 64
    s = np.exp(np.log(100.) + np.cumsum((.02-.2**2/2)/n
               + .2*rng.standard_normal((m, n))/np.sqrt(n), axis=1))
    # Contract averages the n dates t_j=j/n, j=1,...,n (excludes t=0).
    arith = np.exp(-.02)*np.maximum(s.mean(axis=1)-100., 0)
    geom = np.exp(-.02)*np.maximum(np.exp(np.log(s).mean(axis=1))-100., 0)
    mu = np.log(100.) + (.02-.2**2/2)*(n+1)/(2*n)
    var = .2**2*(n+1)*(2*n+1)/(6*n*n)
    d2 = (mu-np.log(100.))/np.sqrt(var)
    exact = np.exp(-.02)*(np.exp(mu+var/2)*float(cdf(d2+np.sqrt(var)))-100*float(cdf(d2)))
    # Independent pilot to estimate beta, then freeze beta for the main run.
    pilot_rng = np.random.default_rng(202611130)
    sp = np.exp(np.log(100.) + np.cumsum((.02-.2**2/2)/n
                + .2*pilot_rng.standard_normal((4096,n))/np.sqrt(n), axis=1))
    ap = np.exp(-.02)*np.maximum(sp.mean(axis=1)-100., 0)
    gp = np.exp(-.02)*np.maximum(np.exp(np.log(sp).mean(axis=1))-100., 0)
    beta = np.cov(ap,gp,ddof=1)[0,1]/np.var(gp,ddof=1)
    cv = arith - beta*(geom-exact)
    return dict(n=n, m=m, geometric_exact=float(exact), beta=float(beta),
                raw=stats(arith), control=stats(cv),
                convergence=[dict(m=mi, **stats(arith[:mi])) for mi in [512,2048,8192,32768]])


def heston_run(seed, m=65536, n=512):
    rng = np.random.default_rng(seed)
    s = np.full(m, 100.); v = np.full(m, .04); maximum = s.copy()
    for _ in range(n):
        zs = rng.standard_normal(m); zv = rng.standard_normal(m)
        vp = np.maximum(v, 0.)
        s *= np.exp((.02-vp/2)/n + np.sqrt(vp/n)*zs)
        # Full truncation: retain the raw v; truncate in drift and diffusion.
        v += 2*(.04-vp)/n + .5*np.sqrt(vp/n)*(-.7*zs + np.sqrt(1-.7**2)*zv)
        maximum = np.maximum(maximum, s)
    return stats(np.exp(-.02)*np.maximum(s-100.,0)), stats(np.exp(-.02)*np.maximum(maximum-100.,0))


def heston_experiment():
    calibration, _ = heston_run(20261114, m=65536)
    sig = implied_vol(calibration['mean'])
    call, lookback = heston_run(20261115)
    rng = np.random.default_rng(20261116)
    m, n = 65536, 512
    s = np.full(m,100.); mx = s.copy()
    for _ in range(n):
        s *= np.exp((.02-sig*sig/2)/n + sig*rng.standard_normal(m)/np.sqrt(n))
        mx = np.maximum(mx,s)
    return dict(sigma_match=sig, calibration_call=calibration, heston_call=call,
                heston_lookback=lookback,
                bs_call=stats(np.exp(-.02)*np.maximum(s-100.,0)),
                bs_lookback=stats(np.exp(-.02)*np.maximum(mx-100.,0)), m=m,n=n)


def hedge_experiment():
    results = []
    m = 32768
    for hedge_sigma in [.2, .15]:
        for n in [12, 52, 252]:
            rng = np.random.default_rng(20261117+n)
            s = np.full(m,100.)
            d1 = (math.log(1.) + (.02+hedge_sigma**2/2))/(hedge_sigma)
            delta = np.full(m,float(cdf(d1)))
            premium = float(bs_call(sigma=hedge_sigma))
            cash = np.full(m,premium)-delta*s
            for j in range(n):
                cash *= np.exp(.02/n)
                s *= np.exp((.06-.2**2/2)/n + .2*rng.standard_normal(m)/np.sqrt(n))
                if j < n-1:
                    tau = 1-(j+1)/n
                    nd = cdf((np.log(s/100.)+(.02+hedge_sigma**2/2)*tau)/(hedge_sigma*np.sqrt(tau)))
                    cash -= (nd-delta)*s
                    delta = nd
            pnl = cash+delta*s-np.maximum(s-100.,0)
            hist, edges = np.histogram(pnl,bins=np.linspace(-8,8,33))
            results.append(dict(sigma=hedge_sigma,n=n,**stats(pnl),
                     histogram=[[float((a+b)/2),float(c/m)] for a,b,c in zip(edges[:-1],edges[1:],hist)]))
    return results


def main():
    data = dict(barrier=barrier_experiment(), asian=asian_experiment(),
                heston=heston_experiment(), hedge=hedge_experiment())
    # Numerical consistency checks that protect the teaching conclusions.
    assert abs(float(bs_call())-8.9160373)<2e-5
    assert data['asian']['control']['se'] < data['asian']['raw']['se']/10
    assert all(x['grid']['mean'] >= x['bridge']['mean'] for x in data['barrier'])
    assert all(a['grid']['mean'] >= b['grid']['mean']-1e-10
               for a,b in zip(data['barrier'],data['barrier'][1:]))
    bridges = data['barrier']
    assert max(x['bridge']['mean'] for x in bridges)-min(x['bridge']['mean'] for x in bridges)<.15
    correct = [x for x in data['hedge'] if x['sigma']==.2]
    assert correct[-1]['sd'] < correct[0]['sd']/3
    mismatched = [x for x in data['hedge'] if x['sigma']==.15][-1]
    assert mismatched['mean'] < -.5
    dest = HERE/'numerical_results.json'
    dest.write_text(json.dumps(data,indent=2)+'\n')
    print(dest)
    print('Checks passed; all examples are simulations, with fixed seeds.')


if __name__ == '__main__':
    main()
