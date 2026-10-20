from __future__ import annotations

import copy
import hashlib
import html as html_lib
import io
import json
import os
import re
import subprocess
from collections import deque
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageOps

BASE_COMMIT = "9ec8a39d671655307017538c35ad6e2e3dda73bc"
TODAY = "2026-10-20"
MONO_IDS = [f"mono-{index:03d}" for index in range(1, 8)]
PHOTO_DIR = Path("assets") / "products"
PAGE_PATH = Path("rgw_page_monoblocks.html")
PRODUCTS_PATH = Path("products.json")
STATUS_PATH = Path("PROJECT_STATUS.md")
PROGRESS_PATH = Path("MONOBLOCK_PHOTO_PROGRESS.json")

PROTECTED_PATHS = [
    "price.csv",
    "product.html",
    "product.js",
    "rgw_page_laptops.html",
    "PHOTO_PROGRESS.json",
]

SOURCES = {
    "mono-001": {
        "model": "Моноблок HP 200 G4 AIO",
        "pages": [
            "https://www.hpshop.co.za/products/hp-200-g4-21-5-inch-fhd-all-in-one-pc-intel-core-i3-1215u-512gb-ssd-8gb-ram-win-11-pro-998k4et-321167",
        ],
        "direct": [],
        "hosts": ["hpshop.co.za", "hp.com", "hp.widen.net"],
        "keywords": ["200-g4", "200_g4", "998k4et", "hp-200"],
        "match_note": "Exact HP 200 G4 chassis, i3-1215U and Iron Grey source page; the catalog RAM/storage option is not visually distinguishable.",
    },
    "mono-002": {
        "model": "Моноблок HP 290",
        "pages": [],
        "direct": [],
        "hosts": [],
        "keywords": [],
        "match_note": "",
        "skip_reason": "В каталоге указано только «HP 290» без поколения, артикула и точного форм-фактора; подтверждённое фото именно этой AIO-модификации не найдено.",
    },
    "mono-003": {
        "model": "Моноблок HP AIO 27-CR0008L",
        "pages": ["https://www.hp.com/lk-en/products/desktops/product-details/2102883702"],
        "direct": [],
        "hosts": ["hp.com", "hp.widen.net"],
        "keywords": ["27-cr0008l", "b7jc2pa", "cr0008"],
        "match_note": "Official HP page for HP 27 inch All-in-One 27-cr0008l PC (B7JC2PA), matching the catalog configuration.",
    },
    "mono-004": {
        "model": "Моноблок Lenovo IdeaCentre 27IRH9, Core i7",
        "pages": [
            "https://www.lenovo.com/jp/ja/p/desktops/ideacentre/all-in-one/ideacentre-aio-i-gen-9-%2827-inch-intel%29/len102d0034",
            "https://psref.lenovo.com/Product/IdeaCentre/IdeaCentre_AIO_27IRH9?MT=F0HM",
        ],
        "direct": [
            "https://p4-ofp.static.pub/ShareResource/JPResource/JP-Images/products/ideacentre-aio-i-gen-9-27/ideacentre-aio-i-gen-9-27-584x584-hero-1.png?height=584&width=584",
        ],
        "hosts": ["lenovo.com", "psref.lenovo.com", "p4-ofp.static.pub"],
        "keywords": ["ideacentre-aio-i-gen-9-27", "27irh9", "f0hm"],
        "match_note": "Exact Lenovo IdeaCentre AIO 27IRH9 family/chassis source; the catalog has no Lenovo machine type for the i7/8GB/512GB DOS variant.",
    },
    "mono-005": {
        "model": "Моноблок Lenovo IdeaCentre 27IRH9, Core i5",
        "pages": [
            "https://www.lenovo.com/jp/ja/p/desktops/ideacentre/all-in-one/ideacentre-aio-i-gen-9-%2827-inch-intel%29/len102d0034",
            "https://elenovo.pl/lenovo-ideacentre-aio-27irh9-intel-core-i5-13420h-27-fhd-16-gb-1tb-w11-h",
        ],
        "direct": [
            "https://p4-ofp.static.pub/ShareResource/JPResource/JP-Images/products/ideacentre-aio-i-gen-9-27/ideacentre-aio-i-gen-9-27-584x584-hero-1.png?height=584&width=584",
            "https://elenovo.pl/img/cms/produkt/F0HM002PPB/07_Ideacentre_AIO_3_Hero_Front_Facing_KBM.jpg",
        ],
        "hosts": ["lenovo.com", "elenovo.pl", "p4-ofp.static.pub"],
        "keywords": ["ideacentre-aio-27irh9", "f0hm002ppb", "27irh9", "ideacentre-aio-i-gen-9-27"],
        "match_note": "Exact Lenovo IdeaCentre AIO 27IRH9 product family and matching i5/16GB/1TB configuration source.",
    },
    "mono-006": {
        "model": "Моноблок MSI Pro AP272P AIO 27",
        "pages": ["https://www.msi.com/All-in-One-PC/PRO-AP272P-14MX"],
        "direct": [
            "https://storage-asset.msi.com/global/picture/image/feature/AIO/PRO-AP272P-14M/kv.jpg",
            "https://storage-asset.msi.com/global/picture/image/feature/AIO/PRO-AP272P-14M/kv-title.png",
            "https://storage-asset.msi.com/global/picture/image/feature/AIO/PRO-AP272P-14M/ADL-title.png",
        ],
        "hosts": ["msi.com", "storage-asset.msi.com"],
        "keywords": ["pro-ap272p-14m", "ap272p"],
        "match_note": "Official MSI PRO AP272P 14M page; the page documents the i5-14500 14MQ variant and the same exact AP272P 27-inch chassis.",
    },
    "mono-007": {
        "model": "Моноблок HP AIO 27-CR0156NH",
        "pages": [
            "https://www.hp.com/emea_africa-en/products/desktops/product-details/2102522176",
            "https://www.alshariqa-erbil.com/shop/542-aio-hp-27-cr0156nh-ci7-1355u-8gb-ddr4-512gb-ssd-shared-27-inch-ips-fhd-dos-shell-white-eng-1333",
        ],
        "direct": [
            "https://www.alshariqa-erbil.com/web/image/product.image/1335/image_1024/23C1_INTEL_OPP_Maokong_27_ShellWhite_T_NT_Fixed_CaptainCrunchWired_CoreSet_FrontLeft_CamUp_GreyBG_M1547233.webp?unique=cd58b5b",
        ],
        "hosts": ["hp.com", "hp.widen.net", "alshariqa-erbil.com"],
        "keywords": ["27-cr0156nh", "a9va3ea", "cr0156"],
        "match_note": "Official HP page and an exact-config product page for HP 27-cr0156nh (A9VA3EA), i7-1355U/8GB/512GB/FHD/white.",
    },
}

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (compatible; RGW-store exact product photo stage/1.0)",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
})


