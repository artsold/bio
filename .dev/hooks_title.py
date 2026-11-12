import sys
p=sys.argv[1]; s=open(p).read()
for o,n in [("  .logo-name { color: var(--text); }","  .logo-name { color: var(--title, var(--text)); }"),
            ("    font-weight: var(--display-weight);\n    color: var(--text-2);\n    line-height: 1;","    font-weight: var(--display-weight);\n    color: var(--title, var(--text-2));\n    line-height: 1;"),
            ("    line-height: 0.9;\n    color: var(--text);\n  }","    line-height: 0.9;\n    color: var(--title, var(--text));\n  }")]:
    assert s.count(o)==1,o; s=s.replace(o,n)
open(p,'w').write(s)
