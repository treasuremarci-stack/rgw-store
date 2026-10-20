#!/usr/bin/env python3
"""Find exact component product images from manufacturer domains and localize them as WebP."""
from __future__ import annotations

import html
import json
import re
import time
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from urllib.parse import quote, urljoin, urlparse

import requests
from PIL import Image, ImageOps

ROOT = Path(".")
PRODUCTS_PATH = ROOT / "products.json"
PROGRESS_PATH = ROOT / "COMPONENTS_PHOTO_PROGRESS.json"
IMAGE_ROOT = ROOT / "images" / "products"

TARGET_CATEGORIES = [
    "Видеокарты",
    "Процессоры",
    "Материнские платы",
    "Оперативная память",
    "SSD",
    "HDD",
    "Корпуса",
    "Блоки питания",
    "Охлаждение",
]

PAGE_MAP = {
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

DIRECT_PAGE_URLS = {
    "gpu-005": ["https://galax.com/en/product/geforce-rtx-5080-16gb-1-click-oc-3x/"],
    "gpu-007": ["https://www.asus.com/motherboards-components/graphics-cards/asus/gt710-sl-2gd5/"],
    "gpu-008": ["https://www.msi.com/Graphics-Card/GeForce-RTX-5060-8G-VENTUS-2X"],
}

DIRECT_IMAGE_URLS = {
    "gpu-007": ["https://www.asus.com/media/global/products/os8hWTXz7e7Le4Fx/P_setting_xxx_0_90_end_692.png"],
}

DOMAIN_BY_BRAND = {
    "asus": "asus.com",
    "msi": "msi.com",
    "gigabyte": "gigabyte.com",
    "galax": "galax.com",
    "intel": "intel.com",
    "lexar": "lexar.com",
    "samsung": "samsung.com",
    "kingston": "kingston.com",
    "hp": "hp.com",
    "wd": "westerndigital.com",
    "western digital": "westerndigital.com",
    "aigo": "aigo.com.cn",
    "gamemax": "gamemaxpc.com",
    "deepcool": "deepcool.com",
    "segotep": "segotep.com",
    "cooler master": "coolermaster.com",
}

GENERIC_WORDS = {
    "official", "product", "image", "images", "graphics", "card", "cards",
    "video", "процессор", "материнка", "материнские", "платы", "оперативка",
    "память", "ssd", "hdd", "кулер", "охлаждение", "case", "кейс", "power",
    "supply", "блок", "питания", "cooler", "liquid", "air", "water",
    "new", "black", "white", "with", "fans", "fan", "rgb", "argb", "pcie",
    "gddr", "ddr", "nvme", "sata", "m2", "mm", "gb", "tb", "wat", "w",
    "atx", "plus", "pro", "wifi", "the", "and", "one", "click", "oc",
    "gf", "tray", "notebook", "laptop", "китай", "радиатор", "водянка",
    "кулер", "куллера", "вентилятора", "мини", "оем", "модель",
}

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (compatible; AKS-component-photo-audit/1.0)",
    "Accept-Language": "en-US,en;q=0.8,ru;q=0.6",
})

