"""Collect future-work and limitation passages from library papers on arXiv, 2024 onward. Reads only."""
import json,re,subprocess,time,os,tempfile,urllib.request
D=os.path.dirname(os.path.abspath(__file__))
cat=json.load(open(os.path.join(D,'../../sources/catalog.json')))
out=[];ok=fail=0
PAT=re.compile(r"(future (work|research|direction|stud)|remains? (an )?(open|unclear|unknown|unexplored)|open (question|problem|challenge)|we (do not|did not|leave|left)\b|left (for|to) future|not (yet )?(address|consider|evaluat|stud|explor)|limitation|beyond the scope|an interesting direction|promising direction|worth (investigating|exploring))",re.I)
for r in cat:
    blob=' '.join(str(r.get(k,'')) for k in('url','pdf_url','html_url'))
    m=re.search(r'arxiv\.org/(?:abs|pdf|html)/(\d{4}\.\d{4,5})',blob)
    if not m or int(r.get('year') or 0)<2024: continue
    aid=m.group(1);p=os.path.join(D,'text',aid+'.txt')
    if not os.path.exists(p):
        try:
            req=urllib.request.Request(f'https://arxiv.org/pdf/{aid}',headers={'User-Agent':'Mozilla/5.0'})
            data=urllib.request.urlopen(req,timeout=60).read()
            with tempfile.NamedTemporaryFile(suffix='.pdf') as f:
                f.write(data);f.flush();subprocess.run(['pdftotext',f.name,p],check=True,stderr=subprocess.DEVNULL)
            time.sleep(1)
        except Exception as e:
            fail+=1;out.append(dict(key=r['key'],arxiv=aid,error=str(e)[:80]));continue
    ok+=1
    t=re.sub(r'\s+',' ',open(p,errors='ignore').read())
    cut=max(t.rfind(' References '),t.rfind(' REFERENCES '))
    body=t[:cut] if cut>len(t)*.3 else t
    sents=re.split(r'(?<=[.!?])\s+(?=[A-Z])',body)
    hits=[s[:420] for s in sents if PAT.search(s) and 40<len(s)]
    out.append(dict(key=r['key'],arxiv=aid,year=r.get('year'),title=r['title'],n=len(hits),hits=hits[-10:]))
json.dump(out,open(os.path.join(D,'passages.json'),'w'),indent=1)
print('ok',ok,'fail',fail)
