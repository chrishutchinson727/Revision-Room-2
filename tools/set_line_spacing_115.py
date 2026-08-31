from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
for old,new in [
('line-height:1.10;outline:none;white-space:pre-wrap','line-height:1.15;outline:none;white-space:pre-wrap'),
('margin-top:9px;line-height:1.10;font-family:var(--poem-font)','margin-top:9px;line-height:1.15;font-family:var(--poem-font)')
]:
    if old not in s:
        raise SystemExit('Expected text not found: '+old)
    s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('Set working draft and version history line spacing to 1.15')
