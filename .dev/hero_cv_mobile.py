import sys,re
p=sys.argv[1]; s=open(p).read()
def rep(o,n):
    global s
    assert s.count(o)==1,o[:70]; s=s.replace(o,n)
btn=re.search(r'        (<a href="CV_ArtiomSoldatov[^\n]*class="hero-cv">.*?</a>)\n',s).group(1)
mob=btn.replace('class="hero-cv"','class="hero-cv hero-cv--mobile"')
# mobile copy right under the photo
i=s.index('<div class="hero-photo-col">'); j=s.index('          <div class="photo-frame"></div>\n        </div>\n',i)+len('          <div class="photo-frame"></div>\n        </div>\n')
s=s[:j]+'        '+mob+'\n'+s[j:]
rep("  .hero-text-col .hero-cv { margin: 28px 0 8px; opacity: 0; animation: fadeUp 0.8s 0.9s forwards; }\n",
"""  .hero-text-col .hero-cv { margin: 28px 0 8px; opacity: 0; animation: fadeUp 0.8s 0.9s forwards; }
  .hero-cv--mobile { display: none; }
  @media (max-width: 768px) {
    .hero-text-col .hero-cv { display: none; }
    .hero-photo-col { flex-direction: column; align-items: flex-start; }
    .hero-cv--mobile { display: inline-flex; margin-top: 4px; opacity: 0; animation: fadeUp 0.8s 0.9s forwards; }
  }
""")
# parallax: photo + mobile button drift together, capped by the lowest visible one
a=s.index("const heroPhoto = document.querySelector('.hero-photo-wrap');")
b=s.index("  window.addEventListener('scroll', drift, { passive: true });\n}",a)+len("  window.addEventListener('scroll', drift, { passive: true });\n}")
s=s[:a]+"""const heroPhoto = document.querySelector('.hero-photo-wrap');
if (heroPhoto) {
  // Parallax: the photo (and, on mobile, the CV button under it) drift down together.
  // Drift is capped by the free space left under them inside .hero-content (overflow:hidden),
  // so nothing gets clipped – on any screen size.
  const heroBox = document.querySelector('.hero-content');
  const mobBtn = document.querySelector('.hero-cv--mobile');
  const movers = () => [heroPhoto, ...(mobBtn && mobBtn.offsetParent ? [mobBtn] : [])];
  let room = 0;
  const measure = () => {
    const els = movers();
    heroPhoto.style.transform = 'none';
    if (mobBtn) mobBtn.style.translate = '0px';
    const ringBottom = heroPhoto.getBoundingClientRect().bottom + 16;   // ring sits ~14px outside the photo
    const btnBottom = els.length > 1 ? mobBtn.getBoundingClientRect().bottom + 8 : 0;  // + button shadow
    room = Math.max(0, heroBox.getBoundingClientRect().bottom - Math.max(ringBottom, btnBottom));
  };
  const drift = () => {
    const y = Math.min(window.scrollY * 0.18, room) + 'px';
    heroPhoto.style.transform = `translateY(${y})`;
    if (mobBtn) mobBtn.style.translate = mobBtn.offsetParent ? `0 ${y}` : '';
  };
  window.addEventListener('load', () => { measure(); drift(); });
  window.addEventListener('resize', () => { measure(); drift(); });
  window.addEventListener('scroll', drift, { passive: true });
}"""+s[b:]
open(p,'w').write(s)
