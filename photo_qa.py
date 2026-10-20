from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageOps

progress = json.loads(Path("PHOTO_PROGRESS.json").read_text(encoding="utf-8"))
paths = []
for record in progress["records"]:
    for value in record.get("paths", []):
        if value not in paths:
            paths.append(value)

metrics = []
for filename in paths:
    path = Path(filename)
    if not path.is_file():
        metrics.append({"path": filename, "status": "missing"})
        continue
    image = Image.open(path).convert("RGBA")
    alpha = image.getchannel("A")
    extrema = alpha.getextrema()
    bbox = alpha.getbbox()
    corners = [image.getpixel(point) for point in [(0,0), (image.width-1,0), (0,image.height-1), (image.width-1,image.height-1)]]
    transparent = sum(1 for value in alpha.getdata() if value == 0)
    metrics.append({
        "path": filename,
        "status": "ok",
        "size": [image.width, image.height],
        "alpha_extrema": list(extrema),
        "transparent_pixels": transparent,
        "transparent_ratio": round(transparent / (image.width * image.height), 4),
        "visible_bbox": list(bbox) if bbox else None,
        "corners": [list(pixel) for pixel in corners]
    })

Path("PHOTO_QA.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

tile_w, tile_h = 390, 330
cols = 4
rows = (len(paths) + cols - 1) // cols
sheet = Image.new("RGBA", (cols * tile_w, rows * tile_h), (237, 240, 247, 255))
draw = ImageDraw.Draw(sheet)

for index, filename in enumerate(paths):
    x0 = (index % cols) * tile_w
    y0 = (index // cols) * tile_h
    tile = Image.new("RGBA", (tile_w - 20, tile_h - 55), (255, 255, 255, 255))
    path = Path(filename)
    if path.is_file():
        image = Image.open(path).convert("RGBA")
        fitted = ImageOps.contain(image, (tile.width - 16, tile.height - 16))
        left = (tile.width - fitted.width) // 2
        top = (tile.height - fitted.height) // 2
        tile.alpha_composite(fitted, (left, top))
    else:
        ImageDraw.Draw(tile).text((20, 40), "placeholder", fill=(120, 128, 145, 255))
    sheet.alpha_composite(tile, (x0 + 10, y0 + 10))
    label = filename.replace("assets/products/", "")
    draw.text((x0 + 12, y0 + tile_h - 35), label, fill=(35, 42, 60, 255))

sheet.convert("RGB").save("PHOTO_QA.png", "PNG", optimize=True)
print(json.dumps(metrics, ensure_ascii=False, indent=2))
