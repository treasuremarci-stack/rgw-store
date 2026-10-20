from collections import deque
from pathlib import Path
import json
from PIL import Image

progress = json.loads(Path("PHOTO_PROGRESS.json").read_text(encoding="utf-8"))
paths = []
for record in progress["records"]:
    for value in record.get("paths", []):
        if value not in paths:
            paths.append(value)

changed = []
untouched = []
reports = []

def near_white(pixel):
    r, g, b, a = pixel
    return a > 0 and min(r, g, b) >= 235 and max(r, g, b) - min(r, g, b) <= 28

for filename in paths:
    path = Path(filename)
    if not path.is_file():
        reports.append(f"{filename}: missing")
        continue

    image = Image.open(path).convert("RGBA")
    width, height = image.size
    pixels = image.load()
    corners = [
        pixels[0, 0],
        pixels[width - 1, 0],
        pixels[0, height - 1],
        pixels[width - 1, height - 1],
    ]

    if any(pixel[3] < 250 for pixel in corners) or not all(near_white(pixel) for pixel in corners):
        untouched.append(filename)
        reports.append(f"{filename}: unchanged")
        continue

    exterior = bytearray(width * height)
    queue = deque()

    def enqueue(x, y):
        index = y * width + x
        if not exterior[index] and near_white(pixels[x, y]):
            exterior[index] = 1
            queue.append((x, y))

    for x in range(width):
        enqueue(x, 0)
        if height > 1:
            enqueue(x, height - 1)
    for y in range(height):
        enqueue(0, y)
        if width > 1:
            enqueue(width - 1, y)

    while queue:
        x, y = queue.popleft()
        if x:
            enqueue(x - 1, y)
        if x + 1 < width:
            enqueue(x + 1, y)
        if y:
            enqueue(x, y - 1)
        if y + 1 < height:
            enqueue(x, y + 1)

    removed = sum(exterior)
    if removed < max(100, width * height // 100):
        untouched.append(filename)
        reports.append(f"{filename}: unchanged (no connected white field)")
        continue

    alpha = image.getchannel("A")
    alpha_pixels = alpha.load()
    for index, is_background in enumerate(exterior):
        if is_background:
            alpha_pixels[index % width, index // width] = 0

    image.putalpha(alpha)
    image.save(path, "WEBP", quality=86, method=6)
    changed.append(filename)
    reports.append(f"{filename}: transparent exterior ({removed} pixels), size {width}x{height}")

section = """## Laptop photo background correction (2026-10-20)

- Reviewed all 16 existing WebP files linked to the first 10 laptop records. laptop-008 and laptop-009 remain placeholders and have no photo files to process.
- The light-gray catalog/product containers come from existing CSS; the visible white rectangles were embedded in source images.
- Removed only border-connected near-white pixels from affected images. Enclosed white laptop areas were not flood-filled. Dimensions, aspect ratios and visual scale were preserved; no cropping or stretching was introduced.
- Approved non-white/transparent images were left unchanged.

### Files checked

""" + "\n".join(f"- {line}" for line in reports) + """
- Product names, IDs, SKUs, characteristics, prices, price.csv, catalog markup, product-page logic and card design were not changed in this photo-only stage.
"""

status_path = Path("PROJECT_STATUS.md")
status = status_path.read_text(encoding="utf-8")
marker = "## Laptop photo background correction (2026-10-20)"
if marker in status:
    status = status.split(marker, 1)[0].rstrip() + "\n\n" + section
elif "\n## Next proposed stage" in status:
    status = status.replace("\n## Next proposed stage", "\n\n" + section + "\n## Next proposed stage", 1)
else:
    status = status.rstrip() + "\n\n" + section
status_path.write_text(status.rstrip() + "\n", encoding="utf-8")

print("Changed files:")
for item in changed:
    print("  " + item)
print("Unchanged files:")
for item in untouched:
    print("  " + item)
print(f"Processed {len(paths)} linked files; changed {len(changed)}.")
