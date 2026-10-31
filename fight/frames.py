#!/usr/bin/env python3
"""Seeks the SVG to exact times and screenshots them. Usage: frames.py <svg> <outdir> <bg> <t> [t...] or --all fps"""
import os, pathlib, sys
from playwright.sync_api import sync_playwright
svg, out, bg = pathlib.Path(sys.argv[1]).read_text(), pathlib.Path(sys.argv[2]), sys.argv[3]
out.mkdir(parents=True, exist_ok=True)
ts = [i / int(sys.argv[5]) for i in range(int(26 * int(sys.argv[5])))] if sys.argv[4] == '--all' else [float(x) for x in sys.argv[4:]]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['CHROME'])
    pg = b.new_page(viewport={'width': 830, 'height': 310}, device_scale_factor=2)
    pg.set_content(f'<body style="margin:0;background:{bg}">{svg}</body>')
    pg.evaluate("document.querySelector('svg').pauseAnimations()")
    for i, t in enumerate(ts):
        pg.evaluate(f"document.querySelector('svg').setCurrentTime({t})")
        pg.screenshot(path=str(out / f'{i:05d}.png'))
    b.close()
