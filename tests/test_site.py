"""Dependency-free regression checks for the built academic website.

Run after `bundle exec jekyll build`: python3 -m unittest discover -s tests -v
Set SITE_DIR to validate a separate build destination.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import hashlib
import os
import unittest

SITE = Path(os.environ.get('SITE_DIR', '_site'))
BASE = '/younghwan-kil'


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids = []
        self.links = []
        self.assets = []
        self.statuses = []
        self.papers = {}
        self.active_paper = None
        self.text = []
        self.feed(source)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        classes = attrs.get('class', '').split()
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])
        if tag in ('img', 'script') and 'src' in attrs:
            self.assets.append(attrs['src'])
        if tag == 'link' and attrs.get('rel') == 'stylesheet':
            self.assets.append(attrs['href'])
        if tag == 'li' and 'publication-item' in classes:
            self.active_paper = attrs['id']
            self.papers[self.active_paper] = []
        if 'publication-status' in classes:
            self.statuses.append('accepted' if 'publication-status--accepted' in classes else 'review')

    def handle_endtag(self, tag):
        if tag == 'li':
            self.active_paper = None

    def handle_data(self, text):
        self.text.append(text)
        if self.active_paper:
            self.papers[self.active_paper].append(text)

    def paper_text(self, paper_id):
        return ' '.join(' '.join(self.papers[paper_id]).split())


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (SITE / 'index.html').is_file():
            raise RuntimeError('Build the Jekyll site first, or set SITE_DIR to a built site.')
        cls.home = Page((SITE / 'index.html').read_text())
        cls.publications = Page((SITE / 'wiki/publications/index.html').read_text())

    def test_publication_statuses_and_counts(self):
        self.assertEqual(self.publications.statuses, ['accepted'] * 3 + ['review'] * 3)
        self.assertEqual(set(self.publications.papers), {'ebsg', 'ascg', 'cross-lingual', 'forbidden-fruit', 'reasoning-safety', 'placement'})
        self.assertIn('6 papers', ' '.join(self.publications.text))
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

    def test_home_uses_same_accepted_publications(self):
        self.assertEqual(self.home.statuses, ['accepted'] * 3)
        for paper in ('ebsg', 'ascg', 'cross-lingual'):
            self.assertEqual(self.home.paper_text(paper), self.publications.paper_text(paper))

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

    def test_private_and_development_files_not_published(self):
        for name in ('credentials', '.omx', '.omc', 'tests', 'scripts', 'DESIGN.md', 'README.md'):
            self.assertFalse((SITE / name).exists(), name)

    def test_internal_routes_assets_and_ids(self):
        for path in [SITE / 'index.html', *SITE.glob('wiki/**/index.html')]:
            source = path.read_text()
            page = Page(source)
            with self.subTest(page=str(path)):
                self.assertEqual(len(page.ids), len(set(page.ids)), 'Duplicate HTML id')
                self.assertIn('id="main-content"', source)
                self.assertIn('Skip to content', source)
                self.assertNotIn('5 international papers', source)
                self.assertNotIn('{{', source)
                self.assertNotIn('{%', source)
                for link in page.links + page.assets:
                    parts = urlsplit(link)
                    if parts.scheme or parts.netloc or not parts.path:
                        continue
                    if parts.path.startswith('/'):
                        self.assertTrue(parts.path.startswith(BASE + '/'), link)
                        target = SITE / unquote(parts.path[len(BASE):].lstrip('/'))
                    else:
                        target = path.parent / unquote(parts.path)
                    if target.is_dir():
                        target /= 'index.html'
                    self.assertTrue(target.is_file(), f'{path}: missing {link}')


if __name__ == '__main__':
    unittest.main()
