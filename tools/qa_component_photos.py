from __future__ import annotations

import json
import shutil
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "rgw-store-photo-import/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def save_webp(source: Path | bytes, destination: Path, max_size: int = 1000) -> None:
    if isinstance(source, Path):
        image = Image.open(source)
    else:
        from io import BytesIO

        image = Image.open(BytesIO(source))
    image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGBA" if "A" in image.getbands() else "RGB")
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, "WEBP", quality=85, method=6)


def update_records() -> None:
    products_path = ROOT / "products.json"
    products = json.loads(products_path.read_text(encoding="utf-8"))
    image_paths = {
        "gpu-001": ["images/products/gpu-001/main.webp"],
        "gpu-002": ["images/products/gpu-002/main.webp"],
        "gpu-004": [
            "images/products/gpu-004/main.webp",
            "images/products/gpu-004/01.webp",
            "images/products/gpu-004/02.webp",
        ],
        "gpu-005": ["images/products/gpu-005/main.webp"],
        "gpu-006": ["images/products/gpu-006/main.webp"],
        "cooling-018": [
            "images/products/cooling-018/main.webp",
            "images/products/cooling-018/01.webp",
        ],
    }
    for product in products:
        paths = image_paths.get(product["id"])
        if paths:
            product["image"] = paths[0]
            product["images"] = paths
    products_path.write_text(json.dumps(products, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    progress_path = ROOT / "COMPONENTS_PHOTO_PROGRESS.json"
    progress = json.loads(progress_path.read_text(encoding="utf-8"))
    progress["updatedAt"] = datetime.now(timezone.utc).isoformat()
    progress["policy"] = (
        "Официальный источник предпочтителен; если чистая фотография отсутствует, "
        "допускается точный источник надёжного магазина; при отсутствии подтверждения "
        "сохраняется заглушка."
    )
    progress["totals"]["webp"] = 202
    changes = {
        "gpu-001": (
            ["images/products/gpu-001/main.webp"],
            [
                "https://galax.com/en/product/geforce-rtx-3050-ex-white-1-click-oc/",
                "https://galax.com/wp-content/uploads/2025/10/3050wface-1024x926.png",
            ],
            "Точная модель подтверждена официальным источником; широкая промо-графика заменена на чистую фотографию платы.",
        ),
        "gpu-002": (
            ["images/products/gpu-002/main.webp"],
            [
                "https://galax.com/en/product/geforce-rtx-5060-ti-8gb-1-click-oc-white-2x/",
                "https://secomputer.com.hk/products/galax-geforce-rtx5060ti-1-click-oc-white-8gb-gddr7",
                "https://secomputer.com.hk/uploads/products/cover/44f2069fa5da1c119c7e503cc672d0d9.webp",
            ],
            "Точная модель подтверждена по коду производителя 56ISN8MDCQWH; вместо широкого баннера использована фотография точной модели из SE Computer.",
        ),
        "gpu-004": (
            [
                "images/products/gpu-004/main.webp",
                "images/products/gpu-004/01.webp",
                "images/products/gpu-004/02.webp",
            ],
            [
                "https://galax.com/en/product/geforce-rtx-5050-1-click-oc/",
                "https://galax.com/wp-content/uploads/2025/06/951A5802-gx.png",
                "https://galax.com/wp-content/uploads/2025/06/951A5807-1-500x500.png",
                "https://galax.com/wp-content/uploads/2025/06/951A5802-led-gx-500x500.png",
            ],
            "Точная модель подтверждена официальным источником; широкая промо-графика и крупный crop заменены чистыми фото платы и задней панели.",
        ),
        "gpu-005": (
            ["images/products/gpu-005/main.webp"],
            [
                "https://galax.com/en/product/geforce-rtx-5080-16gb-1-click-oc-3x/",
                "https://galax.com/wp-content/uploads/2025/01/5080.png",
            ],
            "Точная модель подтверждена официальным источником; дополнительный широкий промо-баннер удалён, оставлено чистое основное фото.",
        ),
        "gpu-006": (
            ["images/products/gpu-006/main.webp"],
            [
                "https://galax.com/en/graphics-card/geforce-rtx-3060-1-click-oc.html",
                "https://galax.com/wp-content/uploads/2025/02/3060-carbon_02-GX.png",
            ],
            "Точная модель подтверждена официальным источником; широкая промо-графика заменена полноразмерным рендером платы.",
        ),
        "cooling-018": (
            [
                "images/products/cooling-018/main.webp",
                "images/products/cooling-018/01.webp",
            ],
            [
                "https://uk.deepcool.com/products/Cooling/cpuaircoolers/2021/14270.shtml",
                "https://cdn.deepcool.com/public/ProductFile/DEEPCOOL/Cooling/CPUAirCoolers/CK_11508/Gallery/608X760/01.jpg?auto=format,compress&q=90",
                "https://cdn.deepcool.com/public/ProductFile/DEEPCOOL/Cooling/CPUAirCoolers/CK_11508/Gallery/608X760/02.jpg?auto=format,compress&q=90",
            ],
            "Точная модель подтверждена официальным источником; три одинаковых декоративных фоновых изображения удалены, оставлены два изображения самого CK-11508.",
        ),
    }
    for record in progress["records"]:
        change = changes.get(record["id"])
        if change:
            paths, sources, reason = change
            record["photo_count"] = len(paths)
            record["paths"] = paths
            record["source_urls"] = sources
            record["reason"] = reason
    progress_path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    status_path = ROOT / "PROJECT_STATUS.md"
    status = status_path.read_text(encoding="utf-8")
    marker = "## Контроль качества фотографий комплектующих (2026-10-21)"
    if marker not in status:
        status += (
            "\n\n"
            + marker
            + "\n\nПосле визуальной проверки заменены четыре широких промо-баннера видеокарт "
            "(gpu-001, gpu-002, gpu-004, gpu-006) на полноразмерные изображения точных моделей. "
            "Для gpu-002 использован точный снимок SE Computer с подтверждённым кодом производителя "
            "56ISN8MDCQWH; остальные новые снимки для видеокарт взяты с официального домена GALAX. "
            "У gpu-005 удалён дополнительный широкий баннер, оставлено чистое основное фото.\n\n"
            "У cooling-018 удалены три одинаковых декоративных фоновых изображения, в галерее оставлены "
            "только фотографии самого DeepCool CK-11508. После контроля в комплектующих осталось 202 "
            "локальных WebP-файла; остальные товары, для которых точный источник не подтверждён, "
            "по-прежнему используют заглушки. Цены, характеристики, ID, SKU, фильтры, карточки и товары "
            "ноутбуков, моноблоков и системных блоков не изменялись.\n"
        )
        status_path.write_text(status, encoding="utf-8")


def main() -> None:
    save_webp(ROOT / "images/products/gpu-001/01.webp", ROOT / "images/products/gpu-001/main.webp")
    save_webp(
        fetch("https://secomputer.com.hk/uploads/products/cover/44f2069fa5da1c119c7e503cc672d0d9.webp"),
        ROOT / "images/products/gpu-002/main.webp",
    )
    save_webp(
        fetch("https://galax.com/wp-content/uploads/2025/06/951A5802-gx.png"),
        ROOT / "images/products/gpu-004/main.webp",
    )
    save_webp(
        fetch("https://galax.com/wp-content/uploads/2025/06/951A5807-1-500x500.png"),
        ROOT / "images/products/gpu-004/01.webp",
    )
    save_webp(
        fetch("https://galax.com/wp-content/uploads/2025/06/951A5802-led-gx-500x500.png"),
        ROOT / "images/products/gpu-004/02.webp",
    )
    save_webp(ROOT / "images/products/gpu-006/01.webp", ROOT / "images/products/gpu-006/main.webp")
    for path in [
        ROOT / "images/products/gpu-001/01.webp",
        ROOT / "images/products/gpu-004/03.webp",
        ROOT / "images/products/gpu-005/01.webp",
        ROOT / "images/products/gpu-006/01.webp",
        ROOT / "images/products/cooling-018/02.webp",
        ROOT / "images/products/cooling-018/03.webp",
        ROOT / "images/products/cooling-018/04.webp",
    ]:
        if path.exists():
            path.unlink()
    update_records()
    subprocess.run(
        [
            "git",
            "add",
            "products.json",
            "COMPONENTS_PHOTO_PROGRESS.json",
            "PROJECT_STATUS.md",
            "images/products/gpu-001",
            "images/products/gpu-002",
            "images/products/gpu-004",
            "images/products/gpu-005",
            "images/products/gpu-006",
            "images/products/cooling-018",
        ],
        cwd=ROOT,
        check=True,
    )
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode == 0:
        return
    subprocess.run(["git", "commit", "-m", "QA component product photos"], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()

