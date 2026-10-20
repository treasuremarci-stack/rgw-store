from __future__ import annotations

import copy
import hashlib
import io
import json
import re
import subprocess
from collections import deque
from pathlib import Path

import requests
from PIL import Image, ImageOps

TODAY = "2026-10-20"
BASE_COMMIT = "9ec8a39d671655307017538c35ad6e2e3dda73bc"
PRODUCTS_PATH = Path("products.json")
PAGE_PATH = Path("rgw_page_monoblocks.html")
STATUS_PATH = Path("PROJECT_STATUS.md")
PROGRESS_PATH = Path("MONOBLOCK_PHOTO_PROGRESS.json")
PROTECTED = ["price.csv", "product.html", "product.js", "rgw_page_laptops.html", "PHOTO_PROGRESS.json"]

SOURCE_PAGE = "https://www.msi.com/All-in-One-PC/PRO-AP272P-14MX/Gallery"
URLS = [
    "https://storage-asset.msi.com/global/picture/product/product_170435730656885befcbd0dd4ae128c4e5e2ddfdb2.webp",
    "https://storage-asset.msi.com/global/picture/product/product_170435730666d72249e958c6bd40d9ae65f935f37a.webp",
    "https://storage-asset.msi.com/global/picture/product/product_1704357309b6b7f0af88b73502671246c1fcc07fe5.webp",
    "https://storage-asset.msi.com/global/picture/product/product_1704357308882a70a64d24bc6bd2eeb30f804aefbb.webp",
    "https://storage-asset.msi.com/global/picture/product/product_1704357310e79022bb1b646afe76824d0459f57a23.webp",
]
ROLES = ["main", "angle", "back", "detail", "side"]

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (compatible; RGW-store exact MSI gallery correction/1.0)",
    "Accept": "image/avif,image/webp,image/*,*/*;q=0.8",
})


