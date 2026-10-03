# Design

## Source of truth
Status: Active
Date: 2026-10-03
Product surfaces: personal academic homepage (`/`), publication archive (`/wiki/publications/`), research and education wiki routes, shared default layout, shared publication-list include styling.
Evidence reviewed: `Gemfile`, `_config.yml`, `DESIGN.md`, `index.md`, `_layouts/default.html`, `assets/css/site.css`, `_includes/publication-list.html`, `_data/publications.yml`, `wiki/education.md`, `wiki/index.md`, and the available local `.omx` artifact inventory. The prior light editorial dossier direction is rejected by the current brief.

## Brand
Personality: severe, calm, exact, academic, black-canvas, immediately legible.
Trust signals: KAIST AI role, real portrait, direct email/GitHub/OpenReview links, accepted papers placed directly below the identity block, real venues/status labels, education and honors exposed in primary navigation.
Avoid: AI-generated portfolio cues, purple/blue gradients, glow, grid textures, monograms, oversized serif dossier headlines, numbered rails, fake counters, dashboard strips, bento cards, motivational filler, and visible non-English metadata in the shared UI.

## Product goals
Goals:
- Make the homepage explain who Younghwan Kil is, his M.S./KAIST/SIML role, what he studies, and how to contact him without scrolling.
- Put the three accepted publications immediately after the hero with readable titles, authors, venues, status, and direct links.
- Keep the rest of the site as a clean dark academic archive rather than a marketing landing page.
- Add Education & Honors as a first-class primary navigation item.

Non-goals:
- Changing publication facts, PDF/OpenReview paths, portrait pixels, Jekyll configuration, or wiki content owned by other lanes.
- Adding dependencies, external fonts, generated images, decorative JavaScript, analytics, or deployment changes.
- Reusing the rejected light editorial/serif visual system.

Success signals: Jekyll builds, all public routes inherit the dark redesign, navigation has five clear items, active states are unique, accepted papers are prominent, long text and tables do not overflow, and contrast remains AA-minded on near-black.

## Personas and jobs
Primary personas:
- Faculty/PIs/reviewers scanning credibility and current research focus.
- Collaborators looking for papers, projects, and contact links.
- Recruiters or academic readers checking education, honors, and trajectory.

User jobs:
- Understand identity, affiliation, research focus, and contact path in seconds.
- Open accepted papers or OpenReview/PDF links quickly.
- Move between Publications, Research, Education & Honors, and Wiki without ambiguity.
- Read long academic pages on desktop and mobile without decorative clutter.

Contexts of use: GitHub Pages static site with `baseurl: /younghwan-kil`, desktop academic browsing, mobile follow-up after meetings, no external asset loading.

## Information architecture
Navigation: five primary routes in this order — Home, Publications, Research, Education & Honors, Wiki. Education links to `/wiki/education/` and owns its own active state; Wiki excludes publications, research, and education from its active condition.
Routes/screens:
- `/`: compact hero with portrait/contact, selected accepted publications, two research directions, education highlights, and a short archive callout.
- `/wiki/publications/`: full bibliography/archive using the existing publication include contract.
- `/wiki/research/`: concise research overview.
- `/wiki/education/`: education and honors, directly accessible from top navigation.
- `/wiki/` and child pages: readable dark archive with related wiki navigation.

Content hierarchy:
1. Name plus one factual M.S./KAIST/SIML role paragraph, compact portrait, and verified contact/profile links.
2. Accepted publications from `_data/publications.yml` through the existing include.
3. Two concise research interests.
4. Education and honors highlights.
5. Archive/wiki routing.

## Design principles
- Black canvas first: the site should feel like a quiet academic reading room, not an inverted template.
- Information over decoration: every visible element must clarify identity, route, paper status, or reading structure.
- Bibliography as bibliography: publication rows stay flat, typographic, and link-rich; no pseudo-index counters or product cards.
- System sans discipline: body and headings use sharp local system sans only, because the rejected serif dossier tone is out of scope.
- Progressive enhancement: navigation and content work without JavaScript; JS only enhances compact menu behavior.

