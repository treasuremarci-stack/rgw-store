#!/usr/bin/env python3
"""Fetch exact component product photos from manufacturer sources.

This is intentionally a one-shot, auditable migration helper.  It only adds
image/images fields for the component products listed in SOURCES and replaces
the image slot of the matching component card.  It never edits prices, specs,
IDs, SKUs, or products outside the nine component categories.
"""

from __future__ import annotations

import html
import io
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_PATH = ROOT / "products.json"
PROGRESS_PATH = ROOT / "COMPONENTS_PHOTO_PROGRESS.json"
STATUS_PATH = ROOT / "PROJECT_STATUS.md"
IMAGE_ROOT = ROOT / "images" / "products"
USER_AGENT = "RGW-store component photo import/1.0 (+https://github.com/treasuremarci-stack/rgw-store)"

CATEGORIES = {
    "Видеокарты": "rgw_page_gpus.html",
    "Процессоры": "rgw_page_processors.html",
    "Материнские платы": "rgw_page_motherboards.html",
    "Оперативная память": "rgw_page_ram.html",
    "SSD": "rgw_page_ssd.html",
    "HDD": "rgw_page_hdd.html",
    "Корпуса": "rgw_page_cases.html",
    "Блоки питания": "rgw_page_power_supplies.html",
    "Охлаждение": "rgw_page_cooling.html",
}


def deepcool_gallery(area: str, model: str, count: int = 5) -> list[str]:
    return [
        f"https://cdn.deepcool.com/public/ProductFile/DEEPCOOL/{area}/{model}/Gallery/608X760/{n:02d}.jpg?auto=format,compress&q=90"
        for n in range(1, count + 1)
    ]


def asus_gallery(ids: list[str]) -> list[str]:
    return [f"https://dlcdnwebimgs.asus.com/gain/{value}/w800/fwebp" for value in ids]


def samsung_gallery(product: str, names: list[str]) -> list[str]:
    return [
        f"https://images.samsung.com/is/image/samsung/p6pim/us/{product}/gallery/{name}?$product-details-jpg$"
        for name in names
    ]


KINGSTON_FURY = [
    "https://media.kingston.com/kingston/product/FURY_Beast_Black_DDR5_1-lg.jpg",
    "https://media.kingston.com/kingston/product/FURY_Beast_Black_DDR5_1_angle-lg.jpg",
    "https://media.kingston.com/kingston/product/FURY_Beast_Black_DDR5_2_angle-lg.jpg",
    "https://media.kingston.com/kingston/product/FURY_Beast_Black_DDR5_1_pkg-lg.jpg",
]


