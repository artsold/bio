import sys
p=sys.argv[1]; s=open(p).read()
def rep(o,n):
    global s
    assert s.count(o)==1,(o[:50],s.count(o)); s=s.replace(o,n)
rep('const VIDEOS = [\n', '''const VIDEOS = [
  { id: "XdeWSCT_XkA", label: "Cooking Fever", ai: true, tag: "AI-generated",
    desc: "Appetite is the hook. Under the lights of the amusement park, one perfect hot dog turns a crowd into customers — and a food truck into an empire. Fully AI-generated, from script to final frame." },
''')
rep('''      <div class="car-thumb">
''','''      <div class="car-thumb">
        ${v.ai ? '<span class="car-badge">AI</span>' : ''}
''')
rep("  .lb-tag {","""  .car-badge {
    position: absolute; top: 10px; left: 10px; z-index: 3;
    font-family: var(--font-display); font-size: 16px; letter-spacing: 0.04em; line-height: 1;
    padding: 6px 10px 5px; border-radius: var(--radius-btn);
    background: var(--accent); color: var(--on-accent);
    box-shadow: var(--btn-shadow); pointer-events: none;
  }
  .lb-tag {""")
open(p,'w').write(s)
