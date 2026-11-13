# Redesign safety kit

Not deployed (GitHub Pages/Jekyll ignores dot-folders).

## Rules
1. Never edit `main` directly during redesign. Work in `redesign`, merge after approval.
2. Rollback point: tag `pre-redesign`.
3. Component CSS uses only `var(--token)`. Colors/fonts live in `:root` and `[data-theme="..."]`.
4. Section look = `data-theme` attribute in HTML. Theme look = token values.
5. Every change: screenshots desktop 1440 + mobile 390, diff vs previous.

## Checks
```
python3 .dev/shot.py /abs/path/old.html shots/a      # full-page screenshots, animations frozen
python3 .dev/shot.py /abs/path/new.html shots/b
python3 .dev/diff.py shots/a shots/b                   # pixel diff
python3 .dev/hovercheck.py old.html new.html           # computed colors incl. hover states
```
Fonts are served locally from fontsource packages (`npm pack @fontsource/<name>` into FONTROOT).

## Legacy notes
Tokens marked LEGACY reproduce old hover/inherit quirks (dead hovers caused by #id specificity).
Revisit them in the redesign.

## Photo pipeline
Source: `photo-source.jpg` (iPhone, Display P3). Pipeline: P3 -> sRGB, rembg (u2net_human_seg) cutout,
head centered (cx=485, cy=512, side=930), smoothed silhouette + even rings (white 9px, Flame 5px) on Deep Navy,
skin fix E: `{"hue":20,"hue_amt":0.75,"sat_target":0.36,"sat_amt":0.7,"shine":0.6}`, contrast +8%.
Run from a folder with full_srgb.png / full_cut.png: `python3 sticker.py '<json>' out`. CSS photo filters are off.
