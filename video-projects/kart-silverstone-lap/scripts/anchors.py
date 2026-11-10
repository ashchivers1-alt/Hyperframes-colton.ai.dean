import numpy as np, json
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks
cl=np.load('cl.npy'); X,Y=cl.T; N=len(X)
h=np.unwrap(np.arctan2(np.gradient(Y),np.gradient(X)))
k=gaussian_filter1d(np.gradient(h),8,mode='wrap'); ak=np.abs(k)
path=np.load('map_t.npy')  # 5fps, unwrapped idx
t5=np.arange(len(path))/5
pk,_=find_peaks(np.r_[ak,ak],height=np.percentile(ak,62),distance=10)
pk=[p for p in pk if path[0]+5<p<path[-1]-5]
anchors=[(0.0,float(path[0]))]
for p in pk:
    i=np.searchsorted(path,p)  # first time reaching apex
    # time where path crosses p: take middle of samples at p
    js=np.nonzero(path==p)[0]
    t=t5[js].mean() if len(js) else t5[i]
    anchors.append((float(t),float(p)))
anchors.append((83.4,float(path[0]+N)))  # lap complete at S/F
anchors.sort()
for a in anchors: print(f"{a[0]:6.2f} idx {a[1]:7.1f} ({int(X[int(a[1])%N])},{int(Y[int(a[1])%N])}) |k|={ak[int(a[1])%N]:.3f}")
json.dump(anchors,open('anchors.json','w'))
