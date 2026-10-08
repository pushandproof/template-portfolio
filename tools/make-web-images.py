"""Turn photos into the two AVIF sizes the site loads.

Usage:  python3 tools/make-web-images.py <folder-with-photos>
Needs:  pip install pillow   (Pillow 11.3 or newer, built with AVIF support)

Input files must already be named <series>-NN.<jpg|jpeg|png|tif|tiff> (for example alpha-01.jpg).
Output: img/<name>.avif   long edge 2000 px  (opened in the full-screen viewer and the PDF)
        img/web/<name>.avif  long edge 1400 px  (grids, index, About hover)

Originals stay where they are. Do not commit originals to the site repo (see README, storage).
"""
import os
import sys
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXT = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}
SIZES = {"img": 2000, "img/web": 1400}
QUALITY = 60


def main(src):
    files = sorted(f for f in os.listdir(src) if os.path.splitext(f)[1].lower() in EXT)
    if not files:
        sys.exit("no images found in " + src)
    for f in files:
        name = os.path.splitext(f)[0]
        with Image.open(os.path.join(src, f)) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            for folder, edge in SIZES.items():
                out = im
                scale = edge / max(im.size)
                if scale < 1:
                    out = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
                dest = os.path.join(ROOT, folder)
                os.makedirs(dest, exist_ok=True)
                out.save(os.path.join(dest, name + ".avif"), quality=QUALITY)
        print("ok", name)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
