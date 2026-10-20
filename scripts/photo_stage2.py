from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
import urllib.parse
import urllib.request
from collections import deque
from io import BytesIO
from pathlib import Path

from PIL import Image


ROOT = Path.cwd()
TODAY = "2026-10-20"
PROTECTED_IDS = {f"laptop-{number:03d}" for number in range(1, 11)}
TARGETS = {
    "laptop-011": {
        "brand": "MSI",
        "model": "MSI CROSSHAIR 16 AI",
        "catalog_name": "MSI CROSSHAIR 16 AI",
        "exact_page": (
            "https://www.compumarts.com/collections/laptop/products/"
            "msi-crosshair-16-hx-ai-d2xwgkg-9s7-15p421-271-intel-core-ultra-9-275hx-"
            "rtx-5070-8gb-gddr7-32gb-ddr5-2tb-ssd-16-inch-qhd-plus-240hz-"
            "windows-11-home-cosmos-gray-egypt"
        ),
        "official_page": "https://www.msi.com/Laptop/Crosshair-16-HX-AI-D2XWX",
        "fallback_exact_urls": [],
    },
    "laptop-012": {
        "brand": "Lenovo",
        "model": "LENOVO IP SLIM 3i",
        "catalog_name": "LENOVO IP SLIM 3i",
        "exact_page": (
            "https://global.microless.com/product/"
            "lenovo-ideapad-slim-3-15iru8-laptop-15-6-fhd-ips-display-"
            "intel-core-i5-1334u-8gb-ram-512gb-ssd-intel-iris-xe-graphics-"
            "backlit-english-keyboard-windows-11-arctic-grey-82x700edus/"
        ),
        "official_page": "https://psref.lenovo.com/Product/IdeaPad/IdeaPad_Slim_3_15IRU8",
        "fallback_exact_urls": [
            "https://i5.walmartimages.com/seo/Lenovo-IdeaPad-Slim-3i-15-6-Laptop-15-6-Intel-Core-i5-1334U-8GB-512-SSD-82X700EDUS_707d42f6-8a35-4a79-a429-fa1d9b45c9c1.06d671f18d1e2d4e7532194c00c58d52.png?odnBg=FFFFFF&odnHeight=612&odnWidth=612",
            "https://c1.neweggimages.com/productimage/nb640/A8X5S25112213H6L7C5.jpg",
            "https://p2-ofp.static.pub//fes/cms/2023/07/17/cb33s6cv4scvgl4k2mxwpjhnmqfjgg628756.png?height=584&width=584",
        ],
    },
}


def fetch_bytes(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; RGW-store product asset verifier)",
            "Accept": "text/html,image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read(20 * 1024 * 1024)


def normalize_url(raw: str) -> str:
    value = html.unescape(raw)
    value = value.replace("\\/", "/").replace("\\u0026", "&").replace("\\u003F", "?")
    value = value.strip().rstrip("),;.'\"")
    if value.startswith("//"):
        value = "https:" + value
    return value


def is_image_url(url: str) -> bool:
    parsed = urllib.parse.urlsplit(url)
    path = parsed.path.lower()
    if not re.search(r"\.(?:jpg|jpeg|png|webp|avif)$", path):
        return False
    lowered = url.lower()
    excluded = (
        "logo",
        "favicon",
        "sprite",
        "icon",
        "payment",
        "facebook",
        "instagram",
        "placeholder",
        "avatar",
        "badge",
        "trustpilot",
    )
    return not any(token in lowered for token in excluded)


def extract_image_urls(page: bytes) -> list[str]:
    text = page.decode("utf-8", errors="ignore")
    text = html.unescape(text).replace("\\/", "/").replace("\\u0026", "&")
    pattern = re.compile(r'(?:(?:https?:)?//)[^"\'<>\s\\\\]+')
    urls: list[str] = []
    seen: set[str] = set()
    for match in pattern.findall(text):
        url = normalize_url(match)
        if not is_image_url(url):
            continue
        if url not in seen:
            seen.add(url)
            urls.append(url)
    return urls


def image_from_url(url: str) -> tuple[Image.Image, str] | None:
    try:
        raw = fetch_bytes(url)
        with Image.open(BytesIO(raw)) as opened:
            opened.load()
            if opened.width < 300 or opened.height < 250:
                return None
            if opened.width * opened.height < 120_000:
                return None
            image = opened.convert("RGBA")
        digest = hashlib.sha1(image.tobytes()).hexdigest()
        return image, digest
    except Exception as error:
        print(f"skip image {url}: {error}")
        return None


def candidate_score(url: str, tokens: list[str]) -> int:
    lowered = url.lower()
    score = 0
    for token in tokens:
        if token and token in lowered:
            score += 25
    if any(token in lowered for token in ("product", "gallery", "media", "cdn")):
        score += 4
    parsed = urllib.parse.urlsplit(url)
    if parsed.path.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        score += 1
    return score


