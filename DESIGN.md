# Design

## Source of truth
Status: Active
Date: 2026-10-03
Product surfaces: personal academic homepage (`/`), publication archive (`/wiki/publications/`), research/wiki pages under `/wiki/`, shared default layout, publication-list include styling.
Evidence reviewed: `Gemfile` (Jekyll 4.3 + `just-the-docs` + `jekyll-seo-tag`), `_config.yml` (GitHub Pages baseurl, search/footer metadata, SEO plugin), current `index.md`, wiki pages (`wiki/index.md`, `wiki/profile.md`, `wiki/research.md`, `wiki/publications.md`, `wiki/projects/index.md`), `assets/profile.jpg` (425×567 portrait), recent git history, and the user-provided Giung Nam reference-page direction. Existing local edits in wiki/publications/project pages are treated as content-owner work and are not part of this design ownership.

## Brand
Personality: restrained, exacting, research-first, quietly premium, Korean/English academic identity.
Trust signals: KAIST AI affiliation, accepted/under-review publication status, named research themes, project/archive links, consistent metadata, clear contact path, source-of-truth wiki framing.
Avoid: dashboard cards, oversized SaaS hero language, generic purple gradients, playful emoji-heavy UI, unverified CV/download links, and visual decoration that distracts from publication credibility.

## Product goals
Goals:
- Present Younghwan Kil as a trustworthy AI researcher with a polished academic portfolio rather than a default documentation theme.
- Make the homepage immediately useful: identity, contact, research areas, selected accepted publications, position/education snapshot, and routes into the full wiki.
- Keep long-form wiki pages readable and reusable for CV/research-statement writing.
- Style publication metadata and links so accepted versus under-review status is scan-friendly.

Non-goals:
- Rewriting publication facts or research claims owned by the publication/data lane.
- Adding JavaScript-heavy search, analytics, new dependencies, or deployment/publishing changes.
- Pixel-copying the reference site.

Success signals: pages build in Jekyll, all markdown routes keep their URLs, homepage feels like an academic CV/profile, wiki pages have comfortable reading measure and table handling, keyboard users can skip/navigation-focus reliably, and mobile navigation remains compact.

## Personas and jobs
Primary personas:
- Faculty/PIs and admissions/recruiting readers who need a fast credibility scan.
- Research collaborators checking papers, projects, and contact links.
- Younghwan reusing wiki material for CVs, statements, and 자기소개서.

User jobs:
- Understand current role, research focus, and academic trajectory in under one minute.
- Find publications and project details with minimal friction.
- Read long-form wiki content without documentation-theme clutter.
- Verify links and status labels without confusing submissions and accepted work.

Contexts of use: desktop academic browsing, mobile quick checks after meeting/conference conversations, GitHub Pages with `baseurl: /younghwan-kil`, static no-dependency hosting.

## Information architecture
Navigation: global header with four primary routes — Home, Publications, Research, Wiki — plus a compact mobile menu.
Routes/screens:
- `/`: editorial profile homepage with portrait, bio, contact, research areas, selected accepted publications, position/education, archive links.
- `/wiki/publications/`: full publication archive, separately content-owned.
- `/wiki/research/`: research overview route.
- `/wiki/`: wiki index and related knowledge pages.

Content hierarchy:
1. Identity and research thesis.
2. Contact/social verification links.
3. Research pillars.
4. Selected accepted publications from data when available.
5. Position/education and archive routing.
6. Footer provenance and maintenance note.

## Design principles
- Academic restraint over spectacle: whitespace, hairlines, elegant type, and precise metadata beats marketing-card density.
- Content first, chrome second: navigation and wiki asides should support reading without dominating it.
- Status clarity: accepted/under-review tags are visually distinct but not loud.
- Baseurl-safe static output: all internal assets/routes use `relative_url`.
- Progressive enhancement: HTML works without JavaScript; JS only improves compact navigation.

