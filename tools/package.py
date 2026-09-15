from pathlib import Path
import zipfile
r = Path(__file__).resolve().parents[1]
skill = ['SKILL.md','LICENSE','NOTICE.md','templates/master-prompt.md','references/design-and-model-notes.md','scripts/validate_timeline.py','assets/example-timeline.json','examples/desk-organizer.md']
text = r.joinpath('SKILL.md').read_text().split('---',2)[2].strip()
text += '\n\n# Embedded supporting materials\n'
for name in ['templates/master-prompt.md','references/design-and-model-notes.md','examples/desk-organizer.md']:
 text += '\n\n'+r.joinpath(name).read_text()
text += '\n\n# Tool-free use\nThe supporting prose above is embedded, not dependent on local paths. If Python execution or the validator file is unavailable, mark timing UNVERIFIED and provide the manifest for a later check. Never simulate a successful tool result.\n\n'+r.joinpath('LICENSE').read_text()+'\n'+r.joinpath('NOTICE.md').read_text()
r.joinpath('editions/CREATIVE-AD-DIRECTOR.txt').write_text(text)
for name, files in [('creative-ad-director.zip',skill),('creative-ad-director-all-platforms.zip',skill+['README.md','editions/CREATIVE-AD-DIRECTOR.txt','editions/PROJECT-INSTRUCTIONS.txt','editions/STARTER-PROMPT.txt'])]:
 with zipfile.ZipFile(r/name,'w',zipfile.ZIP_DEFLATED) as z:
  for f in files:
   info=zipfile.ZipInfo('creative-ad-director/'+f,date_time=(2026,1,1,0,0,0))
   info.compress_type=zipfile.ZIP_DEFLATED
   z.writestr(info,r.joinpath(f).read_bytes())
 with zipfile.ZipFile(r/name) as z:
  assert z.testzip() is None
  assert len(z.namelist()) == len(files)
 print(name, 'verified entries:',len(files))
