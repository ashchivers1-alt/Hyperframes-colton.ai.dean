import numpy as np, json
from scipy.ndimage import gaussian_filter1d
cl=np.load('cl.npy'); X,Y=cl.T; N=len(X)
h=np.unwrap(np.arctan2(np.gradient(Y),np.gradient(X)))
ak=np.abs(gaussian_filter1d(np.gradient(h),10,mode='wrap'))
inv_v=1+2.0*ak/ak.max()*1.0  # corners up to 3x slower... tuned below
inv_v=1+1.6*(ak/np.percentile(ak,95)).clip(0,1)
A=json.load(open('anchors.json'))
FPS=30; T_END=85.0
ts=np.arange(0,T_END+1e-9,1/FPS); idx=np.zeros_like(ts)
for (t0,i0),(t1,i1) in zip(A[:-1],A[1:]):
    ii=np.arange(int(i0),int(i1)+1)
    w=inv_v[ii%N]; cum=np.r_[0,np.cumsum(w[:-1])]; cum=cum/cum[-1]
    m=(ts>=t0)&(ts<=t1)
    idx[m]=np.interp((ts[m]-t0)/(t1-t0),cum,ii)
# after lap: continue along straight at final speed
tL,iL=A[-1]; m=ts>tL
v=(A[-1][1]-A[-2][1])/(A[-1][0]-A[-2][0])  # avg
idx[m]=iL+(ts[m]-tL)*22
np.save('idx30.npy',idx)
# smooth slightly to avoid kinks at anchors
s=gaussian_filter1d(idx,8,mode='nearest')
s=np.maximum.accumulate(s)
np.save('idx30.npy',s)
# print speed px/s at seconds
sp=np.gradient(s)*FPS*6.83
for t in range(0,85,3): print(t, int(sp[t*FPS]), int(s[t*FPS])%N)
