# Selective HSL: hue band red..orange (skin). Lower lightness, add saturation.
import sys, numpy as np
from PIL import Image
src,out,ldrop,sgain=sys.argv[1],sys.argv[2],float(sys.argv[3]),float(sys.argv[4])
a=np.asarray(Image.open(src).convert('RGB')).astype(np.float32)/255
r,g,b=a[...,0],a[...,1],a[...,2]
mx=a.max(-1); mn=a.min(-1); d=mx-mn; L=(mx+mn)/2
S=np.where(d==0,0,d/(1-np.abs(2*L-1)+1e-6))
h=np.zeros_like(L)
m=d>0
rc=np.where(m&(mx==r),((g-b)/(d+1e-6))%6,0); gc=np.where(m&(mx==g),(b-r)/(d+1e-6)+2,0); bc=np.where(m&(mx==b),(r-g)/(d+1e-6)+4,0)
h=np.where(mx==r,rc,np.where(mx==g,gc,bc))*60; h=np.where(m,h,0)%360
# weight: reds 345..360/0..15 and oranges 15..45 full, soft falloff 30° on each side
hh=np.where(h>180,h-360,h)            # -180..180
w=np.clip(1-np.maximum(0,np.maximum(-15-hh,hh-45))/30,0,1)
w*=np.clip(S/0.12,0,1)                # ignore near-grey pixels
L2=L*(1-ldrop*w)
S2=np.clip(S*(1+sgain*w),0,1)
C=(1-np.abs(2*L2-1))*S2; X=C*(1-np.abs((h/60)%2-1)); m0=L2-C/2
hi=(h//60).astype(int)%6
z=np.zeros_like(C)
R=np.choose(hi,[C,X,z,z,X,C]); G=np.choose(hi,[X,C,C,X,z,z]); B=np.choose(hi,[z,z,X,C,C,X])
o=np.stack([R+m0,G+m0,B+m0],-1)
Image.fromarray((np.clip(o,0,1)*255+0.5).astype(np.uint8)).save(out,quality=90)
