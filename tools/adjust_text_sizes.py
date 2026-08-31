from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="SIZE_MAP={small:'19px',medium:'25px',large:'31px'}"
new="SIZE_MAP={small:'16px',medium:'19px',large:'22px'}"
if old not in s:
    raise SystemExit('Expected SIZE_MAP not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('Adjusted poem text sizes')
