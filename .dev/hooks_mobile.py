import sys
p=sys.argv[1]; s=open(p).read()
def rep(o,n):
    global s
    assert s.count(o)==1,o[:60]; s=s.replace(o,n)
rep("    display: grid;\n    grid-template-rows: auto 1fr auto;\n","    display: grid;\n    grid-template-rows: auto 1fr auto;\n    grid-template-columns: minmax(0, 1fr);\n")
rep("    .hero-footer { grid-template-columns: 1fr 1fr; }","    .hero-footer { grid-template-columns: minmax(0,1fr) minmax(0,1fr); }")
rep("    .contact-inner { grid-template-columns: 1fr; }","    .contact-inner { grid-template-columns: minmax(0,1fr); }\n    .contact-left, .contact-right, .contact-links, .contact-link { min-width: 0; }\n    .contact-link { overflow-wrap: anywhere; }")
rep("    .about-grid { grid-template-columns: 1fr; }","    .about-grid { grid-template-columns: minmax(0,1fr); }")
open(p,'w').write(s)
