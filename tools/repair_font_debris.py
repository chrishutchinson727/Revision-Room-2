from pathlib import Path

path = Path('index.html')
s = path.read_text(encoding='utf-8')

def replace_once(old, new):
    global s
    if old not in s:
        raise SystemExit('Expected text not found: ' + old[:220])
    s = s.replace(old, new, 1)

# Make whole-poem typography authoritative in editor/history without disturbing bold/italic/underline.
replace_once(
    ".editor{min-height:480px;padding:38px 54px;font-family:var(--poem-font);font-size:var(--poem-size);font-weight:var(--poem-weight);line-height:1.7;outline:none;white-space:pre-wrap}",
    ".editor{min-height:480px;padding:38px 54px;font-family:var(--poem-font);font-size:var(--poem-size);font-weight:var(--poem-weight);line-height:1.7;outline:none;white-space:pre-wrap}.editor,.editor *{font-family:var(--poem-font)!important;font-size:var(--poem-size)!important}.editor *{line-height:inherit}"
)
replace_once(
    ".vb{white-space:pre-wrap;margin-top:9px;line-height:1.5;font-family:var(--poem-font);font-size:calc(var(--poem-size)*.76);font-weight:var(--poem-weight)}",
    ".vb{white-space:pre-wrap;margin-top:9px;line-height:1.5;font-family:var(--poem-font);font-size:calc(var(--poem-size)*.76);font-weight:var(--poem-weight)}.vb,.vb *{font-family:var(--poem-font)!important;font-size:calc(var(--poem-size)*.76)!important}.vb *{line-height:inherit}"
)

# Clarify that typography applies to the whole poem only.
replace_once(
    "<dialog id=\"textDialog\" class=\"appDialog\"><div class=\"dialogInner\"><h2>Poem text</h2><p>Choose how poems appear while you write, review saved drafts, and compare versions.</p>",
    "<dialog id=\"textDialog\" class=\"appDialog\"><div class=\"dialogInner\"><h2>Poem text</h2><p><b>Whole poem only.</b> Choose the display font and size for the poem. Italics, bold, and underline can still be applied to selected text.</p>"
)

# Replace normalize with a sanitizer that removes the corrupt inline typography from all stored material.
old_normalize = "function normalize(s){if(!s||!Array.isArray(s.poems))return fresh();s.schema=4;if(!Array.isArray(s.trash))s.trash=[];if(!s.poems.length){const p=blank();s.poems=[p];s.activePoemId=p.id}if(!s.poems.some(p=>p.id===s.activePoemId))s.activePoemId=s.poems[0].id;for(const p of s.poems){p.versions=Array.isArray(p.versions)?p.versions:[];p.notes=p.notes||'';p.html=p.html||''}return s}"
new_normalize = """function cleanPoemHtml(html){
 const box=document.createElement('div');box.innerHTML=html||'';
 box.querySelectorAll('*').forEach(el=>{
   if(el.hasAttribute('style')){
     el.style.removeProperty('font-family');el.style.removeProperty('font-size');
     const fw=(el.style.fontWeight||'').trim().toLowerCase();
     if(['100','200','300','400','500','normal','lighter'].includes(fw))el.style.removeProperty('font-weight');
     if(!el.getAttribute('style')||!el.getAttribute('style').trim())el.removeAttribute('style');
   }
   el.removeAttribute('face');el.removeAttribute('size');
 });
 box.querySelectorAll('font').forEach(el=>{const p=el.parentNode;while(el.firstChild)p.insertBefore(el.firstChild,el);p.removeChild(el)});
 box.querySelectorAll('span').forEach(el=>{if(el.attributes.length===0){const p=el.parentNode;while(el.firstChild)p.insertBefore(el.firstChild,el);p.removeChild(el)}});
 return box.innerHTML;
}
function cleanStoredPoem(p){if(!p)return;p.versions=Array.isArray(p.versions)?p.versions:[];p.notes=p.notes||'';p.html=cleanPoemHtml(p.html||'');for(const v of p.versions){v.html=cleanPoemHtml(v.html||'');v.notes=v.notes||''}}
function normalize(s){if(!s||!Array.isArray(s.poems))return fresh();s.schema=4;if(!Array.isArray(s.trash))s.trash=[];if(!s.poems.length){const p=blank();s.poems=[p];s.activePoemId=p.id}if(!s.poems.some(p=>p.id===s.activePoemId))s.activePoemId=s.poems[0].id;for(const p of s.poems)cleanStoredPoem(p);for(const p of s.trash)cleanStoredPoem(p);return s}"""
replace_once(old_normalize, new_normalize)

# Persist the repaired browser archive immediately after loading it.
replace_once(
    "let state=load(),ui=loadUI(); const active=()=>state.poems.find(p=>p.id===state.activePoemId)||state.poems[0];",
    "let state=load(),ui=loadUI();localStorage.setItem(KEY,JSON.stringify(state)); const active=()=>state.poems.find(p=>p.id===state.activePoemId)||state.poems[0];"
)

# Ensure comparison windows also ignore stale inline typography.
replace_once(
    ".v{background:white;border:1px solid #ddd5ca;border-radius:10px;padding:22px;white-space:pre-wrap;line-height:1.6;min-height:60vh;font-family:'+poemFont+';font-size:'+poemSize+';font-weight:'+poemWeight+'}",
    ".v{background:white;border:1px solid #ddd5ca;border-radius:10px;padding:22px;white-space:pre-wrap;line-height:1.6;min-height:60vh;font-family:'+poemFont+';font-size:'+poemSize+';font-weight:'+poemWeight+'}.v,.v *{font-family:'+poemFont+'!important;font-size:'+poemSize+'!important}.v *{line-height:inherit}"
)

# Sanity checks.
for needle in ["function cleanPoemHtml", "Whole poem only.", ".editor,.editor *", "for(const p of s.trash)cleanStoredPoem(p)"]:
    if needle not in s:
        raise SystemExit('Repair marker missing: '+needle)

path.write_text(s, encoding='utf-8')
print('Font debris repair migration applied')
