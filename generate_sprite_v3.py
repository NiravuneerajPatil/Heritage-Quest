"""
Heritage Quest – Enemy Sprite Sheet Generator v3
Fully hand-crafted pixel-art, 32x32 per frame, transparent PNG.
3 archetypes × 4 animation rows × up to 6 frames = 192 × 384 px total sheet.
"""
from PIL import Image

# --- Constants ---
FW = 32  # frame width
FH = 32  # frame height

# --- Color palette (RGBA) ---
XX = (0,   0,   0,   0)    # transparent
KK = (20,  16,  30,  255)  # outline
S0 = (200, 205, 215, 255)  # steel mid
S1 = (140, 145, 155, 255)  # steel dark
S2 = (240, 248, 255, 255)  # steel highlight
CR = (160, 20,  20,  255)  # crimson
CD = (100, 10,  10,  255)  # crimson dark
CH = (220, 60,  60,  255)  # crimson highlight
BR = (184, 115, 51,  255)  # bronze
BD = (120, 75,  30,  255)  # bronze dark
BH = (240, 190, 90,  255)  # bronze highlight
SL = (45,  48,  72,  255)  # slate armor
LD = (28,  30,  50,  255)  # slate dark
LH = (80,  88,  120, 255)  # slate highlight
SK = (200, 165, 120, 255)  # skin
SD = (160, 120, 80,  255)  # skin dark
SH = (230, 200, 165, 255)  # skin highlight
GD = (220, 185, 45,  255)  # gold
GH = (255, 235, 120, 255)  # gold highlight
GX = (150, 120, 20,  255)  # gold dark
HA = (30,  22,  12,  255)  # dark hair
WH = (240, 235, 220, 255)  # white/cloth
WD = (110, 70,  30,  255)  # wood
WX = (70,  45,  15,  255)  # wood dark
WL = (180, 130, 70,  255)  # wood light
FT = (90,  60,  20,  255)  # feather
FL = (240, 140, 20,  255)  # feather light
OR = (230, 120, 30,  255)  # orange warpaint
RD = (220, 30,  30,  255)  # blood red
EY = (255, 120, 0,   255)  # glowing eye
ED = (180, 60,  0,   255)  # eye dark


def grid_to_img(grid):
    img = Image.new('RGBA', (FW, FH), (0, 0, 0, 0))
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c != XX and c[3] > 0:
                img.putpixel((x, y), c)
    return img


def copy_grid(g):
    return [row[:] for row in g]


