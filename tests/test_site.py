"""Dependency-free regression checks for the built academic website.

Run after `bundle exec jekyll build`: python3 -m unittest discover -s tests -v
Set SITE_DIR to validate a separate build destination.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import hashlib
import json
import os
import re
import unittest

SITE = Path(os.environ.get('SITE_DIR', '_site'))
BASE = '/younghwan-kil'
SITE_URL = 'https://younghwankil.github.io'
EXPECTED_ROUTES = {
    '/',
    '/wiki/',
    '/wiki/education/',
    '/wiki/profile/',
    '/wiki/projects/',
    '/wiki/projects/ascg/',
    '/wiki/projects/datan/',
    '/wiki/projects/ebsg/',
    '/wiki/projects/llm-safety/',
    '/wiki/publications/',
    '/wiki/research/',
    '/wiki/skills/',
    '/wiki/timeline/',
    '/wiki/values/',
}
EXPECTED_NAV = {
    '/': 'Home',
    '/wiki/publications/': 'Publications',
    '/wiki/research/': 'Research',
    '/wiki/education/': 'Education & Honors',
}
EXPECTED_PRIMARY_NAV = (
    ('Home', f'{BASE}/'),
    ('Publications', f'{BASE}/wiki/publications/'),
    ('Research', f'{BASE}/wiki/research/'),
    ('Education & Honors', f'{BASE}/wiki/education/'),
    ('Wiki', f'{BASE}/wiki/'),
)
HANGUL_RE = re.compile(r'[\u1100-\u11FF\u3130-\u318F\uA960-\uA97F\uAC00-\uD7AF\uD7B0-\uD7FF]')
SOURCE_PAGES = [Path('index.md'), *sorted(Path('wiki').glob('**/*.md'))]


def _normalized_text(parts):
    return ' '.join(' '.join(parts).split())


def _assert_no_hangul(testcase, text, context):
    match = HANGUL_RE.search(text)
    if match:
        start = max(0, match.start() - 30)
        end = min(len(text), match.end() + 30)
        excerpt = text[start:end].replace('\n', ' ')
        testcase.fail(f'{context}: Hangul/Jamo character {match.group(0)!r} found near {excerpt!r}')


def _route_for_index(path):
    rel = path.relative_to(SITE)
    if rel == Path('index.html'):
        return '/'
    if rel.name != 'index.html':
        return None
    parent = rel.parent.as_posix()
    if parent == '.' or not (parent == 'wiki' or parent.startswith('wiki/')):
        return None
    return f'/{parent}/'




def _source_route_titles():
    route_titles = {}
    for source_page in SOURCE_PAGES:
        text = source_page.read_text(encoding='utf-8')
        route = re.search(r'^permalink:\s*(\S+)\s*$', text, re.MULTILINE)
        title = re.search(r'^title:\s*(.+?)\s*$', text, re.MULTILINE)
        if route and title:
            route_titles[route.group(1)] = title.group(1).strip().strip('\"\'')
    return route_titles

def _target_for_url(current_file, url):
    parts = urlsplit(url)
    if parts.scheme or parts.netloc:
        return None, parts.fragment
    if not parts.path:
        return current_file, parts.fragment
    if parts.path.startswith('/'):
        if not parts.path.startswith(BASE + '/') and parts.path != BASE:
            return None, parts.fragment
        local = unquote(parts.path[len(BASE):].lstrip('/'))
        target = SITE / local
    else:
        target = current_file.parent / unquote(parts.path)
    if target.is_dir():
        target /= 'index.html'
    return target, parts.fragment


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.source = source
        self.lang = None
        self.ids = []
        self.links = []
        self.assets = []
        self.statuses = []
        self.papers = {}
        self.active_paper = None
        self.text = []
        self.title_parts = []
        self.viewport = None
        self.description = None
        self.og_url = None
        self.canonicals = []
        self.h1s = []
        self.images = []
        self.landmarks = []
        self.primary_nav_links = []
        self.anchors = []
        self._stack = []
        self._active_anchor = None
        self._active_primary_nav = False
        self._primary_nav_depth = 0
        self.feed(source)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        classes = attrs.get('class', '').split()
        self._stack.append((tag, attrs))

        if tag == 'html':
            self.lang = attrs.get('lang')
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag in ('header', 'main', 'footer', 'nav'):
            self.landmarks.append((tag, attrs))
        if tag == 'nav' and attrs.get('aria-label') == 'Primary navigation':
            self._active_primary_nav = True
            self._primary_nav_depth = len(self._stack)
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])
            self._active_anchor = {'href': attrs['href'], 'attrs': attrs, 'text': []}
        if tag in ('img', 'script') and 'src' in attrs:
            self.assets.append(attrs['src'])
        if tag == 'img':
            self.images.append(attrs)
        if tag == 'link':
            rel = set(attrs.get('rel', '').split())
            if 'stylesheet' in rel and 'href' in attrs:
                self.assets.append(attrs['href'])
            if 'canonical' in rel and 'href' in attrs:
                self.canonicals.append(attrs['href'])
        if tag == 'meta':
            key = attrs.get('name') or attrs.get('property')
            if key == 'viewport':
                self.viewport = attrs.get('content')
            if key == 'description':
                self.description = attrs.get('content')
            if key == 'og:url':
                self.og_url = attrs.get('content')
        if tag == 'li' and 'publication-item' in classes:
            self.active_paper = attrs.get('id')
            self.papers[self.active_paper] = []
        if 'publication-status' in classes:
            self.statuses.append('accepted' if 'publication-status--accepted' in classes else 'review')

    def handle_endtag(self, tag):
        if tag == 'a' and self._active_anchor:
            self._active_anchor['text'] = _normalized_text(self._active_anchor['text'])
            self.anchors.append(self._active_anchor)
            if self._active_primary_nav:
                self.primary_nav_links.append(self._active_anchor)
            self._active_anchor = None
        if tag == 'li':
            self.active_paper = None
        if tag == 'nav' and self._active_primary_nav and len(self._stack) == self._primary_nav_depth:
            self._active_primary_nav = False
            self._primary_nav_depth = 0
        for index in range(len(self._stack) - 1, -1, -1):
            if self._stack[index][0] == tag:
                del self._stack[index:]
                break

    def handle_data(self, text):
        self.text.append(text)
        if self.active_paper:
            self.papers[self.active_paper].append(text)
        if self._active_anchor:
            self._active_anchor['text'].append(text)
        if self._stack:
            current_tag = self._stack[-1][0]
            if current_tag == 'title':
                self.title_parts.append(text)
            if current_tag == 'h1':
                self.h1s.append(text)

    @property
    def title(self):
        return _normalized_text(self.title_parts)

    @property
    def h1_text(self):
        return _normalized_text(self.h1s)

    def paper_text(self, paper_id):
        return _normalized_text(self.papers[paper_id])


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (SITE / 'index.html').is_file():
            raise RuntimeError('Build the Jekyll site first, or set SITE_DIR to a built site.')
        cls.pages = {}
        for path in SITE.rglob('index.html'):
            route = _route_for_index(path)
            if route:
                cls.pages[route] = (path, Page(path.read_text(encoding='utf-8')))
        cls.home = cls.pages['/'][1]
        cls.publications = cls.pages['/wiki/publications/'][1]
        cls.source_titles = _source_route_titles()

    def test_source_and_build_route_inventory_contains_exact_public_wiki_site(self):
        source_routes = set()
        for source_page in SOURCE_PAGES:
            text = source_page.read_text(encoding='utf-8')
            match = re.search(r'^permalink:\s*(\S+)\s*$', text, re.MULTILINE)
            self.assertIsNotNone(match, source_page)
            source_routes.add(match.group(1))
        self.assertEqual(source_routes, EXPECTED_ROUTES)
        self.assertEqual(set(self.pages), EXPECTED_ROUTES)
        self.assertEqual(len(self.pages), 14)

    def test_each_page_has_semantic_document_metadata_and_current_primary_nav(self):
        for route, (_path, page) in sorted(self.pages.items()):
            with self.subTest(route=route):
                canonical = f'{SITE_URL}{BASE}{"" if route == "/" else route}'
                if route == '/':
                    canonical = f'{SITE_URL}{BASE}/'
                self.assertEqual(page.lang, 'en')
                self.assertIn('width=device-width', page.viewport or '')
                self.assertIn('initial-scale=1', page.viewport or '')
                self.assertEqual(page.canonicals, [canonical])
                self.assertEqual(page.og_url, canonical)
                self.assertTrue(page.description and len(page.description.split()) >= 8)
                source_title = self.source_titles[route]
                self.assertTrue(page.title)
                self.assertIn('Younghwan Kil', page.title)
                self.assertIn(source_title, page.title)
                self.assertTrue(page.h1_text)
                if route == '/':
                    self.assertIn('Younghwan Kil', page.h1_text)
                else:
                    self.assertIn(source_title.split(' — ')[0].lower(), page.h1_text.lower())
                self.assertNotIn('{{', page.source)
                self.assertNotIn('{%', page.source)

                nav_pairs = [(link['text'], link['href']) for link in page.primary_nav_links]
                self.assertEqual(nav_pairs, list(EXPECTED_PRIMARY_NAV))
                education_links = [link for link in page.primary_nav_links if link['text'] == 'Education & Honors']
                self.assertEqual(len(education_links), 1)
                self.assertEqual(education_links[0]['href'], f'{BASE}/wiki/education/')

                current = [link for link in page.primary_nav_links if link['attrs'].get('aria-current') == 'page']
                self.assertEqual(len(current), 1)
                self.assertTrue(all(link is current[0] or link['attrs'].get('aria-current') != 'page' for link in page.primary_nav_links))
                expected_label = EXPECTED_NAV.get(route, 'Wiki')
                self.assertEqual(current[0]['text'], expected_label)
                if route == '/wiki/education/':
                    self.assertEqual(current[0]['href'], f'{BASE}/wiki/education/')

    def test_each_page_has_core_landmarks_and_accessibility_scaffolding(self):
        for route, (_path, page) in sorted(self.pages.items()):
            with self.subTest(route=route):
                tags = [tag for tag, _attrs in page.landmarks]
                self.assertIn('header', tags)
                self.assertIn('main', tags)
                self.assertIn('footer', tags)
                self.assertTrue(any(tag == 'nav' and attrs.get('aria-label') == 'Primary navigation' for tag, attrs in page.landmarks))
                self.assertIn('id="main-content"', page.source)
                self.assertIn('Skip to content', page.source)
                self.assertEqual(len(page.ids), len(set(page.ids)), 'Duplicate HTML id')

    def test_links_assets_images_and_internal_fragments_are_resolvable(self):
        for route, (path, page) in sorted(self.pages.items()):
            with self.subTest(route=route):
                for anchor in page.anchors:
                    href = anchor['href']
                    self.assertTrue(href.strip(), f'{path}: empty href')
                    self.assertTrue(anchor['text'] or anchor['attrs'].get('aria-label'), f'{path}: link has no accessible label: {href}')
                    self.assertNotIn('{{', href)
                    self.assertNotIn('{%', href)
                for image in page.images:
                    self.assertTrue(image.get('alt', '').strip(), f'{path}: image missing meaningful alt')
                for link in page.links + page.assets:
                    target, fragment = _target_for_url(path, link)
                    if target is None:
                        continue
                    self.assertTrue(target.is_file(), f'{path}: missing {link}')
                    if fragment:
                        target_page = page if target == path else Page(target.read_text(encoding='utf-8'))
                        self.assertIn(unquote(fragment), set(target_page.ids), f'{path}: missing fragment target {link}')

    def test_publication_statuses_and_counts(self):
        self.assertEqual(self.publications.statuses, ['accepted'] * 3 + ['review'] * 3)
        self.assertEqual(set(self.publications.papers), {'ebsg', 'ascg', 'cross-lingual', 'forbidden-fruit', 'reasoning-safety', 'placement'})
        self.assertIn('6 papers', _normalized_text(self.publications.text))
        for paper in ('forbidden-fruit', 'reasoning-safety', 'placement'):
            text = self.publications.paper_text(paper)
            self.assertIn('Under review', text)
            for stale in ('NeurIPS', 'AXIOM', 'ETRI', 'revision'):
                self.assertNotIn(stale, text)

    def test_official_author_order_and_title(self):
        self.assertIn('Younghwan Kil , Joonhyeong Park, Giung Nam, Jinwoo Shin, Juho Lee', self.publications.paper_text('ebsg'))
        text = self.publications.paper_text('placement')
        self.assertIn('Placement over Device Diversity: Efficient Learning with Fixed Physical Nonlinearities', text)
        self.assertIn('Songhyun Kim, Deukhwan Cho, Younghwan Kil , Seunghyup Yoo', text)
        self.assertIn('Cross-lingual safety asymmetry in open-weight LLMs', self.publications.paper_text('cross-lingual'))
        self.assertIn('Younghwan Gil', self.publications.paper_text('cross-lingual'))

    def test_conference_presentations_preserve_all_titles_and_acceptance_markers(self):
        text = _normalized_text(self.publications.text)
        for title in (
            'DATAN: Diffusion-Augmented Temporal Attention Network for ICU Mortality Prediction Under Sparse Clinical Observations.',
            'Uncertainty-Aware Deep Feature Interaction Attention Network for Reliable Type 2 Diabetes Detection.',
            'Set-Based Temporal Attention Networks for Clinical Time Series: A Clinical Informatics Framework.',
            'Time-Dependent Queuing Distribution for Resilient Capacity Arrangement.',
            'Optimization of Sequential Agent Order in Competitive Systems.',
        ):
            self.assertIn(title, text)
        self.assertIn('8 conference presentations', text)
        self.assertIn('International · HealthAI 2026 · Prague', text)
        self.assertEqual(text.count('HealthAI 2026 · Poster (accepted)'), 2)
        self.assertIn('Co-first author', text)
        self.assertIn('Sole author', text)
        self.assertIn('Domestic · KIIE', text)

    def test_published_sciforum_posters_are_separate_from_papers(self):
        expected = {
            'iocdt-periodontal-gat': ('https://sciforum.net/paper/34014',
                'Graph Attention Networks for Tooth-Level Periodontal Status Prediction via Inter-Tooth Spatial Dependency Modeling'),
            'iocdt-implant-classification': ('https://sciforum.net/paper/34015',
                'Temperature-Scaled Convolutional Neural Networks with Split Conformal Prediction for Reliable Dental Implant Type Classification from Panoramic Radiographs'),
            'iocdt-oral-histology-mil': ('https://sciforum.net/paper/34018',
                'Attention-Based Multi-Instance Learning for Weakly-Supervised Identification of Diagnostically Relevant Regions in Oral Squamous Cell Carcinoma Histopathology'),
        }
        for page in (self.home, self.publications):
            text = _normalized_text(page.text)
            for poster_id, (url, title) in expected.items():
                self.assertIn(poster_id, page.ids)
                self.assertIn(url, page.links)
                self.assertIn(title, text)
                self.assertNotIn(poster_id, page.papers)
            self.assertEqual(page.source.count('class="conference-poster"'), 3)
            self.assertEqual(text.count('Published 02 Oct 2026'), 3)
            self.assertIn('Nakyung Kil', text)
            self.assertIn('MDPI / Sciforum · Poster', text)
            self.assertNotIn('Poster uploaded', text)
            self.assertNotIn('PerioEDL', text)
            self.assertNotIn('178305', text)

    def test_pdf_visible_label_is_short_and_link_is_unchanged(self):
        target = BASE + '/assets/papers/ebsg-neurips-2026-camera-ready.pdf'
        for route in ('/', '/wiki/publications/', '/wiki/projects/ebsg/'):
            page = self.pages[route][1]
            anchors = [a for a in page.anchors if a['href'] == target]
            self.assertEqual(len(anchors), 1)
            self.assertTrue(anchors[0]['text'].startswith('PDF'))
            self.assertNotIn('Camera-ready', anchors[0]['text'])
            self.assertNotIn('PDF · Camera-ready', page.source)

    def test_home_uses_same_accepted_publications(self):
        self.assertEqual(self.home.statuses, ['accepted'] * 3)
        for paper in ('ebsg', 'ascg', 'cross-lingual'):
            self.assertEqual(self.home.paper_text(paper), self.publications.paper_text(paper))

    def test_home_has_no_rejected_logo_or_stats_strip(self):
        self.assertNotIn('site-brand__mark', self.home.source)
        self.assertNotIn('index-strip', self.home.source)
        self.assertNotIn('research pillars', _normalized_text(self.home.text).lower())

    def test_confirmed_work_experience_dates(self):
        for route in ('/', '/wiki/profile/', '/wiki/timeline/'):
            page = self.pages[route][1]
            text = _normalized_text(page.text)
            self.assertIn('Haean Research Institute', text)
            self.assertIn('April 2026–Present', text)
            self.assertIn('AIRS Medical', text)
            self.assertIn('Medical AI Intern', text)
        self.assertIn('September–December 2022', _normalized_text(self.home.text))

    def test_verified_links(self):
        for url in (
            'https://openreview.net/profile?id=~Younghwan_Kil1',
            'https://openreview.net/forum?id=kCWbL63oQy',
            'https://openreview.net/forum?id=S9HxdLOgqt',
            'https://doi.org/10.4218/etrij.2026-0180',
            BASE + '/assets/papers/ebsg-neurips-2026-camera-ready.pdf',
        ):
            self.assertIn(url, self.publications.links)
        self.assertNotIn('https://openreview.net/forum?id=7PYbqjhjCC', self.publications.links)

    def test_camera_ready_is_exact_verified_file(self):
        pdf = SITE / 'assets/papers/ebsg-neurips-2026-camera-ready.pdf'
        self.assertEqual(hashlib.sha256(pdf.read_bytes()).hexdigest(), '1f9355f8bdbadf1a6608d1a7486015f7eed89b57f34bfb16575b0a4b6e082914')
        self.assertEqual([p.name for p in (SITE / 'assets/papers').glob('*.pdf')], [pdf.name])

    def test_public_html_metadata_and_search_index_are_english_only(self):
        public_text_files = sorted(SITE.rglob('*.html')) + sorted(SITE.rglob('*.json'))
        self.assertTrue(public_text_files, 'built site should publish HTML and optional search JSON text files')
        for path in public_text_files:
            with self.subTest(path=path.relative_to(SITE)):
                raw = path.read_text(encoding='utf-8')
                _assert_no_hangul(self, raw, path.relative_to(SITE).as_posix())
                if path.suffix == '.json':
                    decoded = json.dumps(json.loads(raw), ensure_ascii=False)
                    _assert_no_hangul(self, decoded, f'{path.relative_to(SITE).as_posix()} decoded JSON')

    def test_education_page_preserves_degree_and_honor_facts(self):
        text = _normalized_text(self.pages['/wiki/education/'][1].text)
        for expected in (
            'M.S., Kim Jaechul Graduate School of AI',
            'Korea Advanced Institute of Science and Technology',
            'B.S., Industrial Engineering',
            'Computer Science',
            'Seoul National University',
            'Summa Cum Laude',
            'Cumulative GPA 4.00 / 4.30',
            'Merit scholarship',
            'Physics tutor',
            'KAIRI intern',
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, text)

    def test_private_and_development_files_not_published(self):
        for name in ('credentials', '.omx', '.omc', 'tests', 'scripts', 'DESIGN.md', 'README.md'):
            self.assertFalse((SITE / name).exists(), name)

    def test_no_stale_publication_copy_or_template_tokens(self):
        for route, (_path, page) in sorted(self.pages.items()):
            with self.subTest(route=route):
                self.assertNotIn('5 international papers', page.source)
                self.assertNotIn('{{', page.source)
                self.assertNotIn('{%', page.source)


if __name__ == '__main__':
    unittest.main()
