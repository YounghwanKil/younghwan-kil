# Younghwan Kil — academic website

A personal academic homepage and research wiki, built with Jekyll and published at
[younghwankil.github.io/younghwan-kil](https://younghwankil.github.io/younghwan-kil/).

## Structure

- `index.md`: academic homepage and selected accepted publications.
- `_data/publications.yml`: shared paper titles, authors, statuses, venues, and verified links.
- `_includes/publication-list.html`: publication rendering used by the homepage and archive.
- `_layouts/default.html`: responsive shared navigation and page layout.
- `assets/css/site.css`, `assets/js/site.js`: design tokens/styles and progressive mobile navigation.
- `assets/papers/`: verified, author-owned camera-ready PDFs only.
- `wiki/`: full publication archive, projects, profile, research, education, and notes.
- `DESIGN.md`: maintained design contract.

## Preview and verify

With Ruby, its development headers, and Bundler installed:

```sh
bundle install
bundle exec jekyll build
python3 -m unittest discover -s tests -v
bundle exec jekyll serve
# http://localhost:4000/younghwan-kil/
```

The regression checks cover paper status/author metadata, shared homepage data,
verified links, the camera-ready checksum, local routes, and private-file exclusions.
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
