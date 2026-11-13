import sys, re
src, out, v = sys.argv[1:4]
s = open(src).read()

def hx(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
def rgba(h,a): r,g,b=hx(h); return f"rgba({r},{g},{b},{a})"
def L(h):
    c=[x/255 for x in hx(h)]; c=[x/12.92 if x<=.03928 else ((x+.055)/1.055)**2.4 for x in c]
    return .2126*c[0]+.7152*c[1]+.0722*c[2]
def cr(a,b): a,b=L(a),L(b); return (max(a,b)+.05)/(min(a,b)+.05)

def roles(t):
    fg,fg2,mu,ac,ink,on,bg=t['fg'],t['fg2'],t['muted'],t['accent'],t['ink'],t['on'],t['bg']
    for name,c,need in [('fg',fg,4.5),('fg2',fg2,4.5),('muted',mu,4.5),('ink',ink,4.5),('on/accent',on,4.5)]:
        bgc = ac if name=='on/accent' else bg
        k=cr(c,bgc)
        if k<need: print(f"  WARN {v}:{t['name']} {name} {c} on {bgc} = {k:.2f}")
    over={k:x for k,x in t.items() if k.startswith('--')}
    return {**{
     '--bg':bg,'--text':fg,'--text-2':fg2,'--muted':mu,'--subtle':mu,
     '--accent':ac,'--accent-ink':ink,'--accent-ink-hover':fg,'--on-accent':on,
     '--line':rgba(fg,0.18),'--h2':fg,'--num':ink,'--rule':ac,'--hairline':rgba(fg,0.15),
     '--body':fg2,'--text-3':fg2,'--text-3-hover':fg,'--em':ink,'--desc':fg2,
     '--row-line':rgba(fg,0.12),'--row-mark':ac,'--row-hover':rgba(fg,0.06),
     '--div-bg':rgba(fg,0.06),'--div-line':rgba(fg,0.10),
     '--ctl-border':'transparent','--card-border':'transparent','--card-border-hover':ac,
     '--dot':rgba(fg,0.30),'--dot-hover':rgba(fg,0.6),
     '--tag-border':'transparent','--tag-text':fg,'--tag-bg':rgba(fg,0.10),
     '--card-bg':'rgba(255,255,255,0.14)','--ctl-bg':ac,'--ctl-text':on,
     '--tag-border-h':ac,'--tag-text-h':fg,'--tag-bg-h':rgba(ac,0.25),
    }, **over}

V = {
 "A": dict(  # ROYAL: sky blue + gold, Lilita One
   fonts="family=DM+Mono:ital,wght@0,300;0,400;1,300&family=Lilita+One&family=Nunito:wght@500;700;800",
   display="'Lilita One', 'Nunito', sans-serif", dweight="400", dtrack="0.005em", h2w="400",
   dshadow="0 4px 0 rgba(10,20,60,0.30)", btnshadow="0 5px 0 #C98A00", cardshadow="0 8px 0 rgba(10,20,60,0.22)",
   page="sky",
   themes=[
    dict(name="sky",   bg="#1766D6", fg="#FFFFFF", fg2="#FFFFFF", muted="#E2ECFF", accent="#FFC21A", ink="#FFF1B8", on="#14214F"),
    dict(name="cream", bg="#FFF5DD", fg="#14214F", fg2="#3B4A7A", muted="#5A6690", accent="#FFC21A", ink="#1766D6", on="#14214F"),
    dict(name="royal", bg="#4A2BB8", fg="#FFFFFF", fg2="#ECE6FF", muted="#D4CAFA", accent="#FFC21A", ink="#FFD54A", on="#14214F"),
    dict(name="navy",  bg="#162457", fg="#FFFFFF", fg2="#D3DCF7", muted="#AEBBE6", accent="#FFC21A", ink="#FFD54A", on="#14214F"),
   ],
   map={"about":"cream","work":"royal","experience-block":"navy","education":"cream","contact":"sky"}),
 "B": dict(  # CANDY: grape + yellow + berry, Fredoka
   fonts="family=DM+Mono:ital,wght@0,300;0,400;1,300&family=Fredoka:wght@500;600;700&family=Nunito:wght@500;700;800",
   display="'Fredoka', 'Nunito', sans-serif", dweight="700", dtrack="-0.01em", h2w="700",
   dshadow="0 4px 0 rgba(40,10,80,0.28)", btnshadow="0 5px 0 #D9A400", cardshadow="0 8px 0 rgba(40,10,80,0.20)",
   page="grape",
   themes=[
    dict(name="grape", bg="#6A35E0", fg="#FFFFFF", fg2="#FFFFFF", muted="#E9E0FF", accent="#FFD23F", ink="#FFE680", on="#2A1660"),
    dict(name="cream", bg="#FFF3E6", fg="#2A1660", fg2="#4A3A80", muted="#625596", accent="#FF4D8D", ink="#B0186A", on="#2A1660"),
    dict(name="mint",  bg="#14B8A6", fg="#0B2433", fg2="#0F2F40", muted="#123848", accent="#FFD23F", ink="#5A0F3C", on="#2A1660"),
    dict(name="berry", bg="#BE1B57", fg="#FFFFFF", fg2="#FFFFFF", muted="#FFE8EF", accent="#FFD23F", ink="#FFE680", on="#2A1660"),
   ],
   map={"about":"cream","work":"mint","experience-block":"berry","education":"cream","contact":"grape"},
   extra={"--label-scale":"1.3","--text-scale":"1.3",
          "--photo-filter":"saturate(0.85) contrast(1.08) brightness(1.04)",
          "--photo-filter-hover":"saturate(1) contrast(1.1) brightness(1.06)",
          "--photo-tint":"#6A35E0",
          "--photo-blend":"soft-light","--photo-tint-opacity":"1"}),
 "C": dict(  # PAPER 2: sky + sun + orange, Lilita One with navy outline
   fonts="family=DM+Mono:ital,wght@0,300;0,400;1,300&family=Lilita+One&family=Nunito:wght@500;700;800",
   display="'Lilita One', 'Nunito', sans-serif", dweight="400", dtrack="0.01em", h2w="400",
   dshadow="0 0.07em 0 #102A63", btnshadow="0 5px 0 #102A63", cardshadow="0 8px 0 #102A63",
   page="sky", pagebg="linear-gradient(180deg, #1F86EA 0%, #5CC0F7 100%)",
   themes=[
    dict(name="sky",   bg="#2F9BF0", fg="#0E2556", fg2="#0E2556", muted="#0E2556", accent="#FFB81C", ink="#0E2556", on="#0E2556",
         **{"--h2":"#FFFFFF","--em":"#FFC93C","--rule":"#102A63","--card-bg":"rgba(255,255,255,0.22)"}),
    dict(name="cream", bg="#FFF4DC", fg="#0E2556", fg2="#24386B", muted="#40527F", accent="#FF9F1C", ink="#B23A08", on="#0E2556",
         **{"--h2":"#FFFFFF","--rule":"#FF9F1C"}),
    dict(name="deep",  bg="#1C5FD6", fg="#FFFFFF", fg2="#FFFFFF", muted="#E3EEFF", accent="#FFC93C", ink="#FFE38A", on="#0E2556",
         **{"--h2":"#FFFFFF","--rule":"#FFC93C","--card-bg":"rgba(255,255,255,0.14)"}),
    dict(name="sun",   bg="#FFC21E", fg="#0E2556", fg2="#0E2556", muted="#1F3566", accent="#FF5FC8", ink="#7A1A00", on="#0E2556",
         **{"--h2":"#FFFFFF","--rule":"#102A63"}),
   ],
   map={"about":"cream","work":"deep","experience-block":"sun","education":"cream","contact":"sky"},
   extra={"--label-scale":"1.3","--text-scale":"1.3",
          "--title":"#FFFFFF","--display-stroke":"0.12em","--display-stroke-color":"#102A63","--display-case":"uppercase",
          "--photo-filter":"saturate(1.05) contrast(1.06) brightness(1.05)",
          "--photo-filter-hover":"saturate(1.15) contrast(1.08) brightness(1.08)",
          "--photo-tint":"linear-gradient(200deg, #FFC93C 0%, #2F9BF0 75%)",
          "--photo-blend":"soft-light","--photo-tint-opacity":"0.9"}),
 "D": dict(  # HOT: user palette — flame/orange/gold/ember/cherry + deep navy
   fonts="family=DM+Mono:ital,wght@0,300;0,400;1,300&family=Lilita+One&family=Nunito:wght@500;700;800",
   display="'Lilita One', 'Nunito', sans-serif", dweight="400", dtrack="0.01em", h2w="400",
   dshadow="0 0.07em 0 #1A1A2E", btnshadow="0 5px 0 #1A1A2E", cardshadow="0 8px 0 #1A1A2E",
   page="flame", pagebg="linear-gradient(180deg, #FF4B12 0%, #FF6B35 100%)",
   themes=[
    dict(name="flame",  bg="#FF4B12", fg="#1A1A2E", fg2="#1A1A2E", muted="#1A1A2E", accent="#FFD700", ink="#1A1A2E", on="#1A1A2E",
         **{"--h2":"#FFFFFF","--em":"#FFD700","--rule":"#1A1A2E","--card-bg":"rgba(255,255,255,0.18)"}),
    dict(name="gold",   bg="#FFD700", fg="#1A1A2E", fg2="#1A1A2E", muted="#2A2A44", accent="#FF4B12", ink="#1A1A2E", on="#1A1A2E",
         **{"--h2":"#FFFFFF","--rule":"#FF4B12","--row-mark":"#FF2D55","--tag-bg":"rgba(26,26,46,0.10)"}),
    dict(name="navy",   bg="#1A1A2E", fg="#FFFFFF", fg2="#ECECF4", muted="#BDBDD0", accent="#FF6B35", ink="#FFD700", on="#1A1A2E",
         **{"--h2":"#FFFFFF","--rule":"#FF6B35","--card-bg":"rgba(255,255,255,0.06)","--card-shadow":"0 8px 0 #FF4B12"}),
    dict(name="orange", bg="#FF8C00", fg="#1A1A2E", fg2="#1A1A2E", muted="#1A1A2E", accent="#FF2D55", ink="#1A1A2E", on="#1A1A2E",
         **{"--h2":"#FFFFFF","--rule":"#1A1A2E","--row-mark":"#FF2D55"}),
    dict(name="cherry", bg="#FF2D55", fg="#1A1A2E", fg2="#1A1A2E", muted="#1A1A2E", accent="#FFD700", ink="#1A1A2E", on="#1A1A2E",
         **{"--h2":"#FFFFFF","--em":"#FFD700","--rule":"#1A1A2E"}),
   ],
   map={"about":"gold","work":"navy","experience-block":"orange","education":"gold","contact":"cherry"},
   extra={"--label-scale":"1.3","--text-scale":"1.3",
          "--title":"#FFFFFF","--display-stroke":"0.12em","--display-stroke-color":"#1A1A2E","--display-case":"uppercase",
          "--photo-filter":"saturate(1.1) contrast(1.08)",
          "--photo-filter-hover":"saturate(1.2) contrast(1.1) brightness(1.04)",
          "--photo-tint":"#FF4B12",
          "--photo-blend":"color","--photo-tint-opacity":"0.3"}),
}[v]

def setvar(k,val):
    global s
    s,n=re.subn(rf"(\n\s+{re.escape(k)}:\s*)[^;]+;",lambda m:m.group(1)+val+";",s,count=1); assert n==1,k

# typography + shape
for k,val in {"--font-display":V['display'],"--font-body":"'Nunito', sans-serif","--display-weight":V['dweight'],
    "--display-tracking":V['dtrack'],"--hero-size":"clamp(60px, 9.5vw, 140px)","--h2-size":"clamp(46px, 6.4vw, 84px)",
    "--h2-weight":V['h2w'],"--h2-style":"normal","--h2-tracking":V['dtrack'],"--cta-size":"clamp(38px, 7vw, 100px)",
    "--em-style":"normal","--city-size":"clamp(44px, 5vw, 64px)","--body-weight":"600","--body-size":"19px","--body-leading":"1.6",
    "--desc-size":"17px","--card-label-size":"19px","--card-desc-size":"15px","--display-shadow":V['dshadow'],
    "--radius-pill":"999px","--radius-btn":"16px","--radius-card":"22px","--btn-shadow":V['btnshadow'],
    "--card-shadow":V['cardshadow'],"--noise-opacity":"0"}.items(): setvar(k,val)

extra = V.get('extra', {})
s = s.replace("    /* shape & surface */\n", "    /* variant extras */\n" + "".join(f"    {k}: {val};\n" for k,val in extra.items()) + "\n    /* shape & surface */\n", 1)
T={t['name']:t for t in V['themes']}
# page level = page theme
pg=T[V['page']]; R=roles(pg)
for k,val in R.items():
    if k in ('--bg','--card-bg','--ctl-bg','--ctl-text'): continue
    setvar(k,val)
for k,val in {"--page-bg":pg['bg'],"--bg-gradient":V.get('pagebg',pg['bg']),"--cta":pg['accent'],"--cta-hover-text":pg['on'],
    "--nav-line":pg['accent'],"--line-strong":rgba(pg['fg'],0.4),"--grid":"transparent","--photo-border":pg['fg'],
    "--accent-ring":pg['accent'],"--media-bg":"#0B1230","--overlay":"rgba(10,14,40,0.92)"}.items(): setvar(k,val)

# replace theme blocks
a=s.index("  [data-theme] {"); b=s.index("  /* labels & meta always use the mono face */")
css="  [data-theme] { background: var(--bg); color: var(--inherit-color, var(--text)); }\n\n"
for t in V['themes']:
    css+=f'  [data-theme="{t["name"]}"] {{\n'+"".join(f"    {k}: {val};\n" for k,val in roles(t).items())+"  }\n\n"
s=s[:a]+css+s[b:]
for sec,th in V['map'].items():
    s,n=re.subn(rf'(id="{sec}" data-theme=")[^"]+"',rf'\g<1>{th}"',s); assert n==1,sec
s=re.sub(r"https://fonts.googleapis.com/css2\?[^\"]*?&display=swap",f"https://fonts.googleapis.com/css2?{V['fonts']}&display=swap",s,count=1)
# flat casual extras: filled CV button
s=s.replace("</style>","  @media (max-width: 768px) { :root { --text-scale: 1.1; --label-scale: 1.15; } }\n</style>",1)
s=s.replace("</style>","  .download-btn { background: var(--cta); color: var(--cta-hover-text); border-color: var(--cta); font-weight: 700; }\n  .download-btn:hover { transform: translateY(2px); box-shadow: 0 2px 0 rgba(0,0,0,0.25); }\n</style>",1)
open(out,'w').write(s); print("ok",v)
