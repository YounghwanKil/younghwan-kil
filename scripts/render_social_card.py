"""Render the site's text-only 1200x630 share preview using existing dev Playwright.

No network access, photo manipulation, or generated imagery is used.
Run from any directory: python3 scripts/render_social_card.py
"""
from html import escape
from pathlib import Path
import json
import subprocess
import struct

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
author_value = json.loads(subprocess.check_output([
    'ruby', '-ryaml', '-rjson', '-e',
    'print JSON.generate(YAML.safe_load(File.read(ARGV[0]), aliases: true).fetch("author"))',
    str(ROOT / '_config.yml'),
], text=True))
author = author_value['name'] if isinstance(author_value, dict) else author_value
if not isinstance(author, str) or not author.strip():
    raise ValueError('Site author must have a non-empty name')
css = (ROOT / 'assets/css/site.css').read_text()
html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<style>{css}
html, body {{ margin: 0; width: 1200px; height: 630px; overflow: hidden; }}
.share-card {{ width: 1200px; height: 630px; padding: 84px 88px; background: var(--canvas); color: var(--ink); font-family: var(--font-sans); }}
.share-card h1 {{ margin: 0 0 22px; font-size: 76px; font-weight: 600; letter-spacing: -2px; line-height: 1.08; }}
.share-role {{ margin: 0; color: var(--ink-soft); font-size: 28px; line-height: 1.45; }}
.share-focus {{ margin: 52px 0 0; max-width: 980px; font-size: 25px; line-height: 1.5; color: var(--ink-soft); }}
.share-address {{ position: absolute; left: 88px; bottom: 62px; margin: 0; color: var(--muted); font-size: 19px; }}
</style></head><body><main class="share-card">
<h1>{escape(author)}</h1>
<p class="share-role">M.S. student &amp; graduate researcher · KAIST AI</p>
<p class="share-focus">Generative-model safety · LLM safety auditing<br>Uncertainty-aware clinical AI</p>
<p class="share-address">younghwankil.github.io/younghwan-kil</p>
</main></body></html>'''
output = ROOT / 'assets/social-card.png'
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1200, 'height': 630}, device_scale_factor=1)
    page.route('**/*', lambda route: route.abort())
    page.set_content(html, wait_until='load')
    page.screenshot(path=str(output))
    browser.close()
assert struct.unpack('>II', output.read_bytes()[16:24]) == (1200, 630)
print(output)
