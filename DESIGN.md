# Design

## Source of truth
Status: Active
Date: 2026-10-03
Product surfaces: personal academic homepage (`/`), publication archive (`/wiki/publications/`), research/wiki pages under `/wiki/`, shared default layout, publication-list include styling.
Evidence reviewed: Jekyll/Just-the-Docs setup (`Gemfile`, `_config.yml`), current homepage (`index.md`), shared layout (`_layouts/default.html`), publication include contract, publication data (`_data/publications.yml`), wiki pages, `assets/profile.jpg` (425×567 portrait), live screenshots under `.omx/artifacts/editorial-v2/`, and the Giung Nam reference as a credibility benchmark rather than a visual template. Existing unrelated local edits in `.gitignore`, `wiki/education.md`, and `wiki/projects/ascg.md` are outside design ownership.

## Brand
Personality: exacting, research-first, editorial, quietly severe, Korean/English academic identity.
Trust signals: KAIST AI affiliation, accepted/under-review publication status, named research themes, project/archive links, consistent metadata, clear contact path, and source-of-truth wiki framing.
Avoid: warm beige portfolio templates, capsule/pill UI everywhere, raised marketing cards, decorative gradients/shadows, dashboard tiles, generic SaaS hero language, playful emoji-heavy UI, unverified CV/download links, and publication facts not backed by the data/wiki source.

## Product goals
Goals:
- Present Younghwan Kil as a trustworthy AI researcher through an academic dossier/index, not a portfolio landing page.
- Make the homepage immediately useful: identity, role, contact/profile links, compact publication counts, accepted publications high on the page, research ledger, and education/current path.
- Make publications read as a flat bibliography/index with sharp hierarchy and status clarity.
- Keep long-form wiki pages readable and reusable for CV/research-statement writing.

Non-goals:
- Rewriting publication facts, statuses, authors, PDF links, or research claims owned by the publication/content lane.
- Adding JavaScript-heavy search, analytics, new dependencies, external fonts, new images, or deployment/publishing changes.
- Pixel-copying the reference site.

Success signals: pages build in Jekyll, all markdown routes keep their URLs, homepage feels like a distinctive academic research dossier, accepted work appears before secondary content, wiki pages have comfortable reading measure and table handling, keyboard users can skip/navigation-focus reliably, and mobile navigation remains compact at 320/390px.

## Personas and jobs
Primary personas:
- Faculty/PIs and admissions/recruiting readers who need a fast credibility scan.
- Research collaborators checking papers, projects, and contact links.
- Younghwan reusing wiki material for CVs, statements, and 자기소개서.

User jobs:
- Understand current role, research focus, and academic trajectory in under one minute.
- Find accepted publications, under-review work, and project detail with minimal friction.
- Read long-form wiki content without documentation-theme clutter.
- Verify links and status labels without confusing submissions and accepted work.

Contexts of use: desktop academic browsing, mobile quick checks after meeting/conference conversations, GitHub Pages with `baseurl: /younghwan-kil`, static no-dependency hosting.

## Information architecture
Navigation: global header with four primary routes — Home, Publications, Research, Wiki — plus a compact mobile menu using the existing `data-nav-toggle`/`data-site-nav` JavaScript contract.
Routes/screens:
- `/`: editorial dossier homepage with masthead, real portrait, verified contact/profile links, compact research/publication index, selected accepted publications, research ledger, position/education, and archive links.
- `/wiki/publications/`: full publication archive with summary row and flat bibliography sections.
- `/wiki/research/`: research overview route using research-section/keyword-list patterns where applicable.
- `/wiki/`: wiki index and related knowledge pages, with compact aside navigation.

Content hierarchy:
1. Identity and research thesis.
2. Verified contact/profile links.
3. Compact counts/index from data.
4. Accepted publications from shared data/include.
5. Research ledger/pillars.
6. Position/education and archive routing.
7. Footer provenance.

## Design principles
- Paper and ink over glass and cards: flat surfaces, ruled rows, precise spacing, and near-black text should do the work.
- Academic restraint over spectacle: one dark-teal signature accent, no decorative noise.
- Bibliography credibility: papers are indexed rows, not product cards.
- Status clarity: accepted/under-review labels are visible but small and typographic.
- Baseurl-safe static output: all internal assets/routes use `relative_url`.
- Progressive enhancement: HTML works without JavaScript; JS only improves compact navigation.

## Visual language
Color: near-paper canvas (`#f7f7f2` family), white/ivory paper panels only where needed, strong ink, cool gray metadata, hairline rules, and a limited dark-teal signature accent for links/focus/status. Warm beige, gradients, and soft sand fills are avoided.
Typography: local distinctive serif stack for masthead and headings (`Charter`, `Iowan Old Style`, `Palatino Linotype`, Georgia, serif); local sans for labels/navigation/body metadata; no external font dependency and no Arial/Inter/Roboto/Space Grotesk defaults.
Spacing: broad page gutters, a 76rem shell, 46rem prose measure, dense metadata rows, generous section rhythm, and 1px rules.
Shape/elevation: sharp system with 0–4px radii for controls/media/tables; no decorative shadows; no capsule navigation/frame language.
Motion: minimal opacity/translate entry and hover/focus transitions only; disabled under `prefers-reduced-motion`.
Imagery/iconography: use the existing portrait only, displayed as a real archival photo with a sharp border and caption/metadata; no generated imagery or decorative icon systems.

