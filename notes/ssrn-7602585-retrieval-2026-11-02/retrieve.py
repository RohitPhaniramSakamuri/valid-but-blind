"""Retrieve public SSRN routes and preserve response provenance; never label HTML a PDF."""
import concurrent.futures,datetime,hashlib,json,subprocess
from pathlib import Path
from curl_cffi import requests

BASE=Path(__file__).resolve().parent
OUT=BASE/'evidence';OUT.mkdir(exist_ok=True)
URLS=[
 ('landing','https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7602585'),
 ('delivery_query','https://papers.ssrn.com/sol3/Delivery.cfm?abstractid=7602585'),
 ('delivery_download','https://papers.ssrn.com/sol3/Delivery.cfm?abstractid=7602585&download=yes'),
 ('delivery_id','https://papers.ssrn.com/sol3/Delivery.cfm/7602585.pdf?abstractid=7602585&mirid=1'),
 ('abstract_short','https://ssrn.com/abstract=7602585'),
 ('doi','https://doi.org/10.2139/ssrn.7602585'),
]
def fetch(item):
 name,url=item;record={'name':name,'url':url,'date':'2026-11-02','method':'curl_cffi normal browser TLS; public unauthenticated route'}
 try:
  r=requests.get(url,impersonate='chrome',timeout=25,allow_redirects=True,headers={'Referer':'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7602585'})
  body=r.content;pdf=body.lstrip().startswith(b'%PDF-');p=OUT/(name+('.pdf' if pdf else '.html'))
  p.write_bytes(body);record.update(status=r.status_code,final_url=r.url,content_type=r.headers.get('Content-Type'),bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),file=str(p.relative_to(BASE)),is_pdf=pdf)
 except Exception as e:record['error']=str(e)
 return record
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:records=list(pool.map(fetch,URLS))
(BASE/'retrieval-manifest.json').write_text(json.dumps(records,indent=2)+'\n')
for r in records:print(json.dumps(r))
