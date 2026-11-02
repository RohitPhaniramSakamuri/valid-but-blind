"""Read-only bibliographic API attempts; no model/data experiment code."""
import csv,json,urllib.request,urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'evidence'/'tta_causes'
seeds=[('Wang2021Tent','2006.10726'),('Amin2025OverCertainty','2404.16168'),('Nam2026SICL','2512.07390'),('Lee2024AETTA','2404.01351'),('Press2024EntropyEnigma','2405.05012'),('Bar2024ProtectedTTA','2408.07511'),('Zhao2023Pitfalls','2306.03803')]
rows=[]
for key,aid in seeds:
    url=f'https://api.semanticscholar.org/graph/v1/paper/ARXIV:{aid}?fields=title,year,citationCount,referenceCount,citations.title,citations.year,citations.url,references.title,references.year,references.url'
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'LiteratureReview/1.0'}),timeout=20) as r:
            body=r.read().decode(); status=r.status
    except urllib.error.HTTPError as e:
        body=e.read().decode(errors='replace'); status=e.code
    except Exception as e:
        body=str(e); status='error'
    (OUT/(key+'-s2-trace.json')).write_text(json.dumps({'url':url,'date':'2026-11-02','http_status':status,'body':body},indent=2))
    rows.append({'date':'2026-11-02','source':'Semantic Scholar Graph API','query':url,'result_count':'not available' if status!=200 else 'see saved JSON','results_url':f'evidence/tta_causes/{key}-s2-trace.json','relevant_papers':key,'blocked_notes':f'HTTP {status}; cannot enumerate citations/references' if status!=200 else 'citation/reference fields may have provider limits; not a complete audit'})
    print(key,status)
with (ROOT/'agents'/'tta_causes'/'api-search-log.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=rows[0]); w.writeheader();w.writerows(rows)
