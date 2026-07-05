# younghwan-kil

A personal **living wiki** (Karpathy-style) about Younghwan Kil (길영환) — ML researcher
in Trustworthy AI. Built with Jekyll + [just-the-docs](https://just-the-docs.com/) and
served via GitHub Pages.

**Purpose:** a single, durable source of truth about who I am, my research, and my
motivations — used to draft CVs, cover letters (자기소개서), and research statements.

## Structure

```
index.md            # landing / about
wiki/               # the knowledge base
  index.md          #   wiki table of contents
  profile.md        #   biography & background
  timeline.md       #   career timeline
  education.md      #   education & honors
  values.md         #   values & motivation (자소서 core)
  research.md       #   research overview & themes
  publications.md   #   full publication list
  skills.md         #   technical skills
  projects/         #   one page per project
assets/             # images (profile, etc.)
```

## Local preview

```bash
bundle install
bundle exec jekyll serve
# http://localhost:4000/younghwan-kil/
```

## Deploy

Push to `main`; GitHub Pages (Settings → Pages → Deploy from branch `main` `/`) builds
and publishes to `https://younghwankil.github.io/younghwan-kil/`.

## Maintenance

This wiki is meant to **grow**. When something new happens (a paper, a project, a
lesson learned), add or extend a page rather than starting over. Keep claims
evidence-backed — supporting documents live outside this repo.
