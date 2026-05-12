import logging
import filecmp
import tempfile
import contextlib
from pathlib import Path
from playwright.sync_api import sync_playwright

import kilmer.compare.pdf as pdf

logger = logging.getLogger(__name__)

def cmp(a, b, wrapper=None):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        tmpdir_a = tmpdir / 'a'
        tmpdir_b = tmpdir / 'b'
        tmpdir_a.mkdir()
        tmpdir_b.mkdir()
        pdf_a = html_to_pdf(a, tmpdir_a)
        pdf_b = html_to_pdf(b, tmpdir_b)
        logger.debug(f'comparing {pdf_a} to {pdf_b}')
        return pdf.cmp(pdf_a, pdf_b, wrapper=wrapper)

def html_to_pdf(path, outdir):
    saveto = outdir / path.with_suffix('.pdf').name
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(path.as_uri())
        page.add_style_tag(content='img { max-width: 100%; height: auto; }')
        page.locator('div.info table').evaluate_all(
            'tables => tables.forEach(table => table.remove())'
        )
        page.pdf(path=saveto, format='A4')
        browser.close()
    return saveto

