"""Playwright whole-site browser smoke checks for the built academic website.

Run after `bundle exec jekyll build`:
  python3 tests/browser_smoke.py

Configuration:
  SITE_DIR      built site directory, default: _site
  BASE_URL      optional already-running site root, e.g. http://127.0.0.1:4000/younghwan-kil
  ARTIFACT_DIR  JSON and screenshot output, default: .omx/artifacts/dark-english
"""
from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import os
import threading
import unittest

from playwright.sync_api import sync_playwright

SITE = Path(os.environ.get('SITE_DIR', '_site')).resolve()
BASE_PATH = '/younghwan-kil'
ARTIFACT_DIR = Path(os.environ.get('ARTIFACT_DIR', '.omx/artifacts/dark-english'))
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
VIEWPORTS = (320, 390, 768, 900, 1440)
SCREENSHOT_ROUTES = {
    'home': '/',
    'publications': '/wiki/publications/',
    'research': '/wiki/research/',
    'wiki': '/wiki/',
    'projects': '/wiki/projects/',
    'detail': '/wiki/projects/ebsg/',
    'education': '/wiki/education/',
    'timeline': '/wiki/timeline/',
}
TABLE_ROUTES = {'/wiki/education/', '/wiki/profile/', '/wiki/timeline/'}
NO_JS_ROUTES = ('/', '/wiki/projects/ebsg/', '/wiki/education/')
EXPECTED_PRIMARY_NAV = (
    ('Home', f'{BASE_PATH}/'),
    ('Publications', f'{BASE_PATH}/wiki/publications/'),
    ('Research', f'{BASE_PATH}/wiki/research/'),
    ('Education & Honors', f'{BASE_PATH}/wiki/education/'),
    ('Wiki', f'{BASE_PATH}/wiki/'),
)


def route_for_index(path):
    rel = path.relative_to(SITE)
    if rel == Path('index.html'):
        return '/'
    if rel.name != 'index.html':
        return None
    parent = rel.parent.as_posix()
    if parent == '.' or not (parent == 'wiki' or parent.startswith('wiki/')):
        return None
    return f'/{parent}/'


def built_routes():
    routes = set()
    for path in SITE.rglob('index.html'):
        route = route_for_index(path)
        if route:
            routes.add(route)
    return routes


class SiteRootHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        split = urlsplit(path)
        request_path = unquote(split.path)
        if request_path == BASE_PATH:
            request_path = BASE_PATH + '/'
        if not request_path.startswith(BASE_PATH + '/'):
            return str(SITE / '__missing__')
        local = request_path[len(BASE_PATH):].lstrip('/')
        translated = (SITE / local).resolve()
        try:
            translated.relative_to(SITE)
        except ValueError:
            return str(SITE / '__missing__')
        return str(translated)

    def log_message(self, _format, *args):
        return


