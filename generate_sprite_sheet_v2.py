import os
from PIL import Image, ImageDraw

# Sprite sheet settings
FRAME_W, FRAME_H = 32, 32
COLUMNS = 6  # keep 6 columns to fit within 192px width
ROWS = 4    # idle, walk, attack, hurt/death
WIDTH = FRAME_W * COLUMNS
HEIGHT = FRAME_H * ROWS

# Palette (RGBA)
PALETTE = {
    "slate": (45, 45, 70, 255),   # deep iron
    "crimson": (150, 20, 20, 255),
    "bronze": (184, 115, 51, 255),
    "steel": (200, 200, 200, 255),
    "gold": (230, 190, 50, 255),
    "eye": (30, 0, 0, 255),
    "transparent": (0, 0, 0, 0),
    "skin": (230, 190, 150, 255),
    "hair": (30, 20, 10, 255),
}

# Helper drawing functions for each archetype
def draw_mughal(draw, frame_type, idx):
    # Base body
    draw.rectangle([9, 13, 23, 28], fill=PALETTE["slate"])  # torso
    draw.rectangle([12, 5, 19, 12], fill=PALETTE["skin"])   # head
    # Helmet with plume
    draw.polygon([(12,5),(19,5),(15,0)], fill=PALETTE["gold"])  # simple plume
    # Eyes
    draw.rectangle([14,7,15,8], fill=PALETTE["eye"])
    draw.rectangle([16,7,17,8], fill=PALETTE["eye"])
    # Hair
    draw.rectangle([12,6,19,7], fill=PALETTE["hair"])    # simple hair band
    # Armor pauldrons
    draw.rectangle([8,13,10,28], fill=PALETTE["bronze"])  # left
    draw.rectangle([22,13,24,28], fill=PALETTE["bronze"]) # right
    # Weapon: curved Talwar
    if frame_type == "idle":
        draw.line([16,12,28,0], fill=PALETTE["steel"], width=2)  # raised
    elif frame_type == "walk":
        offset = (idx % 2) * 2
        draw.line([12,20+offset,28,20+offset], fill=PALETTE["steel"], width=2)
    elif frame_type == "attack":
        sweep = idx * 5
        draw.line([8,28,28-sweep,8], fill=PALETTE["steel"], width=2)
    elif frame_type == "hurt":
        draw.ellipse([10,10,22,22], outline=PALETTE["crimson"], width=2)

def draw_vijayanagara(draw, frame_type, idx):
    # Body & head
    draw.rectangle([9,13,23,28], fill=PALETTE["slate"])
    draw.rectangle([12,5,19,12], fill=PALETTE["skin"])   # head
    # Feathered headdress
    draw.polygon([(12,5),(19,5),(15,0)], fill=PALETTE["crimson"])  # bright feather
    # Eyes
    draw.rectangle([14,7,15,8], fill=PALETTE["eye"])
    draw.rectangle([16,7,17,8], fill=PALETTE["eye"])
    # Armor accents (gold trims)
    draw.rectangle([8,13,10,28], fill=PALETTE["gold"])
    draw.rectangle([22,13,24,28], fill=PALETTE["gold"])
    # Weapon: bamboo longbow
    if frame_type == "idle":
        # bow held vertically
        draw.arc([5,2,27,30], start=45, end=135, fill=PALETTE["steel"], width=2)
        draw.line([16,12,16,0], fill=PALETTE["steel"], width=1)  # string
    elif frame_type == "walk":
        # bow at side
        draw.arc([8,8,28,28], start=30, end=150, fill=PALETTE["steel"], width=2)
    elif frame_type == "attack":
        # arrow drawn
        draw.line([6,20,26,4], fill=PALETTE["steel"], width=2)  # arrow shaft
        draw.polygon([(26,4),(24,5),(24,3)], fill=PALETTE["steel"])  # tip
    elif frame_type == "hurt":
        draw.ellipse([10,10,22,22], outline=PALETTE["crimson"], width=2)

def draw_maratha(draw, frame_type, idx):
    # Body & head
    draw.rectangle([9,13,23,28], fill=PALETTE["slate"])
    draw.rectangle([12,5,19,12], fill=PALETTE["skin"])   # head
    # Turban
    draw.rectangle([11,3,18,6], fill=PALETTE["bronze"])  # simple turban band
    # Eyes
    draw.rectangle([14,7,15,8], fill=PALETTE["eye"])
    draw.rectangle([16,7,17,8], fill=PALETTE["eye"])
    # Armor (bronze pauldrons)
    draw.rectangle([8,13,10,28], fill=PALETTE["bronze"])
    draw.rectangle([22,13,24,28], fill=PALETTE["bronze"])
    # Weapon: spear
    if frame_type == "idle":
        draw.line([16,12,28,0], fill=PALETTE["steel"], width=2)  # spear pointed up
    elif frame_type == "walk":
        offset = (idx % 2) * 2
        draw.line([12,20+offset,28,20+offset], fill=PALETTE["steel"], width=2)
    elif frame_type == "attack":
        swing = idx * 4
        draw.line([8,28,28-swing,8], fill=PALETTE["steel"], width=2)
    elif frame_type == "hurt":
        draw.ellipse([10,10,22,22], outline=PALETTE["crimson"], width=2)

# Mapping of column to archetype
ARchetype_funcs = [draw_mughal, draw_vijayanagara, draw_maratha]
# We'll repeat each archetype twice across the 6 columns (2 each)
column_to_func = []
for func in ARchetype_funcs:
    column_to_func.extend([func, func])

# Create empty sheet
sheet = Image.new('RGBA', (WIDTH, HEIGHT), PALETTE["transparent"])

layout = {
    0: "idle",
    1: "walk",
    2: "attack",
    3: "hurt",
}

for row, frame_type in layout.items():
    for col in range(COLUMNS):
        if col >= len(column_to_func):
            continue
        draw_func = column_to_func[col]
        frame = Image.new('RGBA', (FRAME_W, FRAME_H), PALETTE["transparent"])
        draw = ImageDraw.Draw(frame)
        draw_func(draw, frame_type, col)
        sheet.paste(frame, (col*FRAME_W, row*FRAME_H))

# Save
out_path = os.path.join(os.path.dirname(__file__), 'enemy_sprite_sheet_v2.png')
sheet.save(out_path)
print('Saved sprite sheet to', out_path)
