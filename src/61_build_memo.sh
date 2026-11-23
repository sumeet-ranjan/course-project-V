#!/usr/bin/env bash
# Build the memo PDF (A4) from outputs/deliverables/memo.md: pandoc -> standalone HTML (figures embedded) -> Chromium (Playwright) PDF.
# Requires pandoc and the pre-installed Playwright/Chromium. Check the page count afterwards (limit: 5 pages, tables and figures included).
set -e
cd "$(dirname "$0")/../outputs/deliverables"
pandoc memo.md -s --css=../../src/memo_style.css --embed-resources --metadata lang=en -o memo.html
node ../../src/memo_to_pdf.js "$PWD/memo.html" "$PWD/memo.pdf"
python3 -c "from pypdf import PdfReader; print('memo.pdf pages:', len(PdfReader('memo.pdf').pages))"
