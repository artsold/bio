import sys
p=sys.argv[1]; s=open(p).read()
def rep(o,n,c=1):
    global s
    assert s.count(o)==c,(o[:70],s.count(o)); s=s.replace(o,n)
MAP={"XdeWSCT_XkA":"cf-amusement-park","A3iu7YE_jVM":"cf-fail-hook","QUwZglDG3pQ":"cfd-food-fight","GN_d3L-CyPk":"ac-mexico"}
for vid,f in MAP.items():
    rep(f'{{ id: "{vid}", ',f'{{ id: "{vid}", src: "media/{f}.mp4", poster: "media/{f}.jpg", ')
# card: local <video> when src exists, YouTube otherwise
rep('''        <iframe src="${embedUrl(v.id)}" frameborder="0"
          allow="autoplay; fullscreen; picture-in-picture"
          style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"></iframe>''',
'''        ${v.src
          ? `<video class="car-video" src="${v.src}" poster="${v.poster || ''}" muted autoplay loop playsinline preload="metadata" disablepictureinpicture></video>`
          : `<iframe src="${embedUrl(v.id)}" frameborder="0"
          allow="autoplay; fullscreen; picture-in-picture"
          style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"></iframe>`}''')
# lightbox: own video element for local files (with sound, no controls)
rep('''      <iframe id="lbFrame" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>''',
'''      <iframe id="lbFrame" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>
      <video id="lbVideo" playsinline loop disablepictureinpicture></video>''')
rep('''const lbFrame  = document.getElementById("lbFrame");''','''const lbFrame  = document.getElementById("lbFrame");
const lbVideo  = document.getElementById("lbVideo");''')
rep('''function openLightbox(v) {
  lbFrame.src = embedUrl(v.id);''','''function openLightbox(v) {
  if (v.src) {
    lbFrame.style.display = "none"; lbFrame.src = "";
    lbVideo.style.display = "block"; lbVideo.src = v.src; lbVideo.poster = v.poster || "";
    lbVideo.muted = false; lbVideo.currentTime = 0;
    lbVideo.play().catch(() => { lbVideo.muted = true; lbVideo.play(); });  // fallback if sound is blocked
  } else {
    lbVideo.pause(); lbVideo.removeAttribute("src"); lbVideo.style.display = "none";
    lbFrame.style.display = "block"; lbFrame.src = embedUrl(v.id);
  }''')
rep('''  lbFrame.src = "";
  document.body.style.overflow = "";''','''  lbFrame.src = "";
  lbVideo.pause(); lbVideo.removeAttribute("src"); lbVideo.load();
  document.body.style.overflow = "";''')
# play card videos only while visible (battery / data on phones)
rep('''buildCards();
''','''buildCards();

// Local card videos: play while on screen, pause when off screen
(() => {
  const vids = document.querySelectorAll('.car-video');
  if (!('IntersectionObserver' in window)) return;
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { const p = e.target.play(); if (p) p.catch(() => {}); } else e.target.pause();
  }), { threshold: 0.15 });
  vids.forEach(v => io.observe(v));
})();
''')
rep('''  #lbFrame {''','''  .car-video {
    position: absolute; inset: 0; width: 100%; height: 100%;
    object-fit: cover; display: block; pointer-events: none;
  }
  .car-video::-webkit-media-controls, .car-video::-webkit-media-controls-start-playback-button { display: none !important; }
  #lbVideo {
    display: none; width: 100%; aspect-ratio: 9/16; max-height: 78vh;
    object-fit: contain; background: #000; border: 1px solid var(--line);
  }
  #lbFrame {''')
open(p,'w').write(s)
