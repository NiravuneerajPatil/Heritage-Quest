"""
Heritage Quest - Collectible Artifacts & Power-Ups Generator
Generates pixel-perfect 32x32 animated Indian historical artifacts and clothing power-ups:
1. Koh-i-Noor Diamond (Radiant Gem)
2. Bronze Nataraja Idol (Cosmic Fire Ring)
3. Ashoka Lion Capital Crest (Golden Dharma Wheel)
4. Shivrai Gold Coin (3D Spin)
5. Ancient Palm-Leaf Manuscript (Floating Runes)
6. Saffron Pagri / Turban (Vitality Power-Up)
7. Zari Angavastram Silk Drape (Agility & Double Jump Power-Up)
8. Mavala Steel Vambrace (Attack Power-Up)
"""

import os
import math
import zlib
import struct

WIDTH = 32
HEIGHT = 32

PALETTE = {
    'trans':        (0, 0, 0, 0),
    'outline':      (24, 20, 18, 255),
    
    # Diamond / Koh-i-Noor
    'dia_white':    (255, 255, 255, 255),
    'dia_hi':       (224, 242, 254, 255),
    'dia_cyan':     (125, 211, 252, 255),
    'dia_mid':      (56, 189, 248, 255),
    'dia_deep':     (2, 132, 199, 255),
    'dia_glow':     (14, 165, 233, 160),
    
    # Gold & Bronze
    'gold_white':   (255, 255, 255, 255),
    'gold_hi':      (254, 240, 138, 255),
    'gold_lit':     (250, 204, 21, 255),
    'gold_mid':     (234, 179, 8, 255),
    'gold_sh':      (180, 83, 9, 255),
    'gold_dk':      (120, 53, 15, 255),
    
    # Bronze / Copper
    'bronze_hi':    (253, 186, 116, 255),
    'bronze_mid':   (217, 119, 6, 255),
    'bronze_sh':    (146, 64, 14, 255),
    'bronze_dk':    (92, 42, 17, 255),
    
    # Fire & Energy
    'fire_white':   (255, 255, 255, 255),
    'fire_yellow':  (254, 240, 138, 255),
    'fire_orange':  (249, 115, 22, 255),
    'fire_red':     (220, 38, 38, 255),
    'fire_glow':    (239, 68, 68, 140),
    
    # Silk & Turban Fabrics
    'saffron_hi':   (254, 215, 170, 255),
    'saffron_lit':  (251, 146, 60, 255),
    'saffron_mid':  (234, 88, 12, 255),
    'saffron_sh':   (194, 65, 12, 255),
    'saffron_dk':   (124, 45, 18, 255),
    
    'ruby_hi':      (248, 113, 113, 255),
    'ruby_mid':     (220, 38, 38, 255),
    'ruby_sh':      (153, 27, 27, 255),
    'ruby_dk':      (88, 28, 28, 255),
    
    # Steel
    'steel_hi':     (255, 255, 255, 255),
    'steel_lit':    (226, 232, 240, 255),
    'steel_mid':    (148, 163, 184, 255),
    'steel_sh':     (71, 85, 105, 255),
    'steel_dk':     (30, 41, 59, 255),
    
    # Palm-leaf Manuscript
    'leaf_hi':      (254, 243, 199, 255),
    'leaf_mid':     (245, 208, 111, 255),
    'leaf_sh':      (217, 119, 6, 255),
    'leaf_dk':      (146, 64, 14, 255),
    'ink':          (67, 56, 40, 255),
}


