import sys, numpy as np
from PIL import Image
from skimage.morphology import skeletonize, binary_opening, disk, remove_small_objects
from skimage.measure import label
im=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(int)
w=(im.min(axis=2)>235)
w=binary_opening(w,disk(4))
lab=label(w); sizes=np.bincount(lab.ravel()); sizes[0]=0
w=lab==sizes.argmax()
print('track px',w.sum(), w.shape)
sk=skeletonize(w)
ys,xs=np.nonzero(sk); print('skel px',len(xs))
# neighbor counts
from scipy.ndimage import convolve
n=convolve(sk.astype(int),np.ones((3,3),int),mode='constant')-1
n=n*sk
print('endpoints',np.argwhere(n==1).tolist()[:20]); print('junctions',len(np.argwhere(n>=3)))
np.save(sys.argv[2],sk)
out=np.zeros_like(im); out[w]=(60,60,60); out[sk]=(255,0,0)
Image.fromarray(out.astype('uint8')).save(sys.argv[3])
