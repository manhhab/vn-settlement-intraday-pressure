"""Regular 1-minute grid of the two continuous sessions (previous-tick sampling), plus the official close."""
import pandas as pd, numpy as np, sys, pickle

SESS=[(0,'09:15','11:30'),(1,'13:00','14:30')]
def grid(n):
    df=pd.read_pickle(f'data/{n}.pkl'); df['t']=pd.to_datetime(df.TradingDate)
    df=df[df.t>='2022-06-09'].sort_values('t'); df['d']=df.t.dt.normalize()
    out={}
    for d,g in df.groupby('d'):
        s=g.set_index('t').CloseIndex
        paths=[]
        for k,a,b in SESS:
            A=pd.Timestamp(f'{d.date()} {a}'); Bt=pd.Timestamp(f'{d.date()} {b}')
            x=s[(s.index>=A)&(s.index<=Bt)]
            if len(x)==0: paths.append(None); continue
            idx=pd.date_range(A,Bt,freq='1min')
            y=x.reindex(idx.union(x.index)).ffill().reindex(idx)
            y=y.bfill()   # leading minutes before first print take first print (zero return)
            paths.append(np.log(y.values))
        # extra info: day open (9:15 first print), official close (last record <=14:45 incl ATC)
        ato=s[s.index>=pd.Timestamp(f'{d.date()} 09:15')]
        close=s[s.index<=pd.Timestamp(f'{d.date()} 14:45')].iloc[-1]
        out[d]=dict(paths=paths, open=np.log(ato.iloc[0]), close=np.log(close),
                    nrec=len(g))
    return out
if __name__=='__main__':
    for n in ['VNINDEX','VN30']:
        o=grid(n); pickle.dump(o,open(f'data/{n}_B.pkl','wb')); print(n,len(o))