## Visual language
Color: pure black canvas (`#000000`), off-white text, `#ccc` body copy, `#999` metadata, hairline charcoal rules, and a restrained ice-blue link/focus accent (`#c3d9f3`). No gradients, glow, patterned backgrounds, bright panels, or beige/gray paper fields.
Typography: system sans for body and headings (`ui-sans-serif`, `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `Helvetica Neue`, sans-serif) with natural case, weight contrast, and no external fonts.
Spacing: compact above the fold so accepted publications begin immediately, generous row rhythm for papers, readable 44–50rem prose, shell width around 76rem, mobile gutters no smaller than 1rem.
Shape/elevation: square edges, 1px rules, no drop shadows; charcoal surfaces only for mobile menus or table headers when they aid legibility.
Motion: restrained opacity/translate page entry and link transitions only; disabled under reduced motion.
Imagery/iconography: use only the existing `assets/profile.jpg`, small and real, optionally grayscale; no new image assets, monogram, abstract mark, automotive stripe, or decorative icon system.
Reference synthesis: adopt Bugatti-like black discipline only for canvas severity; adopt Mobbin-like natural-case sans spacing and plain links; adopt BMW-like functional hierarchy and clear navigation. Decline literal cloning, licensed/custom fonts, automotive imagery, stripes, chrome pills, and marketing-dashboard layouts.

## Components
Existing/new components:
- Shared default layout: skip link, sticky black header, text-only brand, five-item primary nav, breadcrumb, content shell, wiki aside, footer.
- Homepage: `.home-hero`, `.home-hero__identity`, `.home-hero__bio`, `.home-portrait`, `.profile-links`, selected publication section, `.research-directions`, `.education-highlights`, `.archive-callout`.
- Publication include contract preserved exactly in markup expectation: `<ol class="publication-list" role="list"><li class="publication-item" id data-status><div class="publication-main"><h3 class="publication-title">...` with authors/venue/status and `.publication-links`.
- Archive classes styled globally: `.publication-summary`, `.author-key`, `.archive-jump`, `.conference-list`, `.directory-list`, `.page-intro`, `.page-kicker`, `.section-heading`, `.section-number`, `.research-number`, `.keyword-list`.

Variants/states: hover, focus-visible, active nav, mobile nav open/closed, accepted/review publication status, narrow publication links, no-JS navigation.
Token ownership: `assets/css/site.css` owns design tokens, layout, type, rules, and responsive behavior.

## Accessibility
Target standard: WCAG 2.1 AA-minded static site.
Keyboard/focus: visible skip link, focus rings, button-based mobile nav with `aria-expanded`, clear source order, Escape support retained by existing JS.
Contrast: off-white and muted gray values are tuned for near-black; accent blue is used sparingly and must remain legible.
Semantics: landmark header/main/footer, `nav` labels, breadcrumb, descriptive publication links, real headings, and list semantics preserved.
Reduced motion: all animation/transition effects are minimized and disabled under `prefers-reduced-motion`.
Sensory concerns: no flashing, auto-play, parallax, glow, or busy background texture.

## Responsive behavior
Breakpoints/devices:
- Desktop ≥ 960px: compact header, two-column hero with restrained portrait, full-width flat publication rows, optional wiki aside.
- Tablet 720–959px: hero remains two-column when possible, metadata stacks, aside moves below content.
- Mobile < 720px: text-first hero, portrait small, menu button controls nav, publication rows stack, tables scroll horizontally, touch targets remain large enough.

Touch/hover differences: hover is only an enhancement; route and link meaning remains visible through text, borders, and focus.

## Interaction states
Loading: static content-first render; optional minimal page entry.
Empty: homepage publication block falls back to the archive link if data is unavailable.
Error: no custom error route in scope.
Success: active nav state and publication status communicate current location and publication state.
Disabled: no disabled controls in scope.
Offline/slow network: local CSS, JS, portrait, and PDFs only; no CDN/font dependency.

## Content voice
Tone: concise, factual, academic, restrained.
Terminology: KAIST AI, Trustworthy AI, generative-model safety, LLM safety auditing, uncertainty-aware clinical AI, accepted, under review, to appear.
Microcopy rules: no motivational filler, no invented counts, no repeated generic AI prose, no visible non-English metadata in owned layout/homepage surfaces.

## Implementation constraints
Framework/styling: Jekyll 4.3 with `just-the-docs`; no `package.json` frontend framework; `_layouts/default.html` overrides theme layout; `assets/css/site.css` is a lean single-file redesign.
Tokens/performance: no new dependencies, no external fonts, no new images, preserve existing portrait pixels and publication paths.
Compatibility: use `relative_url` for internal routes/assets, preserve `data-nav-toggle`, `#site-nav`, and `data-site-nav` contracts.
Test/screenshot expectations: run a local Jekyll build and inspect generated HTML for nav, publication links, and unintended non-English owned metadata. Main lane owns screenshots, visual verdict, deploy, and commits.

## Open questions
- [ ] Site owner: decide later whether wiki pages should be content-edited to remove bilingual source notes; outside this design lane's four-file ownership.
- [ ] Main verifier: confirm screenshots across all routes after integration with the translation/config/test lanes.

## Selected reference and final user overrides
The downloaded Linear reference at https://getdesign.md/linear.app/design-md is the single token/typography baseline (source Markdown: https://getdesign.md/design-md/linear.app/DESIGN.md). Local reference copies stay in excluded `.omx/artifacts/dark-english/references/getdesign/`.
- Adopt restrained 56px display / 28px section scales, 600/500 heading weights, 16–18px body text, neutral charcoal surfaces, and quiet hairlines.
- Keep the user's explicitly requested pure-black canvas. Do not import Linear's purple branding, product UI, gradients, logo, or stats tiles.
- Home order: introduction, research interests, work experience, Education & Honors, then Publications as a normal section containing papers and conference posters. Further HealthAI/KIIE presentations remain accessible in an expandable list.
- Use the supplied outdoor portrait, preserving the original decoded pixels and presenting a chest-level 4:5 CSS crop. Remove metadata without recompressing the JPEG. Do not use the generative-image preview as the website portrait.
- New user-confirmed metadata: Haean Research Institute April 2026–Present; Reasoning and Same-Loss co-first authors; Cross-lingual ETRI Journal (SCIE) with the supplied Wiley ePDF link. Do not infer an employment role for Haean.

## Release validation
The final candidate has an independent visual pass and code review approval. The website is English-only across all 14 routes, has an explicit Education & Honors primary navigation item, and omits the rejected logo/statistics display. Publication counts are derived from data (7 papers; 8 conference presentations) without a homepage statistics strip. The original portrait is pixel-preserved and metadata-sanitized, with a CSS chest-level crop; the older portrait is excluded from publication.
