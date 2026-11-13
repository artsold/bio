import numpy as np
from PIL import Image, ImageFilter
def f(img): return np.asarray(img).astype(np.float32)/255
def u8(a): return Image.fromarray((np.clip(a,0,1)*255+.5).astype(np.uint8))
def hexc(h): return np.array([int(h[i:i+2],16) for i in (1,3,5)],np.float32)/255
def lum(a): return a[...,0]*.2126+a[...,1]*.7152+a[...,2]*.0722
def contrast(a,k,pivot=.5): return (a-pivot)*k+pivot
def sat(a,k): l=lum(a)[...,None]; return l+(a-l)*k
def wb(a,r=1,g=1,b=1): return a*np.array([r,g,b],np.float32)
def skin(a,ldrop,sgain):
    import colorsys
    mx=a.max(-1); mn=a.min(-1); d=mx-mn; L=(mx+mn)/2
    S=np.where(d==0,0,d/(1-np.abs(2*L-1)+1e-6))
    r,g,b=a[...,0],a[...,1],a[...,2]
    h=np.where(mx==r,((g-b)/(d+1e-6))%6,np.where(mx==g,(b-r)/(d+1e-6)+2,(r-g)/(d+1e-6)+4))*60
    h=np.where(d>0,h,0)%360; hh=np.where(h>180,h-360,h)
    w=np.clip(1-np.maximum(0,np.maximum(-15-hh,hh-45))/30,0,1)*np.clip(S/.12,0,1)
    L2=L*(1-ldrop*w); S2=np.clip(S*(1+sgain*w),0,1)
    C=(1-np.abs(2*L2-1))*S2; X=C*(1-np.abs((h/60)%2-1)); m=L2-C/2; z=np.zeros_like(C); i=(h//60).astype(int)%6
    return np.stack([np.choose(i,[C,X,z,z,X,C])+m,np.choose(i,[X,C,C,X,z,z])+m,np.choose(i,[z,z,X,C,C,X])+m],-1)
def splittone(a,shadow,high,amt=.25,bal=.5):
    l=lum(a)[...,None]; ws=np.clip((bal-l)/bal,0,1); wh=np.clip((l-bal)/(1-bal),0,1)
    return a+(hexc(shadow)-.5)*ws*amt*2*0.5+(hexc(high)-.5)*wh*amt
def gradmap(a,stops):
    l=np.clip(contrast(lum(a),1.15),0,1); out=np.zeros(a.shape,np.float32)
    xs=[s for s,_ in stops]; cs=[hexc(c) for _,c in stops]
    for ch in range(3): out[...,ch]=np.interp(l,xs,[c[ch] for c in cs])
    return out
def natural(a): return np.clip(contrast(skin(wb(a,1.04,1.0,0.93),0.06,0.12),1.06),0,1)

def rgb2hls(a):
    mx=a.max(-1); mn=a.min(-1); d=mx-mn; L=(mx+mn)/2
    S=np.where(d==0,0,d/(1-np.abs(2*L-1)+1e-6))
    r,g,b=a[...,0],a[...,1],a[...,2]
    h=np.where(mx==r,((g-b)/(d+1e-6))%6,np.where(mx==g,(b-r)/(d+1e-6)+2,(r-g)/(d+1e-6)+4))*60
    return np.where(d>0,h,0)%360,L,np.clip(S,0,1)
def hls2rgb(h,L,S):
    C=(1-np.abs(2*L-1))*S; X=C*(1-np.abs((h/60)%2-1)); m=L-C/2; z=np.zeros_like(C); i=(h//60).astype(int)%6
    return np.stack([np.choose(i,[C,X,z,z,X,C])+m,np.choose(i,[X,C,C,X,z,z])+m,np.choose(i,[z,z,X,C,C,X])+m],-1)
def skinfix(a, hue=20, hue_amt=0.8, sat_target=0.38, sat_amt=0.6, even=0.5, ldelta=0.0, shine=0.0):
    """Skin band 320..50deg: pull hue toward `hue`, saturation toward target (evens blotches), lightness shift, tame highlights."""
    h,L,S=rgb2hls(a)
    hh=np.where(h>180,h-360,h)
    w=np.clip(1-np.maximum(0,np.maximum(-40-hh,hh-50))/25,0,1)*np.clip(S/0.08,0,1)*np.clip((L-0.12)/0.15,0,1)
    dh=((hue-hh+180)%360)-180
    h2=(hh+dh*hue_amt*w)%360
    S2=S+(sat_target-S)*sat_amt*w*even + (sat_target-S)*sat_amt*w*(1-even)*0
    L2=L+ldelta*w
    if shine: L2=L2-np.clip(L2-0.78,0,1)*shine*w
    return np.clip(hls2rgb(h2,np.clip(L2,0,1),np.clip(S2,0,1)),0,1)