def normalize(value: str) -> str:
    value = value.replace("Аsus", "Asus").replace("аsus", "asus")
    value = value.replace("Аsus", "Asus")
    value = value.replace("Дип Кул", "DeepCool").replace("Дипкул", "DeepCool")
    value = value.replace("К", "K").replace("М", "M").replace("Н", "H")
    value = value.replace("Т", "T")
    value = re.sub(r"\s*-\s*", "-", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()

def query_for(product: dict) -> str:
    name = normalize(str(product.get("name", "")))
    for prefix in (
        "Видеокарта ", "Процессор ", "Материнка ", "Оперативка ",
        "SSD ", "HDD ", "Кейс ", "Блок Питания ", "Кулер ",
    ):
        if name.lower().startswith(prefix.lower()):
            name = name[len(prefix):].strip()
    if product.get("category") == "Процессоры" and not re.search(r"\bIntel\b", name, re.I):
        name = "Intel " + name
    if product.get("category") == "Видеокарты" and re.search(r"\b(?:A76D|B67D|B67O|B76O|B37S)\b", name, re.I):
        name = "GALAX " + name
    return name

def domains_for(product: dict) -> list[str]:
    name = normalize(str(product.get("name", ""))).lower()
    domains = []
    for brand, domain in DOMAIN_BY_BRAND.items():
        if brand in name:
            domains.append(domain)
    if re.search(r"\b(?:a76d|b67d|b67o|b76o|b37s)\b", name):
        domains.append("galax.com")
    if product.get("category") == "Процессоры" and (
        re.search(r"\b(?:i[3579]|ultra)\b", name) or "intel" in name
    ):
        domains.append("intel.com")
    if "purple" in name and "wd" in name:
        domains.append("westerndigital.com")
    return list(dict.fromkeys(domains))

def distinctive_tokens(query: str, product: dict) -> list[str]:
    tokens = re.findall(r"[a-z0-9]+", query.lower())
    tokens = [t for t in tokens if t not in GENERIC_WORDS and len(t) >= 2]
    category = product.get("category")
    # Capacity-only catalog labels are not enough to establish an exact model.
    if category in {"SSD", "Оперативная память"}:
        known = ("990", "980", "700", "790", "fx", "lnm", "thor", "fury", "beast")
        if not any(k in query.lower().replace(" ", "") for k in known):
            return []
    if category == "Корпуса" and not any(re.search(r"[a-z].*\d|\d.*[a-z]|\d{3,}", t) for t in tokens):
        return []
    if category == "Блоки питания" and not any(re.search(r"[a-z].*\d|\d.*[a-z]", t) for t in tokens):
        return []
    if category == "Охлаждение" and not any(re.search(r"[a-z].*\d|\d.*[a-z]", t) for t in tokens):
        return []
    # Ignore standalone capacities, interfaces and memory generations when scoring.
    useful = [
        t for t in tokens
        if not (t.isdigit() and len(t) < 3)
        and t not in {"128", "256", "512", "1000", "2000", "1tb", "2tb", "4gb", "8gb", "16gb", "32gb"}
    ]
    return useful or tokens

def page_domain_match(url: str, domain: str) -> bool:
    host = (urlparse(url).hostname or "").lower().rstrip(".")
    return host == domain or host.endswith("." + domain)

def image_candidates(query: str, domain: str, limit: int = 8) -> list[dict]:
    url = "https://www.bing.com/images/search?form=HDRSC2&q=" + quote(
        "site:" + domain + " " + query
    )
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
    except Exception:
        return []
    candidates = []
    tags = re.findall(
        r'<a[^>]*class=["\'][^"\']*iusc[^"\']*["\'][^>]*>',
        response.text,
        flags=re.I,
    )
    for tag in tags:
        match = re.search(r'\bm=["\'](.*?)["\']', tag, flags=re.I)
        if not match:
            continue
        try:
            meta = json.loads(html.unescape(match.group(1)))
        except Exception:
            continue
        purl = html.unescape(meta.get("purl") or "")
        murl = html.unescape(meta.get("murl") or "")
        if not murl or not page_domain_match(purl, domain):
            continue
        searchable = (str(meta.get("t", "")) + " " + purl).lower()
        tokens = re.findall(r"[a-z0-9]+", query.lower())
        score = sum(1 for token in tokens if len(token) > 2 and token in searchable)
        if score < 1:
            continue
        candidates.append({
            "image_url": murl,
            "page_url": purl,
            "title": meta.get("t", ""),
            "score": score,
        })
    seen = set()
    ordered = []
    for item in sorted(candidates, key=lambda x: (-x["score"], x["image_url"])):
        if item["image_url"] not in seen:
            seen.add(item["image_url"])
            ordered.append(item)
        if len(ordered) >= limit:
            break
    return ordered

def official_page_candidates(query: str, domain: str, direct_pages: list[str] | None = None, limit: int = 8) -> list[dict]:
    page_urls = list(direct_pages or [])
    if not page_urls:
        search_url = "https://www.bing.com/search?q=" + quote(
            "site:" + domain + " " + query
        )
        try:
            response = session.get(search_url, timeout=30)
            response.raise_for_status()
        except Exception:
            return []
        for href in re.findall(r'<a[^>]+href=["\'](https?://[^"\']+)["\']', response.text, flags=re.I):
            href = html.unescape(href)
            if page_domain_match(href, domain) and href not in page_urls:
                page_urls.append(href)
            if len(page_urls) >= 6:
                break
    tokens = re.findall(r"[a-z0-9]+", query.lower())
    candidates = []
    seen = set()
    for page_url in page_urls:
        try:
            page = session.get(page_url, timeout=30)
            page.raise_for_status()
        except Exception:
            continue
        page_text = page.text
        title_match = re.search(r"<title[^>]*>(.*?)</title>", page_text, flags=re.I | re.S)
        title = html.unescape(re.sub(r"<[^>]+>", " ", title_match.group(1))).strip() if title_match else ""
        searchable = (title + " " + page_url + " " + page_text[:250000]).lower()
        score = sum(1 for token in tokens if len(token) > 2 and token in searchable)
        if score < 1:
            continue
        image_urls = []
        meta_patterns = [
            r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)',
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
            r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)',
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']twitter:image["\']',
            r'<link[^>]+rel=["\']image_src["\'][^>]+href=["\']([^"\']+)',
        ]
        for pattern in meta_patterns:
            image_urls.extend(re.findall(pattern, page_text, flags=re.I))
        source_urls = list(image_urls)
        source_urls.extend(re.findall(
            r'(?:src|data-src|data-original)=["\']([^"\']+)["\']',
            page_text,
            flags=re.I,
        ))
        for raw_url in source_urls:
            image_url = urljoin(page_url, html.unescape(raw_url))
            lowered = image_url.lower()
            if (
                not image_url.startswith("http")
                or any(word in lowered for word in ("logo", "icon", "favicon", "avatar", "sprite"))
                or lowered.endswith(".svg")
            ):
                continue
            if image_url not in seen:
                seen.add(image_url)
                candidates.append({
                    "image_url": image_url,
                    "page_url": page_url,
                    "title": title,
                    "score": score,
                })
            if len(candidates) >= limit:
                break
        if len(candidates) >= limit:
            break
    return candidates[:limit]

