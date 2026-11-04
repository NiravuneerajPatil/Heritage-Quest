"""
Converts all animated GIFs in enemy_animations/ into PNG sprite sheets.
Each PNG has all frames laid out horizontally (Godot-friendly).
Also generates a JSON metadata file for each animation with frame count & size.
"""
from PIL import Image
import os, json

GIF_DIR = r"C:\Users\ASUS\Documents\Field Project\Heritage Quest\Heritage Quest\enemy_animations"
PNG_DIR = os.path.join(GIF_DIR, "png")
os.makedirs(PNG_DIR, exist_ok=True)

meta_all = {}

for fname in sorted(os.listdir(GIF_DIR)):
    if not fname.endswith(".gif"):
        continue

    gif_path = os.path.join(GIF_DIR, fname)
    name = fname.replace(".gif", "")

    gif = Image.open(gif_path)
    frames = []

    try:
        while True:
            frame = gif.convert("RGBA")
            frames.append(frame)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    n = len(frames)
    fw, fh = frames[0].size

    # Horizontal sprite sheet
    sheet = Image.new("RGBA", (fw * n, fh), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        sheet.paste(f, (i * fw, 0))

    out_path = os.path.join(PNG_DIR, f"{name}.png")
    sheet.save(out_path)

    # Metadata
    meta_all[name] = {
        "file": f"{name}.png",
        "frame_count": n,
        "frame_width": fw,
        "frame_height": fh,
        "sheet_width": fw * n,
        "sheet_height": fh,
        "godot_hframes": n,
        "godot_vframes": 1,
    }

    print(f"  {fname} → {name}.png  ({n} frames, {fw*n}x{fh}px)")

# Save combined metadata JSON
meta_path = os.path.join(PNG_DIR, "animations_meta.json")
with open(meta_path, "w") as f:
    json.dump(meta_all, f, indent=2)

print(f"\nAll PNGs + metadata saved to:\n  {PNG_DIR}")
print(f"  Metadata: animations_meta.json")