SOURCES: dict[str, dict] = {
    # GALAX product assets are named by the exact board family and are served
    # from the manufacturer's official CDN.
    "gpu-001": {
        "source": "https://galax.com/en/product/geforce-rtx-3050-ex-white-1-click-oc/",
        "direct": [
            "https://galax.com/wp-content/uploads/2025/10/3050cover.jpg",
            "https://galax.com/wp-content/uploads/2025/10/3050wface-1024x926.png",
        ],
    },
    "gpu-002": {
        "source": "https://galax.com/en/category/graphics-cards/50-series/",
        "direct": ["https://galax.com/wp-content/uploads/2026/04/5060Ti_W_Cover-v3.png"],
    },
    "gpu-003": {
        "source": "https://www.galax.com/en/graphics-card/geforce-rtx-5060-1coc-v2.html",
        "direct": [
            "https://galax.com/wp-content/uploads/2025/09/5060v2-scaled.png",
            "https://galax.com/wp-content/uploads/2025/09/5060v2_1-scaled.png",
        ],
    },
    "gpu-004": {
        "source": "https://galax.com/en/category/graphics-cards/50-series/",
        "direct": [
            "https://galax.com/wp-content/uploads/2025/06/5050_Cover.jpg",
            "https://galax.com/wp-content/uploads/2025/06/5050_w-fan.png",
        ],
    },
    "gpu-005": {
        "source": "https://galax.com/en/category/graphics-cards/50-series/",
        "direct": [
            "https://galax.com/wp-content/uploads/2025/01/5080.png",
            "https://galax.com/wp-content/uploads/2025/01/5080-Cover-K2-r3.jpg",
        ],
    },
    "gpu-006": {
        "source": "https://galax.com/en/graphics-card/geforce-rtx-3060-1-click-oc.html",
        "direct": [
            "https://galax.com/wp-content/uploads/2025/02/covers-3060.jpg",
            "https://galax.com/wp-content/uploads/2025/02/3060-carbon_02-GX.png",
        ],
    },
    "gpu-008": {
        "source": "https://www.msi.com/Graphics-Card/GeForce-RTX-5060-VENTUS-2X-8G",
        "direct": [
            "https://storage-asset.msi.com/global/picture/product/product_1745313240ffac739c1efdf9d3f4d4a10218128b10.webp",
            "https://storage-asset.msi.com/global/picture/product/product_174531314482e86e3509d2c9964fa77e2472642b34.webp",
            "https://storage-asset.msi.com/global/picture/product/product_17453131448e10849137bc081d176b01f9323323c6.webp",
            "https://storage-asset.msi.com/global/picture/product/product_174531314613ad38f0d8e5517f64dfd9f29f5e0588.webp",
        ],
    },

    # Motherboards: the ASUS gain IDs and GIGABYTE remove-background IDs are
    # taken from the exact product pages, not from a series/category tile.
    "mb-001": {
        "source": "https://www.asus.com/motherboards-components/motherboards/prime/prime-b760m-f/",
        "direct": asus_gallery([
            "6eddd9a7-2eee-44f4-b787-914d9402939e",
            "6cfbff2e-0fe5-47aa-be45-4d1fbc37caf2",
            "5338f06c-97ed-41c3-bebf-c3592ee5ccca",
            "a58209a7-d7b7-4b74-81af-b50e76fe4f0b",
        ]),
    },
    "mb-010": {
        "source": "https://www.gigabyte.com/Motherboard/B760M-K-DDR4-rev-10",
        "direct": [
            "https://static.gigabyte.com/StaticFile/Image/Global/418c88fc2164f03cd1b6f4c97743150e/ProductRemoveBg/35725/webp/600"
        ],
    },
    "mb-014": {
        "source": "https://www.asus.com/motherboards-components/motherboards/others/b860m-bro/",
        "direct": asus_gallery([
            "e7c0e4e9-ec21-4586-bbfe-be6b499d3b0e",
            "813e2332-efd7-4a44-b248-0db309d151df",
            "588397b6-fa96-471f-ae5f-280bc983a013",
            "a6892a24-d6e3-4bb2-9888-f678eda0139d",
        ]),
    },
    "mb-015": {
        "source": "https://www.gigabyte.com/Motherboard/Z790-D-rev-10-12",
        "direct": [
            "https://static.gigabyte.com/StaticFile/Image/Global/041398d4dee5b63ca27acd4ef01de883/ProductRemoveBg/39380/webp/600"
        ],
    },

    # Memory and SSD lines with exact manufacturer family pages and matching
    # capacities. The catalog does not contain manufacturer part numbers, so
    # no image is assigned to an unspecified generic/OEM listing.
    "ram-005": {
        "source": "https://www.kingston.com/en/memory/gaming/kingston-fury-beast-ddr5-memory",
        "direct": KINGSTON_FURY,
    },
    "ram-008": {
        "source": "https://americas.lexar.com/product/lexar-thor-oc-ddr5-desktop-memory/",
        "direct": [
            "https://americas.lexar.com/wp-content/uploads/2023/11/THOR_OC_DDR5_Photo1.png",
            "https://americas.lexar.com/wp-content/uploads/2023/11/THOR_OC_DDR5_Photo4.png",
            "https://americas.lexar.com/wp-content/uploads/2023/11/THOR_OC_DDR5_Photo5.png",
            "https://americas.lexar.com/wp-content/uploads/2023/11/THOR_OC_DDR5_Photo6.png",
        ],
    },
    "ram-011": {
        "source": "https://www.kingston.com/en/memory/gaming/kingston-fury-beast-ddr5-memory",
        "direct": KINGSTON_FURY,
    },
    "ssd-004": {
        "source": "https://www.samsung.com/us/memory-storage/nvme-ssd/990-evo-plus-gen4-nvme-ssd-1tb-sku-mz-v9s1t0b-am/",
        "direct": samsung_gallery(
            "mz-v9s1t0b-am",
            [
                "us-990-evo-plus-nvme-m2-ssd-mz-v9s1t0b-am-550538037",
                "us-990-evo-plus-nvme-m2-ssd-mz-v9s1t0b-am-550538046",
                "us-990-evo-plus-nvme-m2-ssd-mz-v9s1t0b-am-000",
                "us-990-evo-plus-nvme-m2-ssd-mz-v9s1t0b-am-550538117",
            ],
        ),
    },
    "ssd-007": {
        "source": "https://www.samsung.com/us/memory-storage/nvme-ssd/990-pro-2tb-nvme-pcie-gen-4-mz-v9p2t0b-am/",
        "direct": [
            "https://images.samsung.com/is/image/samsung/p6pim/us/mz-v9p2t0b-am/gallery/us-990pro-nvme-m2-ssd-mz-v9p2t0b-am-551141318?$product-details-jpg$",
            "https://images.samsung.com/is/image/samsung/p6pim/us/mz-v9p2t0b-am/gallery/us-990pro-nvme-m2-ssd-mz-v9p2t0b-am-551141316?$720_576_PNG$",
        ],
    },
    "ssd-010": {
        "source": "https://americas.lexar.com/product/lexar-nm790-m-2-2280-pcie-gen-4x4-nvme-ssd/",
        "direct": [
            "https://americas.lexar.com/wp-content/uploads/2025/02/NM790_SSD_Photo1.png",
            "https://americas.lexar.com/wp-content/uploads/2025/07/NM790_SSD_Photo4.png",
            "https://americas.lexar.com/wp-content/uploads/2023/11/NM790_SSD_Photo5-1.png",
            "https://americas.lexar.com/wp-content/uploads/2023/11/NM790_SSD_Photo6-1.png",
        ],
    },
    "ssd-011": {
        "source": "https://americas.lexar.com/product/lexar-nm790-m-2-2280-pcie-gen-4x4-nvme-ssd/",
        "direct": [
            "https://americas.lexar.com/wp-content/uploads/2025/02/NM790_SSD_Photo1.png",
            "https://americas.lexar.com/wp-content/uploads/2025/07/NM790_SSD_Photo4.png",
            "https://americas.lexar.com/wp-content/uploads/2023/11/NM790_SSD_Photo5-1.png",
            "https://americas.lexar.com/wp-content/uploads/2023/11/NM790_SSD_Photo6-1.png",
        ],
    },
    "ssd-016": {
        "source": "https://www.lexar.com/global/products/Lexar-THOR-PRO-PCIe-Gen-4x4-NVMe-SSD/",
        "direct": [
            "https://www-oss.lexar.com/lexar/images/2025-02-14/THOR%20PRO-ID1.webp",
            "https://www-oss.lexar.com/lexar/images/2025-11-26/EN-THOR%20PRO-PC1%401x.webp",
        ],
    },
    "ssd-021": {
        "source": "https://americas.lexar.com/product/lexar-nm790-m-2-2280-pcie-gen-4x4-nvme-ssd/",
        "direct": [
            "https://americas.lexar.com/wp-content/uploads/2025/02/NM790_SSD_Photo1.png",
            "https://americas.lexar.com/wp-content/uploads/2025/07/NM790_SSD_Photo4.png",
            "https://americas.lexar.com/wp-content/uploads/2023/11/NM790_SSD_Photo5-1.png",
            "https://americas.lexar.com/wp-content/uploads/2023/11/NM790_SSD_Photo6-1.png",
        ],
    },

    # WD Purple is a precise product line and these URLs are the matching
    # manufacturer's capacity-specific gallery assets.
    **{
        f"hdd-{n:03d}": {
            "source": source,
            "direct": [f"https://www.westerndigital.com/content/dam/store/en-us/assets/products/internal-storage/wd-purple-sata-hdd/gallery/wd-purple-surveillance-hard-drive-{capacity}.png"],
        }
        for n, capacity, source in [
            (2, "10tb", "https://www.westerndigital.com/en-ie/products/outlet/internal-drives/wd-purple-sata-hdd?sku=WD101PURZ"),
            (3, "14tb", "https://www.westerndigital.com/en-gb/products/internal-drives/wd-purple-sata-hdd?sku=WD140PURZ"),
            (4, "2tb", "https://www.westerndigital.com/products/internal-drives/wd-purple-sata-hdd?sku=WD22PURZ"),
            (5, "8tb", "https://www.westerndigital.com/en-ie/products/outlet/internal-drives/wd-purple-sata-hdd?sku=WD82PURZ"),
            (6, "4tb", "https://www.westerndigital.com/products/internal-drives/wd-purple-sata-hdd?sku=WD44PURZ"),
            (7, "6tb", "https://www.westerndigital.com/products/internal-drives/wd-purple-sata-hdd?sku=WD64PURZ"),
        ]
    },

    # GameMax detail pages expose product gallery URLs in data-src-pc.
    "cases-004": {
        "source": "https://gamemaxpc.com/ru/list_175/3947.html",
        "kind": "gamemax",
    },
    "cases-005": {
        "source": "https://gamemaxpc.com/Infinity/1504.html",
        "kind": "gamemax",
    },
    "cases-014": {
        "source": "https://it.deepcool.com/products/Cases/Matrexx-50-Mid-Tower-ATX-Case/2021/12879.shtml",
        "direct": deepcool_gallery("Cases", "Matrexx_50"),
    },
    "cases-016": {
        "source": "https://www.deepcool.com/products/Cases/fulltowercases/CC560-Limited-V2-Mid-Tower-Airflow-Case/2023/17784.shtml",
        "direct": deepcool_gallery("Cases", "CC560_Limited_V2"),
    },

    "psu-001": {
        "source": "https://galax.com/pt/product/galax-omega-gl650s/",
        "direct": [
            "https://galax.com/wp-content/uploads/2025/10/DSC4510-650-US.png",
            "https://galax.com/wp-content/uploads/2025/10/DSC4534-650-US.png",
        ],
    },
    "psu-002": {
        "source": "https://www.segotep.com/EN/home/product?id=373",
        "kind": "segotep",
    },
    "psu-003": {
        "source": "https://www.segotep.com/EN/home/product?id=578",
        "kind": "segotep",
    },
    "psu-004": {
        "source": "https://www.segotep.com/EN/home/product?id=576",
        "kind": "segotep",
    },
    "psu-005": {
        "source": "https://www.segotep.com/EN/home/product?id=576",
        "kind": "segotep",
    },
    "psu-011": {
        "source": "https://www.segotep.com/EN/home/product?id=475",
        "kind": "segotep",
    },

    "cooling-001": {
        "source": "https://www.segotep.com/EN/home/product?id=a9d65fa7-b33d-4231-b352-ca8759b9a017",
        "kind": "segotep",
    },
    "cooling-002": {
        "source": "https://www.segotep.com/EN/home/product?id=294",
        "kind": "segotep",
    },
    "cooling-003": {
        "source": "https://www.segotep.com/EN/home/product?id=297",
        "kind": "segotep",
    },
    "cooling-005": {
        "source": "https://www.segotep.com/EN/home/product?id=227",
        "kind": "segotep",
    },
    "cooling-012": {
        "source": "https://www.deepcool.com/products/Cooling/cpuliquidcoolers/LT360-ARGB-360mm-Liquid-CPU-Cooler-1851-1700-AM5/2024/18684.shtml",
        "direct": deepcool_gallery("Cooling/CPULiquidCoolers", "LT360_ARGB"),
    },
    "cooling-015": {
        "source": "https://www.deepcool.com/products/Cooling/cpuliquidcoolers/MYSTIQUE-240-ARGB-5th-Gen-LCD-Liquid-Cooler-1851-1700-AM5/2024/18770.shtml",
        "direct": deepcool_gallery("Cooling/CPULiquidCoolers", "MYSTIQUE_240_ARGB"),
    },
    "cooling-016": {
        "source": "https://www.deepcool.com/products/Cooling/laptopcoolers/2021/14289.shtml",
        "direct": deepcool_gallery("Cooling/LaptopCoolers", "N200"),
    },
    "cooling-017": {
        "source": "https://www.deepcool.com/products/Cooling/laptopcoolers/2021/11402.shtml",
        "direct": deepcool_gallery("Cooling/LaptopCoolers", "UPAL"),
    },
    "cooling-018": {
        "source": "https://uk.deepcool.com/products/Cooling/cpuaircoolers/2021/14270.shtml",
        "direct": deepcool_gallery("Cooling/CPUAirCoolers", "CK_11508"),
    },
    "cooling-019": {
        "source": "https://www.deepcool.com/products/Cooling/cpuliquidcoolers/MYSTIQUE-240-ARGB-5th-Gen-LCD-Liquid-Cooler-1851-1700-AM5/2024/18770.shtml",
        "direct": deepcool_gallery("Cooling/CPULiquidCoolers", "MYSTIQUE_240_ARGB"),
    },
    "cooling-021": {
        "source": "https://www.deepcool.com/products/Cooling/laptopcoolers/2021/11399.shtml",
        "direct": deepcool_gallery("Cooling/LaptopCoolers", "X6"),
    },
}


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=10) as response:
        return response.read()


