"""SEO, sharing and machine-readable research metadata contracts."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import json
import os
import struct
import unittest

SITE = Path(os.environ.get('SITE_DIR', '_site'))
ROOT_URL = 'https://younghwankil.github.io/younghwan-kil/'
SHARE_IMAGE = ROOT_URL + 'assets/social-card.png'


class HeadMetadata(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.in_head = False
        self.meta = []
        self.links = []
        self.structured = []
        self.script = None
        self.feed(html)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'head':
            self.in_head = True
        if not self.in_head:
            return
        if tag == 'meta':
            self.meta.append(attrs)
        elif tag == 'link':
            self.links.append(attrs)
        elif tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.script = []

    def handle_data(self, text):
        if self.script is not None:
            self.script.append(text)

    def handle_endtag(self, tag):
        if tag == 'script' and self.script is not None:
            self.structured.append(json.loads(''.join(self.script)))
            self.script = None
        elif tag == 'head':
            self.in_head = False

    def values(self, key):
        return [tag.get('content') for tag in self.meta if tag.get('name') == key or tag.get('property') == key]

    def graph_nodes(self):
        return [node for graph in self.structured for node in graph.get('@graph', [graph])]


class MetadataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (SITE / 'metadata.json').is_file():
            raise RuntimeError('Build the site first, or set SITE_DIR to the built site.')
        cls.data = json.loads((SITE / 'metadata.json').read_text())
        cls.pages = [SITE / 'index.html', *sorted(SITE.glob('wiki/**/index.html'))]
        cls.heads = {path: HeadMetadata(path.read_text()) for path in cls.pages}

    def test_unique_page_descriptions_and_share_tags(self):
        self.assertEqual(len(self.pages), 14)
        descriptions = []
        for path, head in self.heads.items():
            with self.subTest(page=str(path)):
                for key in ('description', 'og:title', 'og:description', 'og:url', 'og:image',
                            'twitter:card', 'twitter:title', 'twitter:image'):
                    values = head.values(key)
                    self.assertEqual(len(values), 1, f'Duplicate/missing {key}')
                    self.assertTrue(values[0])
                for data in head.structured:
                    if isinstance(data.get('image'), dict):
                        self.assertEqual(data['image'].get('@type'), 'ImageObject')
                self.assertIn(ROOT_URL + 'metadata.json', [
                    ROOT_URL.rstrip('/') + link['href'][len('/younghwan-kil'):]
                    for link in head.links if link.get('rel') == 'describedby'
                ])
                descriptions.extend(head.values('description'))
                self.assertEqual(head.values('og:image'), [SHARE_IMAGE])
                self.assertEqual(head.values('twitter:image'), [SHARE_IMAGE])
                self.assertEqual(head.values('twitter:card'), ['summary_large_image'])
                self.assertEqual(head.values('og:image:width'), ['1200'])
                self.assertEqual(head.values('og:image:height'), ['630'])
                canonicals = [link['href'] for link in head.links if link.get('rel') == 'canonical']
                self.assertEqual(len(canonicals), 1)
                self.assertEqual(head.values('og:url'), canonicals)
        self.assertEqual(len(set(descriptions)), 14, 'Each public route needs a relevant distinct description')

    def test_share_image_size(self):
        png = (SITE / 'assets/social-card.png').read_bytes()
        self.assertTrue(png.startswith(b'\x89PNG\r\n\x1a\n'))
        self.assertEqual(struct.unpack('>II', png[16:24]), (1200, 630))

    def test_person_and_site_identity(self):
        for path, head in self.heads.items():
            with self.subTest(page=str(path)):
                nodes = {node.get('@id'): node for node in head.graph_nodes() if node.get('@id')}
                person = nodes[ROOT_URL + '#person']
                self.assertEqual(person['@type'], 'Person')
                self.assertEqual(person['name'], 'Younghwan Kil')
                self.assertEqual(person['email'], 'mailto:yhgil99@snu.ac.kr')
                self.assertEqual(person['sameAs'], [
                    'https://github.com/YounghwanKil',
                    'https://openreview.net/profile?id=~Younghwan_Kil1',
                ])
                site = nodes[ROOT_URL + '#website']
                self.assertEqual(site['@type'], 'WebSite')
                self.assertEqual(site['url'], ROOT_URL)
                self.assertEqual(site['publisher']['@id'], person['@id'])

    def test_machine_readable_record_fidelity(self):
        self.assertEqual(self.data['schema_version'], '1.0')
        self.assertEqual(self.data['site']['url'], ROOT_URL)
        self.assertEqual(self.data['site']['language'], 'en')
        papers = {paper['id']: paper for paper in self.data['papers']}
        self.assertEqual(len(papers), 7)
        self.assertEqual(Counter(p['classification'] for p in papers.values()), {'accepted': 3, 'under_review': 4})
        self.assertEqual(papers['cross-lingual']['authors'][1]['name'], 'Younghwan Gil')
        self.assertEqual(papers['cross-lingual']['venue'], 'ETRI Journal (SCIE)')
        self.assertIn({'label': 'PDF', 'url': 'https://onlinelibrary.wiley.com/doi/epdf/10.4218/etrij.2026-0180'}, papers['cross-lingual']['links'])
        for paper_id in ('reasoning-safety', 'same-loss-validation'):
            self.assertEqual([a['marker'] for a in papers[paper_id]['authors']], ['*', '*'])
            self.assertEqual(papers[paper_id]['status'], 'review')
            self.assertNotIn('venue', papers[paper_id])
        self.assertEqual([a['name'] for a in papers['same-loss-validation']['authors']], ['Sungwon Chae', 'Younghwan Kil'])
        self.assertEqual([a['name'] for a in papers['reasoning-safety']['authors']], ['Younghwan Kil', 'Sungwon Chae'])
        presentations = self.data['presentations']
        self.assertEqual(len(presentations), 8)
        self.assertEqual(Counter(p['classification'] for p in presentations), {'published_conference_poster': 3, 'conference_presentation': 5})
        for record in [*papers.values(), *presentations]:
            for link in record.get('links', []):
                self.assertEqual(urlsplit(link['url']).scheme, 'https', 'Metadata links must be portable absolute URLs')
                self.assertTrue(urlsplit(link['url']).netloc)

    def test_article_schema_does_not_invent_publication_dates(self):
        head = self.heads[SITE / 'wiki/publications/index.html']
        lists = [node for node in head.graph_nodes() if node.get('@type') == 'ItemList']
        self.assertEqual(len(lists), 1)
        self.assertEqual(lists[0]['numberOfItems'], 7)
        items = lists[0]['itemListElement']
        self.assertEqual([item['position'] for item in items], list(range(1, 8)))
        articles = [item['item'] for item in items]
        self.assertEqual(Counter(p['creativeWorkStatus'] for p in articles), {'Accepted': 3, 'Under review': 4})
        self.assertEqual(len([p for p in articles if 'identifier' in p]), 1)
        for article in articles:
            self.assertEqual(article['@type'], 'ScholarlyArticle')
            self.assertTrue(article['url'].startswith(ROOT_URL + 'wiki/publications/#'))
            self.assertNotIn('datePublished', article)
            self.assertNotIn('citationCount', article)
            paper = next(p for p in self.data['papers'] if p['id'] == article['url'].split('#')[-1])
            self.assertEqual(article['name'], paper['title'])
            self.assertEqual([a['name'] for a in article['author']], [a['name'] for a in paper['authors']])


if __name__ == '__main__':
    unittest.main()
