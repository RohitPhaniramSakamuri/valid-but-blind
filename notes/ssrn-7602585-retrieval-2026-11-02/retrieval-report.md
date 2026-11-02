# SSRN7602585 full-text retrieval attempt

Date: 2 November 2026. Requested paper: Mohammad Reza Mahdiani, *Diagnosing and repairing the conformal coverage guarantee of test-time-adapted image classifiers*, DOI10.2139/ssrn.7602585, SSRN record7602585, advertised34pages, posted12October2026.

**Outcome: no complete PDF retrieved.** No HTML challenge or abstract has been saved or presented as the paper. Source content beyond the indexed abstract/references remains unread. The earlier novelty review's full-text-access qualification remains applicable.

## Routes actually checked

- Public SSRN landing, DOI/short-link redirects, delivery/query/download/mirror/type2 routes:403. `retrieval-manifest.json` and `alternate-manifest.json` record URLs, statuses, content types, hashes, and `%PDF` checks.
- Installed Chrome in a fresh temporary headless profile: publisher's explicit Content Blocked page. A separate normal desktop profile stayed in Cloudflare human verification. The user reported completing it six times without success; further verification retries were stopped. No existing user browser profile, credentials, or cookies were used.
- Crossref DOI metadata:200; confirms exact title and authenticated author ORCID; provides only the SSRN landing link, no PDF/content link.
- OpenAlex W7221552712:200; only SSRN DOI location, `pdf_url:null`, `has_fulltext:false`, `has_content.pdf:false`, no content URLs. Its green/OA label does not mean it hosts a downloadable copy.
- Semantic Scholar DOI lookup:404. OpenAIRE exact-DOI search:200 with0 results. Zenodo exact-ID query:403, so no absence conclusion from that endpoint.
- Google Scholar exact-title search: one SSRN record, no external PDF link in the retrieved page. Exact title/DOI/CDN/repository searches did not expose another identifiable full-text copy; saved web outputs retain irrelevant hits rather than treating them as matches.
- Author's public ORCID0000-0001-9252-8475:200; verifies the personal website and GitHub account. The public GitHub account lists only the personal-site repository. Its complete recursive tree has four items (site HTML/CSS, image directory/profile image), no paper PDF or source. Author's work entry again points to the DOI.
- Public reader proxy returned the same verification page, not paper text.

## Practical remaining routes

A direct author copy or a successful SSRN download from a different working client/network is needed. The author identity and public website are verified from ORCID; an optional request draft is saved in `author-request.txt`. No request was sent to the author or SSRN. We do not assume another network will work.

## Record integrity

This attempt uses installed Python3.13.9 through `uv run --no-project`, installed `curl_cffi`/`websockets`, and installed browsers. No pip, dependency installation, experiments, or implementation tests. Existing dated novelty evidence is preserved. The source's incorrectly generated “arXiv preprint” label is corrected to “SSRN preprint”; this is metadata correction only, not a new reading or changed novelty verdict.
