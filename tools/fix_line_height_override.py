from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
repls={
"el.style.removeProperty('font-family');el.style.removeProperty('font-size');":"el.style.removeProperty('font-family');el.style.removeProperty('font-size');el.style.removeProperty('line-height');",
".editor *{line-height:inherit}":".editor *{line-height:var(--poem-leading)!important}",
".vb *{line-height:inherit}":".vb *{line-height:var(--poem-leading)!important}",
".v *{line-height:inherit}":".v *{line-height:'+poemLeading+'!important}"
}
for old,new in repls.items():
    if old not in s:
        raise SystemExit('Expected text not found: '+old)
    s=s.replace(old,new)
if "removeProperty('line-height')" not in s or "var(--poem-leading)!important" not in s:
    raise SystemExit('Verification failed')
p.write_text(s,encoding='utf-8')
print('Removed stale inline line-height and made poem leading authoritative')