def sha256_file(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fetch_text(url: str) -> str:
    response = session.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def normalize_candidate(url: str, page_url: str) -> str:
    value = html_lib.unescape(url.strip().strip("'\""))
    if value.startswith("//"):
        value = "https:" + value
    return urljoin(page_url, value)


def looks_like_image_url(url: str) -> bool:
    return bool(re.search(r"\.(?:png|jpe?g|webp)(?:$|/)", urlparse(url).path.lower()))


def discover_images(info: dict) -> list[str]:
    candidates: dict[str, int] = {}

    def add(url: str, priority: int, page_url: str = ""):
        if not url:
            return
        normalized = normalize_candidate(url, page_url)
        parsed = urlparse(normalized)
        if parsed.scheme not in {"http", "https"} or not looks_like_image_url(normalized):
            return
        host = parsed.netloc.lower()
        if info["hosts"] and not any(host == allowed or host.endswith("." + allowed) for allowed in info["hosts"]):
            return
        lowered = normalized.lower()
        if any(token in lowered for token in ("favicon", "logo", "sprite", "tracking", "loading", "placeholder", "badge", "icon")):
            return
        score = priority
        for keyword in info["keywords"]:
            if keyword.lower() in lowered:
                score += 40
        if any(token in lowered for token in ("hero", "front", "rear", "side", "angle", "gallery", "product", "kv")):
            score += 4
        candidates[normalized] = max(candidates.get(normalized, -10**9), score)

    for direct in info["direct"]:
        add(direct, 1000)

    for page_url in info["pages"]:
        try:
            source = fetch_text(page_url)
        except Exception as exc:
            print(f"source page unavailable: {page_url}: {exc}")
            continue
        soup = BeautifulSoup(source, "html.parser")
        for meta in soup.find_all("meta"):
            prop = str(meta.get("property") or meta.get("name") or "").lower()
            if prop in {"og:image", "twitter:image", "twitter:image:src"}:
                add(str(meta.get("content") or ""), 180, page_url)
        for tag in soup.find_all(["img", "source"]):
            for attr in ("src", "data-src", "data-original", "data-lazy-src", "data-image"):
                add(str(tag.get(attr) or ""), 80, page_url)
            for attr in ("srcset", "data-srcset"):
                value = str(tag.get(attr) or "")
                for entry in value.split(","):
                    add(entry.strip().split(" ")[0], 70, page_url)
        for raw in re.findall(r"https?://[^\s\"'<>]+", source):
            add(raw.replace("\\/", "/"), 40, page_url)
    return [url for url, _score in sorted(candidates.items(), key=lambda item: (-item[1], item[0]))]


def is_near_white(pixel: tuple[int, int, int, int]) -> bool:
    r, g, b, a = pixel
    return a > 0 and r >= 247 and g >= 247 and b >= 247 and max(r, g, b) - min(r, g, b) <= 12


def remove_border_white(image: Image.Image) -> Image.Image:
    image = image.copy().convert("RGBA")
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


def save_webp(image: Image.Image, path: Path, max_side: int):
    image = remove_border_white(image)
    image.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "WEBP", quality=84, method=6)


