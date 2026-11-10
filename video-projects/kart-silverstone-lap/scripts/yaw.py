import sys,glob,numpy as np
from PIL import Image
from skimage.registration import phase_cross_correlation
fs=sorted(glob.glob(sys.argv[1]+'/*.png'))
prev=None; sh=[]
for f in fs:
    a=np.asarray(Image.open(f)).astype(float)
    a=a-a.mean()
    if prev is not None:
        s,_,_=phase_cross_correlation(prev,a,upsample_factor=10,normalization=None)
        sh.append(s[1])
    prev=a
sh=np.array(sh); np.save(sys.argv[2],sh)
c=np.cumsum(sh)
print('n',len(sh),'total',c[-1])
for i in range(0,len(c),15): print(f"{i/15:5.1f} {c[i]:8.1f} {sh[i:i+15].sum():7.1f}")
