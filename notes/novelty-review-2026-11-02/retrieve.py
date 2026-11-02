"""Read-only literature retrieval; no model, dataset, experiment, or test execution."""
import concurrent.futures
import csv
import hashlib
import html
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent

def retrieve(item):
    folder = BASE / 'evidence' / 'root'
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / item['filename']
    record = dict(item, date='2026-11-02')
    try:
        request = urllib.request.Request(item['url'], headers={'User-Agent': 'Mozilla/5.0 (literature review; read-only)'})
        with urllib.request.urlopen(request, timeout=25) as response:
            body = response.read()
            record.update(status=response.status, final_url=response.url, content_type=response.headers.get('Content-Type', ''))
        path.write_bytes(body)
        record.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest(), evidence=str(path.relative_to(BASE)))
        if body.startswith(b'%PDF'):
            subprocess.run(['pdftotext', '-layout', str(path), str(path.with_suffix('.txt'))], check=True)
        elif 'html' in record['content_type']:
            source = body.decode('utf-8', errors='replace')
            plain = html.unescape(re.sub('<[^>]+>', ' ', source))
            path.with_suffix('.txt').write_text(re.sub(r'[ \t]+', ' ', plain))
            candidates = []
            for link, label in re.findall(r'<a[^>]+href=[\"\x27]([^\"\x27]+)[\"\x27][^>]*>(.*?)</a>', source, re.S | re.I):
                title = html.unescape(re.sub('<[^>]+>', ' ', label)).strip()
                if re.search(r'test.time|harmful.shift|risk.monitor|accuracy.estimat|performance.estimat|conformal|calibrat|model.monitor|failure.detect', title, re.I):
                    candidates.append({'title':title, 'link':link})
            record['title_candidates'] = candidates
        else:
            record['title_candidates'] = []
    except Exception as error:
        record['status'] = 'blocked/error'
        record['error'] = str(error)
        path.with_suffix(path.suffix + '.error.txt').write_text(str(error))
    return record

if __name__ == '__main__':
    requests = json.loads(Path(sys.argv[1]).read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        records = list(pool.map(retrieve, requests))
    destination = BASE / sys.argv[2]
    destination.write_text(json.dumps(records, indent=2, ensure_ascii=False))
    for row in records:
        print(json.dumps({k: row[k] for k in ('filename','url','status','bytes','error','title_candidates') if k in row}, ensure_ascii=False))
