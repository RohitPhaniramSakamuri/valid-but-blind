"""Save selected public primary reading material and hashes; no research execution."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import datetime
import hashlib
import json
import urllib.request

HERE = Path(__file__).resolve().parent
DEST = HERE / "primary-snapshots"
DEST.mkdir(exist_ok=True)
PAGES = {
    "Lu2026AgenticTTT": "https://arxiv.org/html/2610.12002v1",
    "Jhawar2026Identifiability": "https://arxiv.org/html/2609.11235v1",
    "Park2025HybridTTA": "https://arxiv.org/html/2409.08566v2",
    "Lim2026ASR": "https://arxiv.org/html/2603.03796v1",
    "Huang2026TTABC": "https://arxiv.org/html/2606.14299v3",
    "Yeo2023RNAProject": "https://rapid-network-adaptation.epfl.ch/",
    "WILDSSubmissionRules": "https://wilds.stanford.edu/submit/",
}


def fetch(item):
    key, url = item
    result = {"key": key, "url": url, "retrieved_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    path = DEST / (key + ".html")
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Research literature archiving"}), timeout=20) as response:
            data = response.read()
            result.update({"final_url": response.url, "content_type": response.headers.get_content_type()})
        path.write_bytes(data)
        result.update({"status": "saved", "file": str(path.relative_to(HERE)), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    except Exception as exc:
        result.update({"status": "failed", "error": str(exc)})
    return result


with ThreadPoolExecutor(max_workers=7) as pool:
    manifest = list(pool.map(fetch, PAGES.items()))
for path in (HERE / "verifier-evidence").glob("*"):
    if path.is_file():
        data = path.read_bytes()
        manifest.append({"key": "Vianna2025ChannelSelective", "file": str(path.relative_to(HERE)), "status": "previously_saved_by_verifier", "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
(HERE / "snapshot-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps({"saved_html": sum(x["status"] == "saved" for x in manifest), "failed": sum(x["status"] == "failed" for x in manifest), "verifier_files": sum(x["status"] == "previously_saved_by_verifier" for x in manifest)}))
