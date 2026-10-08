"""Generate placeholder images and icons so the template runs before real photos exist.

Run from the repo root:  python3 tools/make-placeholders.py
Needs: pip install pillow reportlab   (Pillow with AVIF support, 11.3 or newer)

Writes img/<series>-NN.avif (long edge 2000), img/web/<series>-NN.avif (long edge 1400),
og.jpg, favicons, manifest icons, download/PortfolioCV.zip and download/Portfolio_end.pdf.
Replace every one of these with real files. Real photos keep the same naming: <series>-NN.avif.
"""
import os
import zipfile
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_PATH = os.path.join(ROOT, "fonts", "Pretendard-Medium-subset.ttf")

# series -> (count, rule for landscape)
SERIES = {
    "alpha": (8, lambda i: i % 2 == 0),
    "beta": (8, lambda i: i == 5),
    "gamma": (8, lambda i: i % 2 == 1),
    "delta": (12, lambda i: i % 4 == 0),
}
LONG_EDGE = 2000
WEB_EDGE = 1400


def font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except OSError:
        return ImageFont.load_default()


def tone(series_idx, i):
    # a few dark frames on purpose, so the hover-contrast (white text on dark photo) can be tested
    if (series_idx + i) % 5 == 0:
        return 58
    return 205 + ((series_idx * 7 + i * 11) % 40)


def make_frame(w, h, label, gray):
    img = Image.new("RGB", (w, h), (gray, gray, gray))
    d = ImageDraw.Draw(img)
    ink = (255, 255, 255) if gray < 120 else (0, 0, 0)
    d.rectangle([0, 0, w - 1, h - 1], outline=ink, width=3)
    d.line([0, 0, w, h], fill=ink, width=2)
    d.line([0, h, w, 0], fill=ink, width=2)
    f = font(max(40, w // 14))
    tw = d.textlength(label, font=f)
    box = [(w - tw) / 2 - 24, h / 2 - f.size, (w + tw) / 2 + 24, h / 2 + f.size]
    d.rectangle(box, fill=(gray, gray, gray))
    d.text(((w - tw) / 2, h / 2 - f.size / 2), label, fill=ink, font=f)
    return img


def save_avif(img, path, edge):
    w, h = img.size
    scale = edge / max(w, h)
    if scale < 1:
        img = img.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, quality=55)


def photos():
    for si, (name, (count, is_land)) in enumerate(SERIES.items()):
        for i in range(1, count + 1):
            land = is_land(i)
            w, h = (2000, 1333) if land else (1500, 2000)
            label = f"{name}-{i:02d}"
            img = make_frame(w, h, label, tone(si, i))
            save_avif(img, os.path.join(ROOT, "img", f"{label}.avif"), LONG_EDGE)
            save_avif(img, os.path.join(ROOT, "img", "web", f"{label}.avif"), WEB_EDGE)


def icons():
    def mark(size, bg=(255, 255, 255)):
        img = Image.new("RGB", (size, size), bg)
        d = ImageDraw.Draw(img)
        m = size * 0.22
        d.ellipse([m, m, size - m, size - m], fill=(0, 0, 0))
        return img

    mark(96).save(os.path.join(ROOT, "favicon-96x96.png"))
    mark(180).save(os.path.join(ROOT, "apple-touch-icon.png"))
    mark(192).save(os.path.join(ROOT, "web-app-manifest-192x192.png"))
    mark(512).save(os.path.join(ROOT, "web-app-manifest-512x512.png"))
    mark(64).save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])

    og = make_frame(1200, 630, "og.jpg 1200x630", 225)
    og.save(os.path.join(ROOT, "og.jpg"), quality=85)


def downloads():
    d = os.path.join(ROOT, "download")
    os.makedirs(d, exist_ok=True)
    with zipfile.ZipFile(os.path.join(d, "PortfolioCV.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("README.txt", "Replace download/PortfolioCV.zip with the real portfolio and CV.\n")
    try:
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(os.path.join(d, "Portfolio_end.pdf"), pagesize=(630, 480))
        c.setFont("Helvetica", 8)
        c.drawString(42, 480 - 42 - 8, "Replace download/Portfolio_end.pdf with the closing page (630 x 480 pt).")
        c.save()
    except ImportError:
        print("reportlab not installed: download/Portfolio_end.pdf was not created")


if __name__ == "__main__":
    photos()
    icons()
    downloads()
    print("placeholders written")
