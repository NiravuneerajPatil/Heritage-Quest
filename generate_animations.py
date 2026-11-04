"""
Heritage Quest – Enemy Animation GIF Exporter
Exports 12 animated GIFs (3 archetypes × 4 animations):
  mughal_idle.gif, mughal_walk.gif, mughal_attack.gif, mughal_hurt.gif
  archer_idle.gif, archer_walk.gif, archer_attack.gif, archer_hurt.gif
  maratha_idle.gif, maratha_walk.gif, maratha_attack.gif, maratha_hurt.gif
Each GIF is 32x32, scaled 4x (128x128) for visibility, transparent BG.
"""
from PIL import Image
import os

OUT_DIR = r"C:\Users\ASUS\Documents\Field Project\Heritage Quest\Heritage Quest\enemy_animations"
os.makedirs(OUT_DIR, exist_ok=True)

FW = 32
FH = 32
SCALE = 4  # output at 128x128 for visibility

# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------
XX = (0,   0,   0,   0)
KK = (20,  16,  30,  255)
S0 = (200, 205, 215, 255)
S1 = (140, 145, 155, 255)
S2 = (240, 248, 255, 255)
CR = (160, 20,  20,  255)
CD = (100, 10,  10,  255)
CH = (220, 60,  60,  255)
BR = (184, 115, 51,  255)
BD = (120, 75,  30,  255)
BH = (240, 190, 90,  255)
SL = (45,  48,  72,  255)
LD = (28,  30,  50,  255)
LH = (80,  88,  120, 255)
SK = (200, 165, 120, 255)
SD = (160, 120, 80,  255)
SH = (230, 200, 165, 255)
GD = (220, 185, 45,  255)
GH = (255, 235, 120, 255)
GX = (150, 120, 20,  255)
HA = (30,  22,  12,  255)
WH = (240, 235, 220, 255)
WD = (110, 70,  30,  255)
WX = (70,  45,  15,  255)
WL = (180, 130, 70,  255)
FT = (90,  60,  20,  255)
FL = (240, 140, 20,  255)
OR = (230, 120, 30,  255)
RD = (220, 30,  30,  255)
EY = (255, 120, 0,   255)
ED = (180, 60,  0,   255)


def grid_to_img(grid, scale=SCALE):
    img = Image.new('RGBA', (FW, FH), (0, 0, 0, 0))
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c != XX and c[3] > 0:
                img.putpixel((x, y), c)
    return img.resize((FW * scale, FH * scale), Image.NEAREST)


def copy_grid(g):
    return [row[:] for row in g]


def save_gif(frames, path, duration=120, loop=0):
    """Save RGBA frames as animated GIF with transparency."""
    pals = []
    for f in frames:
        p = f.convert('P', palette=Image.ADAPTIVE, colors=255)
        pals.append(p)
    pals[0].save(
        path,
        save_all=True,
        append_images=pals[1:],
        duration=duration,
        loop=loop,
        optimize=False,
        transparency=0,
        disposal=2,
    )
    print(f"  Saved: {os.path.basename(path)}")


# ===========================================================================
#  MUGHAL GUARD BASE GRID
# ===========================================================================
MG_BASE = [
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,S2,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,S2,S0,KK,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,S2,S0,KK,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,S2,S1,KK,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,S2,S0,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,CR,CR,CR,CR,CR,CR,KK,S2,S0,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,CR,CH,CH,CH,CH,CH,CR,XX,KK,S1,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,CR,CH,GD,CR,GD,CH,CR,XX,XX,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,KK,SK,SK,SK,SK,SK,SK,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,KK,SK,ED,EY,SK,EY,ED,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,KK,SK,SK,OR,SK,OR,SK,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,KK,SD,SK,SK,SK,SK,SD,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,KK,BR,SL,LH,SL,SL,LH,SL,BR,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,BD,KK,BR,BR,LD,SL,LH,SL,SL,SL,SL,LH,SL,LD,BR,BR,KK,BD,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,BD,KK,BR,LD,SL,SL,LH,SL,SL,SL,SL,LH,SL,SL,LD,BR,KK,BD,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,SK,BD,KK,BR,LD,SL,SL,SL,LH,SL,SL,LH,SL,SL,SL,LD,BR,KK,SK,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,SK,SH,SD,KK,LD,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,LD,KK,SH,SK,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,SK,SH,SD,KK,LD,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,LD,KK,SD,SK,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,SD,KK,BD,BR,LD,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,LD,BR,BD,KK,SD,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,KK,GD,GH,GD,GX,GD,GH,GD,GX,GX,GD,GH,GD,GX,GD,GH,GD,KK,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,KK,SL,LH,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,LH,SL,KK,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,KK,SL,SL,SL,SL,SL,SL,XX,XX,XX,SL,SL,SL,SL,SL,SL,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,KK,SL,LH,SL,LD,XX,XX,XX,XX,LD,SL,LH,SL,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,KK,LD,SL,SL,XX,XX,XX,XX,XX,XX,SL,SL,LD,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,KK,LD,SL,SL,XX,XX,XX,XX,XX,XX,SL,SL,LD,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,KK,LD,SL,SL,XX,XX,XX,XX,XX,XX,SL,SL,LD,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,KK,WH,WH,WH,XX,XX,XX,XX,XX,XX,WH,WH,WH,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,KK,WH,WH,WH,WH,WD,XX,XX,XX,WD,WH,WH,WH,WH,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,KK,WX,WH,WH,WX,KK,XX,XX,XX,KK,WX,WH,WH,WX,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
]

