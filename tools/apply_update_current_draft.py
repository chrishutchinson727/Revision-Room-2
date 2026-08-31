from pathlib import Path

path = Path('index.html')
s = path.read_text(encoding='utf-8')

def replace_once(old, new):
    global s
    if old not in s:
        raise SystemExit(f'Expected text not found:\n{old[:180]}')
    s = s.replace(old, new, 1)

replace_once(
    '<button class="btn" id="compareBtn">Compare versions</button><button class="btn primary" id="versionBtn">✓ Save version</button>',
    '<button class="btn" id="compareBtn">Compare versions</button><button class="btn" id="updateBtn" hidden>↻ Update current draft</button><button class="btn primary" id="versionBtn">✓ Save version</button>'
)
replace_once('Saving a version also creates a dated recovery copy.', 'Saving or updating a version also creates a dated recovery copy.')
replace_once(
    '<p><b>Storage:</b> browser cache plus your external archive folder. Saved versions are append-only snapshots.</p>',
    '<p><b>Storage:</b> browser cache plus your external archive folder. Updating a saved draft creates a recovery copy first.</p>'
)
replace_once(
    '<dialog id="compareDialog" class="appDialog">',
    '<dialog id="updateDraftDialog" class="appDialog"><div class="dialogInner"><h2 id="updateDraftTitle">Update current draft?</h2><p id="updateDraftText">This replaces the latest saved draft with the current working draft without creating a new draft number.</p><p class="newPoemNote">Revision Room will create a recovery copy first, so the version you replace can still be recovered from your backups.</p><div class="dialogActions"><button class="btn" id="updateCancel" type="button">Cancel</button><button class="btn primary" id="updateConfirm" type="button">Update draft</button></div></div></dialog>\n<dialog id="compareDialog" class="appDialog">'
)

start = s.index('function render(){')
end = s.index('\nfunction autosave()', start)
s = s[:start] + '''function render(){const p=active();$('title').value=p.title;$('editor').innerHTML=p.html||'';$('notes').value=p.notes||'';const list=$('poemList');list.innerHTML='';for(const x of state.poems){const d=document.createElement('div');d.className='item'+(x.id===state.activePoemId?' active':'');d.innerHTML='<b>'+esc(x.title)+'</b><small>'+x.versions.length+' saved version'+(x.versions.length===1?'':'s')+'</small>';d.onclick=()=>{sync();state.activePoemId=x.id;persist();render()};list.appendChild(d)}const n=p.versions.length,unchanged=same(p);$('meta').textContent=n+' saved version'+(n===1?'':'s')+(n?' • '+(unchanged?'Working draft matches latest version':'Working draft has unsaved changes'):'');$('draftLabel').textContent=n?'Working draft — '+(unchanged?'Draft '+n:'revising Draft '+n):'Working draft — not yet saved';$('compareBtn').disabled=n<2;$('trashBtn').disabled=!state.trash.length;$('versionBtn').textContent=n?'✓ Save as Draft '+(n+1):'✓ Save first draft';$('updateBtn').hidden=n===0;$('updateBtn').disabled=n===0||unchanged;$('updateBtn').textContent=n?'↻ Update Draft '+n:'↻ Update current draft';const h=$('history');h.innerHTML='';[...p.versions].reverse().forEach((v,i)=>{const num=n-i,d=document.createElement('div');d.className='version';const stamp=v.updatedAt?'Updated '+new Date(v.updatedAt).toLocaleString():new Date(v.savedAt).toLocaleString();d.innerHTML='<div class="vh"><b>Draft '+num+'</b><span>'+stamp+'</span></div><div class="vb">'+(v.html||'')+'</div><button class="btn" data-restore="'+v.id+'">Restore as working draft</button>';h.appendChild(d)});h.querySelectorAll('[data-restore]').forEach(b=>b.onclick=()=>{const v=p.versions.find(x=>x.id===b.dataset.restore);if(!v)return;p.title=v.title;p.html=v.html;p.notes=v.notes||'';p.updatedAt=now();persist();render()})}''' + s[end:]