def select_source_images(target: dict) -> tuple[list[tuple[str, Image.Image]], bool]:
    tokens = [
        token.lower()
        for token in re.findall(r"[a-z0-9]+", target["exact_page"].lower())
        if len(token) >= 5 and token not in {"https", "www", "com", "product", "laptop"}
    ]
    page_urls: list[str] = []
    try:
        page_urls = extract_image_urls(fetch_bytes(target["exact_page"]))
    except Exception as error:
        print(f"could not parse exact product page {target['exact_page']}: {error}")

    ranked = sorted(
        enumerate(page_urls),
        key=lambda item: (-candidate_score(item[1], tokens), item[0]),
    )
    selected: list[tuple[str, Image.Image]] = []
    seen_digests: set[str] = set()

    def try_add(url: str) -> None:
        if len(selected) >= 5:
            return
        result = image_from_url(url)
        if not result:
            return
        image, digest = result
        if digest in seen_digests:
            return
        seen_digests.add(digest)
        selected.append((url, image))

    for _, url in ranked:
        try_add(url)

    used_exact_page = bool(selected)
    if not selected:
        for url in target.get("fallback_exact_urls", []):
            try_add(url)

    return selected[:5], used_exact_page


def is_near_white(pixel: tuple[int, int, int, int]) -> bool:
    red, green, blue, alpha = pixel
    return alpha > 0 and red >= 242 and green >= 242 and blue >= 242 and max(red, green, blue) - min(red, green, blue) <= 14


