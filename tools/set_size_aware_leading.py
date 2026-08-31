from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

repls=[
("--poem-weight:400}","--poem-weight:400;--poem-leading:1.15}"),
("line-height:1.15;outline:none;white-space:pre-wrap","line-height:var(--poem-leading);outline:none;white-space:pre-wrap"),
("margin-top:9px;line-height:1.15;font-family:var(--poem-font)","margin-top:9px;line-height:var(--poem-leading);font-family:var(--poem-font)"),
("root.style.setProperty('--poem-size',SIZE_MAP[ui.poemSize]);root.style.setProperty('--poem-weight',ui.poemFont==='helvetica'?'300':'400');","root.style.setProperty('--poem-size',SIZE_MAP[ui.poemSize]);root.style.setProperty('--poem-weight',ui.poemFont==='helvetica'?'300':'400');root.style.setProperty('--poem-leading',ui.poemSize==='large'?'1.25':'1.15');"),
("poemWeight=ui.poemFont==='helvetica'?'300':'400';","poemWeight=ui.poemFont==='helvetica'?'300':'400',poemLeading=ui.poemSize==='large'?'1.25':'1.15';"),
("white-space:pre-wrap;line-height:1.6;min-height:60vh","white-space:pre-wrap;line-height:'+poemLeading+';min-height:60vh")
]
for old,new in repls:
    if old not in s:
        raise SystemExit('Expected text not found: '+old)
    s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
print('Applied size-aware leading: 1.15 small/medium, 1.25 large')
