"""Build daily intraday-segment returns and lagged abnormal trading value."""
import pickle, numpy as np, pandas as pd
W = 'data/'
RULE = pd.Timestamp('2022-08-29')
KRX = pd.Timestamp('2025-05-05')

def build(n, win=10):
    o = pickle.load(open(W + f'{n}_B.pkl', 'rb'))
    raw = pd.read_pickle(W + f'{n}.pkl'); raw['t'] = pd.to_datetime(raw.TradingDate); raw['d'] = raw.t.dt.normalize()
    raw = raw[raw.t.dt.time <= pd.Timestamp('14:45').time()]
    val = raw.groupby('d').TotalMatchValue.max() / 1e9      # VND bn, matched (order-book) value incl. ATC
    vol = raw.groupby('d').TotalMatchVolume.max() / 1e6
    rows = []; prev = None; paths = {}
    for d in sorted(o):
        x = o[d]; p0, p1 = x['paths']
        if p0 is None or p1 is None: prev = x['close']; continue
        if prev is not None:
            rows.append(dict(d=d, ON=p0[0] - prev, AM=p0[135] - p0[0], LUNCH=p1[0] - p0[135], PM=p1[90] - p1[0], ATC=x['close'] - p1[90],
                             CC=x['close'] - prev, PM5=p1[5] - p1[0], PM30=p1[30] - p1[0], PMR=p1[90] - p1[30],
                             AM30=p0[30] - p0[0], AMR=p0[135] - p0[30]))
            paths[d] = np.concatenate([[0.0], p0 - prev, p1 - prev, [x['close'] - prev]])
        prev = x['close']
    df = pd.DataFrame(rows).set_index('d') * 100
    df['val'] = val.reindex(df.index); df['vol'] = vol.reindex(df.index)
    for c, s in (('AV', df.val), ('AQ', df.vol)):
        df[c] = np.log(s / s.rolling(win, min_periods=5).mean().shift(1))
    df['AV20'] = np.log(df.val / df.val.rolling(20, min_periods=10).mean().shift(1))
    for k in (1, 2, 3, 4):
        df[f'AV{k}'] = df.AV.shift(k); df[f'R{k}'] = df.CC.shift(k); df[f'AQ{k}'] = df.AQ.shift(k); df[f'AV20_{k}'] = df.AV20.shift(k)
    df['POST'] = (df.index >= RULE).astype(int); df['KRX'] = (df.index >= KRX).astype(int)
    return df, paths

if __name__ == '__main__':
    for n in ['VNINDEX', 'VN30']:
        df, paths = build(n)
        df.to_pickle(f'results/{n}.pkl'); pickle.dump(paths, open(f'results/{n}_paths.pkl', 'wb'))
        print(n, df.shape, df.index[0].date(), df.index[-1].date(), 'pre', (df.POST == 0).sum(), 'post', df.POST.sum())
        print('  check: components sum to close-to-close, max abs error =', (df[['ON', 'AM', 'LUNCH', 'PM', 'ATC']].sum(axis=1) - df.CC).abs().max())
