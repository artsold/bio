import sys, asyncio, json
sys.path.insert(0,"/home/claude/tools")
from playwright.async_api import async_playwright
import importlib.util
spec=importlib.util.spec_from_file_location("shot_mod","/home/claude/tools/shot.py")
src=open("/home/claude/tools/shot.py").read().split("async def main")[0]
ns={}; exec(src.replace("html, outprefix = sys.argv[1], sys.argv[2]",""),ns)
SELS=[".tag",".exp-item",".car-card",".car-dot",".car-arrow.car-next",".contact-link","nav a",".download-btn",".hero-photo"]
PROPS=["color","backgroundColor","borderTopColor","borderBottomColor","borderLeftColor","fontFamily"]
JS="""(props)=>{const out=[];document.querySelectorAll('body *').forEach((e,i)=>{const c=getComputedStyle(e);const b=getComputedStyle(e,'::before');const a=getComputedStyle(e,'::after');out.push([i,e.tagName,e.className,...props.map(p=>c[p]),b.backgroundColor,a.backgroundColor])});return out}"""
def norm(rows):
    # known & accepted: CV button fallback chain 'DM Mono','Courier New' -> token (DM Mono always loads)
    return [[x.replace('"DM Mono", "Courier New", monospace','"DM Mono", monospace') if isinstance(x,str) else x for x in r] for r in rows]
async def run(html):
    res={}
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        pg=await b.new_page(viewport={"width":1440,"height":900})
        await pg.route("**/*",ns["router"]); await pg.goto("file://"+html); await pg.add_style_tag(content=ns["FREEZE"]); await pg.wait_for_timeout(1500)
        res["static"]=norm(await pg.evaluate(JS,PROPS))
        for s in SELS:
            els=await pg.query_selector_all(s)
            for k,e in enumerate(els):
                try:
                    await e.scroll_into_view_if_needed(); await e.hover(force=True); await pg.wait_for_timeout(50)
                    res[f"{s}#{k}"]=norm(await pg.evaluate(JS,PROPS))
                except Exception as ex: res[f"{s}#{k}"]=str(ex)[:60]
        await b.close()
    return res
async def main():
    A=await run(sys.argv[1]); B=await run(sys.argv[2])
    bad=0
    for k in A:
        if A[k]!=B.get(k):
            diffs=[(x,y) for x,y in zip(A[k],B[k]) if x!=y] if isinstance(A[k],list) else [(A[k],B.get(k))]
            bad+=1; print("DIFF",k,str(diffs[:1])[:300])
    print("states checked:",len(A),"diffs:",bad)
asyncio.run(main())