def mg_idle_frame(t):
    """Idle: subtle sword bob + eye pulse."""
    g = copy_grid(MG_BASE)
    if t % 2 == 1:
        # bob sword 1px down
        for y in range(5, 1, -1):
            for x in range(19, 27):
                if MG_BASE[y-1][x] != XX:
                    g[y][x] = MG_BASE[y-1][x]
                    g[y-1][x] = XX
        # slightly dim eyes on inhale
        g[9][13] = ED; g[9][16] = ED
    return grid_to_img(g)

def mg_walk_frame(t):
    """Walk: left/right leg stride, arm swing."""
    g = copy_grid(MG_BASE)
    offsets = [0, 1, 2, 1, 0, -1]
    shift = offsets[t % 6]
    # Stride: shift right leg y by -shift (forward) and left leg y by +shift
    if shift > 0:
        for y in range(27, 19, -1):
            for x in range(16, 21):
                ny = y - shift
                if 0 <= ny < 32 and g[y][x] != XX:
                    g[ny][x] = g[y][x]
                    g[y][x] = XX
    elif shift < 0:
        for y in range(20, 28):
            for x in range(7, 12):
                ny = y - shift
                if 0 <= ny < 32 and g[y][x] != XX:
                    g[ny][x] = g[y][x]
                    g[y][x] = XX
    # Slight body bob
    if t in (1, 3, 5):
        for y in range(29, 7, -1):
            for x in range(5, 25):
                if g[y-1][x] != XX:
                    g[y][x] = g[y-1][x]
                    g[y-1][x] = XX
    return grid_to_img(g)

def mg_attack_frame(t):
    """Attack: Talwar sword sweep arc."""
    g = copy_grid(MG_BASE)
    # Clear existing sword
    for y in range(0, 8):
        for x in range(18, 32):
            g[y][x] = XX
    # 6-step sword arc from upper-right → down-left strike
    paths = [
        [(25,0),(24,1),(23,2),(22,3),(21,4)],
        [(23,2),(22,3),(21,4),(20,5),(19,6)],
        [(21,4),(20,5),(19,6),(18,7),(17,8)],
        [(19,6),(18,7),(17,8),(16,9),(15,10)],
        [(17,8),(16,9),(15,10),(14,11),(13,12)],
        [(15,10),(14,11),(13,12),(12,13),(11,14)],
    ]
    for (px, py) in paths[t]:
        if 0<=py<32 and 0<=px<32:
            g[py][px] = S2
        if 0<=py<32 and 0<=px-1<32:
            g[py][px-1] = S0
    # On final frame add impact flash
    if t == 5:
        for dy in range(-1,2):
            for dx in range(-1,2):
                ny,nx = 14+dy, 11+dx
                if 0<=ny<32 and 0<=nx<32:
                    g[ny][nx] = GH
    return grid_to_img(g)

def mg_hurt_frame(t):
    """Hurt/death: red flash, collapse."""
    g = copy_grid(MG_BASE)
    if t == 0:
        # Hit flash – tint head/chest red
        for y in range(8, 20):
            for x in range(7, 25):
                if g[y][x] not in (XX, KK):
                    r,gr,b,a = g[y][x]
                    g[y][x] = (min(255,r+80), max(0,gr-40), max(0,b-40), a)
        for (bx,by) in [(10,16),(9,18),(13,15)]:
            g[by][bx] = RD
    else:
        # Collapse – shift everything down 4px
        for y in range(31, 3, -1):
            for x in range(32):
                if g[y-4][x] != XX:
                    g[y][x] = g[y-4][x]
        for y in range(0, 4):
            for x in range(32):
                g[y][x] = XX
        # Redden
        for y in range(12, 32):
            for x in range(7, 25):
                if g[y][x] not in (XX, KK):
                    r,gr,b,a = g[y][x]
                    g[y][x] = (min(255,r+60), max(0,gr-30), max(0,b-30), a)
    return grid_to_img(g)

