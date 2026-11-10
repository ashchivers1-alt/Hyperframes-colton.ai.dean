import numpy as np
from scipy.ndimage import gaussian_filter1d
cl=np.load('cl.npy'); X,Y=cl.T; N=len(X)
h=np.unwrap(np.arctan2(np.gradient(Y),np.gradient(X)))
k=gaussian_filter1d(np.gradient(h),8,mode='wrap')
yaw=np.load('yaw.npy')  # 15fps, per-frame px
T_END=83.0
r=gaussian_filter1d(yaw,6)  # ~0.4s
r=r[:int(T_END*15)]
# downsample to 5fps
r5=r.reshape(-1,3).mean(1); M=len(r5)
zr=r5/np.std(r5); zk=k/np.std(k)
K2=np.r_[zk,zk]; W=len(K2)
INF=1e18
D=np.full(W,INF); D[:N]=(zr[0]-K2[:N])**2  # free start in first lap
back=np.zeros((M,W),np.int8)
MAXA=7
for i in range(1,M):
    best=np.full(W,INF); arg=np.zeros(W,np.int8)
    for a in range(0,MAXA+1):
        sh=np.full(W,INF); sh[a:]=D[:W-a] if a else D
        pen = 0.3 if a==0 else 0
        m=sh+pen<best; best[m]=sh[m]+pen; arg[m]=a
    D=best+(zr[i]-K2)**2; back[i]=arg
j=int(np.argmin(D)); end=j
path=[j]
for i in range(M-1,0,-1):
    j-=int(back[i,j]); path.append(j)
path=path[::-1]
print('start idx',path[0]%N,'end idx',end%N,'covered',end-path[0],'cost',D[end]/M)
np.save('map_t.npy',np.array(path))
for i in range(0,M,10): print(f"t={i/5:5.1f} idx={path[i]%N:4d} xy=({int(X[path[i]%N])},{int(Y[path[i]%N])})")
