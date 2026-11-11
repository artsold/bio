import sys
from PIL import Image, ImageChops
for n in ("desktop","mobile"):
    a=Image.open(f"{sys.argv[1]}-{n}.png").convert("RGB"); b=Image.open(f"{sys.argv[2]}-{n}.png").convert("RGB")
    if a.size!=b.size: print(n,"SIZE DIFF",a.size,b.size); continue
    d=ImageChops.difference(a,b); bbox=d.getbbox()
    px=sum(1 for v in d.convert("L").getdata() if v>0)
    print(n, a.size, "identical" if not bbox else f"DIFF px={px} bbox={bbox}")
