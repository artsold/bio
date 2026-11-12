import sys
p=sys.argv[1]; s=open(p).read()
o="  .logo-name, .logo-surname, h2, .contact-cta { text-shadow: var(--display-shadow); }\n"
assert s.count(o)==1
s=s.replace(o,o+"""  .logo-name, .logo-surname, h2, .contact-cta, .contact-city, .stat-num {
    -webkit-text-stroke: var(--display-stroke, 0) var(--display-stroke-color, transparent);
    paint-order: stroke fill;
  }
  .logo-name, .logo-surname, h2 { text-transform: var(--display-case, none); }
""")
open(p,'w').write(s)
