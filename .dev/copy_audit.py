import sys
p=sys.argv[1]; s=open(p).read()
def rep(o,n,c=1):
    global s
    assert s.count(o)==c,(o[:60],s.count(o)); s=s.replace(o,n)
rep('<span>—</span>6 Years Nordcurrent</span>','<span>—</span>7 Years Nordcurrent</span>',2)
rep('Downloads on titles I work on','Downloads on titles I worked on')
rep('<p>Engineering UA creatives for <strong>Cooking Fever</strong>','<p>Engineered UA creatives for <strong>Cooking Fever</strong>')
i=s.index('<div class="exp-desc">UA creative for Cooking Fever'); j=s.index('</div>',i)
s=s[:i]+'<div class="exp-desc">Produced UA creatives for Cooking Fever (500M+ downloads, 15M MAU) and Airplane Chefs. Owned the full cycle: concept → copy → final video. Ran competitive landscape analysis via Sensor Tower. Developed hook frameworks and A/B tests across Tier-1 markets (US/UK/DE) to optimize CPI/ROAS. Built AI production pipelines: scripts with Claude, assets in Seedream / Flux Kontext, animation in Kling / Seedance; automated After Effects scripting and video adaptations.'+s[j:]
rep('        <div class="hero-eyebrow">','        <div class="hero-status"><span class="dot"></span>Open to UA Creative / Motion roles · Remote</div>\n        <div class="hero-eyebrow">')
rep('  .hero-eyebrow {\n','''  .hero-status {
    display: inline-flex; align-items: center; gap: 10px; width: fit-content; align-self: flex-start; max-width: 100%;
    font-family: var(--font-mono); font-size: calc(11px * var(--label-scale, 1));
    letter-spacing: 0.12em; text-transform: uppercase;
    padding: 8px 16px 8px 12px; margin-bottom: 18px;
    border-radius: var(--radius-pill);
    background: var(--status-bg, var(--text)); color: var(--status-text, var(--page-bg));
    box-shadow: var(--btn-shadow);
    opacity: 0; animation: fadeUp 0.8s 0.2s forwards;
  }
  .hero-status .dot { width: 9px; height: 9px; border-radius: 50%; background: var(--status-dot, var(--accent)); box-shadow: 0 0 0 3px rgba(255,255,255,0.15); }
  .hero-eyebrow {\n''')
# head: icons + meta
i=s.index('<link rel="icon" type="image/x-icon" href="data:'); j=s.index('>',i)+1
s=s[:i]+'''<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png?v=2">
<meta name="description" content="Motion Designer & AI Creative Producer. Video ads built on AI pipelines — UA creatives for Cooking Fever & Airplane Chefs. Open to UA Creative / Motion roles, remote.">
<meta name="theme-color" content="#FF4B12">
<meta property="og:type" content="website">
<meta property="og:url" content="https://souldatov.com/">
<meta property="og:title" content="Artiom Soldatov — Motion Designer & AI Creative Producer">
<meta property="og:description" content="Video ads built on AI pipelines. Proven in paid rotation. Open to UA Creative / Motion roles, remote.">
<meta property="og:image" content="https://souldatov.com/og-image.png?v=1">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://souldatov.com/og-image.png?v=1">'''+s[j:]
rep('<link rel="apple-touch-icon" href="apple-touch-icon.png">','<link rel="apple-touch-icon" href="apple-touch-icon.png?v=2">')
open(p,'w').write(s)
