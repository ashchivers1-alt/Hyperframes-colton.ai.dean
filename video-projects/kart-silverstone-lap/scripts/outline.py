import numpy as np, json
from PIL import Image
from skimage.morphology import binary_opening, binary_closing, disk
from skimage.measure import label, find_contours
from scipy.ndimage import distance_transform_edt, gaussian_filter1d
im=np.asarray(Image.open('../images/1.jpg').convert('RGB')).astype(int)
w=(im.min(axis=2)>235); w=binary_opening(w,disk(4)); w=binary_closing(w,disk(3))
lab=label(w); s=np.bincount(lab.ravel()); s[0]=0; w=lab==s.argmax()
sk=np.load('sk.npy'); dt=distance_transform_edt(w)
print('half width median',np.median(dt[sk]))
cs=find_contours(np.pad(w,2).astype(float),0.5)
cs=sorted(cs,key=len,reverse=True)[:2]
SC=700/1276; OY=30
out=[]
for c in cs:
    y=gaussian_filter1d(c[:,0]-2,3,mode='wrap'); x=gaussian_filter1d(c[:,1]-2,3,mode='wrap')
    d="M"+" L".join(f"{a*SC:.1f},{(b-OY)*SC:.1f}" for a,b in zip(x[::3],y[::3]))+" Z"
    out.append(d); print(len(c), x.min(),x.max(),y.min(),y.max())
json.dump({"outlines":out,"halfw":float(np.median(dt[sk]))*SC},open('outline.json','w'))
