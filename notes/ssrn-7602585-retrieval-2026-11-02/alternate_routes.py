"""Discover public repository/metadata links and SSRN's public delivery routes."""
import concurrent.futures,hashlib,json,re,urllib.request
from pathlib import Path
BASE=Path(__file__).resolve().parent;OUT=BASE/'evidence'
items=[
 ('crossref','https://api.crossref.org/works/10.2139/ssrn.7602585'),
 ('openalex','https://api.openalex.org/works/https://doi.org/10.2139/ssrn.7602585'),
 ('semantic','https://api.semanticscholar.org/graph/v1/paper/DOI:10.2139/ssrn.7602585?fields=title,authors,openAccessPdf,url,externalIds'),
 ('jina_landing','https://r.jina.ai/https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7602585'),
 ('jina_short','https://r.jina.ai/http://ssrn.com/abstract=7602585'),
 ('delivery_type2','https://papers.ssrn.com/sol3/Delivery.cfm?abstractid=7602585&mirid=1&type=2'),
 ('delivery_ssrn_filename','https://papers.ssrn.com/sol3/Delivery.cfm/ssrn_id7602585.pdf?abstractid=7602585&mirid=1'),
 ('delivery_mirid','https://papers.ssrn.com/sol3/Delivery.cfm?abstractid=7602585&mirid=1'),
 ('ssrn_www','https://www.ssrn.com/abstract=7602585'),
 ('ssrn_api','https://api.ssrn.com/abstract/7602585'),
 ('ssrn_api_papers','https://api.ssrn.com/papers/7602585'),
]
def fetch(item):
 name,url=item;r={'name':name,'url':url,'date':'2026-11-02'}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0','Accept':'application/pdf,application/json,text/html;q=0.9,*/*;q=0.8'})
  with urllib.request.urlopen(req,timeout=25) as response:
   body=response.read();r.update(status=response.status,final_url=response.url,content_type=response.headers.get('Content-Type',''))
  pdf=body.lstrip().startswith(b'%PDF-');suffix='.pdf' if pdf else '.json' if 'json' in r['content_type'] else '.txt'
  p=OUT/(name+suffix);p.write_bytes(body);r.update(file=str(p.relative_to(BASE)),bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),is_pdf=pdf)
  if not pdf:
   s=body.decode(errors='replace');r['links']=list(dict.fromkeys(re.findall(r'https?://[^\s<>\"\x27]+',s)))[:60]
 except Exception as e:r['error']=str(e)
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(fetch,items))
(BASE/'alternate-manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
for r in rows:print(json.dumps(r))
