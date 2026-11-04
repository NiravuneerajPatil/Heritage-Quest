import os
from PIL import Image, ImageDraw

# Sprite sheet dimensions
FRAME_W, FRAME_H = 32, 32
COLUMNS = 6  # max frames per row
ROWS = 4
WIDTH = FRAME_W * COLUMNS
HEIGHT = FRAME_H * ROWS

# Colors (RGBA)
PALETTE = {
    "crimson": (150, 0, 0, 255),
    "slate": (50, 50, 80, 255),
    "bronze": (184, 115, 51, 255),
    "steel": (192, 192, 192, 255),
    "eye": (30, 0, 0, 255),
    "transparent": (0, 0, 0, 0),
}

# Helper to draw a simple enemy silhouette
def draw_enemy(draw, frame_category, idx):
    # Base body
    body_color = PALETTE["slate"]
    draw.rectangle([8, 12, 24, 28], fill=body_color)  # torso
    draw.rectangle([12, 4, 20, 12], fill=body_color)  # head
    # Eyes (glowing dark)
    draw.rectangle([14, 6, 15, 7], fill=PALETTE["eye"])
    draw.rectangle([17, 6, 18, 7], fill=PALETTE["eye"])

    # Simple weapon based on category
    if frame_category == "idle":
        # sword raised diagonally
        draw.line([16, 12, 28, 0], fill=PALETTE["steel"], width=2)
    elif frame_category == "walk":
        # sword forward
        offset = (idx % 2) * 2
        draw.line([12, 20 + offset, 28, 20 + offset], fill=PALETTE["steel"], width=2)
    elif frame_category == "attack":
        # slash animation – sweep
        sweep = idx * 5
        draw.line([8, 28, 28 - sweep, 8], fill=PALETTE["steel"], width=2)
    elif frame_category == "hurt":
        # blood splatter
        draw.ellipse([10, 10, 22, 22], outline=PALETTE["crimson"], width=2)

    # Simple armor accent
    draw.rectangle([8, 12, 10, 28], fill=PALETTE["bronze"])  # left pauldrons
    draw.rectangle([22, 12, 24, 28], fill=PALETTE["bronze"])  # right pauldrons

# Create sheet
sheet = Image.new('RGBA', (WIDTH, HEIGHT), PALETTE["transparent"])

# Frame layout definitions
layout = {
    0: ("idle", 4),   # Row 0, 4 frames
    1: ("walk", 6),   # Row 1, 6 frames
    2: ("attack", 6), # Row 2, 6 frames
    3: ("hurt", 2),   # Row 3, 2 frames (death also shown as hurt)
}

for row, (category, count) in layout.items():
    for col in range(COLUMNS):
        if col >= count:
            # leave transparent cell
            continue
        frame = Image.new('RGBA', (FRAME_W, FRAME_H), PALETTE["transparent"])
        draw = ImageDraw.Draw(frame)
        draw_enemy(draw, category, col)
        sheet.paste(frame, (col * FRAME_W, row * FRAME_H))

output_path = os.path.join(os.path.dirname(__file__), 'enemy_sprite_sheet.png')
sheet.save(output_path)
print('Sprite sheet saved to', output_path)
