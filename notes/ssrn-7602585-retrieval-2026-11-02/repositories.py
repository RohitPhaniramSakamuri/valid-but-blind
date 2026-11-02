"""Final public repository/author-record discovery, no authentication."""
import concurrent.futures,hashlib,json,re,urllib.request
from pathlib import Path
BASE=Path(__file__).resolve().parent;OUT=BASE/'evidence'
urls=[
 ('orcid','https://pub.orcid.org/v3.0/0000-0001-9252-8475/record'),
 ('openaire','https://api.openaire.eu/search/publications?doi=10.2139%2Fssrn.7602585&format=json'),
 ('zenodo','https://zenodo.org/api/records?q=%227602585%22&size=10'),
 ('scholar','https://scholar.google.com/scholar?q=%22Diagnosing+and+repairing+the+conformal+coverage+guarantee%22'),
 ('ssrn_text','http://papers.ssrn.com/sol3/papers.cfm?abstract_id=7602585'),
 ('ssrn_cache','https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7602585&download=yes'),
]
def get(item):
 name,url=item;r={'date':'2026-11-02','name':name,'url':url}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0','Accept':'application/json,text/html,application/pdf;q=0.9,*/*;q=0.8'})
  with urllib.request.urlopen(req,timeout=22) as res:
   body=res.read();r.update(status=res.status,final_url=res.url,content_type=res.headers.get('Content-Type',''))
  pdf=body.lstrip().startswith(b'%PDF-');path=OUT/(name+('.pdf' if pdf else '.json' if 'json' in r['content_type'] else '.html'));path.write_bytes(body)
  r.update(file=str(path.relative_to(BASE)),is_pdf=pdf,bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
 except Exception as e:r['error']=str(e)
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(get,urls))
(BASE/'repository-manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
for r in rows:print(json.dumps(r))
