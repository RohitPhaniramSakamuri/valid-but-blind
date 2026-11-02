"""Inspect this task's fresh anonymous desktop browser, never the user's profile."""
import asyncio,json,urllib.request
from pathlib import Path
import websockets
BASE=Path(__file__).resolve().parent
async def main():
 port=int(Path('/tmp/codex-ssrn-7602585-desktop/DevToolsActivePort').read_text().splitlines()[0])
 with urllib.request.urlopen(f'http://127.0.0.1:{port}/json/list') as r:targets=json.load(r)
 target=next(t for t in targets if t.get('type')=='page')
 async with websockets.connect(target['webSocketDebuggerUrl'],max_size=8_000_000) as ws:
  await ws.send(json.dumps({'id':1,'method':'Runtime.evaluate','params':{'expression':'JSON.stringify({title:document.title,url:location.href,text:document.body.innerText,links:Array.from(document.querySelectorAll("a[href]")).map(a=>({text:a.innerText,href:a.href}))})','returnByValue':True}}))
  while True:
   r=json.loads(await ws.recv())
   if r.get('id')==1:break
  v=r.get('result',{}).get('result',{}).get('value','{}');d=json.loads(v)
  (BASE/'evidence/desktop-page.json').write_text(json.dumps(d,indent=2)+'\n')
  print(json.dumps({'title':d.get('title'),'url':d.get('url'),'text':d.get('text','')[:2200],'links':d.get('links',[])[:20]},indent=2))
asyncio.run(main())