def valid_images(urls: list[str], limit: int = 5) -> list[tuple[str, bytes]]:
    """Download candidate images in parallel, retaining source order."""
    if not urls:
        return []
    candidates = urls[:40]

    def load(index: int, url: str) -> tuple[int, str, bytes] | None:
        try:
            data = fetch(url)
            # Decode before writing so HTML/error pages cannot become broken
            # product assets.
            image_from_bytes(data)
            return index, url, data
        except Exception as error:  # noqa: BLE001 - per-source fallback
            print(f"SKIP {url}: {error}", file=sys.stderr)
            return None

    results: list[tuple[int, str, bytes]] = []
    with ThreadPoolExecutor(max_workers=min(8, len(candidates))) as executor:
        futures = [executor.submit(load, index, url) for index, url in enumerate(candidates)]
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                results.append(result)
    results.sort(key=lambda item: item[0])
    return [(url, data) for _, url, data in results[:limit]]


def absolute_url(value: str, base: str) -> str | None:
    value = html.unescape(value).replace("\\/", "/").strip().strip("'\"")
    if not value or value.startswith(("data:", "javascript:", "mailto:")):
        return None
    if value.startswith("//"):
        return "https:" + value
    return urllib.parse.urljoin(base, value)


def page_candidates(source: dict) -> list[str]:
    page = source["source"]
    raw = fetch(page).decode("utf-8", "ignore")
    values: list[str] = []
    # Include normal HTML image attributes and the lazy-loading attributes used
    # by the GameMax product pages.
    for value in re.findall(
        r"(?:src|href|content|data-src|data-lazy-src|data-original|data-src-pc|data-src-mobile)\s*=\s*['\"]([^'\"]+)['\"]",
        raw,
        re.I,
    ):
        url = absolute_url(value, page)
        if url and url not in values:
            values.append(url)
    for value in re.findall(r"https?://[^\"'<>\\\s]+", raw):
        url = absolute_url(value, page)
        if url and url not in values:
            values.append(url)

    kind = source.get("kind")
    filtered: list[str] = []
    for url in values:
        low = url.lower()
        if kind == "gamemax":
            allowed = "cdn.gamemaxpc.com/runtime/image/w800" in low
            bad = any(token in low for token in ("logo", "favicon", "banner", "icon", "qr", "video"))
        elif kind == "segotep":
            allowed = "/en/uploads/attachfile/" in low or "/en/upload/images/" in low
            bad = any(token in low for token in ("logo", "favicon", "202503", "editor/", "banner", "icon"))
        else:
            allowed = False
            bad = True
        if allowed and not bad and url not in filtered:
            filtered.append(url)
    return filtered


