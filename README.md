# Younghwan Kil — academic website

A personal academic homepage and research wiki, built with Jekyll and published at
[younghwankil.github.io/younghwan-kil](https://younghwankil.github.io/younghwan-kil/).

## Structure

- `index.md`: overview-first homepage with research, experience, education, papers, and conference presentations.
- `_data/publications.yml`: shared paper titles, authors, statuses, venues, and verified links.
- `_includes/publication-list.html`: publication rendering used by the homepage and archive.
- `_layouts/default.html`: responsive shared navigation and page layout.
- `assets/css/site.css`, `assets/js/site.js`: design tokens/styles and progressive mobile navigation.
- `assets/papers/`: verified, author-owned camera-ready PDFs only.
- `wiki/`: full publication archive, projects, profile, research, education, and notes.
- `DESIGN.md`: maintained design contract.
- `_data/conference_presentations.yml`: shared HealthAI/KIIE records, shown without a toggle.
- `_includes/structured-metadata.html`: researcher/site and publication JSON-LD.
- `metadata.json`: public machine-readable record derived from the same paper/presentation data.
- `assets/social-card.png`: 1200×630 sharing preview, rendered by `scripts/render_social_card.py`.

## Preview and verify

With Ruby, its development headers, and Bundler installed:

```sh
bundle install
bundle exec jekyll build
python3 -m unittest discover -s tests -v
bundle exec jekyll serve
# http://localhost:4000/younghwan-kil/
```

The regression checks cover all 14 public routes, document metadata, internal
fragment links, paper/author metadata, shared homepage data, the camera-ready
checksum, and private-file exclusions.

For the full responsive/interaction audit, use the existing Python Playwright
tooling in your development environment (not a runtime website dependency):

```sh
python3 tests/browser_smoke.py
```

The browser audit starts an isolated localhost preview automatically, checks every
route at 320/390/768/900/1440px, and exercises keyboard navigation, tables, no-JavaScript
fallbacks, and reduced motion. Screenshots and JSON evidence are kept outside the
published site under `.omx/artifacts/dark-english/`. `SITE_DIR`, `BASE_URL`, and
`ARTIFACT_DIR` can select an explicit build, running preview, or evidence directory.
When intentionally updating publication facts or replacing a verified PDF, update
those corresponding assertions too. No frontend build or external webfont is required.

## Deploy

Pushing to `main` triggers `.github/workflows/pages.yml`: build with Jekyll, run
regression checks, and deploy the artifact to GitHub Pages.

## Publication integrity

Use canonical author lists and metadata from OpenReview, the published paper, or the
publisher. Keep accepted papers separate from manuscripts under review; do not carry
old submission venues into a new generic under-review entry. Do not invent links.
Only host a PDF after confirming it is the intended public final version; anonymous
review copies and PDFs marked “Do not distribute” are not camera-ready artifacts.

Private credential documents and local workflow artifacts are explicitly excluded
from the Jekyll output. Never stage them for Git.

## Search and sharing metadata

Per-route descriptions and the default sharing image are maintained in `_config.yml`.
Jekyll SEO tags remain the single source for title, canonical, description, OpenGraph,
and Twitter card tags. Custom JSON-LD adds stable person/site IDs and a publication
list with explicit Accepted / Under review states, without invented publication dates.
The `/metadata.json` endpoint includes 7 paper and 8 conference records from shared
YAML data. Internal links are exported as absolute URLs for reuse outside the site.

To refresh the native, text-only share preview with the existing development tools:

```sh
python3 scripts/render_social_card.py
```

Metadata makes pages interpretable to crawlers and share clients; it does not guarantee
search indexing, rankings, or immediate refresh of third-party preview caches.
