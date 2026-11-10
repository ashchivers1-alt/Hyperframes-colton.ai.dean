import numpy as np, json, sys
cl=np.load('cl.npy'); N=len(cl); SC=700/1276; OY=30
P=np.c_[cl[:,0]*SC,(cl[:,1]-OY)*SC]
seg=np.hypot(*np.diff(np.r_[P,P[:1]],axis=0).T); cum=np.r_[0,np.cumsum(seg)]; L=cum[-1]
segs=[]
for i in range(0,N,2):
    a=P[i]; b=P[(i+2)%N]
    segs.append([f"M{a[0]:.1f},{a[1]:.1f} L{P[(i+1)%N][0]:.1f},{P[(i+1)%N][1]:.1f} L{b[0]:.1f},{b[1]:.1f}", round(min(cum[i+1]/L,1.0),4)])
open(sys.argv[1],'a').write("window.LAP_PATH.segs="+json.dumps(segs)+";\n")
print(len(segs))
