from pathlib import Path
import re
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[2] / 'evidence' / 'tta_causes'
for p in ROOT.glob('*.txt'):
    if '.clean.' in p.name:
        continue
    pages = p.read_text(errors='replace').split('\f')
    result = []
    for n, page in enumerate(pages, 1):
        page = ''.join(c for c in page if c in '\n\t' or ord(c) >= 32)
        page = re.sub(r'[ \t]{3,}', '  ', page)
        page = re.sub(r'\n[ \t]*\n[ \t]*\n+', '\n\n', page)
        result.append(f'\n[Text form-feed segment {n}; use printed page for citation]\n{page}')
    p.with_name(p.stem+'.clean.txt').write_text(''.join(result))

class Extract(HTMLParser):
    def __init__(self):
        super().__init__(); self.skip=0; self.text=[]
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'): self.skip+=1
        if tag in ('p', 'div', 'h1', 'h2', 'h3', 'h4', 'tr'): self.text.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self.skip=max(0, self.skip-1)
        if tag in ('p', 'div', 'h1', 'h2', 'h3', 'h4', 'tr'): self.text.append('\n')
    def handle_data(self,data):
        if not self.skip: self.text.append(data)
for p in ROOT.glob('*.html'):
    parser=Extract(); parser.feed(p.read_text(errors='replace'))
    p.with_suffix('.clean.txt').write_text(re.sub(r'\n\s*\n+', '\n\n', ''.join(parser.text)))
