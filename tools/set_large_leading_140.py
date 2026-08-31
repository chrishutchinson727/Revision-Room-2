from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old1="root.style.setProperty('--poem-leading',ui.poemSize==='large'?(['georgia','baskerville','helvetica'].includes(ui.poemFont)?'1.32':'1.25'):'1.15')"
new1="root.style.setProperty('--poem-leading',ui.poemSize==='large'?'1.40':'1.15')"
old2="poemLeading=ui.poemSize==='large'?(['georgia','baskerville','helvetica'].includes(ui.poemFont)?'1.32':'1.25'):'1.15'"
new2="poemLeading=ui.poemSize==='large'?'1.40':'1.15'"
if old1 not in s: raise SystemExit('editor leading pattern not found')
if old2 not in s: raise SystemExit('comparison leading pattern not found')
s=s.replace(old1,new1,1).replace(old2,new2,1)
p.write_text(s,encoding='utf-8')
print('Large leading set to 1.40')