@contextmanager
def local_server():
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(SiteRootHandler, directory=str(SITE)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{server.server_port}{BASE_PATH}'
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def route_url(base_url, route):
    return base_url.rstrip('/') + route


class BrowserSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (SITE / 'index.html').is_file():
            raise RuntimeError('Build the Jekyll site first, or set SITE_DIR to a built site.')
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
        try:
            ARTIFACT_DIR.resolve().relative_to(SITE)
        except ValueError:
            pass
        else:
            raise RuntimeError('ARTIFACT_DIR must not be inside the published SITE_DIR.')
        cls.routes = sorted(built_routes())
        cls.assertion_error = None
        if set(cls.routes) != EXPECTED_ROUTES:
            missing = sorted(EXPECTED_ROUTES - set(cls.routes))
            extra = sorted(set(cls.routes) - EXPECTED_ROUTES)
            raise AssertionError(f'Route inventory mismatch; missing={missing}; extra={extra}')

    def run_site(self, callback):
        configured = os.environ.get('BASE_URL')
        if configured:
            return callback(configured.rstrip('/'))
        with local_server() as base_url:
            return callback(base_url)

    def test_all_routes_render_cleanly_across_viewports(self):
        evidence = []

        def scenario(base_url):
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                try:
                    for route in self.routes:
                        for width in VIEWPORTS:
                            page = browser.new_page(viewport={'width': width, 'height': 900}, device_scale_factor=1)
                            console_errors = []
                            page_errors = []
                            failed_local_assets = []
                            bad_statuses = []
                            page.on('console', lambda msg, errors=console_errors: errors.append(msg.text) if msg.type == 'error' else None)
                            page.on('pageerror', lambda error, errors=page_errors: errors.append(str(error)))
                            page.on('requestfailed', lambda request, failures=failed_local_assets: failures.append(request.url) if urlsplit(request.url).netloc == urlsplit(base_url).netloc else None)
                            page.on('response', lambda response, bad=bad_statuses: bad.append({'url': response.url, 'status': response.status}) if urlsplit(response.url).netloc == urlsplit(base_url).netloc and response.status >= 400 else None)
                            page.goto(route_url(base_url, route), wait_until='networkidle')
                            overflow = page.evaluate('''() => Math.ceil(document.documentElement.scrollWidth) > Math.ceil(document.documentElement.clientWidth) + 1''')
                            broken_images = page.locator('img').evaluate_all('''imgs => imgs.filter(img => !img.complete || img.naturalWidth <= 0).map(img => img.currentSrc || img.src || img.alt)''')
                            issues = []
                            if overflow:
                                issues.append('horizontal overflow')
                            if console_errors:
                                issues.append(f'console errors: {console_errors}')
                            if page_errors:
                                issues.append(f'page errors: {page_errors}')
                            if failed_local_assets:
                                issues.append(f'failed local assets: {failed_local_assets}')
                            if bad_statuses:
                                issues.append(f'bad local responses: {bad_statuses}')
                            if broken_images:
                                issues.append(f'broken images: {broken_images}')
                            issues.extend(self.primary_nav_issues(page, route, width))
                            issues.extend(self.dark_canvas_and_text_contrast_issues(page, route, width))
                            if route in TABLE_ROUTES:
                                issues.extend(self.table_content_and_reachability_issues(page, route, width))
                            evidence.append({
                                'route': route,
                                'width': width,
                                'overflow': overflow,
                                'broken_images': broken_images,
                                'console_errors': console_errors,
                                'page_errors': page_errors,
                                'failed_local_assets': failed_local_assets,
                                'bad_statuses': bad_statuses,
                                'issues': issues,
                            })
                            page.close()
                finally:
                    browser.close()

        self.run_site(scenario)
        failures = [case for case in evidence if case['issues']]
        (ARTIFACT_DIR / 'browser-smoke-responsive.json').write_text(json.dumps({'routes': self.routes, 'cases': evidence, 'failures': failures}, indent=2), encoding='utf-8')
        self.assertEqual(failures, [], f'Browser smoke failures written to {ARTIFACT_DIR / "browser-smoke-responsive.json"}')

    def primary_nav_issues(self, page, route, width):
        return page.locator('[data-site-nav]').evaluate('''(nav, args) => {
            const [route, width, expectedNav] = args;
            const issues = [];
            const links = Array.from(nav.querySelectorAll('a')).map(link => ({
              text: link.textContent.trim(),
              href: new URL(link.getAttribute('href'), location.href).pathname,
              current: link.getAttribute('aria-current') === 'page',
              visible: getComputedStyle(link).display !== 'none' && getComputedStyle(link).visibility !== 'hidden',
              rect: link.getBoundingClientRect(),
            }));
            const actualNav = links.map(link => [link.text, link.href]);
            if (JSON.stringify(actualNav) !== JSON.stringify(expectedNav)) {
              issues.push(`${route} at ${width}px primary nav mismatch: ${JSON.stringify(actualNav)}`);
            }
            const current = links.filter(link => link.current);
            if (current.length !== 1) {
              issues.push(`${route} at ${width}px should have exactly one current primary nav item, got ${current.length}`);
            } else {
              const expectedCurrent = route === '/' ? 'Home'
                : route === '/wiki/publications/' ? 'Publications'
                : route === '/wiki/research/' ? 'Research'
                : route === '/wiki/education/' ? 'Education & Honors'
                : 'Wiki';
              if (current[0].text !== expectedCurrent) {
                issues.push(`${route} at ${width}px current nav should be ${expectedCurrent}, got ${current[0].text}`);
              }
              if (route === '/wiki/education/' && current[0].href !== `${location.pathname.split('/wiki/education/')[0]}/wiki/education/`) {
                issues.push(`${route} at ${width}px Education & Honors current link should target /wiki/education/`);
              }
            }
            const toggle = document.querySelector('[data-nav-toggle]');
            const toggleVisible = toggle && getComputedStyle(toggle).display !== 'none' && getComputedStyle(toggle).visibility !== 'hidden';
            const header = document.querySelector('[data-site-header]');
            const headerRect = header && header.getBoundingClientRect();
            const navRect = nav.getBoundingClientRect();
            if (!toggleVisible) {
              const visibleLinks = links.filter(link => link.visible);
              if (visibleLinks.length !== expectedNav.length) {
                issues.push(`${route} at ${width}px desktop/tablet nav should show all ${expectedNav.length} links or switch to menu`);
              }
              if (headerRect && (navRect.right > document.documentElement.clientWidth + 1 || navRect.left < -1)) {
                issues.push(`${route} at ${width}px expanded nav should fit viewport or switch to menu`);
              }
              const rows = new Set(visibleLinks.map(link => Math.round(link.rect.top)));
              if (rows.size > 1 && width >= 768) {
                issues.push(`${route} at ${width}px primary nav wraps; switch to menu or tighten spacing`);
              }
              if (headerRect && navRect.bottom > headerRect.bottom + 1) {
                issues.push(`${route} at ${width}px primary nav overflows header height`);
              }
            } else if (width >= 900) {
              issues.push(`${route} at ${width}px should have enough space for five primary links without mobile menu`);
            }
            return issues;
          }''', [route, width, list(EXPECTED_PRIMARY_NAV)])

    def dark_canvas_and_text_contrast_issues(self, page, route, width):
        return page.evaluate('''([route, width]) => {
            const issues = [];
            const parseRgb = (value) => {
              const match = value.match(/rgba?\(([^)]+)\)/);
              if (!match) return null;
              const parts = match[1].split(',').map(part => parseFloat(part));
              if (parts.length < 3 || parts.some(Number.isNaN)) return null;
              return {r: parts[0], g: parts[1], b: parts[2], a: parts.length >= 4 ? parts[3] : 1};
            };
            const linear = (channel) => {
              const value = channel / 255;
              return value <= 0.03928 ? value / 12.92 : Math.pow((value + 0.055) / 1.055, 2.4);
            };
            const luminance = (rgb) => 0.2126 * linear(rgb.r) + 0.7152 * linear(rgb.g) + 0.0722 * linear(rgb.b);
            const contrast = (fg, bg) => {
              const lighter = Math.max(luminance(fg), luminance(bg));
              const darker = Math.min(luminance(fg), luminance(bg));
              return (lighter + 0.05) / (darker + 0.05);
            };
            const bodyBg = parseRgb(getComputedStyle(document.body).backgroundColor);
            const htmlBg = parseRgb(getComputedStyle(document.documentElement).backgroundColor);
            for (const [name, bg] of [['body', bodyBg], ['html', htmlBg]]) {
              if (!bg || bg.a === 0) {
                issues.push(`${route} at ${width}px ${name} background should be an opaque dark neutral canvas`);
                continue;
              }
              const lum = luminance(bg);
              const channelSpread = Math.max(bg.r, bg.g, bg.b) - Math.min(bg.r, bg.g, bg.b);
              if (lum > 0.08) issues.push(`${route} at ${width}px ${name} background luminance ${lum.toFixed(3)} is not dark enough`);
              if (channelSpread > 32) issues.push(`${route} at ${width}px ${name} background should be neutral black/gray, got rgb(${bg.r}, ${bg.g}, ${bg.b})`);
            }
            const canvas = bodyBg && bodyBg.a !== 0 ? bodyBg : htmlBg;
            if (!canvas) return issues;
            const candidates = Array.from(document.querySelectorAll('main h1, main h2, main h3, main p, main li, main td, main th, [data-site-nav] a'))
              .filter(node => node.textContent.trim().length >= 3)
              .filter(node => {
                const rect = node.getBoundingClientRect();
                const style = getComputedStyle(node);
                return rect.width > 0 && rect.height > 0 && style.visibility !== 'hidden' && style.display !== 'none';
              })
              .slice(0, 80);
            const lowContrast = [];
            for (const node of candidates) {
              const style = getComputedStyle(node);
              const fg = parseRgb(style.color);
              let bg = parseRgb(style.backgroundColor);
              let parent = node.parentElement;
              while ((!bg || bg.a === 0) && parent) {
                bg = parseRgb(getComputedStyle(parent).backgroundColor);
                parent = parent.parentElement;
              }
              bg = bg && bg.a !== 0 ? bg : canvas;
              if (fg && contrast(fg, bg) < 4.5) {
                lowContrast.push(`${node.tagName.toLowerCase()}:${node.textContent.trim().slice(0, 40)} (${contrast(fg, bg).toFixed(2)})`);
              }
            }
            if (lowContrast.length) {
              issues.push(`${route} at ${width}px text contrast below 4.5: ${lowContrast.slice(0, 5).join('; ')}`);
            }
            return issues;
          }''', [route, width])

    def table_content_and_reachability_issues(self, page, route, width):
        tables = page.locator('table')
        count = tables.count()
        if count <= 0:
            return [f'{route} should contain rendered table content']
        checks = tables.evaluate_all('''tables => tables.map((table) => {
            const cells = Array.from(table.querySelectorAll('th,td'));
            const headers = Array.from(table.querySelectorAll('th'));
            const firstColumnCells = Array.from(table.querySelectorAll('tr')).map(row => row.querySelector('th,td')).filter(Boolean);
            const lastColumnCells = Array.from(table.querySelectorAll('tr')).map(row => {
              const rowCells = Array.from(row.querySelectorAll('th,td'));
              return rowCells[rowCells.length - 1];
            }).filter(Boolean);

            const scrollable = (element) => {
              const style = getComputedStyle(element);
              return element.scrollWidth > element.clientWidth + 1 && /(auto|scroll)/.test(style.overflowX);
            };
            const clipsWithoutScroll = (element) => {
              const style = getComputedStyle(element);
              return element.scrollWidth > element.clientWidth + 1 && style.overflowX === 'hidden';
            };
            const visibleBounds = (element) => {
              const rect = element.getBoundingClientRect();
              return {
                left: Math.max(0, rect.left),
                right: Math.min(document.documentElement.clientWidth, rect.right),
              };
            };
            const cellsInside = (targetCells, bounds) => targetCells.every(cell => {
              const rect = cell.getBoundingClientRect();
              return rect.left >= bounds.left - 1 && rect.right <= bounds.right + 1;
            });

            let host = null;
            let clippedBy = null;
            if (scrollable(table)) {
              host = table;
            } else if (clipsWithoutScroll(table)) {
              clippedBy = table.tagName.toLowerCase();
            }
            let ancestor = table.parentElement;
            while (!host && ancestor && ancestor !== document.body) {
              if (scrollable(ancestor)) {
                host = ancestor;
                break;
              }
              if (!clippedBy && clipsWithoutScroll(ancestor)) {
                clippedBy = ancestor.className || ancestor.tagName.toLowerCase();
              }
              ancestor = ancestor.parentElement;
            }

            const tableBox = table.getBoundingClientRect();
            const viewportBounds = {left: 0, right: document.documentElement.clientWidth};
            const outerFitsViewport = tableBox.left >= -1 && tableBox.right <= document.documentElement.clientWidth + 1;
            const visibleHost = host || table;
            const originalScrollLeft = host ? host.scrollLeft : 0;
            let firstColumnReachable = cellsInside(firstColumnCells, host ? visibleBounds(host) : viewportBounds);
            let lastColumnReachable = cellsInside(lastColumnCells, host ? visibleBounds(host) : viewportBounds);

            if (host) {
              host.scrollLeft = 0;
              firstColumnReachable = cellsInside(firstColumnCells, visibleBounds(host));
              host.scrollLeft = host.scrollWidth;
              lastColumnReachable = cellsInside(lastColumnCells, visibleBounds(host));
              host.scrollLeft = originalScrollLeft;
            }

            return {
              rows: table.querySelectorAll('tr').length,
              cells: cells.length,
              headers: headers.length,
              emptyHeaders: headers.filter(header => !header.textContent.trim()).length,
              nativeTable: table.tagName.toLowerCase() === 'table',
              outerFitsViewport,
              hasHorizontalOverflow: visibleHost.scrollWidth > visibleHost.clientWidth + 1,
              hasScrollHost: Boolean(host),
              clippedBy,
              firstColumnReachable,
              lastColumnReachable,
            };
          })''')
        issues = []
        for index, check in enumerate(checks):
            prefix = f'{route} at {width}px table {index}'
            if not check['nativeTable']:
                issues.append(f'{prefix}: expected native table element')
            if check['rows'] < 2:
                issues.append(f'{prefix}: expected at least 2 rows')
            if check['cells'] < 2:
                issues.append(f'{prefix}: expected at least 2 cells')
            if check['headers'] < 1:
                issues.append(f'{prefix}: expected at least one table heading')
            if check['emptyHeaders']:
                issues.append(f'{prefix}: expected non-empty table headings')
            if check['hasHorizontalOverflow'] and not check['hasScrollHost']:
                issues.append(f'{prefix}: horizontally overflowing table needs table-or-ancestor scroll containment')
            if check['clippedBy'] and not check['hasScrollHost']:
                issues.append(f'{prefix}: columns clipped by overflow hidden on {check["clippedBy"]}')
            if not check['outerFitsViewport'] and not check['hasScrollHost']:
                issues.append(f'{prefix}: wide table needs horizontal scroll containment')
            if not check['firstColumnReachable']:
                issues.append(f'{prefix}: first column should be reachable at left scroll extent')
            if not check['lastColumnReachable']:
                issues.append(f'{prefix}: last column should be reachable at right scroll extent')
        return issues

    def test_mobile_menu_keyboard_nojs_and_reduced_motion_behaviors(self):
        evidence = {}

        def scenario(base_url):
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                try:
                    page = browser.new_page(viewport={'width': 390, 'height': 844})
                    page.goto(route_url(base_url, '/'), wait_until='networkidle')
                    toggle = page.locator('[data-nav-toggle]')
                    nav = page.locator('#site-nav')
                    page.keyboard.press('Tab')
                    self.assertTrue(page.locator('.skip-link').evaluate('(element) => document.activeElement === element'), 'first Tab should focus skip link')
                    page.keyboard.press('Enter')
                    self.assertTrue(page.locator('#main-content').evaluate('(element) => document.activeElement === element'), 'skip link should move focus to main content')
                    self.assertTrue(toggle.is_visible(), 'mobile nav toggle should be visible with JS enabled')
                    self.assertEqual(toggle.get_attribute('aria-expanded'), 'false')
                    self.assertFalse(nav.is_visible(), 'closed JS mobile menu should be visually hidden')
                    tabbable_closed = nav.locator('a').evaluate_all('''links => links.filter(link => {
                        const style = getComputedStyle(link);
                        return style.visibility !== 'hidden' && style.display !== 'none' && link.tabIndex >= 0;
                    }).length''')
                    self.assertEqual(tabbable_closed, 0, 'closed JS mobile menu links should not be tabbable')
                    toggle.click()
                    self.assertEqual(toggle.get_attribute('aria-expanded'), 'true')
                    self.assertTrue(nav.is_visible())
                    nav.get_by_text('Publications', exact=True).focus()
                    page.keyboard.press('Escape')
                    self.assertEqual(toggle.get_attribute('aria-expanded'), 'false')
                    self.assertFalse(nav.is_visible())
                    self.assertTrue(toggle.evaluate('(element) => document.activeElement === element'), 'Escape should return focus to menu toggle')
                    toggle.click()
                    nav.get_by_text('Education & Honors', exact=True).click()
                    page.wait_for_url('**/wiki/education/')
                    self.assertEqual(page.locator('[data-site-nav] a[aria-current="page"]').text_content().strip(), 'Education & Honors')
                    self.assertEqual(page.locator('[data-site-nav] a[aria-current="page"]').get_attribute('href'), f'{BASE_PATH}/wiki/education/')

                    toggle.click()
                    nav.get_by_text('Publications', exact=True).click()
                    page.wait_for_url('**/wiki/publications/')
                    self.assertEqual(page.locator('.publication-item').count(), 7)
                    self.assertEqual(page.locator('[data-site-nav] a[aria-current="page"]').text_content().strip(), 'Publications')
                    page.locator('.archive-jump a[href="#under-review"]').click()
                    page.wait_for_function("""() => {
                        const heading = document.querySelector('#under-review').getBoundingClientRect();
                        const header = document.querySelector('.site-header').getBoundingClientRect();
                        return heading.top >= header.bottom - 1 && heading.bottom < innerHeight;
                    }""")
                    evidence['anchor_heading_clear_of_sticky_header'] = 'PASS'
                    page.goto(route_url(base_url, '/'), wait_until='networkidle')
                    self.assertEqual(page.locator('details .conference-list').count(), 0)
                    presentations = page.locator('.home-section--publications .conference-list > li')
                    self.assertEqual(presentations.count(), 8)
                    for item in presentations.all():
                        self.assertTrue(item.is_visible(), 'All conference entries must be visible without a click')
                    self.assertTrue(page.get_by_text('International · HealthAI 2026 · Prague', exact=True).is_visible())
                    self.assertTrue(page.get_by_text('Domestic · KIIE', exact=True).is_visible())
                    evidence['all_conference_presentations_visible'] = 'PASS'
                    evidence['mobile_menu'] = 'PASS'

                    for route in NO_JS_ROUTES:
                        context = browser.new_context(java_script_enabled=False, viewport={'width': 390, 'height': 844})
                        nojs = context.new_page()
                        nojs.goto(route_url(base_url, route), wait_until='load')
                        self.assertTrue(nojs.locator('#site-nav').is_visible(), f'{route} no-JS navigation should remain visible')
                        self.assertFalse(nojs.locator('[data-nav-toggle]').is_visible(), f'{route} no-JS toggle should stay hidden')
                        header = nojs.locator('.site-header').bounding_box()
                        navbox = nojs.locator('#site-nav').bounding_box()
                        self.assertIsNotNone(header, f'{route} no-JS header should have a layout box')
                        self.assertIsNotNone(navbox, f'{route} no-JS navigation should have a layout box')
                        self.assertLessEqual(navbox['y'] + navbox['height'], header['y'] + header['height'] + 1, f'{route} no-JS nav should stay in header flow without overlap')
                        context.close()
                    evidence['no_js_routes'] = list(NO_JS_ROUTES)

                    for route in NO_JS_ROUTES:
                        reduced = browser.new_page(viewport={'width': 390, 'height': 844}, reduced_motion='reduce')
                        reduced.goto(route_url(base_url, route), wait_until='networkidle')
                        scroll_behavior = reduced.locator('html').evaluate('(element) => getComputedStyle(element).scrollBehavior')
                        animated = reduced.locator('*').evaluate_all('''nodes => nodes.filter(node => {
                            const style = getComputedStyle(node);
                            return parseFloat(style.animationDuration) > 0.01 || parseFloat(style.transitionDuration) > 0.01;
                        }).slice(0, 5).map(node => node.className || node.tagName)''')
                        self.assertEqual(scroll_behavior, 'auto', f'{route} should disable smooth scrolling for reduced motion')
                        self.assertEqual(animated, [], f'{route} should suppress animations/transitions for reduced motion')
                        reduced.close()
                    evidence['reduced_motion_routes'] = list(NO_JS_ROUTES)
                finally:
                    browser.close()

        self.run_site(scenario)
        (ARTIFACT_DIR / 'browser-smoke-interactions.json').write_text(json.dumps(evidence, indent=2), encoding='utf-8')

    def test_representative_screenshots_are_captured(self):
        captures = []

        def scenario(base_url):
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                try:
                    for label, route in SCREENSHOT_ROUTES.items():
                        for size_label, viewport in {
                            'desktop': {'width': 1440, 'height': 1000},
                            'mobile': {'width': 390, 'height': 844},
                        }.items():
                            page = browser.new_page(viewport=viewport, device_scale_factor=1)
                            page.goto(route_url(base_url, route), wait_until='networkidle')
                            filename = f'{label}-{size_label}.png'
                            path = ARTIFACT_DIR / filename
                            page.screenshot(path=str(path), full_page=True)
                            captures.append({'route': route, 'viewport': viewport, 'file': str(path)})
                            page.close()
                finally:
                    browser.close()

        self.run_site(scenario)
        (ARTIFACT_DIR / 'browser-smoke-screenshots.json').write_text(json.dumps({'captures': captures}, indent=2), encoding='utf-8')
        self.assertEqual(len(captures), len(SCREENSHOT_ROUTES) * 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
