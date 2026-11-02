"""Requested document/source audit; not an implementation or research test."""
import collections,csv,json,re
from pathlib import Path
from urllib.parse import unquote
BASE=Path(__file__).resolve().parent;PROJECT=BASE.parent.parent
catalog=json.loads((PROJECT/'sources/catalog.json').read_text());keys=[r['key'] for r in catalog]
bibkeys=re.findall(r'@\w+\{([^,\s]+),',(PROJECT/'references.bib').read_text())
records=json.loads((BASE/'record-update.json').read_text())
review=(BASE/'review.md').read_text()
claimrows=[s for s in review.splitlines() if re.match(r'\| \*\*C[1-5]:',s)]
verdicts={}
for line in claimrows:
    cells=[c.strip() for c in line.strip('|').split('|')]
    verdicts[re.search(r'C[1-5]',cells[0])[0]]=re.sub(r'\*','',cells[1])
csvrecords={};csvissues=[]
for name in ['search-log.csv','screened-papers.csv','closest-work.csv','claim-evidence.csv','venue-coverage.csv']:
    with (BASE/name).open(newline='') as f:
        rows=list(csv.DictReader(f));csvrecords[name]=len(rows)
        for n,row in enumerate(rows,2):
            if None in row or any(v is None for v in row.values()):csvissues.append(dict(file=name,row=n,problem='CSV width/blank structural cell'))
            if name=='search-log.csv' and row.get('date')!='2026-11-02':csvissues.append(dict(file=name,row=n,problem='Unexpected/missing search date'))
missing=[];anchors=[]
files=[BASE/'review.md',BASE/'review.provenance.md',PROJECT/'README.md',PROJECT/'REFERENCES.md',PROJECT/'notes/research-branches.md',PROJECT/'CHANGELOG.md']+[PROJECT/'papers'/f'{k}.md' for k in records['note_keys']]
for p in files:
    s=p.read_text()
    # Only newly added portions of historical records are within this task's link audit.
    if p.parent==PROJECT/'papers':s=s.split('## Adversarial review — 2 November 2026',1)[-1]
    elif p==PROJECT/'README.md':s=s.split('## Agent handoff',1)[0]
    elif p==PROJECT/'notes/research-branches.md':s=s.split('## Replication update',1)[0]
    elif p==PROJECT/'CHANGELOG.md':s=s.split('## 1 November',1)[0]
    elif p==PROJECT/'REFERENCES.md':s=s.split('## Adversarial novelty review — 2 November 2026',1)[-1]
    for target in re.findall(r'\]\(([^)]+)\)',s):
        if target.startswith(('http:','https:','mailto:','#')):continue
        target=target.split('#',1)[0].strip('<>')
        path=(p.parent/unquote(target)).resolve()
        if not path.exists():missing.append(dict(file=str(p.relative_to(PROJECT)),target=target))
    if 'Result: pending' in s:anchors.append(str(p))
out=dict(date='2026-11-02',scope='Document/source consistency only; no implementation tests or experiments',catalog_records=len(keys),bibtex_records=len(bibkeys),duplicate_catalog_keys=[k for k,n in collections.Counter(keys).items() if n>1],duplicate_bibtex_keys=[k for k,n in collections.Counter(bibkeys).items() if n>1],catalog_without_bibtex=sorted(set(keys)-set(bibkeys)),bibtex_without_catalog=sorted(set(bibkeys)-set(keys)),csv_rows=csvrecords,csv_structure_issues=csvissues,missing_scoped_local_links=missing,verdicts=verdicts,exactly_five_verdict_rows=len(claimrows)==5,pending_local_outcome_preserved='**Result: pending.**' in (PROJECT/'experiments/004-monitor-blind-spots.md').read_text(),interpretation_labels_present=all(x in review for x in ['**Our interpretation:**','algebraic reading','This is our assessment']),blocking_findings=bool(csvissues or missing or set(keys)!=set(bibkeys) or len(claimrows)!=5))
(BASE/'document-audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