## Visual language
Color: off-white canvas, white content surfaces, charcoal/navy text, muted teal accent, warm sand secondary fills, and hairline borders. Tokens live in `assets/css/site.css` as CSS custom properties.
Typography: display headings use Georgia/Cambria-style serif for editorial academic tone; body uses local platform sans for legibility and performance because no new font dependency is allowed. Avoid Arial/Inter/Roboto/Space Grotesk.
Spacing: generous page gutters, 68rem reading shell, 42rem prose measure for text blocks, 1px hairline separators, compact metadata rows.
Shape/elevation: mostly flat with fine borders; portrait and publication items use subtle radii and minimal shadows only where they clarify layering.
Motion: restrained load-in and hover transitions; disabled under `prefers-reduced-motion`.
Imagery/iconography: use the existing portrait only; avoid decorative icon systems.

## Components
Existing/new components:
- Shared default layout (`_layouts/default.html`): SEO head, skip link, global header, active nav, breadcrumb, main content shell, wiki side navigation, footer.
- Homepage sections (`index.md` + CSS): hero, contact rail, research areas, selected publications, position/education, archive callout.
- Publication list classes from the content lane: `.publication-list`, `.publication-item`, `.publication-title`, `.publication-authors`, `.publication-venue`, `.publication-links`, `.publication-link`, `.publication-status`, `.publication-status--accepted`, `.publication-status--review`.
- Markdown prose: tables, blockquotes, TOC, code, links, headings.

Variants/states: active nav, hover/focus-visible, mobile nav expanded/collapsed, accepted/review status badges, external/internal links.
Token ownership: `assets/css/site.css` owns color, spacing, type, border, and motion tokens.

## Accessibility
Target standard: WCAG 2.1 AA-minded static site.
Keyboard/focus: visible skip link, focus-visible outlines, button-based mobile nav with `aria-expanded`, nav links reachable in source order.
Contrast: charcoal/navy text on off-white/white; teal accent reserved for links and focus and tuned for contrast.
Semantics: landmark header/main/footer, article wrapping page content, nav labels, breadcrumb nav where relevant, descriptive link labels in content.
Reduced motion: transition/animation disabled for users who request reduced motion.
Sensory concerns: no auto-playing media, no large parallax, no flashing.

## Responsive behavior
Breakpoints/devices:
- Desktop ≥ 900px: centered shell, horizontal header nav, homepage hero in two columns, wiki aside floats to the right of prose when useful.
- Tablet 640–899px: stacked hero with portrait retained, nav wraps safely.
- Mobile < 720px: compact header, menu button reveals nav, single-column sections, tables horizontally scroll inside prose, touch targets ≥ 44px where possible.

Touch/hover differences: hover accents are decorative only; core state is visible by text and focus styles.

## Interaction states
Loading: static pages render content-first; subtle entry animation on main shell only.
Empty: if publication data/include is unavailable, homepage shows a concise link to the full publication archive instead of failing.
Error: no custom error surface in scope.
Success: active navigation and status badges confirm current location/content status.
Disabled: no disabled controls in current scope.
Offline/slow network: local CSS/JS/image only; no external font or CDN dependency.

## Content voice
Tone: concise, factual, academically confident, no hype.
Terminology: use “accepted,” “under review,” “to appear,” “Trustworthy AI,” “generative-model safety,” and “uncertainty-aware clinical AI” consistently.
Microcopy rules: avoid unverifiable claims, avoid counts that can drift unless content data owns them, and prefer project/archive links over duplicating long wiki content.

## Implementation constraints
Framework/styling: Jekyll 4.3 with `just-the-docs` gem installed by Gemfile; local `_layouts/default.html` overrides the theme layout; no package.json/frontend framework and no new dependencies.
Tokens/performance: one local CSS file and one tiny local JS file; use system-available serif/sans stacks, no external webfont.
Compatibility: GitHub Pages baseurl via `relative_url`, `jekyll-seo-tag` via `{% seo %}`, content markdown preserved.
Test/screenshot expectations: validate by static inspection/build where local Ruby tooling is available; main agent owns screenshots, visual-verdict loop, functional checks, commit, and deploy per task assignment.

## Open questions
- No CV PDF is linked because no verified current CV was provided; the profile and education pages remain available.
- [x] Publication links verified against OpenReview and the publisher DOI; EBSG camera-ready is self-hosted with a matching source checksum. ASCG anonymous review PDF and Placement submission PDF are intentionally not hosted.
- [ ] Site owner: decide whether to preserve just-the-docs built-in search in a future iteration; impact is wiki discoverability, but not required for this redesign slice.
