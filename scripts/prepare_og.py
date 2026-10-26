#!/usr/bin/env python3
"""Center-crop OG artwork to 1200x630 and export optimized WebP under a size limit.

Usage: python scripts/prepare_og.py input.png output.webp --max-bytes 2000000
Requires: pip install Pillow
"""
import argparse
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageOps


def main():
    p = argparse.ArgumentParser()
    p.add_argument('input')
    p.add_argument('output')
    p.add_argument('--max-bytes', type=int, default=2_000_000)
    a = p.parse_args()
    with Image.open(a.input) as original:
        original = ImageOps.exif_transpose(original)
        img = ImageOps.fit(original.convert('RGB'), (1200, 630), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    for quality in (90, 85, 80, 75, 70, 60, 50, 40):
        buf = BytesIO()
        img.save(buf, format='WEBP', quality=quality, method=6)
        if len(buf.getvalue()) <= a.max_bytes:
            out.write_bytes(buf.getvalue())
            print(f'{out}: 1200x630 image/webp {len(buf.getvalue())} bytes quality={quality}')
            return
    raise SystemExit('Image exceeds size limit even after compression')

if __name__ == '__main__':
    main()
