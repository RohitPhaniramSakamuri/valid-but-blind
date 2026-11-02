"""Extract reproducible title-only screens from saved official indexes."""
import csv, html, json, re
from pathlib import Path
from urllib.parse import urljoin
BASE=Path(__file__).resolve().parent
terms=re.compile(r'test.time|source.free|online.adapt|label.shift|entropy|harmful.shift|monitor|accuracy.estimat|performance.estimat|conformal|calibrat|failure.detect|shift.detect|change.point|changepoint|sequential.test|martingale',re.I)
clean=lambda s: re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',s))).strip()
rows=[]; coverage=[]
for manifest in sorted(BASE.glob('venue-retrieval*.json')):
  for r in json.loads(manifest.read_text()):
    if r.get('status')!=200 or not r.get('evidence','').endswith('.html'):
      coverage.append(dict(source=r['source'],url=r['url'],status=r.get('status'),titles=0,candidates=0,limitation=r.get('error','Non-HTML/API record; inspect separately.')));continue
    s=(BASE/r['evidence']).read_text(errors='replace');titles=[]
    if 'proceedings.mlr.press' in r['url']:
      for block in re.findall(r'<div class="paper">(.*?)</div>',s,re.S):
        t=re.search(r'<p class="title">(.*?)</p>',block,re.S);a=re.search(r'href="([^"]+)"[^>]*>abs<',block)
        if t:titles.append((clean(t[1]),urljoin(r['url'],a[1]) if a else r['url']))
    elif 'jmlr.org' in r['url'] or 'data.mlr.press/volumes/' in r['url']:
      for t,body in re.findall(r'<dt>(.*?)</dt>(.*?)(?=<dt>|</dl>)',s,re.S):
        a=re.search(r'href=[\"\x27]?([^\"\x27 >]+)[\"\x27]?[^>]*>\s*(?:abs|Abstract)',body,re.I)
        titles.append((clean(t),urljoin(r['url'],a[1]) if a else r['url']))
    else:
      for a,t in re.findall(r'<a\b[^>]*href\s*=\s*[\"\x27]?([^\"\x27 >]+)[\"\x27]?[^>]*>(.*?)</a>',s,re.S|re.I):
        t=clean(t)
        if ('Abstract-' in a or '/html/' in a or 'paper.php' in a or '/virtual/' in a or '/papers/' in a) and len(t)>12:titles.append((t,urljoin(r['url'],a)))
      if r['filename']=='ECCV2026-accepted.html':
        for block in re.findall(r'<td>(.*?)</td>',s,re.S):
          titleblock=re.split(r'<(?:div|span|a)\b',block,maxsplit=1)[0]
          t=clean(titleblock)
          if len(t)>12:titles.append((t,r['url']))
    unique=list(dict.fromkeys(titles));selected=[x for x in unique if terms.search(x[0])]
    coverage.append(dict(source=r['source'],url=r['url'],status=r['status'],titles=len(unique),candidates=len(selected),limitation='Mechanical title filter only; uninformative titles can be missed. Initial NeurIPS2025 URL is creative-AI track only.' if r['filename']=='NeurIPS2025.html' else 'Mechanical title filter only; not a full-text search or complete citation review.'))
    for title,url in unique:
      if terms.search(title):rows.append(dict(date='2026-11-02',source=r['source'],title=title,url=url,reading_scope='Mechanical official-index title screen',decision='shortlist for topical screening',reason='Matches declared title filter; no omission claim established',C1='unchecked',C2='unchecked',C3='unchecked',C4='unchecked',C5='unchecked'))
with (BASE/'venue-title-candidates.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with (BASE/'venue-coverage.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(coverage[0]));w.writeheader();w.writerows(coverage)
print('Index titles extracted:',sum(r['titles'] for r in coverage),'matching rows:',len(rows))
for r in coverage:print(r['source'],r['status'],r['titles'],r['candidates'])
print('\nClose-candidate title screen:')
for r in rows:
  if re.search(r'monitor|accuracy.estimat|performance.estimat|test.time.*(confiden|calibrat|reliab|protect)|manufactur|self.mask|harmful.shift',r['title'],re.I):print(r['source'],r['title'],r['url'])
