from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

repls = [
(
".editor{min-height:480px;padding:38px 54px;font-family:var(--poem-font);font-size:var(--poem-size);font-weight:var(--poem-weight);line-height:1.7;outline:none;white-space:pre-wrap}",
".editor{min-height:480px;padding:38px 54px;font-weight:var(--poem-weight);line-height:1.7;outline:none;white-space:pre-wrap}.editor,.editor *{font-family:var(--poem-font)!important;font-size:var(--poem-size)!important}"
),
(
".vb{white-space:pre-wrap;margin-top:9px;line-height:1.5;font-family:var(--poem-font);font-size:calc(var(--poem-size)*.76);font-weight:var(--poem-weight)}",
".vb{white-space:pre-wrap;margin-top:9px;line-height:1.5;font-weight:var(--poem-weight)}.vb,.vb *{font-family:var(--poem-font)!important;font-size:calc(var(--poem-size)*.76)!important}"
),
(
"<dialog id=\"textDialog\" class=\"appDialog\"><div class=\"dialogInner\"><h2>Poem text</h2><p>Choose how poems appear while you write, review saved drafts, and compare versions.</p>",
"<dialog id=\"textDialog\" class=\"appDialog\"><div class=\"dialogInner\"><h2>Poem text</h2><p>These settings apply to the <b>whole poem</b>. Selected-text font and size changes are temporarily disabled while that feature is rebuilt safely.</p>"
),
(
".v{background:white;border:1px solid #ddd5ca;border-radius:10px;padding:22px;white-space:pre-wrap;line-height:1.6;min-height:60vh;font-family:'+poemFont+';font-size:'+poemSize+';font-weight:'+poemWeight+'}",
".v{background:white;border:1px solid #ddd5ca;border-radius:10px;padding:22px;white-space:pre-wrap;line-height:1.6;min-height:60vh;font-weight:'+poemWeight+'}.v,.v *{font-family:'+poemFont+'!important;font-size:'+poemSize+'!important}"
)
]

for old,new in repls:
    if old not in s:
        raise SystemExit('Expected text not found: ' + old[:160])
    s = s.replace(old,new,1)

p.write_text(s, encoding='utf-8')
print('Applied whole-poem font/size display override')
