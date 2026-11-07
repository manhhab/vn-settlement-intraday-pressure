import numpy as np, pandas as pd, statsmodels.api as sm, json, pickle
from scipy import stats
T = 'results/'
SEG = ['ON', 'AM', 'LUNCH', 'PM', 'ATC', 'CC']
def mean_t(x):
    x = x.dropna(); m = sm.OLS(x, np.ones(len(x))).fit(cov_type='HAC', cov_kwds={'maxlags': 5}); return x.mean(), m.tvalues.iloc[0]
def ols(y, X, data):
    d = data[[y] + X].dropna()
    return sm.OLS(d[y], sm.add_constant(d[X])).fit(cov_type='HAC', cov_kwds={'maxlags': 5})
OUT = {}
for n in ['VNINDEX', 'VN30']:
    df = pd.read_pickle(T + f'{n}.pkl'); post = df[df.POST == 1]; pre = df[df.POST == 0]
    R = {}
    # Table I: descriptives post-rule
    R['T1'] = {c: dict(mean=post[c].mean(), sd=post[c].std(), t=mean_t(post[c])[1], pos=(post[c] > 0).mean() * 100) for c in SEG}
    R['T1']['AV'] = dict(mean=post.AV.mean(), sd=post.AV.std(), t=np.nan, pos=(post.AV > 0).mean() * 100)
    R['T1']['val'] = dict(mean=post.val.mean(), sd=post.val.std())
    # Table II: pre vs post + early post-rule bear window
    bear = df[(df.index >= '2022-08-29') & (df.index <= '2022-11-30')]
    R['T2'] = {}
    for c in SEG:
        mp, tp = mean_t(pre[c]); mq, tq = mean_t(post[c]); mb, tb = mean_t(bear[c])
        w = stats.ttest_ind(post[c], pre[c], equal_var=False)
        R['T2'][c] = dict(pre=mp, tpre=tp, post=mq, tpost=tq, diff=mq - mp, tdiff=w.statistic, bear=mb, tbear=tb,
                         negpre=(pre[c] < 0).mean() * 100, negpost=(post[c] < 0).mean() * 100, negbear=(bear[c] < 0).mean() * 100)
    R['T2']['n'] = dict(pre=len(pre), post=len(post), bear=len(bear))
    R['T2']['ccbear'] = bear.CC.sum()
    R['T2']['ccpre'] = pre.CC.sum()
    # Table III: LUNCH on lags, post-rule
    X = ['AV1', 'AV2', 'AV3', 'R1', 'R2', 'R3']
    m1 = ols('LUNCH', ['AV1', 'AV2', 'AV3'], post); m2 = ols('LUNCH', X, post)
    post2 = post.copy(); post2['UP2'] = (post2.R2 > 0).astype(float); post2['AV2xUP2'] = post2.AV2 * post2.UP2
    m3 = ols('LUNCH', ['AV1', 'AV2', 'AV3', 'R1', 'R3', 'UP2', 'AV2xUP2'], post2)
    m4 = ols('LUNCH', ['AV1', 'AV2', 'AV3', 'AV4', 'R1', 'R2', 'R3', 'LUNCH_l1'], post.assign(LUNCH_l1=post.LUNCH.shift(1)))
    R['T3'] = {k: dict(b=m.params.to_dict(), t=m.tvalues.to_dict(), r2=m.rsquared * 100, n=int(m.nobs)) for k, m in (('m1', m1), ('m2', m2), ('m3', m3), ('m4', m4))}
    # placebo: other segments on same regressors (post)
    R['T3p'] = {}
    for c in ['ON', 'AM', 'PM', 'ATC']:
        m = ols(c, X, post); R['T3p'][c] = dict(b=m.params.to_dict(), t=m.tvalues.to_dict(), r2=m.rsquared * 100)
    # Table IV: interaction on full sample
    d = df.copy()
    for k in (2, 3): d[f'POSTxAV{k}'] = d.POST * d[f'AV{k}']
    XI = ['POST', 'AV2', 'POSTxAV2', 'AV3', 'POSTxAV3', 'AV1', 'R1', 'R2', 'R3']
    R['T4'] = {}
    for c in ['LUNCH', 'AM', 'ON', 'PM']:
        m = ols(c, XI, d); R['T4'][c] = dict(b=m.params.to_dict(), t=m.tvalues.to_dict(), r2=m.rsquared * 100, n=int(m.nobs))
    # pre-only regressions
    R['T4pre'] = {}
    for c in ['LUNCH', 'AM', 'ON']:
        m = ols(c, ['AV1', 'AV2', 'AV3'], pre); R['T4pre'][c] = dict(b=m.params.to_dict(), t=m.tvalues.to_dict(), n=int(m.nobs))
    # Table V: robustness on LUNCH ~ AV1..3 + R1..3 (coef on AV2)
    R['T5'] = {}
    def rec(lab, y, Xs, data, key='AV2'):
        m = ols(y, Xs, data); R['T5'][lab] = dict(b=m.params[key], t=m.tvalues[key], r2=m.rsquared * 100, n=int(m.nobs))
    rec('baseline', 'LUNCH', X, post)
    rec('AV20', 'LUNCH', ['AV20_1', 'AV20_2', 'AV20_3', 'R1', 'R2', 'R3'], post, 'AV20_2')
    rec('volume', 'LUNCH', ['AQ1', 'AQ2', 'AQ3', 'R1', 'R2', 'R3'], post, 'AQ2')
    rec('preKRX', 'LUNCH', X, post[post.KRX == 0]); rec('postKRX', 'LUNCH', X, post[post.KRX == 1])
    rec('2022-23', 'LUNCH', X, post[post.index.year <= 2023]); rec('2024', 'LUNCH', X, post[post.index.year == 2024]); rec('2025-26', 'LUNCH', X, post[post.index.year >= 2025])
    q = post.CC.abs().quantile(0.95); rec('excl. extreme days', 'LUNCH', X, post[post.CC.abs() <= q])
    rec('wins1%', 'LUNCH', X, post.assign(LUNCH=post.LUNCH.clip(post.LUNCH.quantile(.01), post.LUNCH.quantile(.99))))
    # reversal: afternoon windows
    for c in ['PM5', 'PM30', 'PMR', 'PM']:
        rec('rev_' + c, c, X, post)
    rec('rev_LUNCH+PM', 'LP', X, post.assign(LP=post.LUNCH + post.PM))
    # quintiles for figure 2 (post)
    Q = {}
    for k in (1, 2, 3):
        g = pd.qcut(post[f'AV{k}'], 5, labels=False)
        Q[k] = post.groupby(g).LUNCH.mean().tolist()
    R['Q'] = Q
    OUT[n] = R
json.dump(OUT, open(T + 'results.json', 'w'), indent=1, default=float)
