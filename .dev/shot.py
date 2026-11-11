import sys, asyncio
from playwright.async_api import async_playwright
import glob, os, re, urllib.parse
FONTROOT="/home/claude/fonts"
def font_css(url):
    q=urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    css=""
    for fam in q.get("family",[]):
        name=fam.split(":")[0].replace("+"," ")
        slug=name.lower().replace(" ","-")
        for f in glob.glob(f"{FONTROOT}/fontsource-{slug}-*/package/files/{slug}-latin-*-*.woff2"):
            m=re.search(r"latin-(\d+)-(normal|italic)\.woff2$",f)
            if not m: continue
            css+=f"@font-face{{font-family:'{name}';font-style:{m.group(2)};font-weight:{m.group(1)};src:url(https://fonts.local/{urllib.parse.quote(f)}) format('woff2');}}\n"
    return css
async def router(route):
    u=route.request.url
    if "fonts.googleapis.com" in u:
        await route.fulfill(status=200, content_type="text/css", body=font_css(u))
    elif u.startswith("https://fonts.local/"):
        path=urllib.parse.unquote(u[len("https://fonts.local"):])
        await route.fulfill(status=200, content_type="font/woff2", body=open(path,"rb").read(), headers={"Access-Control-Allow-Origin":"*"})
    else:
        await route.continue_()
html, outprefix = sys.argv[1], sys.argv[2]
FREEZE = "*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition:none!important;caret-color:transparent!important}"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        for name,(w,h,m) in {"desktop":(1440,900,False),"mobile":(390,844,True)}.items():
            pg = await b.new_page(viewport={"width":w,"height":h}, device_scale_factor=1, is_mobile=m, has_touch=m)
            await pg.route("**/*", router)
            await pg.goto("file://"+html, wait_until="load")
            await pg.add_style_tag(content=FREEZE)
            H = await pg.evaluate("document.body.scrollHeight")
            y=0
            while y < H:
                await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(120); y += h//2
            await pg.evaluate("window.scrollTo(0,0)")
            await pg.wait_for_timeout(3000)
            await pg.evaluate("document.fonts.ready")
            await pg.screenshot(path=f"{outprefix}-{name}.png", full_page=True)
        await b.close()
asyncio.run(main())