# ===========================================================================
#  ARCHER BASE GRID
# ===========================================================================
VA_BASE = [
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,FL,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,FT,FL,FT,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,FT,FT,FL,FT,FL,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,KK,GD,GH,GD,GD,GH,GD,KK,XX,XX,XX,XX,XX,WD,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,KK,GX,GD,GH,GH,GD,GX,KK,XX,XX,XX,XX,WX,WD,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,KK,SK,SK,SK,SK,SK,SK,SK,KK,XX,XX,XX,WX,WD,WL,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,KK,SK,ED,EY,SK,SK,EY,ED,KK,XX,XX,WX,WD,WL,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,KK,SK,OR,SK,SK,SK,SK,OR,KK,XX,WX,WD,WL,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,KK,SD,SK,SK,SK,SK,SK,SD,KK,XX,WX,WD,WL,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,KK,GD,GH,GD,GD,GH,KK,XX,XX,WX,WD,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,WX,WD,WL,KK,BR,BR,SL,LH,SL,SL,LH,SL,SL,SL,SL,LH,SL,BR,BR,KK,WD,WX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [WX,WD,WL,KK,BR,LD,SL,LH,SL,SL,SL,SL,SL,SL,SL,SL,SL,LH,SL,LD,BR,KK,WL,WD,WX,XX,XX,XX,XX,XX,XX,XX],
  [WX,WD,WL,KK,BR,LD,SL,SL,SL,SL,LH,SL,SL,SL,SL,SL,LH,SL,SL,SL,LD,BR,KK,WL,WD,WX,XX,XX,XX,XX,XX,XX],
  [WX,WD,WL,KK,BR,LD,SL,SL,SL,SL,SL,SL,SL,LH,SL,SL,LH,SL,SL,SL,LD,BR,KK,WL,WD,WX,XX,XX,XX,XX,XX,XX],
  [WX,WD,SK,SK,LD,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,LD,SK,SK,WL,WD,WX,XX,XX,XX,XX,XX,XX],
  [WX,WD,SK,SD,KK,LD,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,LD,KK,SD,SK,WL,WD,WX,XX,XX,XX,XX,XX,XX],
  [XX,WX,WD,KK,BD,BR,LD,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,LD,BR,BD,KK,WL,WD,WX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,WX,KK,GD,GH,GX,GD,GH,GX,GD,GH,GX,GD,GH,GH,GD,GX,GD,GH,GX,KK,WD,WX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,KK,SL,LH,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,LH,SL,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,KK,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,KK,LD,SL,SL,SL,XX,XX,XX,XX,XX,XX,XX,XX,SL,SL,LD,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,KK,SL,LH,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,LH,SL,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,KK,SL,LH,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,LH,SL,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,KK,LD,SL,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,SL,LD,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,KK,WH,WH,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,WH,WH,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,KK,WH,WH,WH,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,WH,WH,WH,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,KK,WX,WH,WX,KK,XX,XX,XX,XX,XX,XX,XX,XX,KK,WX,WH,WX,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
]

def va_idle_frame(t):
    g = copy_grid(VA_BASE)
    if t % 2 == 1:
        g[0][14] = FL; g[0][15] = FT
        g[6][12] = EY; g[6][16] = EY
    return grid_to_img(g)

def va_walk_frame(t):
    g = copy_grid(VA_BASE)
    shifts = [0,1,2,1,0,-1]
    shift = shifts[t % 6]
    if shift > 0:
        for y in range(26,19,-1):
            for x in range(16,20):
                ny = y - shift
                if 0<=ny<32 and g[y][x] != XX:
                    g[ny][x] = g[y][x]; g[y][x] = XX
    elif shift < 0:
        for y in range(20,27):
            for x in range(4,8):
                ny = y - shift
                if 0<=ny<32 and g[y][x] != XX:
                    g[ny][x] = g[y][x]; g[y][x] = XX
    if t in (1,3,5):
        for y in range(31,8,-1):
            for x in range(32):
                if g[y-1][x] != XX:
                    g[y][x] = g[y-1][x]; g[y-1][x] = XX
    return grid_to_img(g)

def va_attack_frame(t):
    """Bow draw and release animation."""
    g = copy_grid(VA_BASE)
    # Draw arrow across row 13
    if t == 0:
        for x in range(5,10): g[13][x] = S0
        g[13][10] = S2
    elif t == 1:
        for x in range(3,13): g[13][x] = S0
        g[13][13] = S2
        g[13][2] = WD  # draw hand pulling string
    elif t == 2:
        for x in range(1,15): g[13][x] = S0
        g[13][15] = S2
        g[13][0] = WD
        # tension arm
        g[14][3] = SK; g[14][2] = SD
    elif t == 3:
        # Release flash
        for x in range(16,26): g[12][x] = S2
        for x in range(14,18): g[13][x] = GH
        g[13][16] = S2
    elif t == 4:
        for x in range(22,31): g[11][x] = S2
        g[11][31] = GH
    elif t == 5:
        # Arrow gone, bow settling
        for x in range(29,32): g[10][x] = S1
    return grid_to_img(g)

def va_hurt_frame(t):
    g = copy_grid(VA_BASE)
    if t == 0:
        for y in range(5,10):
            for x in range(10,19):
                if g[y][x] not in (XX,KK):
                    r,gr,b,a = g[y][x]
                    g[y][x] = (min(255,r+80), max(0,gr-40), max(0,b-40), a)
        for (bx,by) in [(9,14),(8,16),(11,17)]: g[by][bx] = RD
    else:
        for y in range(31,3,-1):
            for x in range(32):
                if g[y-4][x] != XX: g[y][x] = g[y-4][x]
        for y in range(0,4):
            for x in range(32): g[y][x] = XX
        for y in range(10,32):
            for x in range(32):
                if g[y][x] not in (XX,KK):
                    r,gr,b,a = g[y][x]
                    g[y][x] = (min(255,r+60), max(0,gr-30), max(0,b-30), a)
    return grid_to_img(g)


# ===========================================================================
#  MARATHA WARRIOR BASE GRID
# ===========================================================================
MW_BASE = [
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,S2,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,S2,S0,KK,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,S0,S2,KK,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,WL,WD,KK,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,WL,WD,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,BR,BR,BR,BR,BR,XX,WL,WD,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,BR,BH,BH,BH,BH,BR,WL,WD,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,KK,SK,SK,SK,SK,KK,WL,WD,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,KK,SK,ED,EY,EY,KK,WL,WD,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,KK,OR,SK,SK,OR,KK,WL,WD,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,KK,SD,SK,SK,SD,KK,XX,WD,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,KK,BR,SL,LH,SL,SL,LH,SL,BR,KK,WD,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,BD,KK,BR,BR,LD,SL,LH,SL,SL,SL,SL,LH,SL,LD,BR,KK,WD,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,CR,CD,CR,SK,SK,LD,SL,SL,SL,SL,SL,SL,SL,SL,SL,LD,SK,SK,WD,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,CR,CH,CD,CR,SK,SH,LD,SL,SL,SL,SL,SL,SL,SL,SL,SL,LD,SK,SH,WD,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,CR,CH,GD,CD,CR,SK,SD,KK,LD,SL,SL,SL,SL,SL,SL,SL,LD,KK,SD,SK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,CR,CH,GD,CD,KK,SD,KK,BD,BR,LD,SL,SL,SL,SL,SL,LD,BR,BD,KK,SD,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,CR,CD,KK,XX,XX,KK,GD,GH,GX,GD,GH,GX,GD,GX,GD,GH,GX,GD,GH,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,KK,XX,XX,XX,XX,KK,SL,LH,SL,SL,SL,SL,SL,SL,SL,SL,LH,SL,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,KK,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,SL,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,KK,LD,SL,SL,XX,XX,XX,XX,XX,XX,SL,LD,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,KK,SL,LH,XX,XX,XX,XX,XX,XX,LH,SL,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,KK,SL,LH,XX,XX,XX,XX,XX,XX,LH,SL,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,KK,LD,SL,XX,XX,XX,XX,XX,XX,SL,LD,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,KK,WH,WH,XX,XX,XX,XX,XX,XX,WH,WH,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,KK,WH,WH,WH,XX,XX,XX,XX,XX,XX,WH,WH,WH,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,KK,WX,WH,WX,KK,XX,XX,XX,XX,KK,WX,WH,WX,KK,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
  [XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX,XX],
]

def mw_idle_frame(t):
    g = copy_grid(MW_BASE)
    if t % 2 == 1:
        for y in range(26,0,-1):
            for x in range(19,26):
                if MW_BASE[y-1][x] in (WD,WL,WX,S0,S2,KK):
                    g[y][x] = MW_BASE[y-1][x]
                    g[y-1][x] = XX
        g[8][14] = EY; g[8][15] = EY
    return grid_to_img(g)

def mw_walk_frame(t):
    g = copy_grid(MW_BASE)
    shifts = [0,1,2,1,0,-1]
    shift = shifts[t % 6]
    if shift > 0:
        for y in range(26,19,-1):
            for x in range(15,19):
                ny = y - shift
                if 0<=ny<32 and g[y][x] != XX:
                    g[ny][x] = g[y][x]; g[y][x] = XX
    elif shift < 0:
        for y in range(20,27):
            for x in range(7,11):
                ny = y - shift
                if 0<=ny<32 and g[y][x] != XX:
                    g[ny][x] = g[y][x]; g[y][x] = XX
    if t in (1,3,5):
        for y in range(31,7,-1):
            for x in range(32):
                if g[y-1][x] != XX:
                    g[y][x] = g[y-1][x]; g[y-1][x] = XX
    return grid_to_img(g)

def mw_attack_frame(t):
    """Spear thrust: shaft extends diagonally rightward."""
    g = copy_grid(MW_BASE)
    # Clear existing spear
    for y in range(0,14):
        for x in range(18,32):
            g[y][x] = XX
    # Thrust path offsets
    base_x = 18 + t * 2
    for i in range(8):
        px = base_x + i
        py = 12 - (i // 3)
        if 0<=py<32 and 0<=px<32:
            g[py][px] = WD
            if i > 0 and 0<=py<32 and 0<=px-1<32:
                g[py][px-1] = WL
    # Tip
    tip_x = base_x + 8
    if tip_x < 32:
        g[11][tip_x] = S2
        g[12][tip_x] = S0
        if tip_x+1 < 32:
            g[10][tip_x+1] = S2
    # Impact flash on last 2 frames
    if t >= 4:
        for dy in range(-1,2):
            nx = min(31, tip_x+1)
            ny = 11 + dy
            if 0<=ny<32:
                g[ny][nx] = GH
    return grid_to_img(g)

def mw_hurt_frame(t):
    g = copy_grid(MW_BASE)
    if t == 0:
        for y in range(7,11):
            for x in range(12,18):
                if g[y][x] not in (XX,KK):
                    r,gr,b,a = g[y][x]
                    g[y][x] = (min(255,r+80), max(0,gr-40), max(0,b-40), a)
        for (bx,by) in [(6,14),(5,16),(8,17),(7,13)]: g[by][bx] = RD
    else:
        for y in range(31,3,-1):
            for x in range(32):
                if g[y-4][x] != XX: g[y][x] = g[y-4][x]
        for y in range(0,4):
            for x in range(32): g[y][x] = XX
        for y in range(10,32):
            for x in range(32):
                if g[y][x] not in (XX,KK):
                    r,gr,b,a = g[y][x]
                    g[y][x] = (min(255,r+60), max(0,gr-30), max(0,b-30), a)
    return grid_to_img(g)


# ===========================================================================
#  Build & save all GIFs
# ===========================================================================
print("Generating enemy animations...")

animations = {
    # Mughal
    "mughal_idle":   ([mg_idle_frame(i) for i in range(4)],    150),
    "mughal_walk":   ([mg_walk_frame(i) for i in range(6)],    100),
    "mughal_attack": ([mg_attack_frame(i) for i in range(6)],   80),
    "mughal_hurt":   ([mg_hurt_frame(i) for i in range(2)],    200),
    # Archer
    "archer_idle":   ([va_idle_frame(i) for i in range(4)],    150),
    "archer_walk":   ([va_walk_frame(i) for i in range(6)],    100),
    "archer_attack": ([va_attack_frame(i) for i in range(6)],   80),
    "archer_hurt":   ([va_hurt_frame(i) for i in range(2)],    200),
    # Maratha
    "maratha_idle":   ([mw_idle_frame(i) for i in range(4)],   150),
    "maratha_walk":   ([mw_walk_frame(i) for i in range(6)],   100),
    "maratha_attack": ([mw_attack_frame(i) for i in range(6)],  80),
    "maratha_hurt":   ([mw_hurt_frame(i) for i in range(2)],   200),
}

for name, (frames, dur) in animations.items():
    path = os.path.join(OUT_DIR, f"{name}.gif")
    save_gif(frames, path, duration=dur)

print(f"\nAll 12 GIFs saved to:\n  {OUT_DIR}")
