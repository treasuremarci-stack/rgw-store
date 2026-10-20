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
REPO = Path(".")
PRODUCTS_PATH = REPO / "products.json"
PAGE_PATH = REPO / "rgw_page_monoblocks.html"
STATUS_PATH = REPO / "PROJECT_STATUS.md"
PROGRESS_PATH = REPO / "MONOBLOCK_PHOTO_PROGRESS.json"

PROTECTED = [
    "price.csv",
    "product.html",
    "product.js",
    "rgw_page_laptops.html",
    "PHOTO_PROGRESS.json",
]

REPLACEMENTS = {
    "mono-003": {
        "model": "Моноблок HP AIO 27-CR0008L",
        "pages": [
            "https://www.hp.com/bd-en/products/desktops/product-details/2102883702",
            "https://www.ictechdistribution.com/product/details/IC70705RRJ/hp-desktop-aio-27-cr0008l-pcintel-i5-1335u-dubai/",
        ],
        "urls": [
            "https://www.ictechdistribution.com/images/products/IC70705RRJ/HP-DESKTOP-AIO-27-CR0008L-PC-INTEL-I5-1335U-B7JC2PA-UUF-I1751M.webp",
            "https://www.ictechdistribution.com/images/products/IC70705RRJ/HP-DESKTOP-AIO-27-CR0008L-PC-INTEL-I5-1335U-B7JC2PA-UUF-I114I8.webp",
            "https://www.ictechdistribution.com/images/products/IC70705RRJ/HP-DESKTOP-AIO-27-CR0008L-PC-INTEL-I5-1335U-B7JC2PA-UUF-I253O7.webp",
        ],
        "match_note": "Точные изображения страницы HP AIO 27-CR0008L B7JC2PA#UUF; модель, корпус и конфигурация подтверждены страницей HP и карточкой с тем же артикулом.",
    },
    "mono-006": {
        "model": "Моноблок MSI Pro AP272P AIO 27",
        "pages": [
            "https://www.msi.com/All-in-One-PC/PRO-AP272P-14MX",
        ],
        "urls": [
            "https://storage-asset.msi.com/global/picture/image/feature/AIO/PRO-AP272P-14M/adjustable-stand-front-display.png",
            "https://asset.msi.com/resize/image/global/product/product_1704357310e79022bb1b646afe76824d0459f57a23.png62405b38c58fe0f07fcef2367d8a9ba1/1024.png",
            "https://storage-asset.msi.com/global/picture/image/feature/AIO/PRO-AP272P-14M/adjustable-stand-front-stand.png",
            "https://storage-asset.msi.com/global/picture/image/feature/AIO/PRO-AP272P-14M/kv.jpg",
        ],
        "match_note": "Точные официальные изображения серии MSI PRO AP272P 14M; изображения баннеров kv-title/ADL-title исключены.",
    },
    "mono-007": {
        "model": "Моноблок HP AIO 27-CR0156NH",
        "pages": [
            "https://www.hp.com/emea_africa-en/products/desktops/product-details/2102522176",
            "https://www.alshariqa-erbil.com/shop/542-aio-hp-27-cr0156nh-ci7-1355u-8gb-ddr4-512gb-ssd-shared-27-inch-ips-fhd-dos-shell-white-eng-1333",
        ],
        "urls": [
            "https://www.alshariqa-erbil.com/web/image/product.image/1335/image_1024/23C1_INTEL_OPP_Maokong_27_ShellWhite_T_NT_Fixed_CaptainCrunchWired_CoreSet_FrontLeft_CamUp_GreyBG_M1547233.webp?unique=cd58b5b",
            "https://www.alshariqa-erbil.com/web/image/product.image/1333/image_1024/23C1_OPP_Maokong_27_ShellWhite_T_NT_HAS_CaptainCrunchWired_Win11_CoreSet_FrontRight_WhiteBG_Intel_M1707533.webp?unique=35dc2df",
            "https://www.alshariqa-erbil.com/web/image/product.image/1334/image_1024/23C1_INTEL_OPP_Maokong_27_ShellWhite_T_NT_Fixed_CaptainCrunchWired_CoreSet_RearLeft_CamUp_GreyBG_M1547231.webp?unique=cd58b5b",
        ],
        "match_note": "Три точных изображения страницы HP 27-CR0156NH A9VA3EA с совпадающими i7-1355U/8GB/512GB/27-inch Shell White; общие HP-баннеры и логотип удалены.",
    },
}

ROLES = ["main", "angle", "back", "detail", "side", "rear"]
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (compatible; RGW-store exact monoblock correction/1.0)",
    "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
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


def save_webp(source_bytes: bytes, destination: Path, max_side: int) -> tuple[int, int]:
    image = ImageOps.exif_transpose(Image.open(io.BytesIO(source_bytes)))
    image.load()
    if image.width < 250 or image.height < 180:
        raise ValueError(f"image too small: {image.size}")
    image = remove_border_white(image)
    image.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, "WEBP", quality=84, method=6)
    with Image.open(destination) as saved:
        return saved.width, saved.height


def download(url: str) -> bytes:
    response = session.get(url, timeout=45)
    response.raise_for_status()
    if len(response.content) < 1500:
        raise ValueError("response is too small")
    return response.content


def clean_rejected_assets(product_id: str):
    folder = Path("assets") / "products" / product_id
    if folder.exists():
        for path in folder.glob("*.webp"):
            path.unlink()