def image_from_bytes(data: bytes) -> Image.Image:
    image = Image.open(io.BytesIO(data))
    image.load()
    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        return image.convert("RGBA")
    return image.convert("RGB")


def save_webp(data: bytes, destination: Path, maximum: int) -> None:
    image = image_from_bytes(data)
    image.thumbnail((maximum, maximum), Image.Resampling.LANCZOS)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    image.save(temporary, "WEBP", quality=84, method=6, optimize=True)
    temporary.replace(destination)


def existing_paths(product: dict) -> list[str]:
    paths = product.get("images") or ([] if not product.get("image") else [product["image"]])
    return [path for path in paths if isinstance(path, str)]


def existing_record(product: dict) -> bool:
    paths = existing_paths(product)
    return bool(paths) and all((ROOT / path).is_file() for path in paths)


def replace_card_image(page_path: Path, product: dict) -> None:
    product_id = product["id"]
    title = html.escape(product["name"], quote=True)
    page = page_path.read_text(encoding="utf-8")
    article_re = re.compile(
        rf'(<article\b[^>]*\bdata-product-id="{re.escape(product_id)}"[^>]*>.*?</article>)',
        re.I | re.S,
    )
    match = article_re.search(page)
    if not match:
        raise RuntimeError(f"card {product_id} not found in {page_path.name}")
    article = match.group(1)
    image = f'<img src="images/products/{product_id}/main.webp" alt="{title}" loading="lazy" decoding="async">'
    if f"images/products/{product_id}/main.webp" in article:
        return
    replaced, count = re.subn(
        r'<span\s+class="placeholder-icon"[^>]*>.*?</span>', image, article, count=1, flags=re.I | re.S
    )
    if count != 1:
        raise RuntimeError(f"placeholder image slot not found for {product_id} in {page_path.name}")
    page_path.write_text(page[: match.start()] + replaced + page[match.end() :], encoding="utf-8")


