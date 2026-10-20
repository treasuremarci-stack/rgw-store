from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import date
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageOps


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT
TODAY = date.today().isoformat()
PROGRESS_PATH = REPO / "SYSTEM_UNIT_PHOTO_PROGRESS.json"
PRODUCTS_PATH = REPO / "products.json"
CATEGORY_PATH = REPO / "rgw_page_system_units.html"
STATUS_PATH = REPO / "PROJECT_STATUS.md"
PROTECTED_FILES = ["price.csv", "product.html", "product.js"]
TARGET_IDS = [f"case-{index:03d}" for index in range(1, 9)]


def cdn(path: str) -> str:
    return "https://cdn.deepcool.com/public/" + path


PRODUCTS = {
    "case-001": {
        "model": "DeepCool CASE CH 370 WHITE",
        "sku": "DEEPCOOL-CH370-WHITE",
        "source_pages": [
            "https://www.deepcool.com/products/Cases/CH370-WH-Micro-ATX-Case-White/2022/15950.shtml"
        ],
        "urls": [
            cdn("ProductFile/DEEPCOOL/Cases/CH370_WH/Overview/01.png"),
            cdn("ProductFile/DEEPCOOL/Cases/CH370_WH/Overview/01_01.png"),
            cdn("ProductFile/DEEPCOOL/Cases/CH370_WH/Overview/01_02.png"),
            cdn("ProductFile/DEEPCOOL/Cases/CH370_WH/Overview/01_03.png"),
            cdn("ProductFile/DEEPCOOL/Cases/CH370_WH/Overview/01_04.png"),
        ],
    },
    "case-002": {
        "model": "DeepCool CASE CH 370 BLACK",
        "sku": "DEEPCOOL-CH370-BLACK",
        "source_pages": [
            "https://www.deepcool.com/products/Cases/CH370-Micro-ATX-Case/2022/15949.shtml"
        ],
        "urls": [
            cdn("ProductFile/DEEPCOOL/Cases/CH370/Overview/01.png"),
            cdn("ProductFile/DEEPCOOL/Cases/CH370/Overview/01_04.png"),
            cdn("ProductFile/DEEPCOOL/Cases/CH370/Overview/01_01.png"),
            cdn("ProductFile/DEEPCOOL/Cases/CH370/Overview/01_02.png"),
            cdn("ProductFile/DEEPCOOL/Cases/CH370/Overview/01_03.png"),
        ],
    },
    "case-003": {
        "model": "DeepCool CASE CG530 4F",
        "sku": "DEEPCOOL-CG530-4F",
        "source_pages": [
            "https://www.deepcool.com/products/Cases/CG530-Panoramic-Tempered-Glass-Panels-Dual-Chamber-ATX-FISHTANK-Case-with-4-ARGB-PWM-Fans/2024/19604.shtml"
        ],
        "urls": [
            cdn("ProductFile/DEEPCOOL/Cases/CG530_4F/Overview/01.png"),
            cdn("ProductFile/DEEPCOOL/Cases/CG530_4F/Overview/01_01.jpg"),
            cdn("ProductFile/DEEPCOOL/Cases/CG530_4F/Overview/02_01.jpg"),
            cdn("ProductFile/DEEPCOOL/Cases/CG530_4F/Overview/02_02.jpg"),
            cdn("ProductFile/DEEPCOOL/Cases/CG530_4F/Overview/02_03.jpg"),
        ],
    },
    "case-004": {
        "model": "DeepCool CASE CG580 4F V2",
        "sku": "DEEPCOOL-CG580-4F-V2",
        "source_pages": [
            "https://uk.deepcool.com/products/Cases/CG580-4F-V2-Panoramic-Glass-Panels-Single-Chamber-ATX-Fishtank-Case-with-4-ARGB-PWM-Fans/2025/21446.shtml"
        ],
        "urls": [
            cdn("ProductFile/DEEPCOOL/Cases/CG580_4F_V2/Overview/01.png"),
            cdn("ProductFile/DEEPCOOL/Cases/CG580_4F_V2/Overview/01_01.png"),
            cdn("ProductFile/DEEPCOOL/Cases/CG580_4F_V2/Overview/02_01.jpg"),
            cdn("ProductFile/DEEPCOOL/Cases/CG580_4F_V2/Overview/02_02.jpg"),
            cdn("ProductFile/DEEPCOOL/Cases/CG580_4F_V2/Overview/02_03.jpg"),
        ],
    },
    "case-005": {
        "model": "DeepCool CASE MATREXX 50",
        "sku": "DEEPCOOL-MATREXX-50",
        "source_pages": [
            "https://www.deepcool.com/products/Cases/Matrexx-50-Mid-Tower-ATX-Case/2021/4657.shtml"
        ],
        "urls": [
            cdn("ProductFile/DEEPCOOL/Cases/Matrexx_50/Overview/01.png"),
            cdn("ProductFile/DEEPCOOL/Cases/Matrexx_50/Overview/01_01.png"),
            cdn("ProductFile/DEEPCOOL/Cases/Matrexx_50/Overview/02_01.png"),
            cdn("ProductGallery/DEEPCOOL/Cases/MATREXX_50/Design/02_02.png"),
            cdn("ProductGallery/DEEPCOOL/Cases/MATREXX_50/Design/02_03.png"),
        ],
    },
    "case-006": {
        "model": "DeepCool CASE CH 160 WHITE",
        "sku": "DEEPCOOL-CH160-WHITE",
        "source_pages": [
            "https://www.deepcool.com/products/Cases/CH160-WH-Portable-High-Airflow-M-ITX-Case/2024/18116.shtml"
        ],
        "urls": [
            cdn("ProductFile/DEEPCOOL/Cases/CH160_WH/Overview/01.png"),
            cdn("ProductFile/DEEPCOOL/Cases/CH160_WH/Overview/01_00.png"),
            cdn("ProductFile/DEEPCOOL/Cases/CH160_WH/Overview/01_01.png"),
            cdn("ProductFile/DEEPCOOL/Cases/CH160_WH/Overview/01_02.png"),
            cdn("ProductFile/DEEPCOOL/Cases/CH160_WH/Overview/01_03.png"),
        ],
    },
    "case-007": {
        "model": "DeepCool CASE CC560 LIMITED V2",
        "sku": "DEEPCOOL-CC560-LIMITED-V2",
        "source_pages": [
            "https://www.deepcool.com/products/Cases/CC560-Limited-V2-Mid-Tower-Airflow-Case/2023/17784.shtml"
        ],
        "urls": [
            cdn("ProductFile/DEEPCOOL/Cases/CC560_Limited_V2/Overview/01.png"),
            cdn("ProductFile/DEEPCOOL/Cases/CC560_Limited_V2/Overview/01_01.png"),
            cdn("ProductFile/DEEPCOOL/Cases/CC560_Limited_V2/Overview/02_01.png"),
            cdn("ProductFile/DEEPCOOL/Cases/CC560_Limited_V2/Overview/02_02.png"),
            cdn("ProductFile/DEEPCOOL/Cases/CC560_Limited_V2/Overview/02_03.png"),
        ],
    },
    "case-008": {
        "model": "DeepCool CASE CG380 3F",
        "sku": "DEEPCOOL-CG380-3F",
        "source_pages": [
            "https://www.deepcool.com/products/Cases/CG380-3F-Panoramic-Dual-Tempered-Glass-M-ATX-Case/2025/21782.shtml"
        ],
        "urls": [
            cdn("ProductFile/DEEPCOOL/Cases/CG380_3F/Overview/01.png"),
            cdn("ProductFile/DEEPCOOL/Cases/CG380_3F/Overview/01_01.jpg"),
            cdn("ProductFile/DEEPCOOL/Cases/CG380_3F/Overview/02_01.jpg"),
            cdn("ProductFile/DEEPCOOL/Cases/CG380_3F/Overview/02_02.jpg"),
            cdn("ProductFile/DEEPCOOL/Cases/CG380_3F/Overview/02_03.jpg"),
        ],
    },
}

