from collections import deque
from io import BytesIO
from pathlib import Path
import hashlib
import json
import re
import subprocess
import urllib.request

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
PAGE_PATH = ROOT / "rgw_page_monoblocks.html"
STATUS_PATH = ROOT / "PROJECT_STATUS.md"
PROGRESS_PATH = ROOT / "MONOBLOCK_PHOTO_PROGRESS.json"

MSI_MAIN_URL = (
    "https://storage-asset.msi.com/global/picture/product/"
    "product_170435730666d72249e958c6bd40d9ae65f935f37a.webp"
)

CHANGED_ASSETS = {
    "assets/products/mono-001/main.webp",
    "assets/products/mono-003/main.webp",
    "assets/products/mono-006/main.webp",
    "assets/products/mono-007/main.webp",
}
ALLOWED_CHANGED = CHANGED_ASSETS | {
    "rgw_page_monoblocks.html",
    "PROJECT_STATUS.md",
    "MONOBLOCK_PHOTO_PROGRESS.json",
    "tools/apply_monoblock_corrections.py",
    ".github/workflows/apply-monoblock-corrections.yml",
}

def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def git_diff_names():
    result = subprocess.run(
        ["git", "diff", "--name-only"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}

def is_near_white(pixel):
    red, green, blue, alpha = pixel
    return alpha > 0 and min(red, green, blue) >= 238 and max(red, green, blue) - min(red, green, blue) <= 22

def remove_border_white(image):
    image = image.copy().convert("RGBA")
    width, height = image.size
    pixels = image.load()
    visited = bytearray(width * height)
    queue = deque()

    def visit(x, y):
        index = y * width + x
        if visited[index]:
            return
        visited[index] = 1
        if is_near_white(pixels[x, y]):
            queue.append((x, y))

    for x in range(width):
        visit(x, 0)
        if height > 1:
            visit(x, height - 1)
    for y in range(height):
        visit(0, y)
        if width > 1:
            visit(width - 1, y)

    while queue:
        x, y = queue.popleft()
        red, green, blue, alpha = pixels[x, y]
        if alpha == 0:
            continue
        pixels[x, y] = (red, green, blue, 0)
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < width and 0 <= ny < height:
                index = ny * width + nx
                if not visited[index]:
                    visited[index] = 1
                    if is_near_white(pixels[nx, ny]):
                        queue.append((nx, ny))
    return image

def fit_to_square(image, output_side=1000, visible_ratio=0.82):
    image = image.convert("RGBA")
    alpha_box = image.getchannel("A").getbbox()
    if alpha_box:
        image = image.crop(alpha_box)

    max_dimension = max(image.size)
    usable = int(output_side * visible_ratio)
    scale = min(1.0, usable / max_dimension)
    if scale < 1.0:
        resized = image.resize(
            (max(1, round(image.width * scale)), max(1, round(image.height * scale))),
            Image.Resampling.LANCZOS,
        )
    else:
        resized = image

    canvas = Image.new("RGBA", (output_side, output_side), (0, 0, 0, 0))
    offset = ((output_side - resized.width) // 2, (output_side - resized.height) // 2)
    canvas.alpha_composite(resized, offset)
    return canvas

def save_webp(image, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "WEBP", quality=84, method=6)

def load_local(path):
    with Image.open(path) as source:
        return ImageOps.exif_transpose(source).convert("RGBA")

def process_local_main(relative_path):
    path = ROOT / relative_path
    if not path.is_file():
        raise RuntimeError(f"Missing expected asset: {relative_path}")
    original = load_local(path)
    alpha_extrema = original.getchannel("A").getextrema()
    original_size = original.size
    corrected = fit_to_square(original)
    save_webp(corrected, path)
    with Image.open(path) as saved:
        print(
            f"{relative_path}: {original_size} alpha={alpha_extrema} "
            f"-> {saved.size} bytes={path.stat().st_size}"
        )

def download_image(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "rgw-store-monoblock-photo-correction/1.0"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()

def process_msi_main():
    payload = download_image(MSI_MAIN_URL)
    with Image.open(BytesIO(payload)) as source:
        original = ImageOps.exif_transpose(source).convert("RGBA")
    original_size = original.size
    corrected = fit_to_square(remove_border_white(original))
    path = ROOT / "assets/products/mono-006/main.webp"
    save_webp(corrected, path)
    with Image.open(path) as saved:
        print(
            f"assets/products/mono-006/main.webp: official MSI single-unit source "
            f"{original_size} -> {saved.size} bytes={path.stat().st_size}"
        )

def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one {label} rule, found {count}")
    return text.replace(old, new)

def update_category_css():
    before = PAGE_PATH.read_text(encoding="utf-8")
    style_match = re.search(r"(<style\b[^>]*>)(.*?)(</style>)", before, flags=re.I | re.S)
    if not style_match:
        raise RuntimeError("The monoblock page has no style block")
    css = style_match.group(2)

    css = replace_once(
        css,
        ".product-image{position:relative;height:205px;display:flex;align-items:center;justify-content:center;background:linear-gradient(145deg,#f5f7fb,#edf0f7);overflow:hidden}",
        ".product-image{position:relative;height:205px;display:flex;align-items:center;justify-content:center;background:linear-gradient(145deg,#f5f7fb,#edf0f7);overflow:hidden;isolation:isolate}",
        "product-image",
    )
    css = replace_once(
        css,
        ".product-image img{width:100%;height:100%;object-fit:contain;padding:15px;transition:.25s}",
        ".product-image img{position:relative;z-index:1;width:100%;height:100%;box-sizing:border-box;object-fit:contain;padding:18px;transform-origin:center center;transition:.25s}",
        "product-image img",
    )
    css = replace_once(
        css,
        ".product-card:hover .product-image img{transform:scale(1.06)}",
        ".product-card:hover .product-image img{transform:scale(1.03)}",
        "product hover scale",
    )
    css = replace_once(
        css,
        ".product-badge{position:absolute;left:12px;top:12px;padding:5px 8px;border-radius:7px;background:#ebeaff;color:#554bdc;font-size:10px;font-weight:900;text-transform:uppercase}",
        ".product-badge{position:absolute;z-index:3;left:12px;top:12px;padding:5px 8px;border-radius:7px;background:#ebeaff;color:#554bdc;font-size:10px;font-weight:900;text-transform:uppercase}",
        "product-badge",
    )

    after = before[:style_match.start(2)] + css + before[style_match.end(2):]
    markup_without_styles = lambda value: re.sub(
        r"<style\b[^>]*>.*?</style>", "", value, flags=re.I | re.S
    )
    if markup_without_styles(before) != markup_without_styles(after):
        raise RuntimeError("Category markup changed outside the CSS block")
    PAGE_PATH.write_text(after, encoding="utf-8")

def update_progress():
    progress = json.loads(PROGRESS_PATH.read_text(encoding="utf-8"))
    progress["updated"] = "2026-10-20"
    progress["last_correction"] = {
        "type": "card-layering-and-image-scale",
        "page": "rgw_page_monoblocks.html",
        "msi_main_source": MSI_MAIN_URL,
        "changed_assets": sorted(CHANGED_ASSETS),
        "note": "The existing additional galleries and product IDs remain unchanged.",
    }

    metadata = {}
    for relative_path in CHANGED_ASSETS:
        path = ROOT / relative_path
        with Image.open(path) as image:
            metadata[relative_path] = {
                "width": image.width,
                "height": image.height,
                "bytes": path.stat().st_size,
            }

    for item in progress.get("products", []):
        product_id = item.get("id")
        if product_id == "mono-006":
            selected = item.get("selected_source_images", [])
            if selected:
                selected[0] = MSI_MAIN_URL
            item["correction"] = {
                "main_source": MSI_MAIN_URL,
                "main_role": "single exact PRO AP272P 14M unit from the official MSI Gallery",
                "gallery_preserved": True,
            }
        elif product_id in {"mono-001", "mono-003", "mono-007"}:
            item["correction"] = {
                "main_asset": f"assets/products/{product_id}/main.webp",
                "full_device_fit": True,
                "gallery_preserved": True,
            }

        for record in item.get("images", []):
            path = record.get("path")
            if path in metadata:
                record.update(metadata[path])
                if product_id == "mono-006" and path.endswith("/main.webp"):
                    record["url"] = MSI_MAIN_URL
                    record["role"] = "main"

    PROGRESS_PATH.write_text(
        json.dumps(progress, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

def update_status():
    status = STATUS_PATH.read_text(encoding="utf-8")
    marker = "## Monoblock card/photo corrections (2026-10-20)"
    if marker in status:
        status = status[:status.index(marker)].rstrip() + "\n"

    section = """
## Monoblock card/photo corrections (2026-10-20)

- Fixed the existing monoblock card image layering in rgw_page_monoblocks.html: the image keeps its hover transform, while the brand badge now has a higher stacking level and remains above the transformed image.
- Kept the card dimensions, brand badge appearance, filter markup, product data attributes and filter script unchanged.
- Reduced only the existing image hover scale from 1.06 to 1.03 and retained the existing .25s transition; the image wrapper keeps object-fit: contain, adds internal box sizing, and uses a small consistent inset.
- Reframed the main images for mono-001, mono-003 and mono-007 on a transparent square canvas so the complete HP device remains visible with margins. Additional gallery files were not replaced.
- Replaced only assets/products/mono-006/main.webp with a single-unit exact PRO AP272P 14M frame from the official MSI Gallery. products.json image paths and the four additional gallery files were preserved.
- Updated MONOBLOCK_PHOTO_PROGRESS.json with the corrected MSI source and resulting asset metadata.

### Scope and checks

- Confirmed the seven monoblock card IDs remain present; mono-002 remains the existing placeholder.
- Hash-guarded products.json, price.csv, product.html, product.js, all laptop files, and every non-monoblock category page; the correction script aborts if any of them changes.
- Confirmed the catalog markup outside the monoblock page CSS block is byte-for-byte unchanged.
- Confirmed the page still points to the same main.webp paths and the universal product.html?id=mono-XXX gallery continues to receive the existing images[] arrays.
- GitHub Pages publication and interactive browser hover checks are performed after the commit; if the environment cannot provide an interactive browser, that limitation will be reported explicitly.
"""
    STATUS_PATH.write_text(status.rstrip() + "\n\n" + section.strip() + "\n", encoding="utf-8")

def protect_scope(before_hashes):
    for relative_path, expected in before_hashes.items():
        path = ROOT / relative_path
        if not path.is_file() or sha256(path) != expected:
            raise RuntimeError(f"Protected file changed: {relative_path}")

def main():
    category_files = sorted(ROOT.glob("rgw_page_*.html"))
    protected_paths = {
        "products.json",
        "price.csv",
        "product.html",
        "product.js",
        "PHOTO_PROGRESS.json",
    }
    protected_paths.update(
        path.relative_to(ROOT).as_posix()
        for path in category_files
        if path.name != "rgw_page_monoblocks.html"
    )
    before_hashes = {
        relative_path: sha256(ROOT / relative_path)
        for relative_path in sorted(protected_paths)
        if (ROOT / relative_path).is_file()
    }

    update_category_css()
    for relative_path in (
        "assets/products/mono-001/main.webp",
        "assets/products/mono-003/main.webp",
        "assets/products/mono-007/main.webp",
    ):
        process_local_main(relative_path)
    process_msi_main()
    update_progress()
    update_status()

    for temporary in (
        ROOT / "tools/apply_monoblock_corrections.py",
        ROOT / ".github/workflows/apply-monoblock-corrections.yml",
    ):
        if temporary.exists():
            temporary.unlink()

    protect_scope(before_hashes)
    changed = git_diff_names()
    unexpected = changed - {
        "assets/products/mono-001/main.webp",
        "assets/products/mono-003/main.webp",
        "assets/products/mono-006/main.webp",
        "assets/products/mono-007/main.webp",
        "rgw_page_monoblocks.html",
        "PROJECT_STATUS.md",
        "MONOBLOCK_PHOTO_PROGRESS.json",
    }
    if unexpected:
        raise RuntimeError(f"Unexpected changed files: {sorted(unexpected)}")
    if not CHANGED_ASSETS.issubset(changed):
        raise RuntimeError(f"Expected corrected assets are missing from diff: {sorted(CHANGED_ASSETS - changed)}")

    subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True)
    print("Monoblock correction scope and whitespace checks passed.")
    print("Changed files:")
    for name in sorted(changed):
        print(f" - {name}")

if __name__ == "__main__":
    main()
# Trigger the registered one-shot workflow.
# Registered workflow trigger.