def update_status(status_before: str, progress: dict) -> str:
    prefix = re.split(r"\n## Monoblock photo stage \(", status_before, maxsplit=1)[0].rstrip()
    lines = [
        "",
        "",
        f"## Monoblock photo stage ({TODAY})",
        "",
        f"Base stage commit: {BASE_COMMIT}. This correction removed rejected non-product images. Laptop files and PHOTO_PROGRESS.json remain untouched.",
        "All 7 monoblock records were checked. Only exact model/configuration sources were retained; similar models, generic banners and logos were excluded.",
        "",
        "### Results",
        "",
    ]
    for item in progress["products"]:
        if item["paths"]:
            lines.append(f"- {item['id']} — {item['model']}: {item['status']}, {item['photo_count']} WebP; main photo {item['paths'][0]}.")
        else:
            lines.append(f"- {item['id']} — {item['model']}: placeholder; reason: {item['reason']}")
    lines.extend([
        "",
        "### Checks",
        "",
        "Changed product image links only for mono-003, mono-006 and mono-007; product names, IDs, SKUs, characteristics, prices and filters were preserved.",
        "The monoblock catalog card paths remain the same main.webp slots, and the existing product.html?id=mono-XXX gallery architecture remains unchanged.",
        "All replacement assets are WebP, are not artificially enlarged, and use border-connected white-background removal only.",
        "External-image reuse rights still require manual review; source pages and direct image URLs are recorded in MONOBLOCK_PHOTO_PROGRESS.json.",
        "",
        "### Next proposed stage",
        "",
        "After owner review, continue with photos for other categories. Laptops after commit 9ec8a39 remain outside this stage.",
    ])
    return prefix + "\n" + "\n".join(lines) + "\n"


def main():
    protected_before = {path: sha256(path) for path in PROTECTED if Path(path).exists()}
    products_before = json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))
    page_before = PAGE_PATH.read_text(encoding="utf-8")
    status_before = STATUS_PATH.read_text(encoding="utf-8")
    progress = json.loads(PROGRESS_PATH.read_text(encoding="utf-8"))

    clean_rejected_assets("mono-003")
    clean_rejected_assets("mono-006")
    clean_rejected_assets("mono-007")

    products_after = copy.deepcopy(products_before)
    results = {}
    by_id = {item["id"]: item for item in products_after}

    for product_id, info in REPLACEMENTS.items():
        output_dir = Path("assets") / "products" / product_id
        entries = []
        seen = set()
        for index, url in enumerate(info["urls"]):
            raw = download(url)
            digest = hashlib.sha256(raw).hexdigest()
            if digest in seen:
                continue
            seen.add(digest)
            role = ROLES[len(entries)]
            destination = output_dir / f"{role}.webp"
            width, height = save_webp(raw, destination, 1000 if len(entries) == 0 else 1400)
            entries.append({
                "url": url,
                "path": str(destination).replace("\\", "/"),
                "role": role,
                "width": width,
                "height": height,
                "bytes": destination.stat().st_size,
            })

        if not entries:
            raise RuntimeError(f"No exact replacement image downloaded for {product_id}")

        paths = [entry["path"] for entry in entries]
        by_id[product_id]["image"] = paths[0]
        by_id[product_id]["images"] = paths
        results[product_id] = {
            "status": "complete" if len(paths) > 1 else "main_only",
            "photo_count": len(paths),
            "paths": paths,
            "source_pages": info["pages"],
            "source_direct": info["urls"],
            "selected_source_images": info["urls"],
            "match_note": info["match_note"],
            "reason": "",
            "images": entries,
        }

    PRODUCTS_PATH.write_text(json.dumps(products_after, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for item in progress["products"]:
        if item["id"] in results:
            item.update(results[item["id"]])
            item["rights_note"] = "Source confirms the exact model/configuration; separate permission for commercial re-hosting was not automatically verified."
    progress["updated"] = TODAY
    progress["base_commit"] = BASE_COMMIT
    PROGRESS_PATH.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    STATUS_PATH.write_text(update_status(status_before, progress), encoding="utf-8")

    if PAGE_PATH.read_text(encoding="utf-8") != page_before:
        raise RuntimeError("Catalog page changed unexpectedly")

    for path, before_hash in protected_before.items():
        if sha256(path) != before_hash:
            raise RuntimeError(f"Protected file changed unexpectedly: {path}")

    for product in products_before:
        if product["id"] not in REPLACEMENTS:
            current = next(item for item in products_after if item["id"] == product["id"])
            if current != product:
                raise RuntimeError(f"Unrelated product record changed: {product['id']}")

    for image_path in [
        path
        for item in results.values()
        for path in item["paths"]
    ]:
        with Image.open(image_path) as image:
            if image.format != "WEBP":
                raise RuntimeError(f"Not WebP: {image_path}")

    for temporary in (
        Path(".github/workflows/monoblock-photo-correction.yml"),
        Path("scripts/monoblock_photo_correction.py"),
    ):
        if temporary.exists():
            temporary.unlink()

    subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
    subprocess.run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], check=True)
    subprocess.run(["git", "add", "-A"], check=True)
    changed = subprocess.check_output(["git", "diff", "--cached", "--name-only"], text=True).splitlines()
    allowed = (
        "assets/products/mono-",
        "products.json",
        "MONOBLOCK_PHOTO_PROGRESS.json",
        "PROJECT_STATUS.md",
        ".github/workflows/monoblock-photo-correction.yml",
        "scripts/monoblock_photo_correction.py",
    )
    forbidden = [path for path in changed if not path.startswith(allowed) or path.startswith("assets/products/laptop-") or path in PROTECTED]
    if forbidden:
        raise RuntimeError(f"Unexpected changed files: {forbidden}")
    subprocess.run(["git", "commit", "-m", "Correct monoblock product photos [skip ci]"], check=True)
    subprocess.run(["git", "push", "origin", "HEAD:main"], check=True)
    print(json.dumps({
        "final_head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "changed_files": changed,
        "results": results,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
