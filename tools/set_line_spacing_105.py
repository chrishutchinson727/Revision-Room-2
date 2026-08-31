from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

pairs=[
('line-height:1.7;outline:none;white-space:pre-wrap','line-height:1.05;outline:none;white-space:pre-wrap'),
('margin-top:9px;line-height:1.5;font-family:var(--poem-font)','margin-top:9px;line-height:1.05;font-family:var(--poem-font)')
]
for old,new in pairs:
    if old not in s:
        raise SystemExit('Expected text not found: '+old)
    s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
print('Set working draft and version history line spacing to 1.05')