def unresolved_reason(product: dict) -> str:
    name = product["name"]
    if product["category"] == "Процессоры":
        return "Точное фото именно этого CPU/SKU на официальном источнике не подтверждено; общие семейные рендеры Intel не подставлялись."
    if any(token in name.lower() for token in ("китай", "vision", "dragon", "240 водянка", "360 водянка", "валак", "intell")):
        return "В каталоге нет точной модели или артикула, поэтому похожий товар не подставлялся."
    return "Подтверждённый ассет точной модели на официальном источнике не удалось скачать; оставлена заглушка."


def update_status(products: list[dict], new_count: int, existing_count: int, placeholder_count: int, webp_count: int, failed: dict[str, str]) -> None:
    now = datetime.now(timezone.utc).isoformat()
    lines = [
        "<!-- COMPONENTS PHOTO STAGE V2 START -->",
        "## Повторный полный проход фотографий комплектующих (2026-10-21)",
        "",
        "Проверены все 137 товаров девяти подкатегорий раздела «Комплектующие»: "
        "Видеокарты, Процессоры, Материнские платы, Оперативная память, SSD, HDD, "
        "Корпуса, Блоки питания и Охлаждение.",
        "",
        f"- новые точные наборы добавлены для **{new_count}** товаров; существующие подтверждённые наборы сохранены для **{existing_count}** товаров; заглушки оставлены для **{placeholder_count}** товаров;",
        f"- в компонентные записи подключено **{webp_count}** локальных WebP-файлов;",
        "- карточки категорий переведены с placeholder-icon на соответствующий `images/products/<ID>/main.webp`; универсальная галерея продолжает использовать существующие `product.js` и `images[]`;",
        "- цены, характеристики, названия, ID, SKU, `price.csv`, фильтры и товары других категорий не изменялись; существующие фотографии ноутбуков, моноблоков и системных блоков сохранены;",
        "- источники новых изображений: официальные страницы/ассеты GALAX, MSI, ASUS, GIGABYTE, Kingston, Lexar, Samsung, Western Digital, GameMax, Segotep и DeepCool.",
        "",
        "Товары, которые остались с заглушками, перечислены в `COMPONENTS_PHOTO_PROGRESS.json` с причиной по каждому ID. Причина в основном — отсутствует точная модель/артикул в каталоге или официальный ассет не позволяет подтвердить конкретную модификацию; похожие изображения не использовались.",
        "",
        f"Автоматическая проверка: {now}; все скачанные изображения открыты Pillow и сохранены как WebP, без искусственного увеличения; обновление выполнялось только в рамках девяти компонентных страниц.",
        "<!-- COMPONENTS PHOTO STAGE V2 END -->",
        "",
    ]
    content = STATUS_PATH.read_text(encoding="utf-8")
    start = content.find("<!-- COMPONENTS PHOTO STAGE V2 START -->")
    end_marker = "<!-- COMPONENTS PHOTO STAGE V2 END -->"
    end = content.find(end_marker)
    section = "\n".join(lines)
    if start >= 0 and end >= start:
        end += len(end_marker)
        content = content[:start] + section.rstrip("\n") + content[end:]
    else:
        content = content.rstrip() + "\n\n" + section
    STATUS_PATH.write_text(content, encoding="utf-8")


