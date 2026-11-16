import sys
p=sys.argv[1]; s=open(p).read()
def rep(o,n,c=1):
    global s
    assert s.count(o)==c,(o[:70],s.count(o)); s=s.replace(o,n)
MAP={"XdeWSCT_XkA":"cf-amusement-park","A3iu7YE_jVM":"cf-fail-hook","QUwZglDG3pQ":"cfd-food-fight","GN_d3L-CyPk":"ac-mexico","pAoLSMh7zlQ":"hc-patients","jgUprjQJv28":"mbc-murder","BByox-1JFPk":"mita-crime-novel","mVP9dEkILPo":"sa-squad","wuN-IWKt5Yk":"ws-brand-new"}
for vid,f in MAP.items():
    rep(f'{{ id: "{vid}", ',f'{{ id: "{vid}", src: "media/{f}.mp4", poster: "media/{f}.jpg", ')
# card: local <video> when src exists, YouTube otherwise
rep('''        <iframe src="${embedUrl(v.id)}" frameborder="0"
          allow="autoplay; fullscreen; picture-in-picture"
          style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"></iframe>''',
'''        ${v.src
          ? `<video class="car-video" src="${v.src}" poster="${v.poster || ''}" muted autoplay loop playsinline preload="${i < 5 ? 'auto' : 'metadata'}" disablepictureinpicture></video>`
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

// Local card videos: play whenever any part is on screen, pause when fully off screen.
// Robust against browsers that block or drop autoplay (iOS Low Power Mode, data saver, tab switches).
(() => {
  const vids = [...document.querySelectorAll('.car-video')];
  vids.forEach(v => { v.muted = true; v.defaultMuted = true; v.setAttribute('muted', ''); v.playsInline = true; });
  const onScreen = new Set();
  const tryPlay = v => { if (v.paused) { const p = v.play(); if (p) p.catch(() => {}); } };
  const kick = () => { if (!document.hidden) onScreen.forEach(tryPlay); };
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { onScreen.add(e.target); tryPlay(e.target); }
      else { onScreen.delete(e.target); e.target.pause(); }
    }), { threshold: 0, rootMargin: '0px 120px' });
    vids.forEach(v => io.observe(v));
  } else vids.forEach(v => onScreen.add(v));
  vids.forEach(v => v.addEventListener('canplay', () => { if (onScreen.has(v)) tryPlay(v); }));
  // a tap anywhere unlocks playback where autoplay was refused
  ['touchend', 'click', 'keydown'].forEach(ev => document.addEventListener(ev, kick, { passive: true }));
  document.addEventListener('visibilitychange', kick);
  setInterval(kick, 1500);   // watchdog: restart anything visible that got stalled or paused
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
