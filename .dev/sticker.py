import sys, json, numpy as np
from PIL import Image
from scipy import ndimage as ndi
sys.path.insert(0,'/home/claude/tools'); from grade import f,u8,hexc,natural,contrast
cx,cy,side,out_px=485,512,930,600
full=Image.open('full_srgb.png'); cut=Image.open('full_cut.png')
box=(cx-side//2,cy-side//2,cx-side//2+side,cy-side//2+side)
rgb=f(full.crop(box)); A=np.asarray(cut.crop(box).split()[-1]).astype(np.float32)/255
# 1. smooth "vector" silhouette: heavy blur + soft threshold
sig=side/600*7                       # ~7px at output scale
B=ndi.gaussian_filter(A,sig)
def smoothstep(e0,e1,x): t=np.clip((x-e0)/(e1-e0),0,1); return t*t*(3-2*t)
S=smoothstep(0.42,0.58,B)            # clean rounded contour, ignores stray strands
Sb=S>0.5
# 2. even-width rings via distance transform (anti-aliased)
dist=ndi.distance_transform_edt(~Sb) - ndi.distance_transform_edt(Sb)   # signed, px
k=side/out_px
w_white, w_navy = 9*k, 5*k
white=np.clip(w_white+0.5*k-dist,0,k)/k   # 1 inside ring, AA edge ~1 output px
outer=np.clip(w_white+w_navy+0.5*k-dist,0,k)/k
# 3. subject: grade + density (+8% contrast, slight gamma)
P=json.loads(sys.argv[1]) if len(sys.argv)>1 else None
from grade import skinfix
sub=(skinfix(rgb,**P) if P is not None else natural(rgb)); sub=np.clip(contrast(sub,1.08),0,1)**1.04
# subject alpha: real alpha, but clipped to smooth silhouette dilated a bit (kills stray specks outside ring)
A=A*smoothstep(0.12,0.45,A)
Aclip=A*np.clip((w_white*0.6-dist)/k,0,1)
bg=np.ones_like(rgb)*hexc('#1A1A2E')
o=bg*(1-outer[...,None])+hexc('#FF4B12')*outer[...,None]
o=o*(1-white[...,None])+hexc('#FFFFFF')*white[...,None]
o=o*(1-Aclip[...,None])+sub*Aclip[...,None]
img=u8(o).resize((out_px,out_px),Image.LANCZOS)
name=sys.argv[2] if len(sys.argv)>2 else 'v4b'
img.save(name+'.png'); img.convert('RGB').save(name+'.jpg',quality=88,optimize=True,progressive=True)
print('ok')
