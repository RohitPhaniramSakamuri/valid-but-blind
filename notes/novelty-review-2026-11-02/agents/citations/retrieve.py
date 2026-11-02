import concurrent.futures,csv,json,pathlib,urllib.request,urllib.parse,datetime
ROOT=pathlib.Path(__file__).resolve().parents[2]
OUT=ROOT/'evidence'/'citations'
OUT.mkdir(parents=True,exist_ok=True)
REQUESTS=[
('arxiv_abs','arXiv','https://arxiv.org/abs/2507.08721'),
('openalex_title','OpenAlex','https://api.openalex.org/works?search='+urllib.parse.quote('Monitoring Risks in Test-Time Adaptation')+'&per-page=100'),
('openalex_arxiv','OpenAlex','https://api.openalex.org/works?filter=locations.source.id:s4306400194&search=2507.08721&per-page=100'),
('s2_arxiv','Semantic Scholar','https://api.semanticscholar.org/graph/v1/paper/ARXIV:2507.08721?fields=paperId,title,year,externalIds,citationCount,referenceCount,url'),
('s2_title','Semantic Scholar','https://api.semanticscholar.org/graph/v1/paper/search?query='+urllib.parse.quote('Monitoring Risks in Test-Time Adaptation')+'&limit=100&fields=paperId,title,year,externalIds,citationCount,referenceCount,url'),
('crossref_title','Crossref','https://api.crossref.org/works?query.title='+urllib.parse.quote('Monitoring Risks in Test-Time Adaptation')+'&rows=100'),
('crossref_doi','Crossref','https://api.crossref.org/works/10.52202/085713-2705'),
('scholar_title','Google Scholar','https://scholar.google.com/scholar?q='+urllib.parse.quote('"Monitoring Risks in Test-Time Adaptation"')),
('openreview_workshop','OpenReview','https://api2.openreview.net/notes?forum=k14ktterKG&limit=1000'),
('github_repo','GitHub','https://api.github.com/repos/monasch/tta-monitor'),
('github_issues','GitHub','https://api.github.com/repos/monasch/tta-monitor/issues?state=all&per_page=100'),
('github_forks','GitHub','https://api.github.com/repos/monasch/tta-monitor/forks?per_page=100'),
('github_commits','GitHub','https://api.github.com/repos/monasch/tta-monitor/commits?per_page=100'),
('github_readme','GitHub','https://raw.githubusercontent.com/monasch/tta-monitor/main/README.md'),
('dblp','DBLP','https://dblp.org/rec/conf/nips/SchirmerJNN25.xml'),
('workshop_papers','PUT workshop','https://tta-icml2025.github.io/papers.html'),
]
def get(row):
    stem,source,url=row
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (research literature review; no experiments)'})
        with urllib.request.urlopen(req,timeout=35) as r: content=r.read(); status=r.status; actual=r.url; typ=r.headers.get('Content-Type','')
        ext='.pdf' if 'pdf' in typ else '.json' if 'json' in typ else '.html' if 'html' in typ else '.txt'
        path=OUT/(stem+ext);path.write_bytes(content)
        record=dict(date='2026-11-02',source=source,query=url,result_count='',results_url=actual,relevant_papers='',blocked_notes='',status=status,file=str(path.relative_to(ROOT)))
        try:
            data=json.loads(content)
            if isinstance(data,list): record['result_count']=len(data)
            if isinstance(data,dict):
                record['result_count']=data.get('meta',{}).get('count',data.get('total',data.get('citationCount',data.get('count',''))))
        except Exception: pass
        print(json.dumps({'name':stem,'status':status,'bytes':len(content),'count':record['result_count']}),flush=True)
    except Exception as e:
        record=dict(date='2026-11-02',source=source,query=url,result_count='',results_url=url,relevant_papers='',blocked_notes=str(e),status='blocked',file='')
        print(json.dumps({'name':stem,'error':str(e)}),flush=True)
    return record
if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex: records=list(ex.map(get,REQUESTS))
    (OUT/'retrieval-manifest.json').write_text(json.dumps(records,indent=2))
    with (ROOT/'agents'/'citations'/'search-log.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['date','source','query','result_count','results_url','relevant_papers','blocked_notes','status','file']);writer.writeheader();writer.writerows(records)
