import sys,re
p,v=sys.argv[1],sys.argv[2]; s=open(p).read()
def rep(o,n):
    global s
    assert s.count(o)==1,o[:60]; s=s.replace(o,n)
icon=re.search(r'(<svg[^>]*><path d="M21 15v4[^\n]*?</svg>)',s).group(1)
href=re.search(r'href="(CV_ArtiomSoldatov\.pdf\?v=[^"]+)"',s).group(1)
btn=f'<a href="{href}" download="CV_ArtiomSoldatov.pdf" class="hero-cv">{icon}<span>Download CV</span></a>'
css="""
  /* ── HERO CV BUTTON ── */
  .hero-cv {
    display: inline-flex; align-items: center; gap: 10px; width: fit-content;
    font-family: var(--font-display); font-size: var(--hero-cv-size, 20px); letter-spacing: 0.03em;
    text-transform: uppercase; line-height: 1;
    padding: 16px 26px 14px; border-radius: var(--radius-btn);
    background: var(--hero-cv-bg, var(--cta)); color: var(--hero-cv-text, var(--on-accent));
    box-shadow: var(--btn-shadow);
    transition: transform 0.15s, box-shadow 0.15s;
  }
  .hero-cv svg { width: 1em; height: 1em; stroke-width: 2.6; }
  .hero-cv:hover { transform: translateY(2px); box-shadow: 0 2px 0 var(--hero-cv-edge, #1A1A2E); }
  .hero-cv:active { transform: translateY(5px); box-shadow: none; }
"""
if v=="A":   # under the name, primary CTA
    rep('          <span class="logo-surname">Soldatov</span>\n        </div>\n','          <span class="logo-surname">Soldatov</span>\n        </div>\n        '+btn+'\n')
    css+="  .hero-text-col .hero-cv { margin: 28px 0 8px; opacity: 0; animation: fadeUp 0.8s 0.9s forwards; }\n"
elif v=="B": # top-right of the nav bar
    rep('    </nav>\n  </div>','    </nav>\n    '+btn+'\n  </div>')
    css+="  .header-top .hero-cv { --hero-cv-size: 14px; padding: 11px 18px 9px; }\n  @media (max-width: 768px) { .header-top .hero-cv span { display: none; } .header-top .hero-cv { padding: 10px 12px; } }\n"
rep("</style>",css+"</style>")
open(p,'w').write(s)