class Frame:
    def __init__(self, w=32, h=32):
        self.w = w
        self.h = h
        self.data = [[PALETTE['trans'] for _ in range(w)] for _ in range(h)]

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            if isinstance(color, str):
                color = PALETTE[color]
            self.data[y][x] = color

    def blend(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            if isinstance(color, str):
                color = PALETTE[color]
            sr, sg, sb, sa = color
            if sa == 0: return
            if sa == 255:
                self.data[y][x] = color
                return
            dr, dg, db, da = self.data[y][x]
            alpha = sa / 255.0
            inv = 1.0 - alpha
            nr = int(sr * alpha + dr * inv)
            ng = int(sg * alpha + dg * inv)
            nb = int(sb * alpha + db * inv)
            na = min(255, int(sa + da * inv))
            self.data[y][x] = (nr, ng, nb, na)

    def add_outline(self, outline_color='outline'):
        col = PALETTE[outline_color]
        orig = [row[:] for row in self.data]
        for y in range(self.h):
            for x in range(self.w):
                if orig[y][x][3] == 0:
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.w and 0 <= ny < self.h:
                            if orig[ny][nx][3] > 100:
                                self.data[y][x] = col
                                break

    def to_png_bytes(self):
        def chunk(chunk_type, data):
            return struct.pack('>I', len(data)) + chunk_type + data + struct.pack('>I', zlib.crc32(chunk_type + data) & 0xffffffff)

        raw = bytearray()
        for y in range(self.h):
            raw.append(0)
            for x in range(self.w):
                r, g, b, a = self.data[y][x]
                raw.extend((r, g, b, a))

        compressed = zlib.compress(bytes(raw), 9)
        ihdr = struct.pack('>IIBBBBB', self.w, self.h, 8, 6, 0, 0, 0)
        return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', compressed) + chunk(b'IEND', b'')


def save_sheet(frames, path):
    n = len(frames)
    sw = WIDTH * n
    sh = HEIGHT
    sheet = Frame(sw, sh)
    for i, f in enumerate(frames):
        ox = i * WIDTH
        for y in range(HEIGHT):
            for x in range(WIDTH):
                sheet.set(ox + x, y, f.data[y][x])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as fp:
        fp.write(sheet.to_png_bytes())
    print(f"Saved: {path} ({sw}x{sh})")


# =========================================================================
# 1. KOH-I-NOOR DIAMOND (4 Frames: Floating & Sparkling Corona)
# =========================================================================
def generate_kohinoor():
    frames = []
    # Subtle bobbing and sparkling light rays
    bobs = [0, -1, -2, -1]
    sparkles = [
        [(7, 9), (24, 20)],
        [(16, 6), (9, 23)],
        [(24, 10), (15, 25)],
        [(8, 15), (23, 7)]
    ]

    for i in range(4):
        f = Frame()
        by = bobs[i]
        cy = 16 + by
        cx = 16

        # Outer diamond glow aura
        for y in range(cy - 7, cy + 9):
            for x in range(cx - 7, cx + 8):
                dist = math.hypot(x - cx, y - cy)
                if dist < 8.5:
                    f.blend(x, y, (125, 211, 252, int(max(0, 140 - dist * 16))))

        # Brilliant cut diamond geometry
        # Table (flat top): cy-5 to cy-3
        for x in range(cx - 4, cx + 5): f.set(x, cy - 5, 'dia_white')
        for x in range(cx - 5, cx + 6): f.set(x, cy - 4, 'dia_hi')
        for x in range(cx - 6, cx + 7): f.set(x, cy - 3, 'dia_cyan')
        # Girdle (widest part): cy-2 to cy
        for x in range(cx - 7, cx + 8): f.set(x, cy - 2, 'dia_hi')
        for x in range(cx - 7, cx + 8): f.set(x, cy - 1, 'dia_white')
        for x in range(cx - 7, cx + 8): f.set(x, cy, 'dia_cyan')
        # Pavilion (tapering to point at bottom): cy+1 to cy+6
        for x in range(cx - 6, cx + 7): f.set(x, cy + 1, 'dia_mid')
        for x in range(cx - 5, cx + 6): f.set(x, cy + 2, 'dia_deep')
        for x in range(cx - 4, cx + 5): f.set(x, cy + 3, 'dia_mid')
        for x in range(cx - 3, cx + 4): f.set(x, cy + 4, 'dia_deep')
        for x in range(cx - 2, cx + 3): f.set(x, cy + 5, 'dia_mid')
        f.set(cx, cy + 6, 'dia_white')

        # Facet glints
        f.set(cx - 2, cy - 4, 'dia_white')
        f.set(cx + 2, cy - 4, 'dia_white')
        f.set(cx - 3, cy, 'dia_white')
        f.set(cx, cy - 1, 'dia_white')
        f.set(cx + 3, cy, 'dia_white')
        f.set(cx, cy + 3, 'dia_white')

        # Sparkling star motes
        for sx, sy in sparkles[i]:
            f.blend(sx, sy, 'dia_white')
            f.blend(sx - 1, sy, 'dia_hi')
            f.blend(sx + 1, sy, 'dia_hi')
            f.blend(sx, sy - 1, 'dia_hi')
            f.blend(sx, sy + 1, 'dia_hi')

        f.add_outline()
        frames.append(f)
    return frames


# =========================================================================
# 2. BRONZE NATARAJA IDOL (4 Frames: Ring of Cosmic Fire Animated)
# =========================================================================
def generate_nataraja():
    frames = []
    bobs = [0, -1, -2, -1]

    for i in range(4):
        f = Frame()
        by = bobs[i]
        cy = 16 + by
        cx = 16

        # Circular ring of cosmic fire (Prabhamandala)
        flame_shift = (i * 2)
        for angle_deg in range(0, 360, 10):
            rad = math.radians(angle_deg)
            r = 11.0 + 0.8 * math.sin(rad * 8 + flame_shift)
            px = int(cx + r * math.cos(rad))
            py = int(cy + r * math.sin(rad))
            f.set(px, py, 'fire_orange')
            # Flame tips
            if angle_deg % 30 == 0:
                f.blend(px + int(math.cos(rad)), py + int(math.sin(rad)), 'fire_yellow')

        # Inner ring structure
        for angle_deg in range(0, 360, 6):
            rad = math.radians(angle_deg)
            px = int(cx + 9.5 * math.cos(rad))
            py = int(cy + 9.5 * math.sin(rad))
            f.set(px, py, 'bronze_mid')

        # Double lotus pedestal at base (Peedam)
        for x in range(cx - 6, cx + 7): f.set(x, cy + 9, 'bronze_dk')
        for x in range(cx - 5, cx + 6): f.set(x, cy + 8, 'bronze_mid')
        for x in range(cx - 4, cx + 5): f.set(x, cy + 7, 'bronze_hi')

        # Nataraja Dancing Figure (Ananda Tandava)
        # Head with Jatamukuta crown & flowing locks
        f.set(cx, cy - 6, 'gold_hi') # Crown
        f.set(cx, cy - 5, 'bronze_hi') # Head
        f.set(cx - 1, cy - 5, 'bronze_mid')
        # Flowing dreadlocks (Ganga)
        f.set(cx - 3, cy - 4, 'bronze_hi')
        f.set(cx + 3, cy - 4, 'bronze_hi')

        # Torso & Waist
        f.set(cx, cy - 4, 'bronze_mid')
        f.set(cx, cy - 3, 'bronze_hi')
        f.set(cx, cy - 2, 'bronze_mid')
        f.set(cx, cy - 1, 'bronze_dk')

        # Four Arms
        # Upper Right: Damaru (drum)
        f.set(cx + 2, cy - 4, 'bronze_mid')
        f.set(cx + 4, cy - 5, 'gold_lit')
        f.set(cx + 5, cy - 5, 'gold_hi') # Damaru drum!

        # Upper Left: Agni (Flame of destruction)
        f.set(cx - 2, cy - 4, 'bronze_mid')
        f.set(cx - 4, cy - 5, 'fire_orange')
        f.set(cx - 5, cy - 6, 'fire_yellow') # Fire in palm!

        # Lower Right: Abhaya Mudra (Blessing gesture)
        f.set(cx + 2, cy - 2, 'bronze_hi')
        f.set(cx + 3, cy - 1, 'gold_hi')

        # Lower Left: Gajahasta (Pointing down across chest to lifted foot)
        f.set(cx - 1, cy - 2, 'bronze_hi')
        f.set(cx - 2, cy - 1, 'bronze_mid')
        f.set(cx - 3, cy, 'bronze_hi')

        # Standing Right Leg (bent on dwarf demon Muyalaka)
        f.set(cx, cy, 'bronze_mid')
        f.set(cx + 1, cy + 1, 'bronze_mid')
        f.set(cx + 1, cy + 2, 'bronze_hi')
        f.set(cx + 1, cy + 3, 'bronze_mid')
        f.set(cx + 1, cy + 4, 'bronze_dk')
        # Crushed ignorance demon
        for x in range(cx - 2, cx + 4): f.set(x, cy + 5, 'bronze_dk')

        # Lifted Graceful Left Leg (kicked across to the right)
        f.set(cx - 1, cy, 'bronze_hi')
        f.set(cx - 2, cy + 1, 'bronze_hi')
        f.set(cx - 1, cy + 2, 'gold_hi')
        f.set(cx + 1, cy + 2, 'gold_hi')

        f.add_outline()
        frames.append(f)
    return frames


# =========================================================================
# 3. ASHOKA LION CAPITAL SEAL (4 Frames: Spinning Golden Dharma Chakra)
# =========================================================================
def generate_ashoka_seal():
    frames = []
    bobs = [0, -1, -2, -1]

    for i in range(4):
        f = Frame()
        by = bobs[i]
        cy = 16 + by
        cx = 16

        # Holy golden radiance background aura
        for y in range(cy - 8, cy + 9):
            for x in range(cx - 8, cx + 9):
                dist = math.hypot(x - cx, y - cy)
                if dist < 9:
                    f.blend(x, y, (250, 204, 21, int(max(0, 120 - dist * 13))))

        # Three visible majestic Lions at top (facing Left, Forward, Right)
        # Forward Lion
        f.set(cx, cy - 7, 'gold_hi') # Mane crest
        f.set(cx - 1, cy - 6, 'gold_lit')
        f.set(cx, cy - 6, 'gold_white')
        f.set(cx + 1, cy - 6, 'gold_lit')
        f.set(cx, cy - 5, 'gold_mid') # Face/muzzle
        f.set(cx, cy - 4, 'gold_sh')

        # Left Lion head profile
        f.set(cx - 3, cy - 6, 'gold_hi')
        f.set(cx - 4, cy - 5, 'gold_lit')
        f.set(cx - 3, cy - 5, 'gold_mid')
        f.set(cx - 2, cy - 4, 'gold_sh')

        # Right Lion head profile
        f.set(cx + 3, cy - 6, 'gold_hi')
        f.set(cx + 4, cy - 5, 'gold_lit')
        f.set(cx + 3, cy - 5, 'gold_mid')
        f.set(cx + 2, cy - 4, 'gold_sh')

        # Abacus platform with sacred animals relief
        for x in range(cx - 6, cx + 7): f.set(x, cy - 3, 'gold_hi')
        for x in range(cx - 6, cx + 7): f.set(x, cy - 2, 'gold_mid')

        # Central 24-Spoke Ashoka Dharma Chakra (rotating spokes)
        rot_offset = i * (math.pi / 4.0)
        for angle in [0, math.pi/4, math.pi/2, 3*math.pi/4]:
            cur_a = angle + rot_offset
            for r in range(1, 5):
                rx = int(cx + r * math.cos(cur_a))
                ry = int(cy + 2 + r * math.sin(cur_a))
                f.set(rx, ry, 'dia_deep')
        # Rim of Wheel
        for angle_deg in range(0, 360, 15):
            rad = math.radians(angle_deg)
            px = int(cx + 4.5 * math.cos(rad))
            py = int(cy + 2 + 4.5 * math.sin(rad))
            f.set(px, py, 'dia_cyan')
        # Center hub of wheel
        f.set(cx, cy + 2, 'gold_white')

        # Inverted Bell / Lotus Base at bottom
        for x in range(cx - 5, cx + 6): f.set(x, cy + 7, 'gold_mid')
        for x in range(cx - 6, cx + 7): f.set(x, cy + 8, 'gold_lit')
        for x in range(cx - 4, cx + 5): f.set(x, cy + 9, 'gold_sh')

        f.add_outline()
        frames.append(f)
    return frames


# =========================================================================
# 4. SHIVRAI GOLD COIN (6 Frames: 3D Spin with Devanagari Relief)
# =========================================================================
def generate_shivrai_coin():
    frames = []
    # 6 frames of smooth 3D rotation: angle from 0 to 180 degrees
    # Scale width horizontally by cos(angle)
    angles = [0, math.pi / 6, 2 * math.pi / 6, math.pi / 2, 4 * math.pi / 6, 5 * math.pi / 6]

    for i, a in enumerate(angles):
        f = Frame()
        cy = 16
        cx = 16
        cos_val = math.cos(a)
        w_factor = abs(cos_val)
        r_vert = 10.0
        r_horiz = max(1.5, 10.0 * w_factor)

        # Draw rotated ellipse coin face
        for y in range(cy - 11, cy + 12):
            dy = (y - cy) / r_vert
            if abs(dy) <= 1.0:
                max_dx = r_horiz * math.sqrt(1.0 - dy * dy)
                min_x = int(cx - max_dx)
                max_x = int(cx + max_dx)
                for x in range(min_x, max_x + 1):
                    # Shading based on coin curvature
                    nx = (x - cx) / max(0.1, max_dx) if max_dx > 0 else 0
                    if nx < -0.4:
                        f.set(x, y, 'gold_lit')
                    elif nx < 0.3:
                        f.set(x, y, 'gold_mid')
                    else:
                        f.set(x, y, 'gold_sh')

        # Coin rim edge thickness when rotated
        if w_factor < 0.95:
            rim_dir = 1 if cos_val >= 0 else -1
            for y in range(cy - 9, cy + 10):
                dy = (y - cy) / r_vert
                if abs(dy) <= 1.0:
                    edge_x = int(cx + rim_dir * (r_horiz * math.sqrt(1.0 - dy * dy) + 1))
                    f.set(edge_x, y, 'gold_dk')

        # Devanagari Inscription relief ("श्री राजा शिवछत्रपती")
        if w_factor > 0.5:
            # Top line: "श्री"
            tx = int(cx - 3 * w_factor)
            for x in range(tx, int(cx + 4 * w_factor)):
                f.set(x, cy - 4, 'gold_white')
            # Middle line: "राजा"
            tx = int(cx - 4 * w_factor)
            for x in range(tx, int(cx + 5 * w_factor)):
                f.set(x, cy, 'gold_white')
            # Bottom line: "शिव"
            tx = int(cx - 3 * w_factor)
            for x in range(tx, int(cx + 4 * w_factor)):
                f.set(x, cy + 4, 'gold_white')

        # Edge shine gleam
        if i == 0 or i == 3:
            f.blend(cx - int(r_horiz * 0.7), cy - 6, 'gold_white')
            f.blend(cx + int(r_horiz * 0.5), cy + 5, 'gold_white')

        f.add_outline()
        frames.append(f)
    return frames


# =========================================================================
# 5. ANCIENT PALM-LEAF MANUSCRIPT (TALAPATRA) (4 Frames: Floating Runes)
# =========================================================================
def generate_manuscript():
    frames = []
    bobs = [0, -1, -2, -1]
    rune_y = [0, -2, -4, -6]

    for i in range(4):
        f = Frame()
        by = bobs[i]
        cy = 17 + by
        cx = 16

        # Holy golden manuscript aura
        for y in range(cy - 7, cy + 8):
            for x in range(cx - 10, cx + 11):
                dist = math.hypot(x - cx, y - cy)
                if dist < 10:
                    f.blend(x, y, (250, 204, 21, int(max(0, 80 - dist * 8))))

        # Three stacked palm leaves
        # Bottom leaf
        for x in range(cx - 10, cx + 11):
            f.set(x, cy + 3, 'leaf_dk')
        # Middle leaf
        for x in range(cx - 11, cx + 12):
            f.set(x, cy + 1, 'leaf_sh')
            f.set(x, cy + 2, 'leaf_mid')
        # Top active leaf
        for x in range(cx - 11, cx + 12):
            f.set(x, cy - 2, 'leaf_hi')
            f.set(x, cy - 1, 'leaf_mid')
            f.set(x, cy, 'leaf_sh')

        # Ancient Sanskrit / Devanagari script etched in lampblack ink
        for x in range(cx - 9, cx + 10, 2):
            f.set(x, cy - 1, 'ink')
            f.set(x, cy + 1, 'ink')

        # Sacred red silk binding cord tied around the center with wooden end slats
        for y in range(cy - 3, cy + 5):
            f.set(cx, y, 'ruby_mid')
            f.set(cx - 1, y, 'ruby_sh')
        # Center knot & trailing tassels
        f.set(cx + 1, cy + 4, 'ruby_mid')
        f.set(cx + 2, cy + 5, 'ruby_hi')

        # Wooden end covers (Kambadika)
        for y in range(cy - 3, cy + 4):
            f.set(cx - 11, y, 'bronze_dk')
            f.set(cx + 11, y, 'bronze_dk')

        # Floating golden Sanskrit knowledge glyphs rising into the air
        ry = (cy - 6 + rune_y[i]) % 32
        if 2 <= ry <= cy - 4:
            f.blend(cx - 4, ry, 'gold_white')
            f.blend(cx - 3, ry, 'gold_lit')
            f.blend(cx - 4, ry + 1, 'gold_lit')
        ry2 = (cy - 5 + rune_y[(i + 2) % 4]) % 32
        if 2 <= ry2 <= cy - 4:
            f.blend(cx + 5, ry2, 'gold_white')
            f.blend(cx + 6, ry2, 'gold_lit')

        f.add_outline()
        frames.append(f)
    return frames


# =========================================================================
# 6. SAFFRON PAGRI / TURBAN (Vitality Power-Up) (4 Frames: Glow Pulse)
# =========================================================================
def generate_turban():
    frames = []
    bobs = [0, -1, -2, -1]

    for i in range(4):
        f = Frame()
        by = bobs[i]
        cy = 16 + by
        cx = 16

        # Vitality pulse aura (heart-like golden warmth)
        pulse = 1.0 + 0.2 * math.sin(i * math.pi / 2.0)
        for y in range(cy - 9, cy + 9):
            for x in range(cx - 10, cx + 11):
                dist = math.hypot(x - cx, y - cy)
                if dist < 9.0 * pulse:
                    f.blend(x, y, (249, 115, 22, int(max(0, 100 - dist * 10))))

        # Base Turban folds (elaborate Maratha / Rajput royal wrap)
        # Lower folds (forehead wrap)
        for x in range(cx - 7, cx + 8): f.set(x, cy + 4, 'saffron_dk')
        for x in range(cx - 8, cx + 9): f.set(x, cy + 3, 'saffron_sh')
        for x in range(cx - 8, cx + 9): f.set(x, cy + 2, 'saffron_mid')
        for x in range(cx - 8, cx + 9): f.set(x, cy + 1, 'saffron_lit')

        # Middle diagonal interlocking wrap folds
        for x in range(cx - 7, cx + 8): f.set(x, cy, 'saffron_mid')
        for x in range(cx - 7, cx + 8): f.set(x, cy - 1, 'saffron_lit')
        for x in range(cx - 6, cx + 7): f.set(x, cy - 2, 'saffron_hi')

        # Crown of turban (crest dome)
        for x in range(cx - 5, cx + 6): f.set(x, cy - 3, 'saffron_lit')
        for x in range(cx - 4, cx + 5): f.set(x, cy - 4, 'saffron_mid')

        # Royal Sarpech / Kalgi (gem-studded golden plume brooch at front)
        f.set(cx - 1, cy - 1, 'gold_white')
        f.set(cx - 1, cy, 'ruby_mid') # Ruby gem center!
        f.set(cx - 1, cy + 1, 'gold_hi')

        # Peacock feather / plume crest rising above
        f.set(cx - 1, cy - 5, 'dia_deep')
        f.set(cx - 1, cy - 6, 'dia_mid')
        f.set(cx, cy - 6, 'gold_hi')
        f.set(cx - 1, cy - 7, 'dia_cyan')
        f.set(cx, cy - 7, 'gold_white')

        # Trailing tail of turban (Shamla / Turra) cascading gracefully
        for y in range(cy + 4, cy + 8):
            f.set(cx + 7, y, 'saffron_mid')
            f.set(cx + 8, y, 'saffron_lit')
        # Gold embroidered border on tail
        f.set(cx + 7, cy + 8, 'gold_hi')
        f.set(cx + 8, cy + 8, 'gold_hi')

        f.add_outline()
        frames.append(f)
    return frames


# =========================================================================
# 7. ZARI ANGAVASTRAM (Agility / Double Jump) (4 Frames: Floating Silk)
# =========================================================================
def generate_angavastram():
    frames = []
    # Ethereal floating S-curve cloth wave
    for i in range(4):
        f = Frame()
        phase = i * (math.pi / 2.0)
        cy = 16
        cx = 16

        # Wind / agility sparkles
        for y in range(6, 26):
            for x in range(5, 27):
                dist = math.hypot(x - cx, y - cy)
                if dist < 10:
                    f.blend(x, y, (234, 179, 8, int(max(0, 60 - dist * 6))))

        # Sine wave cloth ribbon spanning across frame
        for x in range(cx - 9, cx + 10):
            nx = (x - cx) / 8.0
            # Flowing cloth wave height
            wave_y = int(cy + 3.5 * math.sin(nx * 3.0 + phase))
            # Ribbon thickness of 4 pixels
            f.set(x, wave_y - 2, 'ruby_hi')
            f.set(x, wave_y - 1, 'ruby_mid')
            f.set(x, wave_y, 'ruby_sh')
            f.set(x, wave_y + 1, 'ruby_dk')

            # Pure gold Zari brocade border on both edges
            f.set(x, wave_y - 2, 'gold_white')
            f.set(x, wave_y + 1, 'gold_hi')

            # Traditional Indian paisley / Buta motif dot along center
            if x % 4 == 0:
                f.set(x, wave_y - 1, 'gold_white')

        # Dangling golden tassels on the silk cloth ends
        left_y = int(cy + 3.5 * math.sin((-9.0/8.0) * 3.0 + phase))
        right_y = int(cy + 3.5 * math.sin((9.0/8.0) * 3.0 + phase))
        for dy in range(1, 4):
            f.set(cx - 10, left_y + dy, 'gold_lit')
            f.set(cx + 10, right_y + dy, 'gold_lit')

        f.add_outline()
        frames.append(f)
    return frames


# =========================================================================
# 8. MAVALA STEEL VAMBRACE (Attack Power-Up) (4 Frames: Fiery Gleam)
# =========================================================================
def generate_vambrace():
    frames = []
    bobs = [0, -1, -2, -1]
    gleams = [0, 1, 2, 1]

    for i in range(4):
        f = Frame()
        by = bobs[i]
        cy = 16 + by
        cx = 16
        g = gleams[i]

        # Warrior strength red/gold aura
        for y in range(cy - 8, cy + 9):
            for x in range(cx - 8, cx + 9):
                dist = math.hypot(x - cx, y - cy)
                if dist < 9:
                    f.blend(x, y, (220, 38, 38, int(max(0, 90 - dist * 10))))

        # Curved Wootz Damascus Steel Arm-guard (Vambrace / Dastana)
        for y in range(cy - 6, cy + 7):
            w = 5 if abs(y - cy) < 4 else 4
            for x in range(cx - w, cx + w + 1):
                f.set(x, y, 'steel_mid')
            # Light contour highlight
            f.set(cx - w + 1, y, 'steel_hi')
            f.set(cx - w, y, 'steel_lit')
            f.set(cx + w, y, 'steel_dk')

        # Damascus water-steel wavy pattern etching
        for y in range(cy - 5, cy + 6, 2):
            for x in range(cx - 2, cx + 3):
                f.set(x, y, 'steel_sh')

        # Brass/Gold studded reinforcement plates & rivets
        f.set(cx - 3, cy - 4, 'gold_hi')
        f.set(cx + 3, cy - 4, 'gold_hi')
        f.set(cx - 3, cy + 4, 'gold_hi')
        f.set(cx + 3, cy + 4, 'gold_hi')
        # Center royal warrior insignia
        f.set(cx, cy - 1, 'ruby_mid')
        f.set(cx, cy, 'ruby_hi')
        f.set(cx, cy + 1, 'ruby_mid')
        f.set(cx - 1, cy, 'gold_hi')
        f.set(cx + 1, cy, 'gold_hi')

        # Dynamic light gleam traveling across the steel blade-guard
        gx = cx - 3 + g * 3
        f.blend(gx, cy - 2, 'steel_hi')
        f.blend(gx, cy - 1, 'fire_white')
        f.blend(gx, cy, 'steel_hi')

        f.add_outline()
        frames.append(f)
    return frames


# =========================================================================
# BUILD ALL ARTIFACTS
# =========================================================================
def build_artifacts():
    out_dir = "assets/images/artifacts"
    os.makedirs(out_dir, exist_ok=True)

    items = {
        'artifact_kohinoor':    (generate_kohinoor(), "Koh-i-Noor Diamond", "Royal Gem & Radiant Light"),
        'artifact_nataraja':    (generate_nataraja(), "Bronze Nataraja", "Chola Bronze Divine Ward"),
        'artifact_ashoka_seal': (generate_ashoka_seal(), "Ashoka Lion Seal", "Maurya Golden Crest"),
        'artifact_shivrai_coin':(generate_shivrai_coin(), "Shivrai Gold Coin", "Maratha Royal Currency"),
        'artifact_manuscript':  (generate_manuscript(), "Palm-leaf Manuscript", "Ancient Martial Techniques"),
        'powerup_turban':       (generate_turban(), "Saffron Pagri", "Vitality & Max Health (+1 HP)"),
        'powerup_angavastram':  (generate_angavastram(), "Zari Angavastram", "Agility & Double Jump"),
        'powerup_vambrace':     (generate_vambrace(), "Mavala Vambrace", "Warrior Strength & High Damage"),
    }

    # Save individual animated strips
    for key, (frames, name, desc) in items.items():
        sheet_path = os.path.join(out_dir, f"{key}.png")
        save_sheet(frames, sheet_path)

    # Master sheet: 8 rows of items
    max_frames = 6
    master_w = max_frames * WIDTH
    master_h = len(items) * HEIGHT
    master_sheet = Frame(master_w, master_h)

    for row_idx, (key, (frames, _, _)) in enumerate(items.items()):
        oy = row_idx * HEIGHT
        for col_idx, f in enumerate(frames):
            ox = col_idx * WIDTH
            for y in range(HEIGHT):
                for x in range(WIDTH):
                    master_sheet.set(ox + x, oy + y, f.data[y][x])

    master_path = os.path.join(out_dir, "artifacts_master_sheet.png")
    with open(master_path, 'wb') as fp:
        fp.write(master_sheet.to_png_bytes())
    print(f"Saved Master Artifacts Sheet: {master_path} ({master_w}x{master_h})")

    # Generate Godot SpriteFrames resource for artifacts
    generate_artifacts_tres(items, out_dir)


def generate_artifacts_tres(items, out_dir):
    tres_path = os.path.join(out_dir, "artifacts_sprite_frames.tres")
    lines = []
    lines.append('[gd_resource type="SpriteFrames" load_steps=50 format=3]')
    lines.append('')

    ext_id = 1
    ext_map = {}
    for key in items.keys():
        lines.append(f'[ext_resource type="Texture2D" path="res://assets/images/artifacts/{key}.png" id="{ext_id}_{key}"]')
        ext_map[key] = f'{ext_id}_{key}'
        ext_id += 1
    lines.append('')

    atlas_map = {}
    for key, (frames, _, _) in items.items():
        atlas_map[key] = []
        tex_id = ext_map[key]
        for f_idx in range(len(frames)):
            sub_name = f"AtlasTexture_{key}_{f_idx}"
            lines.append(f'[sub_resource type="AtlasTexture" id="{sub_name}"]')
            lines.append(f'atlas = ExtResource("{tex_id}")')
            lines.append(f'region = Rect2({f_idx * 32}, 0, 32, 32)')
            lines.append('')
            atlas_map[key].append(sub_name)

    lines.append('[resource]')
    lines.append('animations = [{')

    blocks = []
    for key, (frames, _, _) in items.items():
        block = []
        block.append('"frames": [')
        f_entries = []
        for sub_name in atlas_map[key]:
            f_entries.append('{\n"duration": 1.0,\n"texture": SubResource("' + sub_name + '")\n}')
        block.append(', '.join(f_entries))
        block.append('],')
        block.append('"loop": true,')
        block.append(f'"name": &"{key}",')
        block.append('"speed": 5.0')
        blocks.append('{\n' + '\n'.join(block) + '\n}')

    lines.append(', '.join(blocks))
    lines.append('}]')

    with open(tres_path, 'w', encoding='utf-8') as fp:
        fp.write('\n'.join(lines))
    print(f"Generated Artifacts SpriteFrames: {tres_path}")


if __name__ == '__main__':
    print("Generating Indian Historical Artifacts & Clothing Power-Ups...")
    build_artifacts()
    print("All artifacts generated successfully!")