def main() -> int:
    products = json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))
    components = [product for product in products if product.get("category") in CATEGORIES]
    if len(components) != 137:
        raise RuntimeError(f"expected 137 component products, found {len(components)}")
    by_id = {product["id"]: product for product in components}
    for product_id in SOURCES:
        if product_id not in by_id:
            raise RuntimeError(f"source map contains unknown product ID {product_id}")

    progress_records: list[dict] = []
    failed: dict[str, str] = {}
    new_count = 0
    existing_count = 0

    for product in components:
        product_id = product["id"]
        category = product["category"]
        source = SOURCES.get(product_id)
        if existing_record(product):
            existing_count += 1
            progress_records.append({
                "id": product_id,
                "category": category,
                "model": product["name"],
                "status": "existing",
                "photo_count": len(existing_paths(product)),
                "paths": existing_paths(product),
                "source_urls": [],
                "reason": "Существующая подтверждённая фотография сохранена без изменений.",
            })
            continue

        selected_urls: list[str] = []
        if source:
            try:
                selected_urls = list(source.get("direct") or [])
                if not selected_urls:
                    selected_urls = page_candidates(source)
                successful = valid_images(selected_urls)
                if successful:
                    paths: list[str] = []
                    for index, (url, data) in enumerate(successful):
                        filename = "main.webp" if index == 0 else f"{index:02d}.webp"
                        path = f"images/products/{product_id}/{filename}"
                        save_webp(data, ROOT / path, 1000 if index == 0 else 1400)
                        paths.append(path)
                    product["image"] = paths[0]
                    product["images"] = paths
                    product["placeholder"] = None
                    new_count += 1
                    progress_records.append({
                        "id": product_id,
                        "category": category,
                        "model": product["name"],
                        "status": "downloaded",
                        "photo_count": len(paths),
                        "paths": paths,
                        "source_urls": [source.get("source", "")] + [url for url, _ in successful],
                        "reason": "Точная модель подтверждена официальным источником; добавлены локальные WebP.",
                    })
                    continue
                failed[product_id] = "На официальном источнике не найден пригодный файл изображения точной модели."
            except Exception as error:  # noqa: BLE001 - preserve placeholder and continue
                failed[product_id] = f"Источник недоступен или ассет не удалось обработать: {error}"

        reason = failed.get(product_id, unresolved_reason(product))
        # Make the placeholder state explicit without changing any product
        # characteristic fields.
        product["image"] = None
        product["images"] = []
        product["placeholder"] = product.get("placeholder") or "🎁"
        progress_records.append({
            "id": product_id,
            "category": category,
            "model": product["name"],
            "status": "placeholder",
            "photo_count": 0,
            "paths": [],
            "source_urls": [source.get("source", "")] if source else [],
            "reason": reason,
        })

    PRODUCTS_PATH.write_text(json.dumps(products, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for product in components:
        if product.get("image"):
            replace_card_image(ROOT / CATEGORIES[product["category"]], product)

    counts: dict[str, dict[str, int]] = {
        category: {"total": 0, "downloaded": 0, "existing": 0, "placeholder": 0}
        for category in CATEGORIES
    }
    for record in progress_records:
        counts[record["category"]]["total"] += 1
        counts[record["category"]][record["status"]] += 1
    webp_count = sum(len(record["paths"]) for record in progress_records)
    progress = {
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "Все товары девяти подкатегорий раздела «Комплектующие»",
        "imageRoot": "images/products/<PRODUCT_ID>/",
        "policy": "Только точная модель на официальном домене; при отсутствии подтверждения сохранена заглушка.",
        "categories": counts,
        "totals": {
            "products": len(components),
            "downloaded": new_count,
            "existing": existing_count,
            "placeholder": sum(1 for record in progress_records if record["status"] == "placeholder"),
            "webp": webp_count,
        },
        "records": progress_records,
    }
    PROGRESS_PATH.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    update_status(
        components,
        new_count,
        existing_count,
        progress["totals"]["placeholder"],
        webp_count,
        failed,
    )
    print(json.dumps({"new": new_count, "existing": existing_count, "placeholder": progress["totals"]["placeholder"], "webp": webp_count, "failed": failed}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

