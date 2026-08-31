from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="root.style.setProperty('--poem-leading',ui.poemSize==='large'?'1.25':'1.15')"
new="root.style.setProperty('--poem-leading',ui.poemSize==='large'?(['georgia','baskerville','helvetica'].includes(ui.poemFont)?'1.32':'1.25'):'1.15')"
if old not in s:
    raise SystemExit('applyTextPrefs leading expression not found')
s=s.replace(old,new,1)
old2="poemLeading=ui.poemSize==='large'?'1.25':'1.15'"
new2="poemLeading=ui.poemSize==='large'?(['georgia','baskerville','helvetica'].includes(ui.poemFont)?'1.32':'1.25'):'1.15'"
if old2 not in s:
    raise SystemExit('comparison leading expression not found')
s=s.replace(old2,new2,1)
p.write_text(s,encoding='utf-8')
print('Set font-aware large leading')
