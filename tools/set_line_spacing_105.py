from pathlib import Path
import re
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

# Comparison panes currently use their own 1.6 line-height.
pattern=r'(min-height:60vh[^<]{0,800}?)line-height:1\.6'
s,n=re.subn(pattern,r'\1line-height:1.05',s,count=1)
if n!=1:
    raise SystemExit('Comparison line-height not found')

p.write_text(s,encoding='utf-8')
print('Set poem line spacing to 1.05')
