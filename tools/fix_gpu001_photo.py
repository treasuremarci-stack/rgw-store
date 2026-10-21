from __future__ import annotations

import json
import subprocess
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
IMAGE_URL = "https://cdn.thuancomputer.com/2025/07/vga-galax-geforce-rtx-3050-6gb-gddr6-ex-white-1-click-oc.png"
SOURCE_PAGE = "https://thuancomputer.com/vga-galax-geforce-rtx-3050-6gb-gddr6-ex-white-1-click-oc/"


def main() -> None:
    req = urllib.request.Request(IMAGE_URL, headers={"User-Agent": "rgw-store-photo-import/1.0"})
    with urllib.request.urlopen(req, timeout=60) as response:
        image = Image.open(BytesIO(response.read()))
    image.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGBA" if "A" in image.getbands() else "RGB")
    destination = ROOT / "images/products/gpu-001/main.webp"
    image.save(destination, "WEBP", quality=85, method=6)

    products_path = ROOT / "products.json"
    products = json.loads(products_path.read_text(encoding="utf-8"))
    for product in products:
        if product["id"] == "gpu-001":
            product["image"] = "images/products/gpu-001/main.webp"
            product["images"] = ["images/products/gpu-001/main.webp"]
            break
    products_path.write_text(json.dumps(products, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    progress_path = ROOT / "COMPONENTS_PHOTO_PROGRESS.json"
    progress = json.loads(progress_path.read_text(encoding="utf-8"))
    for record in progress["records"]:
        if record["id"] == "gpu-001":
            record["photo_count"] = 1
            record["paths"] = ["images/products/gpu-001/main.webp"]
            record["source_urls"] = [
                "https://galax.com/en/product/geforce-rtx-3050-ex-white-1-click-oc/",
                SOURCE_PAGE,
                IMAGE_URL,
            ]
            record["reason"] = "Точная модель A76D подтверждена страницей производителя и карточкой модели у надёжного магазина; выбрано фото с полностью видимой платой."
            break
    progress_path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    status_path = ROOT / "PROJECT_STATUS.md"
    status = status_path.read_text(encoding="utf-8")
    status += "\n\n## Дополнительная проверка gpu-001 (2026-10-21)\n\nДля A76D Black GF RTX3050 6GB EX White заменено изображение, у которого край платы касался границы исходного render-файла. Использовано точное фото модели со страницы товара надёжного магазина; плата полностью помещается в кадре.\n"
    status_path.write_text(status, encoding="utf-8")

    subprocess.run(
        ["git", "add", "products.json", "COMPONENTS_PHOTO_PROGRESS.json", "PROJECT_STATUS.md", "images/products/gpu-001/main.webp"],
        cwd=ROOT,
        check=True,
    )
    subprocess.run(["git", "config", "user.name", "github-actions[bot]"], cwd=ROOT, check=True)
    subprocess.run(
        ["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"],
        cwd=ROOT,
        check=True,
    )
    subprocess.run(["git", "commit", "-m", "Use full gpu-001 product photo"], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()