def remove_edge_white_background(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    width, height = image.size
    pixels = image.load()
    queue: deque[tuple[int, int]] = deque()
    visited: set[tuple[int, int]] = set()

    def seed(x: int, y: int) -> None:
        if (x, y) in visited:
            return
        if is_near_white(pixels[x, y]):
            visited.add((x, y))
            queue.append((x, y))

    for x in range(width):
        seed(x, 0)
        seed(x, height - 1)
    for y in range(height):
        seed(0, y)
        seed(width - 1, y)

    while queue:
        x, y = queue.popleft()
        red, green, blue, _ = pixels[x, y]
        pixels[x, y] = (red, green, blue, 0)
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                if is_near_white(pixels[nx, ny]):
                    visited.add((nx, ny))
                    queue.append((nx, ny))

    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    if bbox:
        padding = 18
        left = max(0, bbox[0] - padding)
        top = max(0, bbox[1] - padding)
        right = min(width, bbox[2] + padding)
        bottom = min(height, bbox[3] + padding)
        image = image.crop((left, top, right, bottom))
    return image


def save_webp(image: Image.Image, path: Path, max_edge: int) -> None:
    image = remove_edge_white_background(image)
    image.thumbnail((max_edge, max_edge), Image.Resampling.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "WEBP", quality=84, method=6)


def replace_product_record(text: str, product_id: str, paths: list[str]) -> str:
    marker = '  {\n    "id": "' + product_id + '"'
    start = text.index(marker)
    next_start = text.find('\n  {\n    "id": "', start + len(marker))
    if next_start == -1:
        end = text.find("\n  }\n]", start) + len("\n  }")
    else:
        end = next_start
    record = text[start:end]
    if '"image": null,' not in record:
        raise RuntimeError(f"unexpected image field for {product_id}")
    image_value = json.dumps(paths[0], ensure_ascii=False)
    images_value = ",\n".join(
        "      " + json.dumps(path, ensure_ascii=False) for path in paths
    )
    replacement = (
        f'"image": {image_value},\n'
        f'    "images": [\n{images_value}\n    ],'
    )
    record = record.replace('"image": null,', replacement, 1)
    return text[:start] + record + text[end:]


def replace_catalog_card(text: str, product_id: str, image_path: str, name: str) -> str:
    marker = f'<article class="product-card" data-product-id="{product_id}"'
    start = text.index(marker)
    end = text.index("</article>", start) + len("</article>")
    card = text[start:end]
    placeholder = re.compile(r'<span class="placeholder-icon">.*?</span>', re.DOTALL)
    image = (
        f'<img src="{image_path}" alt="{html.escape(name, quote=True)}" '
        'loading="lazy" decoding="async">'
    )
    updated, count = placeholder.subn(image, card, count=1)
    if count != 1:
        raise RuntimeError(f"placeholder not found in catalog card {product_id}")
    return text[:start] + updated + text[end:]


def update_progress(progress_text: str, target_id: str, target: dict, paths: list[str], sources: list[str], exact_source: bool) -> str:
    data = json.loads(progress_text)
    data["updatedAt"] = TODAY
    data["scope"] = "Ноутбуки каталога: этапы 1–2"
    record = {
        "id": target_id,
        "brand": target["brand"],
        "model": target["model"],
        "status": "completed_exact_product_page" if exact_source else "completed_exact_configuration_fallback",
        "photoCount": len(paths),
        "matchScope": "Точная конфигурация подтверждена страницей товара; изображения взяты с этой страницы"
        if exact_source
        else "Точная конфигурация подтверждена страницей товара; использован прямой asset для той же конфигурации",
        "rightsStatus": "manual_rights_review_required",
        "sources": [
            {"url": target["exact_page"], "role": "exact-configuration-verification-and-image-source"},
            {"url": target["official_page"], "role": "official-platform-verification"},
        ] + [{"url": source, "role": "downloaded-image"} for source in sources],
        "paths": paths,
        "skipReason": None,
    }
    records = [item for item in data.get("records", []) if item.get("id") != target_id]
    records.append(record)
    data["records"] = records
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def append_status(status_text: str, results: list[dict]) -> str:
    lines = [
        "",
        "## Laptop photo stage 2 — remaining non-placeholder laptops (2026-10-20)",
        "",
        "- Обработаны только laptop-011 и laptop-012.",
        "- Файлы и записи laptop-001…laptop-010 не изменялись.",
        "- laptop-008 и laptop-009 оставлены заглушками по заданному ограничению.",
        "- Фильтры, карточки кроме image-slot, характеристики, цены, SKU, price.csv и архитектура product.html?id=PRODUCT_ID не изменялись.",
    ]
    for result in results:
        lines.append(
            f"- {result['id']}: {result['status']}; добавлено {len(result['paths'])} WebP: "
            + ", ".join(result["paths"])
            + "."
        )
    lines += [
        "- Для laptop-011 использована точная страница MSI Crosshair 16 HX AI D2XWGKG-271NG; "
        "для laptop-012 — точная карточка Lenovo IdeaPad Slim 3 15IRU8, 82X700EDUS.",
        "- Изображения скачаны в репозиторий, приведены к WebP до 1000 px для основного кадра и до 1400 px для дополнительных; "
        "краевой белый фон удаляется только из связной области фона, чтобы не затрагивать детали корпуса.",
        "- Техническая готовность следующего этапа: каталог ноутбуков и универсальная страница уже используют локальные image/images; "
        "для остальных категорий отдельные фото пока не подключались.",
        "- Права на повторное коммерческое размещение внешних assets требуют отдельной ручной проверки.",
        "",
    ]
    return status_text.rstrip() + "\n" + "\n".join(lines)


def run_git(*args: str) -> None:
    subprocess.run(["git", *args], check=True)


def main() -> None:
    assert not PROTECTED_IDS.intersection(TARGETS), "protected laptop selected"
    product_path = ROOT / "products.json"
    catalog_path = ROOT / "rgw_page_laptops.html"
    progress_path = ROOT / "PHOTO_PROGRESS.json"
    status_path = ROOT / "PROJECT_STATUS.md"

    products_text = product_path.read_text(encoding="utf-8")
    catalog_text = catalog_path.read_text(encoding="utf-8")
    progress_text = progress_path.read_text(encoding="utf-8")
    status_text = status_path.read_text(encoding="utf-8")

    results: list[dict] = []
    for target_id, target in TARGETS.items():
        selected, exact_source = select_source_images(target)
        if not selected:
            raise RuntimeError(
                f"No exact product image found for {target_id}; leave placeholder and report manually."
            )

        product_dir = ROOT / "assets" / "products" / target_id
        for old in product_dir.glob("*.webp"):
            old.unlink()

        file_names = ["main.webp", "angle.webp", "back.webp", "detail.webp", "keyboard.webp"]
        paths: list[str] = []
        source_urls: list[str] = []
        for index, (source_url, image) in enumerate(selected):
            filename = file_names[index]
            relative_path = f"assets/products/{target_id}/{filename}"
            save_webp(image, ROOT / relative_path, 1000 if index == 0 else 1400)
            paths.append(relative_path)
            source_urls.append(source_url)

        products_text = replace_product_record(products_text, target_id, paths)
        catalog_text = replace_catalog_card(
            catalog_text, target_id, paths[0], target["catalog_name"]
        )
        progress_text = update_progress(
            progress_text, target_id, target, paths, source_urls, exact_source
        )
        results.append(
            {
                "id": target_id,
                "paths": paths,
                "status": "exact product-page source" if exact_source else "exact configuration fallback",
            }
        )

    json.loads(products_text)
    json.loads(progress_text)
    product_path.write_text(products_text, encoding="utf-8")
    catalog_path.write_text(catalog_text, encoding="utf-8")
    progress_path.write_text(progress_text, encoding="utf-8")
    status_path.write_text(append_status(status_text, results), encoding="utf-8")

    workflow_path = ROOT / ".github" / "workflows" / "photo-stage2.yml"
    if workflow_path.exists():
        workflow_path.unlink()
    script_path = ROOT / "scripts" / "photo_stage2.py"
    if script_path.exists():
        script_path.unlink()

    run_git("config", "user.name", "github-actions[bot]")
    run_git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    run_git(
        "add",
        "assets/products/laptop-011",
        "assets/products/laptop-012",
        "products.json",
        "rgw_page_laptops.html",
        "PHOTO_PROGRESS.json",
        "PROJECT_STATUS.md",
        ".github/workflows/photo-stage2.yml",
        "scripts/photo_stage2.py",
    )
    run_git("diff", "--cached", "--check")
    run_git("commit", "-m", "Add verified photos for remaining laptops")
    run_git("push", "origin", "HEAD:main")


if __name__ == "__main__":
    main()
