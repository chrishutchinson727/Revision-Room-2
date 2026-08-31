from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="p.title=v.title;p.html=v.html;p.notes=v.notes||'';p.updatedAt=now();persist();render()"
new="p.html=v.html;p.notes=v.notes||'';p.updatedAt=now();persist();render()"
if old not in s:
    raise SystemExit('restore-title pattern not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('Current title will be preserved when restoring a saved draft')