def download_image(url: str, referer: str) -> Image.Image | None:
    try:
        response = session.get(url, headers={"Referer": referer}, timeout=35)
        response.raise_for_status()
        if len(response.content) < 1000:
            print("PHOTO_DEBUG_SMALL", url, response.status_code, len(response.content))
            return None
        image = Image.open(BytesIO(response.content))
        image = ImageOps.exif_transpose(image)
        image.load()
        if image.width < 120 or image.height < 120:
            print("PHOTO_DEBUG_DIMENSIONS", url, image.width, image.height)
            return None
        if image.format not in {"JPEG", "PNG", "WEBP", "GIF", "BMP", "TIFF"}:
            print("PHOTO_DEBUG_FORMAT", url, image.format)
            return None
        return image
    except Exception as exc:
        print("PHOTO_DEBUG_ERROR", url, type(exc).__name__, str(exc)[:180])
        return None

def save_webp(image: Image.Image, path: Path, max_side: int) -> None:
    image = image.copy()
    image.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    if "A" in image.getbands():
        image = image.convert("RGBA")
    else:
        image = image.convert("RGB")
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "WEBP", quality=85, method=6)

def replace_catalog_slot(page_text: str, product_id: str, product_name: str, image_path: str) -> tuple[str, bool]:
    article_pattern = re.compile(
        r'(<article class="product-card" data-product-id="' + re.escape(product_id) + r'".*?</article>)',
        re.S,
    )
    match = article_pattern.search(page_text)
    if not match:
        return page_text, False
    card = match.group(1)
    if "<img " in card:
        return page_text, True
    tag = (
        '<img src="' + image_path + '" alt="' + html.escape(product_name, quote=True) +
        '" loading="lazy" decoding="async">'
    )
    new_card, count = re.subn(
        r'<span class="placeholder-icon"[^>]*>.*?</span>',
        tag,
        card,
        count=1,
        flags=re.S,
    )
    if count != 1:
        return page_text, False
    return page_text[:match.start(1)] + new_card + page_text[match.end(1):], True