def card_replace(page_text: str, product_id: str, name: str, main_path: str) -> str:
    def replace_article(match):
        article = match.group(0)
        if f'data-product-id="{product_id}"' not in article or "<img " in article:
            return article
        alt = html_lib.escape(name, quote=True)
        image = (
            f'<img class="product-image-file" src="{main_path}" alt="{alt}" '
            'loading="lazy" decoding="async">'
        )
        return re.sub(r'<span class="placeholder-icon">.*?</span>', image, article, count=1, flags=re.S)

    return re.sub(r"<article\b[\s\S]*?</article>", replace_article, page_text)


def write_status(status_before: str, results: dict) -> str:
    lines = [
        "",
        "",
        f"## Monoblock photo stage ({TODAY})",
        "",
        f"Base stage commit: {BASE_COMMIT}. Laptop files, PHOTO_PROGRESS.json, price.csv, product.html, product.js and rgw_page_laptops.html were not changed.",
        "All 7 monoblock records from rgw_page_monoblocks.html and products.json were processed.",
        "Only exact manufacturer pages or exact configuration pages were used; similar models were not substituted.",
        "",
        "### Results",
        "",
    ]
    for product_id in MONO_IDS:
        result = results[product_id]
        name = SOURCES[product_id]["model"]
        paths = result.get("paths", [])
        if paths:
            lines.append(f"- {product_id} — {name}: {result['status']}, {len(paths)} WebP; main photo {paths[0]}.")
        else:
            lines.append(f"- {product_id} — {name}: placeholder; reason: {result['reason']}")
    lines.extend([
        "",
        "### Checks",
        "",
        "products.json was changed only for monoblocks with found images; image and images[] were added, other product records were preserved.",
        "Only image slots in the monoblock catalog cards were replaced; names, SKUs, data attributes, filters, sorting, prices and design were not changed.",
        "Saved images were converted to WebP without artificial upscaling; only border-connected white background was removed.",
        "Universal product.html?id=mono-XXX links remain unchanged; the existing product.js gallery is used.",
        "External-image reuse rights still require manual review; every source is recorded in MONOBLOCK_PHOTO_PROGRESS.json.",
        "",
        "### Next proposed stage",
        "",
        "After owner review, continue with photos for other categories. Laptops after commit 9ec8a39 were outside this stage.",
    ])
    if "## Monoblock photo stage (" in status_before:
        status_before = re.sub(r"\n\n## Monoblock photo stage [\s\S]*$", "", status_before, count=1)
    return status_before.rstrip() + "\n" + "\n".join(lines) + "\n"