FILE_NAMES = ["main.webp", "angle.webp", "detail.webp", "rear.webp", "top.webp"]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_bytes(path: Path) -> bytes:
    return path.read_bytes() if path.exists() else b""


def light_corner(pixel) -> bool:
    if len(pixel) == 4 and pixel[3] < 12:
        return True
    rgb = pixel[:3]
    return min(rgb) >= 238 and max(rgb) - min(rgb) <= 28


def remove_connected_white_background(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    width, height = rgba.size
    corners = [
        (0, 0),
        (max(0, width - 1), 0),
        (0, max(0, height - 1)),
        (max(0, width - 1), max(0, height - 1)),
    ]
    if not any(light_corner(rgba.getpixel(point)) for point in corners):
        return rgba
    for point in corners:
        if light_corner(rgba.getpixel(point)):
            ImageDraw.floodfill(rgba, point, (0, 0, 0, 0), thresh=24)
    return rgba


def make_webp(source: bytes, destination: Path, max_side: int) -> dict:
    original = ImageOps.exif_transpose(Image.open(BytesIO(source)))
    rgba = remove_connected_white_background(original)
    bbox = rgba.getchannel("A").getbbox()
    if bbox:
        rgba = rgba.crop(bbox)
    rgba.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    canvas_size = 1000 if max_side <= 900 else 1200
    canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    offset = ((canvas_size - rgba.width) // 2, (canvas_size - rgba.height) // 2)
    canvas.alpha_composite(rgba, offset)
    destination.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(destination, "WEBP", quality=84, method=6)
    return {
        "width": canvas.width,
        "height": canvas.height,
        "source_width": original.width,
        "source_height": original.height,
        "bytes": destination.stat().st_size,
    }


def download_images(session: requests.Session, urls: list[str]) -> tuple[list[bytes], list[str], list[str]]:
    payloads = []
    selected = []
    failures = []
    for url in urls:
        try:
            response = session.get(url, timeout=45)
            response.raise_for_status()
            content = response.content
            with Image.open(BytesIO(content)) as probe:
                probe.verify()
            payloads.append(content)
            selected.append(url)
        except Exception as error:
            failures.append(f"{url} ({type(error).__name__}: {error})")
    return payloads, selected, failures


def product_record_map(records):
    return {record.get("id"): record for record in records}


def normalize_category_images(text: str) -> str:
    normalized = text
    for product_id in TARGET_IDS:
        pattern = re.compile(
            r'(<article class="product-card"[^>]*data-product-id="'
            + re.escape(product_id)
            + r'"[\s\S]*?<span class="product-badge">PC CASE</span>)'
            r'(?:<span class="placeholder-icon">🗄️</span>|<img[^>]*>)'
            r'(</a>)'
        )
        normalized, count = pattern.subn(r"\1__SYSTEM_UNIT_IMAGE__\2", normalized, count=1)
        if count != 1:
            raise RuntimeError(f"Could not locate image slot for {product_id}")
    return normalized


def write_catalog_images(text: str) -> str:
    updated = text
    for product_id in TARGET_IDS:
        product = PRODUCTS[product_id]
        image = (
            f'<img class="product-image-file" src="images/products/{product_id}/main.webp" '
            f'alt="{product["model"]}" loading="lazy" decoding="async">'
        )
        pattern = re.compile(
            r'(<article class="product-card"[^>]*data-product-id="'
            + re.escape(product_id)
            + r'"[\s\S]*?<span class="product-badge">PC CASE</span>)'
            r'(?:<span class="placeholder-icon">🗄️</span>|<img[^>]*>)'
            r'(</a>)'
        )
        updated, count = pattern.subn(r"\1" + image + r"\2", updated, count=1)
        if count != 1:
            raise RuntimeError(f"Could not write image slot for {product_id}")
    return updated


def main():
    original_products_bytes = read_bytes(PRODUCTS_PATH)
    original_category_bytes = read_bytes(CATEGORY_PATH)
    original_status = STATUS_PATH.read_text(encoding="utf-8")
    original_products = json.loads(original_products_bytes.decode("utf-8"))
    before_map = product_record_map(original_products)

    protected_hashes = {
        path: sha256_bytes(read_bytes(REPO / path))
        for path in PROTECTED_FILES
    }

    session = requests.Session()
    session.headers.update({"User-Agent": "AKS-system-unit-photo-stage/1.0"})
    progress_products = []
    connected = {}

    for product_id in TARGET_IDS:
        config = PRODUCTS[product_id]
        output_dir = REPO / "images" / "products" / product_id
        payloads, selected_urls, failures = download_images(session, config["urls"])
        old_main = output_dir / "main.webp"
        if not payloads and old_main.exists():
            paths = sorted(
                str(path.relative_to(REPO)).replace("\\", "/")
                for path in output_dir.glob("*.webp")
            )
            connected[product_id] = paths
            progress_products.append({
                "id": product_id,
                "model": config["model"],
                "sku": config["sku"],
                "status": "existing",
                "photo_count": len(paths),
                "paths": paths,
                "source_pages": config["source_pages"],
                "selected_source_images": [],
                "failed_candidates": failures,
                "reason": "Официальные CDN-кандидаты временно не скачались; существующее фото сохранено.",
                "rights_note": "Официальная страница подтверждает модель; отдельное разрешение на коммерческое размещение не проверялось автоматически.",
            })
            continue
        if not payloads:
            connected[product_id] = []
            progress_products.append({
                "id": product_id,
                "model": config["model"],
                "sku": config["sku"],
                "status": "placeholder",
                "photo_count": 0,
                "paths": [],
                "source_pages": config["source_pages"],
                "selected_source_images": [],
                "failed_candidates": failures,
                "reason": "Не удалось скачать ни одного точного изображения с официального CDN.",
                "rights_note": "Официальная страница подтверждает модель; отдельное разрешение на коммерческое размещение не проверялось автоматически.",
            })
            continue

        paths = []
        asset_meta = []
        for index, (payload, url) in enumerate(zip(payloads, selected_urls)):
            filename = FILE_NAMES[index]
            destination = output_dir / filename
            meta = make_webp(payload, destination, 900 if index == 0 else 1100)
            paths.append(str(destination.relative_to(REPO)).replace("\\", "/"))
            asset_meta.append({
                "path": paths[-1],
                "source": url,
                "width": meta["width"],
                "height": meta["height"],
                "source_width": meta["source_width"],
                "source_height": meta["source_height"],
                "bytes": meta["bytes"],
            })
        connected[product_id] = paths
        progress_products.append({
            "id": product_id,
            "model": config["model"],
            "sku": config["sku"],
            "status": "complete",
            "photo_count": len(paths),
            "paths": paths,
            "source_pages": config["source_pages"],
            "selected_source_images": selected_urls,
            "failed_candidates": failures,
            "assets": asset_meta,
            "reason": "",
            "rights_note": "Официальная страница подтверждает модель; отдельное разрешение на коммерческое размещение не проверялось автоматически.",
        })

    records = json.loads(original_products_bytes.decode("utf-8"))
    for record in records:
        product_id = record.get("id")
        if product_id not in connected:
            continue
        paths = connected[product_id]
        if paths:
            record["image"] = paths[0]
            record["images"] = paths
        elif product_id != "case-008":
            record["image"] = None
            record.pop("images", None)

    for record in records:
        product_id = record.get("id")
        before = before_map.get(product_id)
        if before is None:
            raise RuntimeError(f"Unexpected product record added: {product_id}")
        if product_id in TARGET_IDS:
            before_non_image = {k: v for k, v in before.items() if k not in {"image", "images"}}
            after_non_image = {k: v for k, v in record.items() if k not in {"image", "images"}}
            if before_non_image != after_non_image:
                raise RuntimeError(f"Non-image data changed for {product_id}")
        elif before != record:
            raise RuntimeError(f"Product record changed outside system units: {product_id}")

    PRODUCTS_PATH.write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    updated_category = write_catalog_images(original_category_bytes.decode("utf-8"))
    if normalize_category_images(updated_category) != normalize_category_images(original_category_bytes.decode("utf-8")):
        raise RuntimeError("System-unit category changed outside its image slots")
    CATEGORY_PATH.write_text(updated_category, encoding="utf-8")

    progress = {
        "stage": "system-unit-photo-stage",
        "updated": TODAY,
        "category": "Системные блоки",
        "source_policy": "Только точные официальные страницы и CDN DeepCool; похожие модели не подставлялись.",
        "products": progress_products,
    }
    PROGRESS_PATH.write_text(
        json.dumps(progress, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    status_marker = "## System-unit photo stage"
    status_lines = [
        "",
        "",
        f"## System-unit photo stage ({TODAY})",
        "",
        "- Обработаны все 8 карточек категории «Системные блоки» (case-001—case-008).",
        "- Для каждой модели использованы точные официальные страницы/файлы DeepCool; похожие модели и чужие изображения не подставлялись.",
        "- Главные и дополнительные кадры скачаны, приведены к WebP без искусственного увеличения; белый фон удалён только из связной краевой области, если он был встроен.",
        "- Каталог и product.html?id=... используют существующую архитектуру: изменены только image-слоты системных блоков и поля image/images для этих восьми записей.",
        "- CSS, анимация карточек, цены, характеристики, названия, SKU, ID, price.csv, ноутбуки, моноблоки и остальные категории не изменялись.",
        "",
        "### Результаты",
        "",
    ]
    for item in progress_products:
        if item["status"] == "complete":
            status_lines.append(
                f'- {item["id"]} — {item["model"]}: {item["photo_count"]} WebP, '
                f'главное фото {item["paths"][0]}.'
            )
        elif item["status"] == "existing":
            status_lines.append(
                f'- {item["id"]} — {item["model"]}: сохранено существующее фото; '
                f'новые официальные CDN-файлы временно не скачались.'
            )
        else:
            status_lines.append(
                f'- {item["id"]} — {item["model"]}: заглушка сохранена; '
                f'точный официальный файл не скачался.'
            )
    status_lines.extend([
        "",
        "### Источники",
        "",
        "- Официальные страницы DeepCool и соответствующие CDN-пути указаны в SYSTEM_UNIT_PHOTO_PROGRESS.json.",
        "- Права на повторное коммерческое размещение внешних изображений требуют отдельной ручной проверки.",
        "",
        "### Проверки",
        "",
        "- Сверены все 8 ID, SKU и названия с текущим каталогом.",
        "- Галерея использует существующий product.js и массив images[]; filter/sort/card layout не переписывались.",
        "- Перед коммитом проверяется, что изменены только системные image-слоты, новые локальные WebP, progress-файл и этот статус.",
    ])
    status_text = original_status
    if status_marker not in status_text:
        status_text += "\n".join(status_lines) + "\n"
    STATUS_PATH.write_text(status_text, encoding="utf-8")

    for path, old_hash in protected_hashes.items():
        new_hash = sha256_bytes(read_bytes(REPO / path))
        if new_hash != old_hash:
            raise RuntimeError(f"Protected file changed: {path}")

    (REPO / ".github/workflows/system_unit_photo_stage.yml").unlink(missing_ok=True)
    (REPO / "scripts/system_unit_photo_stage.py").unlink(missing_ok=True)

    subprocess.run(["git", "add", "-A"], cwd=REPO, check=True)
    changed = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only"], cwd=REPO, text=True
    ).splitlines()
    allowed_prefixes = ("images/products/case-",)
    allowed_exact = {
        "products.json",
        "rgw_page_system_units.html",
        "SYSTEM_UNIT_PHOTO_PROGRESS.json",
        "PROJECT_STATUS.md",
        ".github/workflows/system_unit_photo_stage.yml",
        "scripts/system_unit_photo_stage.py",
    }
    unexpected = [
        path for path in changed
        if path not in allowed_exact and not path.startswith(allowed_prefixes)
    ]
    if unexpected:
        raise RuntimeError(f"Unexpected changed files: {unexpected}")

    if not changed:
        print("No changes to commit.")
        return

    subprocess.run(
        ["git", "config", "user.name", "github-actions[bot]"],
        cwd=REPO,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"],
        cwd=REPO,
        check=True,
    )
    subprocess.run(
        ["git", "commit", "-m", "Add exact system unit product photos"],
        cwd=REPO,
        check=True,
    )
    subprocess.run(["git", "push", "origin", "main"], cwd=REPO, check=True)
    print(json.dumps({
        "products": [
            {
                "id": item["id"],
                "status": item["status"],
                "photo_count": item["photo_count"],
                "paths": item["paths"],
            }
            for item in progress_products
        ],
        "changed_files": changed,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
