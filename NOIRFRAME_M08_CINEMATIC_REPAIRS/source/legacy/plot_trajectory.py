from pathlib import Path
import gzip,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];fig,axes=plt.subplots(2,1,figsize=(10,6),layout='constrained')
for ax,k in zip(axes,['STAIRS','KEY_DOOR']):
 for tag,col in [('C02','#be665a'),('C03','#1d8d92')]:
  d=json.load(gzip.open(R/'reports'/f'{k}_M03_{tag}_1080_STATE.json.gz','rt'));p=np.array([s['pose']['root'] for s in d['state']]);a=np.linalg.norm(np.diff(p,n=2,axis=0)*900,axis=1);ax.plot(np.arange(1,len(p)-1)/30,a,label=f'{tag}: peak {a.max():.2f} m/s²',color=col,lw=1.6)
 ax.set_title(k.replace('_',' '));ax.set_ylabel('Pelvis acceleration (m/s²)');ax.set_xlabel('Time (seconds)');ax.grid(alpha=.2);ax.legend()
fig.suptitle('Actual exported rig states — fixed contacts retained\nNumerical trajectory evidence, not artistic approval',fontsize=12);fig.savefig(R/'reviews/PELVIS_TRAJECTORY_COMPARISON.png',dpi=150);plt.close(fig)