def main() -> None:
    products = json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))
    target = [p for p in products if p.get("category") in TARGET_CATEGORIES]
    pages = {
        category: (ROOT / PAGE_MAP[category]).read_text(encoding="utf-8")
        for category in TARGET_CATEGORIES
    }
    records = []
    stats = {category: {"total": 0, "downloaded": 0, "existing": 0, "placeholder": 0} for category in TARGET_CATEGORIES}

    for product in target:
        pid = product["id"]
        category = product["category"]
        stats[category]["total"] += 1
        existing = product.get("image")
        if existing and (ROOT / existing).exists():
            records.append({
                "id": pid, "category": category, "model": product.get("name"),
                "status": "existing", "photo_count": len(product.get("images") or [existing]),
                "paths": product.get("images") or [existing], "source_urls": [],
                "reason": "Существующая подтверждённая фотография сохранена без изменений.",
            })
            stats[category]["existing"] += 1
            continue

        query = query_for(product)
        domains = domains_for(product)
        tokens = distinctive_tokens(query, product)
        if not domains or not tokens:
            reason = "Точная модель или официальный домен не определены; похожее изображение не подставлялось."
            records.append({
                "id": pid, "category": category, "model": product.get("name"),
                "status": "placeholder", "photo_count": 0, "paths": [],
                "source_urls": [], "reason": reason,
            })
            stats[category]["placeholder"] += 1
            continue

        candidates = []
        direct_urls = DIRECT_IMAGE_URLS.get(pid, [])
        if direct_urls:
            candidates.extend({
                "image_url": image_url,
                "page_url": (DIRECT_PAGE_URLS.get(pid) or [""])[0],
                "title": query,
                "score": 99,
            } for image_url in direct_urls)
        for domain in domains:
            if not candidates:
                candidates.extend(image_candidates(query, domain))
            if not candidates:
                candidates.extend(official_page_candidates(query, domain, DIRECT_PAGE_URLS.get(pid)))
            if candidates:
                break
        if pid in DIRECT_PAGE_URLS or pid in DIRECT_IMAGE_URLS:
            print("PHOTO_DEBUG_CANDIDATES", pid, len(candidates), [x.get("image_url") for x in candidates[:3]])
        selected = []
        downloaded = []
        seen_urls = set()
        for candidate in candidates:
            if candidate["image_url"] in seen_urls:
                continue
            seen_urls.add(candidate["image_url"])
            image = download_image(candidate["image_url"], candidate["page_url"])
            if image is None:
                continue
            selected.append(candidate)
            downloaded.append(image)
            if len(downloaded) >= 4:
                break

        if not downloaded:
            records.append({
                "id": pid, "category": category, "model": product.get("name"),
                "status": "placeholder", "photo_count": 0, "paths": [],
                "source_urls": [], "reason": "На официальном домене не найден скачиваемый ассет с подтверждаемым совпадением модели.",
                "search_query": query, "domains_checked": domains,
            })
            stats[category]["placeholder"] += 1
            time.sleep(0.25)
            continue

        paths = []
        source_urls = []
        for index, (candidate, image) in enumerate(zip(selected, downloaded)):
            filename = "main.webp" if index == 0 else f"{index:02d}.webp"
            path = IMAGE_ROOT / pid / filename
            save_webp(image, path, 1000 if index == 0 else 1400)
            relative = path.as_posix()
            paths.append(relative)
            source_urls.append({
                "image": candidate["image_url"],
                "page": candidate["page_url"],
                "title": candidate.get("title", ""),
            })
        product["image"] = paths[0]
        product["images"] = paths
        product["placeholder"] = None
        pages[category], linked = replace_catalog_slot(
            pages[category], pid, str(product.get("name", "")), paths[0]
        )
        records.append({
            "id": pid, "category": category, "model": product.get("name"),
            "status": "downloaded", "photo_count": len(paths), "paths": paths,
            "source_urls": source_urls, "search_query": query, "domains_checked": domains,
            "catalog_linked": linked,
        })
        stats[category]["downloaded"] += 1
        time.sleep(0.25)

    PRODUCTS_PATH.write_text(
        json.dumps(products, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    for category, page_text in pages.items():
        (ROOT / PAGE_MAP[category]).write_text(page_text, encoding="utf-8")
    progress = {
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "Все товары девяти подкатегорий раздела «Комплектующие»",
        "imageRoot": "images/products/<PRODUCT_ID>/",
        "policy": "Только точная модель на официальном домене; при отсутствии подтверждения сохранена заглушка.",
        "categories": stats,
        "totals": {
            "products": len(target),
            "downloaded": sum(v["downloaded"] for v in stats.values()),
            "existing": sum(v["existing"] for v in stats.values()),
            "placeholder": sum(v["placeholder"] for v in stats.values()),
            "webp": sum(r["photo_count"] for r in records if r["status"] in {"downloaded", "existing"}),
        },
        "records": records,
    }
    PROGRESS_PATH.write_text(
        json.dumps(progress, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(progress["totals"], ensure_ascii=False))

if __name__ == "__main__":
    main()