# ---------------------------------------------------------------------------
#  MUGHAL GUARD – crimson turban, iron slate armor, curved Talwar
# ---------------------------------------------------------------------------
MG = [
# col: 0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18   19   20   21   22   23   24   25   26   27   28   29   30   31
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  S2,  XX,  XX,  XX,  XX,  XX,  XX], #  0  sword tip
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  S2,  S0,  KK,  XX,  XX,  XX,  XX,  XX,  XX], #  1  blade
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  S2,  S0,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  2
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  S2,  S1,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  3  blade curve
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  S2,  S0,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  4
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  CR,  CR,  CR,  CR,  CR,  CR,  KK,  S2,  S0,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  5  turban + blade
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  CR,  CH,  CH,  CH,  CH,  CH,  CR,  XX,  KK,  S1,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  6  turban
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  CR,  CH,  GD,  CR,  GD,  CH,  CR,  XX,  XX,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  7  turban gold stripe
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  SK,  SK,  SK,  SK,  SK,  SK,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  8  face top
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  SK,  ED,  EY,  SK,  EY,  ED,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  9  eyes
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  SK,  SK,  OR,  SK,  OR,  SK,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 10  warpaint nose
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  SD,  SK,  SK,  SK,  SK,  SD,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 11  jaw
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  BR,  SL,  LH,  SL,  SL,  LH,  SL,  BR,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 12  gorget
  [XX,  XX,  XX,  XX,  XX,  XX,  BD,  KK,  BR,  BR,  LD,  SL,  LH,  SL,  SL,  SL,  SL,  LH,  SL,  LD,  BR,  BR,  KK,  BD,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 13  pauldrons
  [XX,  XX,  XX,  XX,  XX,  XX,  BD,  KK,  BR,  LD,  SL,  SL,  LH,  SL,  SL,  SL,  SL,  LH,  SL,  SL,  LD,  BR,  KK,  BD,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 14  chest
  [XX,  XX,  XX,  XX,  XX,  SK,  BD,  KK,  BR,  LD,  SL,  SL,  SL,  LH,  SL,  SL,  LH,  SL,  SL,  SL,  LD,  BR,  KK,  SK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 15  arm tops
  [XX,  XX,  XX,  XX,  SK,  SH,  SD,  KK,  LD,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  LD,  KK,  SH,  SK,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 16  arms extend
  [XX,  XX,  XX,  XX,  SK,  SH,  SD,  KK,  LD,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  LD,  KK,  SD,  SK,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 17
  [XX,  XX,  XX,  XX,  SD,  KK,  BD,  BR,  LD,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  LD,  BR,  BD,  KK,  SD,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 18  belt area
  [XX,  XX,  XX,  XX,  XX,  XX,  KK,  GD,  GH,  GD,  GX,  GD,  GH,  GD,  GX,  GX,  GD,  GH,  GD,  GX,  GD,  GH,  GD,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 19  gold belt
  [XX,  XX,  XX,  XX,  XX,  XX,  KK,  SL,  LH,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  LH,  SL,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 20  upper leg
  [XX,  XX,  XX,  XX,  XX,  XX,  KK,  SL,  SL,  SL,  SL,  SL,  SL,  XX,  XX,  XX,  SL,  SL,  SL,  SL,  SL,  SL,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 21  crotch gap
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  SL,  LH,  SL,  LD,  XX,  XX,  XX,  XX,  LD,  SL,  LH,  SL,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 22
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  LD,  SL,  SL,  XX,  XX,  XX,  XX,  XX,  XX,  SL,  SL,  LD,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 23
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  LD,  SL,  SL,  XX,  XX,  XX,  XX,  XX,  XX,  SL,  SL,  LD,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 24
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  LD,  SL,  SL,  XX,  XX,  XX,  XX,  XX,  XX,  SL,  SL,  LD,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 25
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  WH,  WH,  WH,  XX,  XX,  XX,  XX,  XX,  XX,  WH,  WH,  WH,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 26  foot
  [XX,  XX,  XX,  XX,  XX,  XX,  KK,  WH,  WH,  WH,  WH,  WD,  XX,  XX,  XX,  WD,  WH,  WH,  WH,  WH,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 27  sandal
  [XX,  XX,  XX,  XX,  XX,  XX,  KK,  WX,  WH,  WH,  WX,  KK,  XX,  XX,  XX,  KK,  WX,  WH,  WH,  WX,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 28  sole
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 29
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 30
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 31
]

def mg_walk(step):
    g = copy_grid(MG)
    # alternating leg stride
    if step % 2 == 0:
        # right leg forward (shift right leg up 2)
        for y in range(26, 20, -1):
            for x in range(16, 21):
                if g[y][x] != XX and y-2 >= 0:
                    g[y-2][x] = g[y][x]
                    g[y][x] = XX
    else:
        # left leg forward
        for y in range(26, 20, -1):
            for x in range(7, 12):
                if g[y][x] != XX and y-2 >= 0:
                    g[y-2][x] = g[y][x]
                    g[y][x] = XX
    return g

def mg_attack(step):
    g = copy_grid(MG)
    # clear sword (top-right)
    for y in range(0, 7):
        for x in range(18, 32):
            g[y][x] = XX
    # Sword sweep: 6 positions from raised to downward slash
    sword_paths = [
        [(5,25),(4,24),(3,23),(2,22),(1,21)],  # frame 0 – far raised
        [(6,24),(5,23),(4,22),(3,21),(2,20)],  # frame 1
        [(7,22),(6,21),(5,20),(4,19),(3,18)],  # frame 2 – mid swing
        [(9,20),(8,19),(7,18),(6,17),(5,16)],  # frame 3
        [(11,18),(10,17),(9,16),(8,15),(7,14)],# frame 4 – near strike
        [(13,16),(12,15),(11,14),(10,13)],     # frame 5 – impact
    ]
    for (px, py) in sword_paths[step]:
        if 0 <= py < 32 and 0 <= px < 32:
            g[py][px] = S2
        if 0 <= py < 32 and 0 <= px+1 < 32:
            g[py][px+1] = S0
    return g

def mg_hurt():
    g = copy_grid(MG)
    # tint head red
    for y in range(8, 12):
        for x in range(11, 19):
            if g[y][x] not in (XX, KK):
                g[y][x] = CD
    # blood splatters
    for (bx, by) in [(10, 15), (9, 17), (13, 18), (8, 14)]:
        if 0 <= by < 32 and 0 <= bx < 32:
            g[by][bx] = RD
    return g

mg_idle   = [grid_to_img(MG)]
# frame 1 – slight sword bob
def mg_idle1():
    g = copy_grid(MG)
    # shift sword 1px down
    for y in range(5, 1, -1):
        for x in range(18, 27):
            if MG[y-1][x] != XX:
                g[y][x] = MG[y-1][x]
                g[y-1][x] = XX
    return g
mg_idle.append(grid_to_img(mg_idle1()))
mg_idle.append(grid_to_img(MG))
mg_idle.append(grid_to_img(mg_idle1()))

mg_walk_frames   = [grid_to_img(mg_walk(i)) for i in range(6)]
mg_attack_frames = [grid_to_img(mg_attack(i)) for i in range(6)]
mg_hurt_frames   = [grid_to_img(mg_hurt()), grid_to_img(mg_hurt())]

# ---------------------------------------------------------------------------
#  VIJAYANAGARA ARCHER – feathered headdress, gold trim, longbow
# ---------------------------------------------------------------------------
VA = [
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  FL,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  0  feather tip
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  FT,  FL,  FT,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  1
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  FT,  FT,  FL,  FT,  FL,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  2
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  GD,  GH,  GD,  GD,  GH,  GD,  KK,  XX,  XX,  XX,  XX,  XX,  WD,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  3  headdress band + bow tip
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  GX,  GD,  GH,  GH,  GD,  GX,  KK,  XX,  XX,  XX,  XX,  WX,  WD,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  4
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  SK,  SK,  SK,  SK,  SK,  SK,  SK,  KK,  XX,  XX,  XX,  WX,  WD,  WL,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  5  face top
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  SK,  ED,  EY,  SK,  SK,  EY,  ED,  KK,  XX,  XX,  WX,  WD,  WL,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  6  eyes
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  SK,  OR,  SK,  SK,  SK,  SK,  OR,  KK,  XX,  WX,  WD,  WL,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  7  warpaint cheeks
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  SD,  SK,  SK,  SK,  SK,  SK,  SD,  KK,  XX,  WX,  WD,  WL,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  8  jaw
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  GD,  GH,  GD,  GD,  GH,  KK,  XX,  XX,  WX,  WD,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  9  neck gorget
  [XX,  XX,  XX,  XX,  WX,  WD,  WL,  KK,  BR,  BR,  SL,  LH,  SL,  SL,  SL,  SL,  LH,  SL,  BR,  BR,  KK,  WD,  WX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 10  shoulders+bow
  [XX,  WX,  WD,  WL,  KK,  BR,  LD,  SL,  LH,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  LH,  SL,  LD,  BR,  KK,  WL,  WD,  WX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 11  chest+bow
  [WX,  WD,  WL,  KK,  BR,  LD,  SL,  SL,  SL,  SL,  LH,  SL,  SL,  SL,  SL,  SL,  LH,  SL,  SL,  SL,  LD,  BR,  KK,  WL,  WD,  WX,  XX,  XX,  XX,  XX,  XX,  XX], # 12  chest
  [WX,  WD,  WL,  KK,  BR,  LD,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  LH,  SL,  SL,  LH,  SL,  SL,  SL,  LD,  BR,  KK,  WL,  WD,  WX,  XX,  XX,  XX,  XX,  XX,  XX], # 13
  [WX,  WD,  SK,  SK,  LD,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  LD,  SK,  SK,  WL,  WD,  WX,  XX,  XX,  XX,  XX,  XX,  XX], # 14  arm
  [WX,  WD,  SK,  SD,  KK,  LD,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  LD,  KK,  SD,  SK,  WL,  WD,  WX,  XX,  XX,  XX,  XX,  XX,  XX], # 15
  [XX,  WX,  WD,  KK,  BD,  BR,  LD,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  LD,  BR,  BD,  KK,  WL,  WD,  WX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 16  belt+bow curve
  [XX,  XX,  WX,  KK,  GD,  GH,  GX,  GD,  GH,  GX,  GD,  GH,  GX,  GD,  GH,  GH,  GD,  GX,  GD,  GH,  GX,  KK,  WD,  WX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 17  belt gold
  [XX,  XX,  XX,  KK,  SL,  LH,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  LH,  SL,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 18  upper leg
  [XX,  XX,  XX,  KK,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 19
  [XX,  XX,  XX,  KK,  LD,  SL,  SL,  SL,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  SL,  SL,  LD,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 20  crotch
  [XX,  XX,  XX,  XX,  KK,  SL,  LH,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  LH,  SL,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 21
  [XX,  XX,  XX,  XX,  KK,  SL,  LH,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  LH,  SL,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 22
  [XX,  XX,  XX,  XX,  KK,  LD,  SL,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  SL,  LD,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 23
  [XX,  XX,  XX,  XX,  KK,  WH,  WH,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  WH,  WH,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 24  feet
  [XX,  XX,  XX,  KK,  WH,  WH,  WH,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  WH,  WH,  WH,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 25
  [XX,  XX,  XX,  KK,  WX,  WH,  WX,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  WX,  WH,  WX,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 26  sole
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 27
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 28
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 29
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 30
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 31
]

def va_attack(step):
    g = copy_grid(VA)
    # Arrow draw: shaft extends from center-left, tip moves right, then flies
    if step == 0:
        # Arrow notched, slight draw
        for x in range(4, 10): g[13][x] = S0
        g[13][10] = S2
    elif step == 1:
        for x in range(2, 12): g[13][x] = S0
        g[13][12] = S2
    elif step == 2:
        # Full draw – arm tension
        for x in range(1, 14): g[13][x] = S0
        g[13][14] = S2
    elif step == 3:
        # Release – arrow mid-flight
        for x in range(16, 25): g[13][x] = S2
        for x in range(14, 16): g[13][x] = S0
    elif step == 4:
        for x in range(22, 30): g[13][x] = S2
    elif step == 5:
        for x in range(27, 32): g[13][x] = S2
    return g

def va_walk(step):
    g = copy_grid(VA)
    if step % 2 == 0:
        for y in range(26, 20, -1):
            for x in range(16, 20):
                if g[y][x] != XX and y-2 >= 0:
                    g[y-2][x] = g[y][x]
                    g[y][x] = XX
    else:
        for y in range(26, 20, -1):
            for x in range(4, 8):
                if g[y][x] != XX and y-2 >= 0:
                    g[y-2][x] = g[y][x]
                    g[y][x] = XX
    return g

def va_hurt():
    g = copy_grid(VA)
    for y in range(5, 9):
        for x in range(10, 19):
            if g[y][x] not in (XX, KK):
                g[y][x] = CD
    for (bx, by) in [(9, 14), (8, 16), (11, 17)]:
        g[by][bx] = RD
    return g

va_idle   = [grid_to_img(VA)] * 2
def va_idle1():
    g = copy_grid(VA)
    g[0][14] = FL; g[0][15] = FT  # feather sway
    return g
va_idle = [grid_to_img(VA), grid_to_img(va_idle1()), grid_to_img(VA), grid_to_img(va_idle1())]

va_walk_frames   = [grid_to_img(va_walk(i)) for i in range(6)]
va_attack_frames = [grid_to_img(va_attack(i)) for i in range(6)]
va_hurt_frames   = [grid_to_img(va_hurt()), grid_to_img(va_hurt())]

# ---------------------------------------------------------------------------
#  MARATHA WARRIOR – crimson shield, spear, orange war paint, turban
# ---------------------------------------------------------------------------
MW = [
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  S2,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  0  spear tip
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  S2,  S0,  KK,  XX,  XX,  XX,  XX,  XX,  XX], #  1  blade
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  S0,  S2,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  2
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  WL,  WD,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  3  spear shaft
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  WL,  WD,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  4
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  BR,  BR,  BR,  BR,  BR,  XX,  WL,  WD,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  5  turban
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  BR,  BH,  BH,  BH,  BH,  BR,  WL,  WD,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  6
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  SK,  SK,  SK,  SK,  KK,  WL,  WD,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  7  face
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  SK,  ED,  EY,  EY,  KK,  WL,  WD,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  8  eyes
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  OR,  SK,  SK,  OR,  KK,  WL,  WD,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], #  9  warpaint
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  SD,  SK,  SK,  SD,  KK,  XX,  WD,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 10  jaw
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  BR,  SL,  LH,  SL,  SL,  LH,  SL,  BR,  KK,  WD,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 11  gorget
  [XX,  XX,  XX,  XX,  XX,  BD,  KK,  BR,  BR,  LD,  SL,  LH,  SL,  SL,  SL,  SL,  LH,  SL,  LD,  BR,  KK,  WD,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 12  pauldrons
  [XX,  XX,  XX,  CR,  CD,  CR,  SK,  SK,  LD,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  LD,  SK,  SK,  WD,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 13  shield edge+chest
  [XX,  XX,  CR,  CH,  CD,  CR,  SK,  SH,  LD,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  LD,  SK,  SH,  WD,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 14  shield
  [XX,  CR,  CH,  GD,  CD,  CR,  SK,  SD,  KK,  LD,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  LD,  KK,  SD,  SK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 15  shield gold
  [XX,  CR,  CH,  GD,  CD,  KK,  SD,  KK,  BD,  BR,  LD,  SL,  SL,  SL,  SL,  SL,  LD,  BR,  BD,  KK,  SD,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 16  belt
  [XX,  CR,  CD,  KK,  XX,  XX,  KK,  GD,  GH,  GX,  GD,  GH,  GX,  GD,  GX,  GD,  GH,  GX,  GD,  GH,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 17  belt gold
  [XX,  KK,  XX,  XX,  XX,  XX,  KK,  SL,  LH,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  LH,  SL,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 18
  [XX,  XX,  XX,  XX,  XX,  XX,  KK,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  SL,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 19
  [XX,  XX,  XX,  XX,  XX,  XX,  KK,  LD,  SL,  SL,  XX,  XX,  XX,  XX,  XX,  XX,  SL,  LD,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 20  crotch
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  SL,  LH,  XX,  XX,  XX,  XX,  XX,  XX,  LH,  SL,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 21
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  SL,  LH,  XX,  XX,  XX,  XX,  XX,  XX,  LH,  SL,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 22
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  LD,  SL,  XX,  XX,  XX,  XX,  XX,  XX,  SL,  LD,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 23
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  KK,  WH,  WH,  XX,  XX,  XX,  XX,  XX,  XX,  WH,  WH,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 24  feet
  [XX,  XX,  XX,  XX,  XX,  XX,  KK,  WH,  WH,  WH,  XX,  XX,  XX,  XX,  XX,  XX,  WH,  WH,  WH,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 25
  [XX,  XX,  XX,  XX,  XX,  XX,  KK,  WX,  WH,  WX,  KK,  XX,  XX,  XX,  XX,  KK,  WX,  WH,  WX,  KK,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 26  sole
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 27
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 28
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 29
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 30
  [XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX,  XX], # 31
]

def mw_attack(step):
    g = copy_grid(MW)
    # Clear existing spear
    for y in range(0, 14):
        for x in range(18, 32):
            g[y][x] = XX
    # Thrust animations: spear extends horizontally to the right
    thrust_x = 18 + step * 2
    for x in range(thrust_x, min(31, thrust_x + 8)):
        g[12][x] = WD
        if x < 31: g[12][x+1] = WL
    # Spear tip
    tip = thrust_x + 8
    if tip < 31:
        g[11][tip] = S2
        g[12][tip] = S0
    return g

def mw_walk(step):
    g = copy_grid(MW)
    if step % 2 == 0:
        for y in range(25, 19, -1):
            for x in range(15, 20):
                if g[y][x] != XX and y-2 >= 0:
                    g[y-2][x] = g[y][x]
                    g[y][x] = XX
    else:
        for y in range(25, 19, -1):
            for x in range(7, 11):
                if g[y][x] != XX and y-2 >= 0:
                    g[y-2][x] = g[y][x]
                    g[y][x] = XX
    return g

def mw_hurt():
    g = copy_grid(MW)
    for y in range(7, 11):
        for x in range(12, 18):
            if g[y][x] not in (XX, KK):
                g[y][x] = CD
    for (bx, by) in [(6, 14), (5, 16), (8, 17), (7, 13)]:
        g[by][bx] = RD
    return g

def mw_idle(step):
    g = copy_grid(MW)
    if step % 2 == 1:
        # Spear bob 1px down
        for y in range(26, 0, -1):
            for x in range(18, 26):
                if MW[y-1][x] in (WD, WL, WX, S0, S2):
                    g[y][x] = MW[y-1][x]
                    g[y-1][x] = XX
    return g

mw_idle_frames   = [grid_to_img(mw_idle(i)) for i in range(4)]
mw_walk_frames   = [grid_to_img(mw_walk(i)) for i in range(6)]
mw_attack_frames = [grid_to_img(mw_attack(i)) for i in range(6)]
mw_hurt_frames   = [grid_to_img(mw_hurt()), grid_to_img(mw_hurt())]

# ---------------------------------------------------------------------------
#  Compose the final sprite sheet
#  Layout: 3 blocks stacked vertically, each block = 4 rows (idle/walk/attack/hurt)
#  Each row is 6 frames wide → sheet = 192 x 384 px
# ---------------------------------------------------------------------------
COLS = 6
ANIM_ROWS = 4   # per archetype
NUM_CHARS = 3

SHEET_W = FW * COLS
SHEET_H = FH * ANIM_ROWS * NUM_CHARS  # 32*4*3 = 384

sheet = Image.new('RGBA', (SHEET_W, SHEET_H), (0, 0, 0, 0))

chars = [
    (mg_idle,         mg_walk_frames,   mg_attack_frames, mg_hurt_frames),
    (va_idle,         va_walk_frames,   va_attack_frames, va_hurt_frames),
    (mw_idle_frames,  mw_walk_frames,   mw_attack_frames, mw_hurt_frames),
]

for ci, (idle_f, walk_f, attack_f, hurt_f) in enumerate(chars):
    base_row = ci * ANIM_ROWS
    for ai, frames in enumerate([idle_f, walk_f, attack_f, hurt_f]):
        row = base_row + ai
        for fi, frame in enumerate(frames[:COLS]):
            sheet.paste(frame, (fi * FW, row * FH))

out_path = r"C:\Users\ASUS\Documents\Field Project\Heritage Quest\Heritage Quest\enemy_sprite_sheet_v3.png"
sheet.save(out_path)
print(f"Saved {SHEET_W}x{SHEET_H}px sprite sheet → {out_path}")