## Components
Existing/new components:
- Shared default layout (`_layouts/default.html`): SEO head, skip link, sharp global header, active nav underline, breadcrumb, main content shell, compact wiki side index, footer.
- Homepage (`index.md` + CSS): dossier masthead (without a redundant identity rail), `.identity-meta`, `.profile-links`, `.index-strip`, `.home-section`, accepted publication block, `.research-ledger`, `.timeline-list`, `.archive-callout`.
- Shared publication include contract: `<ol class="publication-list"><li class="publication-item" data-status="..."><div class="publication-main"><h3 class="publication-title">...` plus `.publication-authors`, `.publication-venue`, and `.publication-links`.
- Archive/content-lane classes: `.page-intro`, `.page-kicker`, `.publication-summary`, `.section-heading` with `.section-number`, `.conference-list`, `.conference-title`, `.conference-authors`, `.conference-venue`, `.directory-list`, `.directory-index`, `.directory-copy`, `.directory-title`, `.directory-description`, `.directory-arrow`, `.research-section`, `.research-number`, `.research-statement`, `.keyword-list`.
- Markdown prose: tables, blockquotes, TOC, code, links, headings.

Variants/states: active nav, hover/focus-visible, mobile nav expanded/collapsed, accepted/review status labels, external/internal publication links, narrow stacked publication rows.
Token ownership: `assets/css/site.css` owns color, spacing, type, border, and motion tokens.

## Accessibility
Target standard: WCAG 2.1 AA-minded static site.
Keyboard/focus: visible skip link, focus-visible outlines, button-based mobile nav with `aria-expanded`, nav links reachable in source order.
Contrast: strong ink on near-paper canvas; dark teal reserved for links/focus and tuned for contrast.
Semantics: landmark header/main/footer, article wrapping page content, nav labels, breadcrumb nav where relevant, descriptive link labels in content.
Reduced motion: transition/animation disabled for users who request reduced motion.
Sensory concerns: no auto-playing media, no large parallax, no flashing.

## Responsive behavior
Breakpoints/devices:
- Desktop ≥ 960px: centered shell, horizontal text nav, dossier masthead grid with compact portrait and identity block, publication rows in multi-column index layout, wiki aside as a slim right index.
- Tablet 720–959px: masthead compresses to two columns then stacks, nav wraps safely, publication links wrap under titles.
- Mobile < 720px, including 320/390px: compact header, menu button reveals nav, compact masthead with portrait beside the opening description, count strip in two columns, publication rows use full-width titles and unboxed text actions; a compact portrait sits alongside the opening description; tables horizontally scroll, touch targets ≥ 44px where possible.

Touch/hover differences: hover accents are decorative only; core state is visible by text, position, and focus styles.

## Interaction states
Loading: static pages render content-first; subtle page entry only.
Empty: if publication data/include is unavailable, homepage shows a concise link to the full publication archive instead of failing.
Error: no custom error surface in scope.
Success: active navigation and status labels confirm current location/content status.
Disabled: no disabled controls in current scope.
Offline/slow network: local CSS/JS/image only; no external font or CDN dependency.

## Content voice
Tone: concise, factual, academically confident, no hype.
Terminology: use “accepted,” “under review,” “to appear,” “Trustworthy AI,” “generative-model safety,” and “uncertainty-aware clinical AI” consistently.
Microcopy rules: avoid unverifiable claims, avoid counts that can drift unless Liquid/data owns them, and prefer project/archive links over duplicating long wiki content.

## Implementation constraints
Framework/styling: Jekyll 4.3 with `just-the-docs` gem installed by Gemfile; local `_layouts/default.html` overrides the theme layout; no package.json/frontend framework and no new dependencies.
Tokens/performance: one local CSS file and one tiny local JS file; use system-available serif/sans stacks, no external webfont.
Compatibility: GitHub Pages baseurl via `relative_url`, `jekyll-seo-tag` via `{% seo %}`, content markdown preserved.
Test/screenshot expectations: no build/publish during the design-worker integration slice; main/test lanes own Jekyll build, screenshots, visual-verdict loop, functional checks, commit, and deploy.

## Open questions
- No CV PDF is linked because no verified current CV was provided; the profile and education pages remain available.
- [x] Publication links verified against OpenReview and the publisher DOI; EBSG camera-ready is self-hosted with a matching source checksum. ASCG anonymous review PDF and Placement submission PDF are intentionally not hosted.
- [ ] Site owner: decide whether to preserve just-the-docs built-in search in a future iteration; impact is wiki discoverability, but not required for this redesign slice.

## Verification record
- Editorial revision independently reviewed against the previous deployed baseline and this brief.
- All 14 public routes checked at 320, 390, 768, and 1440px; zero viewport overflows, failed local assets, broken images, or JavaScript errors.
- Twelve static regressions cover route inventory, metadata, fragments, publication facts, conference presentations, PDF identity, and private-file exclusion.
- Keyboard/skip links, closed-menu focus, Escape focus restoration, sticky-header anchor clearance, table scroll reachability, no-JavaScript navigation, and reduced motion checked.
- Full assistive-technology certification is not claimed. Existing unrelated local edits remain outside the deployment.
