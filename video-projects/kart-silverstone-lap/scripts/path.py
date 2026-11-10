import numpy as np
from scipy.ndimage import gaussian_filter1d
sk=np.load('sk.npy')
pts=set(map(tuple,np.argwhere(sk)))
# prune spur: remove endpoints iteratively
def nb(p):
    y,x=p; return [(y+dy,x+dx) for dy in(-1,0,1) for dx in(-1,0,1) if (dy or dx) and (y+dy,x+dx) in pts]
changed=True
while changed:
    changed=False
    for p in list(pts):
        if len(nb(p))<=1: pts.discard(p); changed=True
# walk: start at bottom straight point near (745, 700)
start=min(pts,key=lambda p:(p[0]-745)**2+(p[1]-700)**2)
path=[start]; seen={start}; cur=start
# initial direction east
while True:
    c=[q for q in nb(cur) if q not in seen]
    if not c: break
    if len(path)==1: c=sorted(c,key=lambda q:-q[1])
    else: c=sorted(c,key=lambda q:abs(q[0]-cur[0])+abs(q[1]-cur[1]))
    cur=c[0]; path.append(cur); seen.add(cur)
P=np.array(path,float)[:,::-1]  # x,y
print('path len',len(P),'of',len(pts), 'end',P[-1],'start',P[0])
# resample by arclength
d=np.r_[0,np.cumsum(np.hypot(*np.diff(P,axis=0).T))]
L=d[-1]+np.hypot(*(P[0]-P[-1]))
N=1000
s=np.linspace(0,d[-1],N)
X=np.interp(s,d,P[:,0]); Y=np.interp(s,d,P[:,1])
X=gaussian_filter1d(X,4,mode='wrap'); Y=gaussian_filter1d(Y,4,mode='wrap')
np.save('cl.npy',np.c_[X,Y])
h=np.unwrap(np.arctan2(np.gradient(Y),np.gradient(X)))
k=np.gradient(gaussian_filter1d(h,6,mode='nearest'))
print('total turn deg',np.degrees(h[-1]-h[0]),'L',L)
# print heading every 20 samples (screen coords: +turn = clockwise visually = RIGHT turn)
for i in range(0,N,20): print(i, int(X[i]),int(Y[i]), int(np.degrees(h[i])), round(np.degrees(k[i])*N/ (N/100),1))
