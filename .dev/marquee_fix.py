import sys,re
p=sys.argv[1]; s=open(p).read()
def rep(o,n):
    global s
    assert s.count(o)==1,o[:60]; s=s.replace(o,n)
# 1) exactly two identical halves: drop the trailing extra item
a=s.index('<div class="marquee-track">'); b=s.index('</div>',a)
items=re.findall(r'    <span class="marquee-item">.*?</span></span>\n|    <span class="marquee-item"><span>[^<]*</span>[^<]*</span>\n',s[a:b])
half=len(items)//2
assert items[:half]==items[half:2*half], "halves differ"
s=s[:a]+'<div class="marquee-track">\n'+''.join(items[:half]*2)+'  '+s[b:]
# 2) track as wide as its content, so -50% == exactly one half; no pause on hover
rep("""    display: flex;
    white-space: nowrap;
    animation: marquee 22s linear infinite;
  }
  .marquee-track:hover { animation-play-state: paused; }""","""    display: flex;
    width: max-content;          /* -50% must equal exactly one copy of the items */
    white-space: nowrap;
    animation: marquee 60s linear infinite;
    will-change: transform;
  }""")
# 3) constant speed regardless of content width / font scale
rep("</script>\n\n</body>","""
// ── Marquee: constant speed (px/s) whatever the content width
(() => {
  const t = document.querySelector('.marquee-track');
  if (!t) return;
  const SPEED = 40;
  const set = () => { t.style.animationDuration = (t.scrollWidth / 2 / SPEED) + 's'; };
  window.addEventListener('load', set);
  window.addEventListener('resize', set);
})();
</script>
</body>""")
open(p,'w').write(s)
