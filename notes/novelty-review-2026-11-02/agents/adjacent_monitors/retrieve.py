import concurrent.futures, datetime, hashlib, json, pathlib, subprocess, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / 'evidence' / 'adjacent_monitors'
SOURCES = {
 'Nguyen2025D3M': 'https://arxiv.org/pdf/2506.05047',
 'Amoukou2024SequentialHarmful': 'https://arxiv.org/pdf/2412.12910',
 'Zhang2026PPRM': 'https://arxiv.org/pdf/2602.02229',
 'Kasa2024EACP': 'https://arxiv.org/pdf/2406.01416',
 'Lyu2025CUI': 'https://arxiv.org/pdf/2502.02998',
 'Mahdiani2026ConformalTTA': 'https://papers.ssrn.com/sol3/Delivery.cfm/7602585.pdf?abstractid=7602585&mirid=1',
 'Prinster2025WATCH': 'https://raw.githubusercontent.com/mlresearch/v267/main/assets/prinster25a/prinster25a.pdf',
 'Feng2024MonitoringClinical': 'https://proceedings.mlr.press/v238/feng24b/feng24b.pdf',
}
def fetch(item):
 key,url=item
 record={'date':'2026-11-02','retrieved_at':datetime.datetime.now().astimezone().isoformat(),'key':key,'url':url}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (research literature review)'})
  with urllib.request.urlopen(req,timeout=45) as response:
   body=response.read();record.update(status=response.status,content_type=response.headers.get('Content-Type'),final_url=response.url)
  ext='.pdf' if body.startswith(b'%PDF') else '.html'
  path=OUT/(key+ext);path.write_bytes(body)
  record.update(bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),path=str(path.relative_to(ROOT)))
  if ext=='.pdf':
   subprocess.run(['pdftotext','-layout',str(path),str(path.with_suffix('.txt'))],check=True)
 except Exception as error:record['error']=str(error)
 return record
OUT.mkdir(parents=True,exist_ok=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:records=list(pool.map(fetch,SOURCES.items()))
(pathlib.Path(__file__).parent/'retrieval-manifest.json').write_text(json.dumps(records,indent=2))
for record in records:print(json.dumps(record))
