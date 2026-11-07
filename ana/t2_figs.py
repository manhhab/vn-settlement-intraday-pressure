import pickle, numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt, json
T='results/'
plt.rcParams.update({'font.family':'serif','font.serif':['DejaVu Serif'],'font.size':9,'axes.spines.top':False,'axes.spines.right':False,
                     'axes.linewidth':0.6,'axes.unicode_minus':False,'xtick.major.width':0.6,'ytick.major.width':0.6})
RULE=pd.Timestamp('2022-08-29')
# Figure 1: average cumulative return path
fig,axes=plt.subplots(1,2,figsize=(7.2,2.9),sharey=True)
for ax,n in zip(axes,['VNINDEX','VN30']):
    P=pickle.load(open(T+f'{n}_paths.pkl','rb'))
    pre=np.mean([v for d,v in P.items() if d<RULE],axis=0)*100; post=np.mean([v for d,v in P.items() if d>=RULE],axis=0)*100
    # x positions: 0 prev close; 1..136 morning 9:15-11:30; gap of 8 units; 145..235 afternoon; close
    x=np.concatenate([[-8],np.arange(136),np.arange(146,237),[245]])
    for y,ls,c,lab in ((post,'-','black','After 29 Aug 2022 (1,014 days)'),(pre,'--','0.55','Before 29 Aug 2022 (56 days)')):
        ax.plot(x[:137],y[:137],ls,color=c,lw=1.2); ax.plot(x[137:228],y[137:228],ls,color=c,lw=1.2,label=lab)
        ax.plot([x[227],x[228]],[y[227],y[228]],ls,color=c,lw=1.2)
        ax.plot([x[136],x[137]],[y[136],y[137]],':',color=c,lw=0.9)
    ax.axvspan(136,146,color='0.92',lw=0); ax.axhline(0,color='0.7',lw=0.5)
    ax.set_xticks([-8,60,135,146,206,245]); ax.set_xticklabels(['Prev.\nclose','10:15','11:30','13:00','14:00','Close'],fontsize=7)
    tl=ax.get_xticklabels(); tl[2].set_ha('right'); tl[3].set_ha('left')
    ax.set_title(n,fontsize=9); ax.text(141,ax.get_ylim()[0] if False else 0.02,'Lunch',ha='center',fontsize=6.5,color='0.4',rotation=90,va='bottom')
axes[0].set_ylabel('Cumulative return (%)')
h,l=axes[0].get_legend_handles_labels(); fig.legend(h,l,frameon=False,fontsize=7.5,loc='lower center',ncol=2)
fig.tight_layout(rect=(0,0.07,1,1)); fig.savefig(T+'Figure1.tif',dpi=600,pil_kwargs={'compression':'tiff_lzw'}); fig.savefig(T+'Figure1.png',dpi=200); fig.savefig(T+'Figure1_300.png',dpi=300)
# Figure 2: lunch return by quintile of lagged abnormal value
R=json.load(open(T+'results.json'))
fig,axes=plt.subplots(1,2,figsize=(7.2,2.7),sharey=True)
w=0.26; cols={'1':'0.8','2':'0.15','3':'0.55'}; labs={'1':'Day t-1','2':'Day t-2','3':'Day t-3'}
for ax,n in zip(axes,['VNINDEX','VN30']):
    for j,k in enumerate(['1','2','3']):
        ax.bar(np.arange(5)+(j-1)*w,R[n]['Q'][k],w*0.92,color=cols[k],label=labs[k],edgecolor='black',linewidth=0.3)
    ax.set_xticks(range(5)); ax.set_xticklabels(['Q1\n(low)','Q2','Q3','Q4','Q5\n(high)'],fontsize=7.5)
    ax.set_title(n,fontsize=9); ax.axhline(0,color='0.5',lw=0.5)
    ax.set_xlabel('Quintile of abnormal trading value',fontsize=8)
axes[0].set_ylabel('Mean lunch return (%)'); axes[0].legend(frameon=False,fontsize=7,loc='lower left')
fig.tight_layout(); fig.savefig(T+'Figure2.tif',dpi=600,pil_kwargs={'compression':'tiff_lzw'}); fig.savefig(T+'Figure2.png',dpi=200); fig.savefig(T+'Figure2_300.png',dpi=300)
