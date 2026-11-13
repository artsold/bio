import sys
p=sys.argv[1]; s=open(p).read()
def rep(o,n,c=1):
    global s
    assert s.count(o)==c,(o[:60],s.count(o)); s=s.replace(o,n)
rep("<title>Artiom Soldatov — Motion Designer</title>","<title>Artiom Soldatov — Motion Designer & AI Creative Producer</title>")
rep(">Engineering video ads that survive in paid rotation.<",">Video ads built on AI pipelines. Proven in paid rotation.<")
ui='    <span class="marquee-item"><span>—</span>UA Creative</span>\n'
rep(ui, ui+'    <span class="marquee-item"><span>—</span>AI Video</span>\n    <span class="marquee-item"><span>—</span>Gen-AI Assets</span>\n    <span class="marquee-item"><span>—</span>Prompt Engineering</span>\n', 2)
# About: new paragraph after the first one
i=s.index('<div class="about-text'); j=s.index('</p>',i)+4
s=s[:j]+'\n      <p>I build AI production pipelines: scripts and storyboards with LLMs, assets in Seedream / Flux Kontext, animation in Kling / Seedance, final polish in After Effects — so more concepts reach testing, faster.</p>'+s[j:]
# Skills: replace single tag with AI Production group (placed first)
rep('          <span class="tag">AI-Assisted Creative</span>\n','')
rep('''    <div class="about-skills reveal">
      <div class="skill-group">''','''    <div class="about-skills reveal">
      <div class="skill-group">
        <div class="skill-group-label">AI Production</div>
        <div class="skill-tags">
          <span class="tag">Gen-AI Assets</span>
          <span class="tag">AI Animation</span>
          <span class="tag">AI Video</span>
          <span class="tag">Automation</span>
        </div>
      </div>
      <div class="skill-group">''')
rep("Hook frameworks and A/B testing across Tier-1 markets (US/UK/DE) to optimize CPI/ROAS.</div>",
    "Hook frameworks and A/B testing across Tier-1 markets (US/UK/DE) to optimize CPI/ROAS. Built AI production pipelines: scripts with Claude, assets in Seedream / Flux Kontext, animation in Kling / Seedance; automated After Effects scripting and video adaptations.</div>")
open(p,'w').write(s)
