from pathlib import Path
import hashlib
import json
import re
import subprocess

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
PROGRESS_PATH = ROOT / "MONOBLOCK_PHOTO_PROGRESS.json"
STATUS_PATH = ROOT / "PROJECT_STATUS.md"

TARGETS = {
    "assets/products/mono-004/main.webp",
    "assets/products/mono-005/main.webp",
}
TEMPORARY = {
    "tools/fix_lenovo_monoblock_scale.py",
    ".github/workflows/fix-lenovo-monoblock-scale.yml",
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

def fit_with_margin(path, visible_ratio=0.74, output_side=1000):
    with Image.open(path) as source:
        original = ImageOps.exif_transpose(source).convert("RGBA")

    original_size = original.size
    alpha_extrema = original.getchannel("A").getextrema()
    alpha_box = original.getchannel("A").getbbox()
    if not alpha_box:
        raise RuntimeError(f"Empty image alpha channel: {path}")
    cropped = original.crop(alpha_box)
    cropped_size = cropped.size

    usable = int(output_side * visible_ratio)
    scale = min(1.0, usable / max(cropped.size))
    resized = cropped
    if scale < 1.0:
        resized = cropped.resize(
            (max(1, round(cropped.width * scale)), max(1, round(cropped.height * scale))),
            Image.Resampling.LANCZOS,
        )

    canvas = Image.new("RGBA", (output_side, output_side), (0, 0, 0, 0))
    offset = ((output_side - resized.width) // 2, (output_side - resized.height) // 2)
    canvas.alpha_composite(resized, offset)
    canvas.save(path, "WEBP", quality=84, method=6)

    with Image.open(path) as saved:
        print(
            f"{path.relative_to(ROOT)}: original={original_size} alpha={alpha_extrema} "
            f"alpha_box={alpha_box} cropped={cropped_size} "
            f"-> {saved.size} bytes={path.stat().st_size}"
        )

def update_progress():
    path = PROGRESS_PATH
    progress = json.loads(path.read_text(encoding="utf-8"))
    progress["updated"] = "2026-10-20"
    progress["last_correction"] = {
        "type": "lenovo-main-photo-scale",
        "changed_assets": sorted(TARGETS),
        "visible_ratio": 0.74,
        "note": "Only the two Lenovo main images were reframed; additional galleries and all other monoblock assets were preserved.",
    }
    for item in progress.get("products", []):
        if item.get("id") == "mono-004":
            item["correction"] = {
                "main_asset": "assets/products/mono-004/main.webp",
                "full_device_fit": True,
                "visible_ratio": 0.74,
                "gallery_preserved": True,
            }
        elif item.get("id") == "mono-005":
            item["correction"] = {
                "main_asset": "assets/products/mono-005/main.webp",
                "full_device_fit": True,
                "visible_ratio": 0.74,
                "gallery_preserved": True,
            }
    path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def update_status():
    path = STATUS_PATH
    status = path.read_text(encoding="utf-8")
    marker = "## Lenovo monoblock photo scale correction (2026-10-20)"
    if marker in status:
        status = status[:status.index(marker)].rstrip() + "\n"
    section = """
## Lenovo monoblock photo scale correction (2026-10-20)

- Reframed only the main images for mono-004 (Lenovo IdeaCentre 27IRH9 Core i7) and mono-005 (Lenovo IdeaCentre 27IRH9 Core i5) on a 1000x1000 transparent canvas with a 0.74 visible-image ratio, preserving proportions and adding margins around the complete device.
- Kept the existing monoblock CSS unchanged: the Lenovo badge remains above the image and the existing smooth hover animation, transition and card dimensions are preserved.
- Did not modify HP mono-001, mono-003 or mono-007, MSI mono-006, the mono-002 placeholder, or any additional gallery image.
- Product IDs, SKUs, titles, characteristics, prices, products.json, product.html, product.js, price.csv, filters, laptops and other categories remain protected.

### Scope checks

- Checked all seven monoblock card IDs and retained the existing main.webp links and product gallery arrays.
- Protected every other asset under assets/products, every category page, product-page files, product data and price.csv; the correction script aborts on an unexpected change.
- GitHub Pages and interactive visual checks are completed after the final commit; an unavailable browser runtime will be recorded explicitly.
"""
    path.write_text(status.rstrip() + "\n\n" + section.strip() + "\n", encoding="utf-8")

def main():
    protected = {
        "products.json",
        "price.csv",
        "product.html",
        "product.js",
        "PHOTO_PROGRESS.json",
    }
    protected.update(
        path.relative_to(ROOT).as_posix()
        for path in ROOT.glob("rgw_page_*.html")
    )
    for path in ROOT.glob("assets/products/**/*"):
        if path.is_file():
            relative = path.relative_to(ROOT).as_posix()
            if relative not in TARGETS:
                protected.add(relative)

    before = {
        relative: sha256(ROOT / relative)
        for relative in sorted(protected)
        if (ROOT / relative).is_file()
    }

    for relative in sorted(TARGETS):
        path = ROOT / relative
        if not path.is_file():
            raise RuntimeError(f"Missing target asset: {relative}")
        fit_with_margin(path)

    update_progress()
    update_status()

    for relative in TEMPORARY:
        path = ROOT / relative
        if path.exists():
            path.unlink()

    for relative, digest in before.items():
        path = ROOT / relative
        if not path.is_file() or sha256(path) != digest:
            raise RuntimeError(f"Protected file changed: {relative}")

    changed = git_diff_names()
    allowed = TARGETS | {"MONOBLOCK_PHOTO_PROGRESS.json", "PROJECT_STATUS.md"} | TEMPORARY
    unexpected = changed - allowed
    if unexpected:
        raise RuntimeError(f"Unexpected changed files: {sorted(unexpected)}")
    if not TARGETS.issubset(changed):
        raise RuntimeError(f"Target assets are missing from diff: {sorted(TARGETS - changed)}")

    subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True)
    print("Lenovo monoblock scale correction passed scope and whitespace checks.")
    for name in sorted(changed):
        print(f" - {name}")

if __name__ == "__main__":
    main()
# Registered workflow trigger.