old_autosave = "function autosave(){sync();persist();const p=active(),n=p.versions.length;$('meta').textContent=n+' saved version'+(n===1?'':'s')+(n?' • '+(same(p)?'Working draft matches latest version':'Working draft has unsaved changes'):'');const activeItem=document.querySelector('.item.active b');if(activeItem)activeItem.textContent=p.title}"
new_autosave = "function autosave(){sync();persist();const p=active(),n=p.versions.length,unchanged=same(p);$('meta').textContent=n+' saved version'+(n===1?'':'s')+(n?' • '+(unchanged?'Working draft matches latest version':'Working draft has unsaved changes'):'');$('draftLabel').textContent=n?'Working draft — '+(unchanged?'Draft '+n:'revising Draft '+n):'Working draft — not yet saved';$('versionBtn').textContent=n?'✓ Save as Draft '+(n+1):'✓ Save first draft';$('updateBtn').hidden=n===0;$('updateBtn').disabled=n===0||unchanged;$('updateBtn').textContent=n?'↻ Update Draft '+n:'↻ Update current draft';const activeItem=document.querySelector('.item.active b');if(activeItem)activeItem.textContent=p.title}"
replace_once(old_autosave, new_autosave)

old_recovery = "async function recovery(reason){if(!dir)return;try{if(!await permission(dir,true))return;const d=await dir.getDirectoryHandle('Revision Room Backups',{create:true});const n='revision-room-'+reason+'-'+now().replace(/[:.]/g,'-')+'.json';const fh=await d.getFileHandle(n,{create:true}),w=await fh.createWritable();await w.write(JSON.stringify(archive(),null,2));await w.close()}catch(e){console.warn(e)}}"
new_recovery = "async function recovery(reason){if(!dir)return false;try{if(!await permission(dir,true))return false;const d=await dir.getDirectoryHandle('Revision Room Backups',{create:true});const n='revision-room-'+reason+'-'+now().replace(/[:.]/g,'-')+'.json';const fh=await d.getFileHandle(n,{create:true}),w=await fh.createWritable();await w.write(JSON.stringify(archive(),null,2));await w.close();return true}catch(e){console.warn(e);return false}}"
replace_once(old_recovery, new_recovery)

old_version = "$('versionBtn').onclick=async()=>{sync();const p=active();p.versions.push({id:crypto.randomUUID(),savedAt:now(),title:p.title,html:p.html,notes:p.notes});persist();render();await writeMain(false);await recovery('saved-version')};"
new_version = """$('versionBtn').onclick=async()=>{sync();const p=active();p.versions.push({id:crypto.randomUUID(),savedAt:now(),title:p.title,html:p.html,notes:p.notes});persist();render();await writeMain(false);await recovery('saved-version')};
$('updateBtn').onclick=()=>{sync();const p=active(),n=p.versions.length;if(!n||same(p))return;$('updateDraftTitle').textContent='Update Draft '+n+'?';$('updateDraftText').textContent='This will replace Draft '+n+' with your current working draft. It will remain Draft '+n+' rather than becoming Draft '+(n+1)+'.';$('updateConfirm').textContent='Update Draft '+n;$('updateDraftDialog').showModal()};
$('updateCancel').onclick=()=>$('updateDraftDialog').close();
$('updateConfirm').onclick=async()=>{sync();const p=active(),n=p.versions.length;if(!n)return;$('updateDraftDialog').close();const before=JSON.stringify(archive(),null,2);let protectedCopy=dir?await recovery('before-update-draft-'+n):false;if(!protectedCopy){download('revision-room-before-update-draft-'+n+'-'+now().slice(0,10)+'.json',before)}const old=p.versions[n-1],stamp=now();p.versions[n-1]={...old,title:p.title,html:p.html,notes:p.notes,updatedAt:stamp};persist();render();await writeMain(false);await recovery('updated-draft-'+n)};
$('updateDraftDialog').addEventListener('click',e=>{if(e.target===$('updateDraftDialog'))$('updateDraftDialog').close()});"""
replace_once(old_version, new_version)

# Basic sanity checks before writing.
for needle in ['id="updateBtn"', 'id="updateDraftDialog"', 'Save as Draft ', 'before-update-draft-', 'updatedAt:stamp']:
    if needle not in s:
        raise SystemExit(f'Missing expected result: {needle}')

path.write_text(s, encoding='utf-8')
print('Patched index.html successfully')
