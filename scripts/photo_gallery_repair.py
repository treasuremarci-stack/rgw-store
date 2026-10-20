import hashlib
import json
import re
import subprocess
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path.cwd()
MSI_URLS = [
    "https://www.compumarts.com/cdn/shop/files/MSI-Crosshair-16-HX-AI-D2XWGKG-271NG-Gaming-Laptop_01.jpg?v=1791994594&width=1500",
    "https://www.compumarts.com/cdn/shop/files/MSI-Crosshair-16-HX-AI-D2XWGKG-271NG-Gaming-Laptop_02.jpg?v=1791994594&width=1500",
    "https://www.compumarts.com/cdn/shop/files/MSI-Crosshair-16-HX-AI-D2XWGKG-271NG-Gaming-Laptop_03.jpg?v=1791994594&width=1500",
    "https://www.compumarts.com/cdn/shop/files/MSI-Crosshair-16-HX-AI-D2XWGKG-271NG-Gaming-Laptop_04.jpg?v=1791994594&width=1500",
]

def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (RGW-store asset verifier)"})
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read(15 * 1024 * 1024)

def load(url):
    try:
        with Image.open(BytesIO(fetch(url))) as source:
            source.load()
            return source.convert("RGBA")
    except Exception as error:
        print("skip", url, error)
        return None

def near_white(pixel):
    r, g, b, a = pixel
    return a > 0 and r >= 242 and g >= 242 and b >= 242 and max(r, g, b) - min(r, g, b) <= 14

def clean(image):
    image = image.convert("RGBA")
    w, h = image.size
    px = image.load()
    queue = []
    seen = set()
    def seed(x, y):
        if (x, y) not in seen and near_white(px[x, y]):
            seen.add((x, y))
            queue.append((x, y))
    for x in range(w):
        seed(x, 0)
        seed(x, h - 1)
    for y in range(h):
        seed(0, y)
        seed(w - 1, y)
    while queue:
        x, y = queue.pop(0)
        r, g, b, _ = px[x, y]
        px[x, y] = (r, g, b, 0)
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen and near_white(px[nx, ny]):
                seen.add((nx, ny))
                queue.append((nx, ny))
    bbox = image.getchannel("A").getbbox()
    if bbox:
        pad = 18
        image = image.crop((max(0, bbox[0]-pad), max(0, bbox[1]-pad), min(w, bbox[2]+pad), min(h, bbox[3]+pad)))
    return image

def save(image, path, edge):
    image = clean(image)
    image.thumbnail((edge, edge), Image.Resampling.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "WEBP", quality=84, method=6)

def patch_record(text, product_id, paths):
    id_position = text.index('"id": "' + product_id + '"')
    start = text.rfind("  {", 0, id_position)
    newline = chr(10)
    next_marker = newline + '  {' + newline + '    "id": "'
    end = text.find(next_marker, id_position)
    if end < 0:
        end = text.find(newline + "  }" + newline + "]", id_position) + len(newline + "  }")
    record = text[start:end]
    items = "," + newline.join([])
    items = ("," + newline).join("      " + json.dumps(path, ensure_ascii=False) for path in paths)
    replacement = '"image": ' + json.dumps(paths[0], ensure_ascii=False) + ',' + newline + '    "images": [' + newline + items + newline + "    ],"
    pattern = re.compile(r'"image": "[^"]+",' + newline + r'    "images": \[.*?' + newline + r"    \],", re.S)
    updated, count = pattern.subn(replacement, record, count=1)
    if count != 1:
        raise RuntimeError("image block not found for " + product_id)
    return text[:start] + updated + text[end:]

def run_git(*args):
    subprocess.run(["git", *args], check=True)

