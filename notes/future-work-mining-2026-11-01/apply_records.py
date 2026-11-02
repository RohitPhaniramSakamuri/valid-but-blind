"""Append 1 November 2026 sources, with metadata read from arXiv abstract pages. Append-only and idempotent."""
import csv,json,re,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];DATE='2026-11-01';LEDGER='outputs/future-work-gaps-2026-11-01.md'
NEW={'Launay2026FairTPT':('2608.25707','Introduction, abstract and problem setup passages.','Evaluates fairness of episodic VLM TTA and proposes FairTPT; reports episodic TTA generally exacerbates majority-minority disparities.','Episodic CLIP prompt tuning; online adaptation is explicitly outside its focus.'),
'Kasa2024EACP':('2406.01416','Abstract and introduction passages.','Entropy-scaled conformal sets without test labels, combined with ETA; reports undercoverage with and without TTA.','No statistical guarantee under its setting; fixed choice of base TTA.'),
'Lyu2025CUI':('2502.02998','Search-result summary of abstract and introduction only.','Adjusts conformal quantiles by model and data shift for continual TTA.','Not read in full; an OpenReview entry was reported as withdrawn, not verified.'),
'Tian2024FairDomain':('2407.08813','Search-result summary of abstract only.','Fairness under domain shift in medical imaging for domain adaptation and generalization.','Not test-time adaptation; not read in full.')}
cat=json.loads((ROOT/'sources/catalog.json').read_text());have={r['key'] for r in cat};added=[]
for k,(aid,scope,ov,lim) in NEW.items():
    if k in have: continue
    h=urllib.request.urlopen(urllib.request.Request(f'https://arxiv.org/abs/{aid}',headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read().decode('utf8','ignore')
    title=re.search(r'citation_title" content="(.*?)"',h).group(1);auth=[' '.join(reversed(a.split(', '))) for a in re.findall(r'citation_author" content="(.*?)"',h)]
    date=re.search(r'citation_date" content="(.*?)"',h).group(1);year=int(date[:4]);url=f'https://arxiv.org/abs/{aid}'
    st=f'arXiv {date}; venue not verified'
    if not auth[0].split()[-1] in k: print('KEY CHECK',k,auth[0])
    cat.append(dict(key=k,title=title,authors=auth,year=year,venue=f'arXiv preprint {aid}',entry_type='misc',url=url,read_scope=scope,locations=[],method_overlap=ov,limitation=lim,publication_status=st,reading_history=[dict(date=DATE,read_scope=scope,locations=[],source_ledger=LEDGER)],freshly_verified=DATE,source_ledger=LEDGER,accessed=DATE))
    added.append((k,title,auth,year,aid,url,st,scope,ov,lim));print(k,title[:60],auth[:3],date)
(ROOT/'sources/catalog.json').write_text(json.dumps(cat,indent=2,ensure_ascii=False)+'\n')
w=csv.writer((ROOT/'sources/catalog.csv').open('a',newline=''))
bib=(ROOT/'references.bib').open('a');t=(ROOT/'REFERENCES.md').read_text().rstrip('\n')
if added: t+=f'\n\n## Addendum {DATE}\n\nThe library now has **{len(cat)} records**.\n\n| Key and source | Publication/status | Last reading scope | Relevance and qualification |\n| --- | --- | --- | --- |\n'
for k,title,auth,year,aid,url,st,scope,ov,lim in added:
    w.writerow([k,title,'; '.join(auth),year,f'arXiv preprint {aid}',url,'',st,scope,'',ov,lim,'',DATE,LEDGER])
    bib.write(f'\n@misc{{{k},\n  title = {{{{{title}}}}},\n  author = {{{" and ".join(auth)}}},\n  year = {{{year}}},\n  howpublished = {{arXiv preprint {aid}}},\n  url = {{{url}}},\n  note = {{{st}}},\n  urldate = {{{DATE}}},\n}}\n')
    t+=f'| `{k}` — [{title}]({url}) | {st} | {DATE}: {scope} | {ov} {lim} |\n'
    (ROOT/'papers'/f'{k}.md').write_text(f'# {title}\n\nCitation key: `{k}`\nAuthors, year, and venue: {", ".join(auth)}; {year}; arXiv preprint {aid}.\nAuthoritative link: {url}\nStatus: {st}.\nReading progress: {DATE}: {scope}\n\n## What the inspected passages cover\n\n{ov}\n\n## Limitations for our use\n\n{lim}\n\n## Connection to our research\n\nSee [the gap review](../{LEDGER}).\n')
(ROOT/'REFERENCES.md').write_text(t.rstrip('\n')+'\n');print(len(cat),len(added))