def main():
    protected_before = {path: sha256_file(path) for path in PROTECTED_PATHS if Path(path).exists()}
    products_before = json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))
    page_before = PAGE_PATH.read_text(encoding="utf-8")
    status_before = STATUS_PATH.read_text(encoding="utf-8")

    by_id = {product["id"]: product for product in products_before}
    for product_id in MONO_IDS:
        if product_id not in by_id or by_id[product_id].get("category") != "Моноблоки":
            raise RuntimeError(f"Missing or invalid expected monoblock record: {product_id}")

    results = {}
    for product_id in MONO_IDS:
        info = SOURCES[product_id]
        if info.get("skip_reason"):
            results[product_id] = {
                "status": "placeholder",
                "paths": [],
                "source_urls": [],
                "selected_urls": [],
                "reason": info["skip_reason"],
            }
            continue

        selected = []
        selected_raw_hashes = set()
        output_dir = PHOTO_DIR / product_id
        roles = ["main", "angle", "back", "detail", "side", "rear"]
        for candidate in discover_images(info):
            if len(selected) >= 6:
                break
            try:
                response = session.get(candidate, timeout=45)
                response.raise_for_status()
                if len(response.content) < 1500:
                    continue
                raw_hash = hashlib.sha256(response.content).hexdigest()
                if raw_hash in selected_raw_hashes:
                    continue
                image = ImageOps.exif_transpose(Image.open(io.BytesIO(response.content)))
                image.load()
                image = image.convert("RGBA")
                if image.width < 250 or image.height < 180:
                    continue
            except Exception as exc:
                print(f"candidate rejected: {candidate}: {exc}")
                continue
            selected_raw_hashes.add(raw_hash)
            output_path = output_dir / f"{roles[len(selected)]}.webp"
            save_webp(image, output_path, 1000 if len(selected) == 0 else 1400)
            selected.append({
                "url": candidate,
                "path": str(output_path).replace(os.sep, "/"),
                "role": roles[len(selected)],
                "width": Image.open(output_path).width,
                "height": Image.open(output_path).height,
                "bytes": output_path.stat().st_size,
            })

        paths = [entry["path"] for entry in selected]
        if paths:
            results[product_id] = {
                "status": "complete" if len(paths) >= 2 else "main_only",
                "paths": paths,
                "source_urls": info["pages"] + info["direct"],
                "selected_urls": [entry["url"] for entry in selected],
                "reason": "",
                "images": selected,
            }
        else:
            results[product_id] = {
                "status": "placeholder",
                "paths": [],
                "source_urls": info["pages"] + info["direct"],
                "selected_urls": [],
                "reason": "Exact page found, but no usable image could be downloaded/decoded; placeholder retained.",
            }

    products_after = copy.deepcopy(products_before)
    for product_id, result in results.items():
        if result["paths"]:
            record = next(product for product in products_after if product["id"] == product_id)
            record["image"] = result["paths"][0]
            record["images"] = result["paths"]
    PRODUCTS_PATH.write_text(json.dumps(products_after, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    page_after = page_before
    for product_id, result in results.items():
        if result["paths"]:
            page_after = card_replace(page_after, product_id, by_id[product_id]["name"], result["paths"][0])
    PAGE_PATH.write_text(page_after, encoding="utf-8")
    STATUS_PATH.write_text(write_status(status_before, results), encoding="utf-8")

    progress = {
        "stage": "monoblock-photo-stage",
        "updated": TODAY,
        "base_commit": BASE_COMMIT,
        "category": "Моноблоки",
        "products": [],
    }
    for product_id in MONO_IDS:
        result = results[product_id]
        info = SOURCES[product_id]
        progress["products"].append({
            "id": product_id,
            "model": info["model"],
            "status": result["status"],
            "photo_count": len(result["paths"]),
            "paths": result["paths"],
            "source_pages": info["pages"],
            "source_direct": info["direct"],
            "selected_source_images": result.get("selected_urls", []),
            "match_note": info.get("match_note", ""),
            "reason": result.get("reason", ""),
            "rights_note": "Source confirms the model; separate permission for commercial re-hosting was not automatically verified.",
        })
    PROGRESS_PATH.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for path, before_hash in protected_before.items():
        if Path(path).exists() and sha256_file(path) != before_hash:
            raise RuntimeError(f"Protected file changed unexpectedly: {path}")

    non_mono_before = [product for product in products_before if product["id"] not in MONO_IDS]
    non_mono_after = [product for product in products_after if product["id"] not in MONO_IDS]
    if non_mono_before != non_mono_after:
        raise RuntimeError("A non-monoblock product record changed")

    def strip_image_slots(text: str) -> str:
        return re.sub(
            r'<(?:span class="placeholder-icon">.*?</span>|img class="product-image-file"[^>]*>)',
            "<image-slot>",
            text,
            flags=re.S,
        )
    if strip_image_slots(page_before) != strip_image_slots(page_after):
        raise RuntimeError("Monoblock catalog changed outside image slots")

    for temporary in (
        Path(".github/workflows/monoblock-photo-stage.yml"),
        Path("scripts/monoblock_photo_stage.py"),
    ):
        if temporary.exists():
            temporary.unlink()

    subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
    subprocess.run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], check=True)
    subprocess.run(["git", "add", "-A"], check=True)
    changed_files = subprocess.check_output(["git", "diff", "--cached", "--name-only"], text=True).splitlines()
    allowed_prefixes = (
        "assets/products/mono-",
        "products.json",
        "rgw_page_monoblocks.html",
        "PROJECT_STATUS.md",
        "MONOBLOCK_PHOTO_PROGRESS.json",
    )
    forbidden = [
        path for path in changed_files
        if not path.startswith(allowed_prefixes)
        or path.startswith("assets/products/laptop-")
        or path in PROTECTED_PATHS
    ]
    if forbidden:
        raise RuntimeError(f"Unexpected changed files: {forbidden}")
    if not changed_files:
        raise RuntimeError("No changes to commit")

    subprocess.run(["git", "commit", "-m", "Add verified monoblock product photos [skip ci]"], check=True)
    subprocess.run(["git", "push", "origin", "HEAD:main"], check=True)
    print(json.dumps({
        "changed_files": changed_files,
        "results": results,
        "final_head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