def main():
    images = []
    seen = set()
    for url in MSI_URLS:
        image = load(url)
        if image is None:
            continue
        digest = hashlib.sha1(image.tobytes()).hexdigest()
        if digest in seen:
            continue
        seen.add(digest)
        images.append((url, image))
    if not images:
        raise RuntimeError("No unique MSI assets downloaded")
    names = ["main.webp", "angle.webp", "back.webp", "detail.webp"]
    msi_dir = ROOT / "assets/products/laptop-011"
    for old in msi_dir.glob("*.webp"):
        old.unlink()
    msi_paths = []
    for index, (url, image) in enumerate(images):
        path = f"assets/products/laptop-011/{names[index]}"
        save(image, ROOT / path, 1000 if index == 0 else 1400)
        msi_paths.append(path)

    products_path = ROOT / "products.json"
    products = products_path.read_text(encoding="utf-8")
    products = patch_record(products, "laptop-011", msi_paths)
    products = patch_record(products, "laptop-012", [
        "assets/products/laptop-012/main.webp",
        "assets/products/laptop-012/angle.webp",
    ])
    json.loads(products)
    products_path.write_text(products, encoding="utf-8")

    progress_path = ROOT / "PHOTO_PROGRESS.json"
    progress = json.loads(progress_path.read_text(encoding="utf-8"))
    for record in progress["records"]:
        if record.get("id") == "laptop-011":
            record["status"] = "completed_exact_product_page"
            record["photoCount"] = len(msi_paths)
            record["paths"] = msi_paths
            record["matchScope"] = "Точная конфигурация подтверждена страницей товара; уникальные кадры exact product page"
            record["sources"] = [
                {
                    "url": "https://www.compumarts.com/collections/laptop/products/msi-crosshair-16-hx-ai-d2xwgkg-9s7-15p421-271-intel-core-ultra-9-275hx-rtx-5070-8gb-gddr7-32gb-ddr5-2tb-ssd-16-inch-qhd-plus-240hz-windows-11-home-cosmos-gray-egypt",
                    "role": "exact-configuration-verification-and-image-source",
                },
                {
                    "url": "https://www.msi.com/Laptop/Crosshair-16-HX-AI-D2XWX",
                    "role": "official-platform-verification",
                },
            ] + [{"url": url, "role": "downloaded-image"} for url, _ in images]
        if record.get("id") == "laptop-012":
            record["photoCount"] = 2
            record["paths"] = [
                "assets/products/laptop-012/main.webp",
                "assets/products/laptop-012/angle.webp",
            ]
            record["sources"] = [
                {
                    "url": "https://global.microless.com/product/lenovo-ideapad-slim-3-15iru8-laptop-15-6-fhd-ips-display-intel-core-i5-1334u-8gb-ram-512gb-ssd-intel-iris-xe-graphics-backlit-english-keyboard-windows-11-arctic-grey-82x700edus/",
                    "role": "exact-configuration-verification",
                },
                {
                    "url": "https://psref.lenovo.com/Product/IdeaPad/IdeaPad_Slim_3_15IRU8",
                    "role": "official-platform-verification",
                },
                {
                    "url": "https://i5.walmartimages.com/seo/Lenovo-IdeaPad-Slim-3i-15-6-Laptop-15-6-Intel-Core-i5-1334U-8GB-512-SSD-82X700EDUS_707d42f6-8a35-4a79-a429-fa1d9b45c9c1.06d671f18d1e2d4e7532194c00c58d52.png?odnBg=FFFFFF&odnHeight=612&odnWidth=612",
                    "role": "downloaded-image-exact-configuration",
                },
                {
                    "url": "https://c1.neweggimages.com/productimage/nb640/A8X5S25112213H6L7C5.jpg",
                    "role": "downloaded-image-exact-configuration",
                },
            ]
            record["matchScope"] = "Точная конфигурация подтверждена страницей товара; два прямых asset exact-конфигурации"
    progress["updatedAt"] = "2026-10-20"
    progress_path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + chr(10), encoding="utf-8")

    status_path = ROOT / "PROJECT_STATUS.md"
    status_lines = status_path.read_text(encoding="utf-8").splitlines()
    new_lines = []
    for line in status_lines:
        if line.startswith("- laptop-011:"):
            line = "- laptop-011: exact product-page source; добавлено " + str(len(msi_paths)) + " уникальных WebP: " + ", ".join(msi_paths) + "."
        elif line.startswith("- laptop-012:"):
            line = "- laptop-012: exact configuration fallback; добавлено 2 WebP: assets/products/laptop-012/main.webp, assets/products/laptop-012/angle.webp."
        new_lines.append(line)
    status_path.write_text(chr(10).join(new_lines) + chr(10), encoding="utf-8")

    for path in [ROOT / ".github/workflows/photo-gallery-repair.yml", ROOT / "scripts/photo_gallery_repair.py"]:
        if path.exists():
            path.unlink()
    run_git("config", "user.name", "github-actions[bot]")
    run_git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    run_git("add", "assets/products/laptop-011", "assets/products/laptop-012", "products.json", "PHOTO_PROGRESS.json", "PROJECT_STATUS.md", ".github/workflows/photo-gallery-repair.yml", "scripts/photo_gallery_repair.py")
    run_git("diff", "--cached", "--check")
    run_git("commit", "-m", "Deduplicate remaining laptop galleries")
    run_git("push", "origin", "HEAD:main")

if __name__ == "__main__":
    main()