def sha256(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def is_near_white(pixel: tuple[int, int, int, int]) -> bool:
    r, g, b, a = pixel
    return a > 0 and r >= 247 and g >= 247 and b >= 247 and max(r, g, b) - min(r, g, b) <= 12


def remove_border_white(source: Image.Image) -> Image.Image:
    image = source.copy().convert("RGBA")
    width, height = image.size
    pixels = image.load()
    visited = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def seed(x: int, y: int):
        index = y * width + x
        if not visited[index] and is_near_white(pixels[x, y]):
            visited[index] = 1
            queue.append((x, y))

    for x in range(width):
        seed(x, 0)
        if height > 1:
            seed(x, height - 1)
    for y in range(height):
        seed(0, y)
        if width > 1:
            seed(width - 1, y)

    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if nx < 0 or ny < 0 or nx >= width or ny >= height:
                continue
            index = ny * width + nx
            if not visited[index] and is_near_white(pixels[nx, ny]):
                visited[index] = 1
                queue.append((nx, ny))

    for y in range(height):
        for x in range(width):
            if visited[y * width + x]:
                r, g, b, _a = pixels[x, y]
                pixels[x, y] = (r, g, b, 0)
    return image


def main():
    protected_before = {path: sha256(path) for path in PROTECTED if Path(path).exists()}
    products_before = json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))
    page_before = PAGE_PATH.read_text(encoding="utf-8")
    status_before = STATUS_PATH.read_text(encoding="utf-8")
    progress = json.loads(PROGRESS_PATH.read_text(encoding="utf-8"))

    output_dir = Path("assets/products/mono-006")
    output_dir.mkdir(parents=True, exist_ok=True)
    for old in output_dir.glob("*.webp"):
        old.unlink()

    entries = []
    seen = set()
    for index, url in enumerate(URLS):
        response = session.get(url, timeout=45)
        response.raise_for_status()
        if len(response.content) < 1500:
            raise RuntimeError(f"Small image response: {url}")
        digest = hashlib.sha256(response.content).hexdigest()
        if digest in seen:
            continue
        seen.add(digest)
        image = ImageOps.exif_transpose(Image.open(io.BytesIO(response.content)))
        image.load()
        image = remove_border_white(image)
        image.thumbnail((1000 if index == 0 else 1400, 1000 if index == 0 else 1400), Image.Resampling.LANCZOS)
        path = output_dir / f"{ROLES[len(entries)]}.webp"
        image.save(path, "WEBP", quality=84, method=6)
        with Image.open(path) as saved:
            entries.append({
                "url": url,
                "path": str(path).replace("\\", "/"),
                "role": ROLES[len(entries)],
                "width": saved.width,
                "height": saved.height,
                "bytes": path.stat().st_size,
            })

    if len(entries) != len(URLS):
        raise RuntimeError(f"Expected {len(URLS)} unique MSI images, got {len(entries)}")

    products_after = copy.deepcopy(products_before)
    record = next(item for item in products_after if item["id"] == "mono-006")
    paths = [item["path"] for item in entries]
    record["image"] = paths[0]
    record["images"] = paths
    PRODUCTS_PATH.write_text(json.dumps(products_after, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    item = next(item for item in progress["products"] if item["id"] == "mono-006")
    item.update({
        "model": "Моноблок MSI Pro AP272P AIO 27",
        "status": "complete",
        "photo_count": len(paths),
        "paths": paths,
        "source_pages": [SOURCE_PAGE],
        "source_direct": URLS,
        "selected_source_images": URLS,
        "match_note": "Пять точных product-изображений официальной Gallery MSI PRO AP272P 14M; feature-баннеры исключены.",
        "reason": "",
        "images": entries,
        "rights_note": "Official MSI source confirms the exact PRO AP272P 14M family; separate permission for commercial re-hosting was not automatically verified.",
    })
    progress["updated"] = TODAY
    progress["base_commit"] = BASE_COMMIT
    PROGRESS_PATH.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prefix = re.split(r"\n## Monoblock photo stage \(", status_before, maxsplit=1)[0].rstrip()
    lines = [
        "",
        "",
        f"## Monoblock photo stage ({TODAY})",
        "",
        f"Base stage commit: {BASE_COMMIT}. Final photo correction replaced rejected non-product assets. Laptop files and PHOTO_PROGRESS.json remain untouched.",
        "All 7 monoblock records were checked. Only exact model/configuration sources were retained; similar models, generic banners and logos were excluded.",
        "",
        "### Results",
        "",
    ]
    for current in progress["products"]:
        if current["paths"]:
            lines.append(f"- {current['id']} — {current['model']}: {current['status']}, {current['photo_count']} WebP; main photo {current['paths'][0]}.")
        else:
            lines.append(f"- {current['id']} — {current['model']}: placeholder; reason: {current['reason']}")
    lines.extend([
        "",
        "### Checks",
        "",
        "Changed product image links only for monoblock records with verified images; product names, IDs, SKUs, characteristics, prices and filters were preserved.",
        "The monoblock catalog card paths remain the same main.webp slots, and the existing product.html?id=mono-XXX gallery architecture remains unchanged.",
        "All replacement assets are WebP, are not artificially enlarged, and use border-connected white-background removal only.",
        "External-image reuse rights still require manual review; source pages and direct image URLs are recorded in MONOBLOCK_PHOTO_PROGRESS.json.",
        "",
        "### Next proposed stage",
        "",
        "After owner review, continue with photos for other categories. Laptops after commit 9ec8a39 remain outside this stage.",
    ])
    STATUS_PATH.write_text(prefix + "\n" + "\n".join(lines) + "\n", encoding="utf-8")

    if PAGE_PATH.read_text(encoding="utf-8") != page_before:
        raise RuntimeError("Catalog page changed unexpectedly")
    for path, before_hash in protected_before.items():
        if sha256(path) != before_hash:
            raise RuntimeError(f"Protected file changed unexpectedly: {path}")
    for before in products_before:
        if before["id"] != "mono-006":
            after = next(item for item in products_after if item["id"] == before["id"])
            if after != before:
                raise RuntimeError(f"Unrelated product record changed: {before['id']}")
    for item in entries:
        with Image.open(item["path"]) as image:
            if image.format != "WEBP":
                raise RuntimeError(f"Not WebP: {item['path']}")

    for temporary in (
        Path(".github/workflows/monoblock-msi-final.yml"),
        Path("scripts/monoblock_msi_final.py"),
    ):
        if temporary.exists():
            temporary.unlink()

    subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
    subprocess.run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], check=True)
    subprocess.run(["git", "add", "-A"], check=True)
    changed = subprocess.check_output(["git", "diff", "--cached", "--name-only"], text=True).splitlines()
    allowed = ("assets/products/mono-006/", "products.json", "MONOBLOCK_PHOTO_PROGRESS.json", "PROJECT_STATUS.md", ".github/workflows/monoblock-msi-final.yml", "scripts/monoblock_msi_final.py")
    forbidden = [path for path in changed if not path.startswith(allowed) or path.startswith("assets/products/laptop-") or path in PROTECTED]
    if forbidden:
        raise RuntimeError(f"Unexpected changed files: {forbidden}")
    subprocess.run(["git", "commit", "-m", "Use official MSI monoblock gallery photos [skip ci]"], check=True)
    subprocess.run(["git", "push", "origin", "HEAD:main"], check=True)
    print(json.dumps({"final_head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(), "changed_files": changed, "results": entries}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
