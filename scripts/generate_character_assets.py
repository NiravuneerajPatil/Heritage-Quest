"""
Heritage Quest - 32x32 Character Asset Generator
Generates pixel-perfect 32x32 animation frames and sprite sheets for the Indian Hero
wearing an authentic yellow Kurta and white Dhoti, armed with a Talwar (curved sword).

Animations generated:
- Idle (6 frames)
- Run (8 frames)
- Jump (4 frames)
- Fall (2 frames)
- Attack1 (Quick Talwar Slash - 6 frames)
- Attack2 (Heavy Overhead Cleave - 6 frames)
- Hit (Hurt Recoil - 3 frames)
- Death (Fallen Hero - 8 frames)
"""

import os
import zlib
import struct

WIDTH = 32
HEIGHT = 32

# Authentic Palette
PALETTE = {
    'trans':       (0, 0, 0, 0),
    'outline':     (24, 20, 18, 255),
    'outline_lt':  (48, 40, 36, 255),
    
    # Indian Skin Tones (warm wheatish / golden-brown)
    'skin_hi':     (226, 161, 118, 255),
    'skin':        (186, 120, 78, 255),
    'skin_sh':     (142, 80, 44, 255),
    'skin_dk':     (98, 48, 22, 255),
    
    # Hair & Mustache (Jet black with warm dark sheen)
    'hair_hi':     (64, 52, 46, 255),
    'hair':        (42, 34, 30, 255),
    'hair_dk':     (24, 20, 18, 255),
    
    # Facial Features
    'eye_white':   (248, 250, 252, 255),
    'eye_pupil':   (24, 20, 18, 255),
    'mustache':    (24, 20, 18, 255),
    'mustache_sh': (16, 12, 10, 255),
    
    # Authentic Yellow Kurta (turmeric/marigold gold with embroidery)
    'kurta_hi':    (254, 240, 138, 255),
    'kurta_lit':   (253, 224, 71, 255),
    'kurta':       (234, 179, 8, 255),
    'kurta_sh':    (180, 83, 9, 255),
    'kurta_dk':    (120, 53, 15, 255),
    'gold_trim':   (255, 237, 160, 255),
    
    # Crimson Waist Sash (Patka / Kamarband)
    'sash_hi':     (239, 68, 68, 255),
    'sash':        (185, 28, 28, 255),
    'sash_sh':     (127, 29, 29, 255),
    'sash_gold':   (251, 191, 36, 255),
    
    # Authentic White Dhoti (pleated cotton fabric)
    'dhoti_hi':    (255, 255, 255, 255),
    'dhoti':       (241, 245, 249, 255),
    'dhoti_sh':    (203, 213, 225, 255),
    'dhoti_dk':    (148, 163, 184, 255),
    'dhoti_line':  (100, 116, 139, 255),
    
    # Traditional Footwear (Leather Mojris / Jutis)
    'juti_hi':     (154, 52, 18, 255),
    'juti':        (120, 53, 15, 255),
    'juti_sh':     (69, 26, 3, 255),
    
    # Talwar (Curved Indian Sword)
    'hilt_hi':     (253, 224, 71, 255),
    'hilt':        (217, 119, 6, 255),
    'hilt_sh':     (146, 64, 14, 255),
    'steel_hi':    (255, 255, 255, 255),
    'steel':       (226, 232, 240, 255),
    'steel_sh':    (148, 163, 184, 255),
    'steel_dk':    (71, 85, 105, 255),
    
    # Slash Arc & Spark Effects
    'slash_hi':    (255, 255, 255, 255),
    'slash_core':  (186, 230, 253, 255),
    'slash_glow':  (56, 189, 248, 230),
    'slash_edge':  (14, 165, 233, 180),
    'spark_gold':  (254, 240, 138, 240),
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
        """Blend RGBA with existing pixel."""
        if 0 <= x < self.w and 0 <= y < self.h:
            if isinstance(color, str):
                color = PALETTE[color]
            sr, sg, sb, sa = color
            if sa == 0:
                return
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

    def rect(self, x1, y1, x2, y2, color):
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                self.set(x, y, color)

    def line(self, x1, y1, x2, y2, color):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        x, y = x1, y1
        while True:
            self.set(x, y, color)
            if x == x2 and y == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def add_outline(self, outline_color='outline'):
        """Adds a subtle contextual 1px outline around non-transparent pixels."""
        col = PALETTE[outline_color]
        orig = [row[:] for row in self.data]
        for y in range(self.h):
            for x in range(self.w):
                if orig[y][x][3] == 0:
                    # Check 4-way neighbors
                    has_neighbor = False
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.w and 0 <= ny < self.h:
                            if orig[ny][nx][3] > 100:
                                has_neighbor = True
                                break
                    if has_neighbor:
                        self.data[y][x] = col

    def to_png_bytes(self):
        def chunk(chunk_type, data):
            return struct.pack('>I', len(data)) + chunk_type + data + struct.pack('>I', zlib.crc32(chunk_type + data) & 0xffffffff)

        raw = bytearray()
        for y in range(self.h):
            raw.append(0) # filter None
            for x in range(self.w):
                r, g, b, a = self.data[y][x]
                raw.extend((r, g, b, a))

        compressed = zlib.compress(bytes(raw), 9)
        ihdr = struct.pack('>IIBBBBB', self.w, self.h, 8, 6, 0, 0, 0)
        return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', compressed) + chunk(b'IEND', b'')


def save_spritesheet(frames, path):
    """Combines a list of Frame objects horizontally into a single spritesheet PNG."""
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
    print(f"Saved: {path} ({sw}x{sh}, {n} frames)")


# =========================================================================
# CHARACTER DRAWING COMPONENTS
# =========================================================================

def draw_head(frame, hx, hy, blink=False, hair_style=0, facing_right=True, hit_tilt=0):
    """Draws head, Indian skin, facial features, eyes, and classic mustache."""
    # Hair Top & Crown
    hair_c = 'hair'
    hair_hi = 'hair_hi'
    hair_dk = 'hair_dk'

    # Hair crown
    for x in range(hx - 2, hx + 4): frame.set(x, hy - 4, hair_c)
    for x in range(hx - 3, hx + 5): frame.set(x, hy - 3, hair_c)
    frame.set(hx - 1, hy - 4, hair_hi)
    frame.set(hx, hy - 4, hair_hi)
    frame.set(hx - 2, hy - 3, hair_hi)

    # Hair back
    if facing_right:
        frame.set(hx - 4, hy - 2, hair_dk)
        frame.set(hx - 4, hy - 1, hair_dk)
        frame.set(hx - 4, hy, hair_dk)
        frame.set(hx - 3, hy + 1, hair_dk)
    else:
        frame.set(hx + 4, hy - 2, hair_dk)
        frame.set(hx + 4, hy - 1, hair_dk)
        frame.set(hx + 4, hy, hair_dk)
        frame.set(hx + 3, hy + 1, hair_dk)

    # Forehead / Face base
    for y in range(hy - 2, hy + 3):
        for x in range(hx - 2, hx + 4):
            frame.set(x, y, 'skin')
    
    # Forehead highlight
    frame.set(hx, hy - 2, 'skin_hi')
    frame.set(hx + 1, hy - 2, 'skin_hi')

    # Sideburns & temples
    if facing_right:
        frame.set(hx - 3, hy - 2, hair_c)
        frame.set(hx - 3, hy - 1, hair_c)
        frame.set(hx - 2, hy - 1, hair_dk)
    else:
        frame.set(hx + 3, hy - 2, hair_c)
        frame.set(hx + 3, hy - 1, hair_c)
        frame.set(hx + 2, hy - 1, hair_dk)

    # Eyes
    if blink:
        # Closed eyes (eyelid skin line + lash)
        if facing_right:
            frame.set(hx, hy - 1, 'mustache')
            frame.set(hx + 1, hy - 1, 'mustache')
            frame.set(hx + 2, hy - 1, 'mustache')
        else:
            frame.set(hx - 1, hy - 1, 'mustache')
            frame.set(hx, hy - 1, 'mustache')
            frame.set(hx + 1, hy - 1, 'mustache')
    else:
        # Expressive eyes with dark pupil and white sclera
        if facing_right:
            frame.set(hx - 1, hy - 1, 'eye_white')
            frame.set(hx, hy - 1, 'eye_pupil')
            frame.set(hx + 1, hy - 1, 'skin')
            frame.set(hx + 2, hy - 1, 'eye_white')
            frame.set(hx + 3, hy - 1, 'eye_pupil')
            # Brow line
            frame.set(hx - 1, hy - 2, 'hair_dk')
            frame.set(hx, hy - 2, 'hair_dk')
            frame.set(hx + 2, hy - 2, 'hair_dk')
            frame.set(hx + 3, hy - 2, 'hair_dk')
        else:
            frame.set(hx - 2, hy - 1, 'eye_pupil')
            frame.set(hx - 1, hy - 1, 'eye_white')
            frame.set(hx, hy - 1, 'skin')
            frame.set(hx + 1, hy - 1, 'eye_pupil')
            frame.set(hx + 2, hy - 1, 'eye_white')
            frame.set(hx - 2, hy - 2, 'hair_dk')
            frame.set(hx - 1, hy - 2, 'hair_dk')
            frame.set(hx + 1, hy - 2, 'hair_dk')
            frame.set(hx + 2, hy - 2, 'hair_dk')

    # Authentic Indian Mustache (thick, well-groomed, majestic curve)
    if facing_right:
        frame.set(hx - 1, hy, 'skin_sh') # nose shadow
        frame.set(hx + 1, hy, 'mustache')
        frame.set(hx + 2, hy, 'mustache')
        frame.set(hx + 3, hy, 'mustache')
        frame.set(hx + 4, hy - 1, 'mustache') # slight upward handlebar curve!
        frame.set(hx, hy, 'mustache')
        frame.set(hx - 1, hy + 1, 'skin_sh')
    else:
        frame.set(hx + 1, hy, 'skin_sh')
        frame.set(hx - 1, hy, 'mustache')
        frame.set(hx - 2, hy, 'mustache')
        frame.set(hx - 3, hy, 'mustache')
        frame.set(hx - 4, hy - 1, 'mustache')
        frame.set(hx, hy, 'mustache')

    # Chin & Jawline
    frame.set(hx, hy + 1, 'skin')
    frame.set(hx + 1, hy + 1, 'skin')
    frame.set(hx + 2, hy + 1, 'skin')
    frame.set(hx - 1, hy + 2, 'skin_sh')
    frame.set(hx, hy + 2, 'skin_sh')
    frame.set(hx + 1, hy + 2, 'skin')

    # Neck
    frame.set(hx, hy + 3, 'skin_sh')
    frame.set(hx + 1, hy + 3, 'skin')


def draw_kurta_torso(frame, tx, ty, width=8, lean=0, breath=0):
    """Draws authentic yellow kurta with Mandarin collar, gold buttons, and shading."""
    k_lit = 'kurta_lit'
    k_base = 'kurta'
    k_sh = 'kurta_sh'
    k_dk = 'kurta_dk'
    gold = 'gold_trim'

    y_start = ty
    y_end = ty + 5

    # Torso body
    for y in range(y_start, y_end):
        cur_lean = int(lean * (y - y_start) / 4.0)
        for x in range(tx - 3 + cur_lean, tx + 4 + cur_lean):
            # Base color
            frame.set(x, y, k_base)
        # Highlight on chest/sunlit side
        frame.set(tx - 1 + cur_lean, y, k_lit)
        frame.set(tx + cur_lean, y, k_lit)
        # Shading on back/shadow side
        frame.set(tx - 3 + cur_lean, y, k_sh)
        frame.set(tx - 4 + cur_lean, y, k_dk)

    # Mandarin Collar (Bandhgala) & V-neck slit
    frame.set(tx, y_start, gold)
    frame.set(tx + 1, y_start, gold)
    frame.set(tx - 1, y_start, k_lit)

    # Traditional button placket down chest with gold buttons
    frame.set(tx, y_start + 1, gold)
    frame.set(tx, y_start + 2, k_sh)
    frame.set(tx, y_start + 3, gold)
    frame.set(tx, y_start + 4, k_sh)


def draw_kamarband(frame, tx, ty, sway=0):
    """Draws crimson waist sash (kamarband/patka) tied with dangling tassel ends."""
    for x in range(tx - 4, tx + 5):
        frame.set(x, ty, 'sash')
    frame.set(tx - 1, ty, 'sash_hi')
    frame.set(tx, ty, 'sash_hi')
    frame.set(tx - 4, ty, 'sash_sh')
    
    # Knot in front/side
    frame.set(tx + 1, ty, 'sash_hi')
    frame.set(tx + 1, ty + 1, 'sash')
    
    # Dangling sash ends with gold fringe
    dx = sway
    frame.set(tx + 1 + dx, ty + 2, 'sash')
    frame.set(tx + 2 + dx, ty + 2, 'sash')
    frame.set(tx + 1 + dx, ty + 3, 'sash')
    frame.set(tx + 2 + dx, ty + 3, 'sash')
    frame.set(tx + 1 + dx, ty + 4, 'sash_gold') # Golden fringe!
    frame.set(tx + 2 + dx, ty + 4, 'sash_gold')


def draw_kurta_skirt(frame, tx, ty, sway=0, spread=0):
    """Draws the lower half of the yellow kurta with authentic side slits (chaaks)."""
    k_lit = 'kurta_lit'
    k_base = 'kurta'
    k_sh = 'kurta_sh'
    k_dk = 'kurta_dk'

    # Kurta extends from waist down over hips to mid-thigh
    for y in range(ty, ty + 5):
        y_prog = (y - ty)
        left = tx - 4 - int(spread * 0.5) + int(sway * y_prog / 4.0)
        right = tx + 4 + int(spread * 0.5) + int(sway * y_prog / 4.0)
        for x in range(left, right + 1):
            frame.set(x, y, k_base)
        
        # Highlights & Shadows
        frame.set(left, y, k_sh)
        frame.set(left + 1, y, k_lit)
        frame.set(right, y, k_sh)
        frame.set(right - 1, y, k_lit)

        # Authentic side slit (chaak) opening at sides on lower rows
        if y >= ty + 2:
            frame.set(tx, y, 'kurta_dk') # Center seam
            # Side slits reveal dhoti/movement
            frame.set(left - 1, y, 'trans')


def draw_dhoti(frame, lx, ly, rx, ry, state='stand', billow=0):
    """
    Draws authentic white dhoti pleated around legs.
    Draped fabric with traditional central pleat folds (kachha).
    """
    d_hi = 'dhoti_hi'
    d_mid = 'dhoti'
    d_sh = 'dhoti_sh'
    d_dk = 'dhoti_dk'
    d_line = 'dhoti_line'

    # Left leg dhoti wrap
    for y in range(ly[0], ly[1] + 1):
        x_min, x_max = lx[0], lx[1]
        for x in range(x_min, x_max + 1):
            frame.set(x, y, d_mid)
        frame.set(x_min, y, d_sh)
        frame.set(x_min + 1, y, d_hi)
        frame.set(x_max, y, d_dk)

    # Right leg dhoti wrap
    for y in range(ry[0], ry[1] + 1):
        x_min, x_max = rx[0], rx[1]
        for x in range(x_min, x_max + 1):
            frame.set(x, y, d_mid)
        frame.set(x_min, y, d_sh)
        frame.set(x_min + 1, y, d_hi)
        frame.set(x_max, y, d_dk)

    # Central pleated gather (kachha)
    cx = (lx[1] + rx[0]) // 2
    for y in range(min(ly[0], ry[0]), max(ly[1], ry[1]) - 1):
        frame.set(cx, y, d_line)
        frame.set(cx - 1, y, d_hi)
        frame.set(cx + 1, y, d_sh)

    # Billowing folds when jumping/running
    if billow != 0:
        bx = cx + billow
        by = max(ly[1], ry[1]) - 1
        frame.set(bx, by, d_mid)
        frame.set(bx + (1 if billow > 0 else -1), by, d_sh)


def draw_juti(frame, x, y, facing_right=True):
    """Draws traditional Indian leather juti/mojri with characteristic curled toe."""
    j_hi = 'juti_hi'
    j_base = 'juti'
    j_sh = 'juti_sh'

    if facing_right:
        # Sole
        frame.set(x - 2, y + 1, j_sh)
        frame.set(x - 1, y + 1, j_sh)
        frame.set(x, y + 1, j_sh)
        frame.set(x + 1, y + 1, j_sh)
        frame.set(x + 2, y + 1, j_sh)
        # Upper body
        frame.set(x - 2, y, j_base)
        frame.set(x - 1, y, j_base)
        frame.set(x, y, j_hi)
        frame.set(x + 1, y, j_base)
        # Curled pointed toe (distinctive mojri feature!)
        frame.set(x + 2, y, j_hi)
        frame.set(x + 3, y - 1, j_base)
    else:
        frame.set(x - 2, y + 1, j_sh)
        frame.set(x - 1, y + 1, j_sh)
        frame.set(x, y + 1, j_sh)
        frame.set(x + 1, y + 1, j_sh)
        frame.set(x + 2, y + 1, j_sh)
        frame.set(x - 1, y, j_base)
        frame.set(x, y, j_hi)
        frame.set(x + 1, y, j_base)
        frame.set(x + 2, y, j_base)
        frame.set(x - 2, y, j_hi)
        frame.set(x - 3, y - 1, j_base)


def draw_talwar(frame, hx, hy, angle='sheathed', glint=False):
    """
    Draws authentic Indian Talwar:
    - Burnished brass disc pommel (katori) & crossguard
    - Gracefully curved single-edged steel blade
    """
    h_hi = 'hilt_hi'
    h_mid = 'hilt'
    h_sh = 'hilt_sh'
    s_hi = 'steel_hi'
    s_mid = 'steel'
    s_sh = 'steel_sh'
    s_dk = 'steel_dk'

    if angle == 'sheathed' or angle == 'idle':
        # Disc pommel & guard
        frame.set(hx, hy - 1, h_hi)
        frame.set(hx - 1, hy, h_mid)
        frame.set(hx, hy, h_hi)
        frame.set(hx + 1, hy, h_sh)
        # Curved blade pointing down and back
        frame.set(hx + 1, hy + 1, s_hi)
        frame.set(hx + 1, hy + 2, s_mid)
        frame.set(hx + 2, hy + 2, s_dk)
        frame.set(hx + 2, hy + 3, s_mid)
        frame.set(hx + 2, hy + 4, s_mid)
        frame.set(hx + 2, hy + 5, s_hi)
        frame.set(hx + 1, hy + 6, s_mid)
        # Curving blade tip
        frame.set(hx, hy + 6, s_hi)
        if glint:
            frame.set(hx + 2, hy + 3, 'slash_hi')
            frame.set(hx + 3, hy + 3, 'slash_core')

    elif angle == 'ready_low':
        frame.set(hx, hy, h_hi)
        frame.set(hx + 1, hy, h_mid)
        frame.set(hx + 2, hy + 1, s_hi)
        frame.set(hx + 3, hy + 2, s_mid)
        frame.set(hx + 4, hy + 3, s_hi)
        frame.set(hx + 5, hy + 3, s_mid)

    elif angle == 'windup_back':
        # Pulled back behind shoulder
        frame.set(hx, hy, h_hi)
        frame.set(hx - 1, hy - 1, s_mid)
        frame.set(hx - 2, hy - 2, s_hi)
        frame.set(hx - 3, hy - 3, s_mid)
        frame.set(hx - 4, hy - 4, s_hi)
        frame.set(hx - 4, hy - 5, s_mid)

    elif angle == 'slash_horizontal':
        # Thrusting forward / horizontal cut
        frame.set(hx, hy, h_hi)
        frame.set(hx + 1, hy, s_hi)
        frame.set(hx + 2, hy, s_hi)
        frame.set(hx + 3, hy, s_mid)
        frame.set(hx + 4, hy - 1, s_hi)
        frame.set(hx + 5, hy - 1, s_mid)
        frame.set(hx + 6, hy - 2, s_hi)
        frame.set(hx + 7, hy - 2, s_mid)

    elif angle == 'overhead_raise':
        # Both hands raised holding talwar high overhead
        frame.set(hx, hy, h_hi)
        frame.set(hx, hy - 1, h_mid)
        frame.set(hx + 1, hy - 2, s_hi)
        frame.set(hx + 1, hy - 3, s_mid)
        frame.set(hx + 2, hy - 4, s_hi)
        frame.set(hx + 2, hy - 5, s_mid)
        frame.set(hx + 3, hy - 6, s_hi)

    elif angle == 'downward_cleave':
        # Slashing down near ground
        frame.set(hx, hy, h_hi)
        frame.set(hx + 1, hy + 1, s_hi)
        frame.set(hx + 2, hy + 2, s_mid)
        frame.set(hx + 2, hy + 3, s_hi)
        frame.set(hx + 3, hy + 4, s_mid)
        frame.set(hx + 3, hy + 5, s_hi)


def draw_slash_fx(frame, fx_type='horizontal', stage=0):
    """Draws blazing energy slash arc and impact sparks."""
    if fx_type == 'horizontal':
        # Brilliant curved crescent cut
        if stage == 1:
            # Big slash arc across X=18..30, Y=10..22
            points = [
                (20, 10, 'slash_glow'),
                (22, 11, 'slash_core'),
                (24, 12, 'slash_hi'),
                (26, 14, 'slash_hi'),
                (27, 16, 'slash_core'),
                (27, 18, 'slash_glow'),
                (25, 20, 'slash_core'),
                (23, 21, 'slash_glow'),
                # Second thickness
                (23, 12, 'slash_core'),
                (25, 14, 'slash_core'),
                (26, 16, 'slash_hi'),
                (24, 19, 'slash_glow'),
            ]
            for x, y, col in points:
                frame.blend(x, y, col)
            # Gold sparks
            frame.blend(28, 15, 'spark_gold')
            frame.blend(26, 10, 'spark_gold')
            frame.blend(25, 22, 'spark_gold')

        elif stage == 2:
            # Dissipating sparks & trail
            points = [
                (25, 12, 'slash_glow'),
                (27, 14, 'slash_glow'),
                (28, 16, 'slash_core'),
                (27, 18, 'slash_glow'),
                (29, 15, 'spark_gold'),
                (30, 17, 'spark_gold'),
            ]
            for x, y, col in points:
                frame.blend(x, y, col)

    elif fx_type == 'overhead':
        # Massive vertical arc cleaving downward
        if stage == 1:
            points = [
                (17, 3, 'slash_glow'),
                (19, 4, 'slash_core'),
                (21, 6, 'slash_hi'),
                (23, 9, 'slash_hi'),
                (24, 13, 'slash_hi'),
                (24, 17, 'slash_core'),
                (23, 21, 'slash_glow'),
                (22, 25, 'slash_core'),
                (21, 27, 'slash_glow'),
                # Thickness
                (20, 6, 'slash_core'),
                (22, 9, 'slash_core'),
                (23, 13, 'slash_hi'),
                (23, 17, 'slash_hi'),
                (22, 21, 'slash_core'),
            ]
            for x, y, col in points:
                frame.blend(x, y, col)
            frame.blend(25, 12, 'spark_gold')
            frame.blend(24, 25, 'spark_gold')

        elif stage == 2:
            # Ground impact burst
            for x in range(20, 27):
                frame.blend(x, 28, 'slash_core')
            frame.blend(21, 27, 'slash_hi')
            frame.blend(23, 27, 'spark_gold')
            frame.blend(25, 27, 'spark_gold')
            frame.blend(27, 26, 'spark_gold')


# =========================================================================
# ANIMATION SEQUENCES
# =========================================================================

def generate_idle_frames():
    """6 Frames: Heroic ready stance, gentle breathing, cloth sway, blink, blade gleam."""
    frames = []
    
    # Offsets for 6 frames:
    # 0: Base
    # 1: Inhale start (+1 chest)
    # 2: Inhale peak (+1 chest, blade glint)
    # 3: Blink (eyes shut, hold)
    # 4: Exhale start
    # 5: Settle
    breathes = [0, -1, -1, -1, 0, 0]
    blinks = [False, False, False, True, False, False]
    glints = [False, False, True, False, False, False]
    sash_sways = [0, 0, 1, 1, 0, 0]

    for i in range(6):
        f = Frame(WIDTH, HEIGHT)
        by = breathes[i]
        
        # Dhoti Legs & Jutis (planted on ground)
        draw_dhoti(f, lx=(11, 14), ly=(20, 27), rx=(16, 19), ry=(20, 27), state='stand')
        draw_juti(f, x=12, y=28, facing_right=True)
        draw_juti(f, x=17, y=28, facing_right=True)

        # Kurta Skirt & Sash
        draw_kurta_skirt(f, tx=15, ty=17 + by, sway=sash_sways[i])
        draw_kamarband(f, tx=15, ty=16 + by, sway=sash_sways[i])

        # Torso & Collar
        draw_kurta_torso(f, tx=15, ty=11 + by)

        # Arms
        # Left arm (resting on hip sash)
        f.set(10, 12 + by, 'kurta_sh')
        f.set(10, 13 + by, 'kurta')
        f.set(10, 14 + by, 'skin')
        f.set(11, 15 + by, 'skin')

        # Right arm (holding talwar)
        f.set(20, 12 + by, 'kurta_lit')
        f.set(20, 13 + by, 'kurta')
        f.set(21, 14 + by, 'skin')
        f.set(21, 15 + by, 'skin')

        # Head & Face
        draw_head(f, hx=15, hy=7 + by, blink=blinks[i], facing_right=True)

        # Talwar at hip
        draw_talwar(f, hx=22, hy=15 + by, angle='idle', glint=glints[i])

        f.add_outline()
        frames.append(f)
    return frames


def generate_run_frames():
    """8 Frames: Full platformer running cycle with dynamic dhoti folds & kurta flutter."""
    frames = []

    # Cycle:
    # 0: Right contact (R forward, L back)
    # 1: Right down / squash (knees bend, body drops 1px)
    # 2: Left passing (L knee bent high, body rises)
    # 3: Left up / push-off (peak height, reaching forward)
    # 4: Left contact (L forward, R back)
    # 5: Left down / squash (knees bend, body drops 1px)
    # 6: Right passing (R knee bent high, body rises)
    # 7: Right up / push-off (peak height, reaching forward)

    y_bobs = [0, 1, 0, -1, 0, 1, 0, -1]
    leans = [1, 2, 1, 1, 1, 2, 1, 1]
    sways = [-1, -2, -1, 0, 1, -2, 1, 0]

    for i in range(8):
        f = Frame(WIDTH, HEIGHT)
        bob = y_bobs[i]
        lean = leans[i]
        sway = sways[i]

        # Legs & Dhoti per run phase
        if i == 0: # R Contact
            draw_dhoti(f, lx=(9, 13), ly=(20 + bob, 26 + bob), rx=(16, 21), ry=(20 + bob, 27 + bob), billow=-1)
            draw_juti(f, x=10, y=27 + bob, facing_right=True)
            draw_juti(f, x=20, y=28 + bob, facing_right=True)
        elif i == 1: # R Down / Squash
            draw_dhoti(f, lx=(8, 12), ly=(21 + bob, 26 + bob), rx=(16, 21), ry=(21 + bob, 27 + bob), billow=-2)
            draw_juti(f, x=9, y=27 + bob, facing_right=True)
            draw_juti(f, x=20, y=28 + bob, facing_right=True)
        elif i == 2: # L Passing
            draw_dhoti(f, lx=(12, 16), ly=(19 + bob, 24 + bob), rx=(14, 18), ry=(20 + bob, 27 + bob), billow=-1)
            draw_juti(f, x=14, y=25 + bob, facing_right=True)
            draw_juti(f, x=16, y=28 + bob, facing_right=True)
        elif i == 3: # L Up / Push-off
            draw_dhoti(f, lx=(15, 20), ly=(19 + bob, 26 + bob), rx=(10, 14), ry=(20 + bob, 26 + bob), billow=-1)
            draw_juti(f, x=19, y=27 + bob, facing_right=True)
            draw_juti(f, x=11, y=27 + bob, facing_right=True)
        elif i == 4: # L Contact
            draw_dhoti(f, lx=(16, 21), ly=(20 + bob, 27 + bob), rx=(9, 13), ry=(20 + bob, 26 + bob), billow=-1)
            draw_juti(f, x=20, y=28 + bob, facing_right=True)
            draw_juti(f, x=10, y=27 + bob, facing_right=True)
        elif i == 5: # L Down / Squash
            draw_dhoti(f, lx=(16, 21), ly=(21 + bob, 27 + bob), rx=(8, 12), ry=(21 + bob, 26 + bob), billow=-2)
            draw_juti(f, x=20, y=28 + bob, facing_right=True)
            draw_juti(f, x=9, y=27 + bob, facing_right=True)
        elif i == 6: # R Passing
            draw_dhoti(f, lx=(14, 18), ly=(20 + bob, 27 + bob), rx=(12, 16), ry=(19 + bob, 24 + bob), billow=-1)
            draw_juti(f, x=16, y=28 + bob, facing_right=True)
            draw_juti(f, x=14, y=25 + bob, facing_right=True)
        elif i == 7: # R Up / Push-off
            draw_dhoti(f, lx=(10, 14), ly=(20 + bob, 26 + bob), rx=(15, 20), ry=(19 + bob, 26 + bob), billow=-1)
            draw_juti(f, x=11, y=27 + bob, facing_right=True)
            draw_juti(f, x=19, y=27 + bob, facing_right=True)

        # Kurta Skirt & Sash fluttering backward
        draw_kurta_skirt(f, tx=15 + lean, ty=17 + bob, sway=sway)
        draw_kamarband(f, tx=15 + lean, ty=16 + bob, sway=sway)

        # Torso
        draw_kurta_torso(f, tx=15 + lean, ty=11 + bob, lean=lean)

        # Arms swinging in opposition
        if i in [0, 1, 2, 3]:
            # Left arm forward, right arm back holding talwar
            f.set(18 + lean, 13 + bob, 'kurta_lit')
            f.set(19 + lean, 14 + bob, 'skin')
            f.set(10 + lean, 13 + bob, 'kurta_sh')
            f.set(9 + lean, 14 + bob, 'skin')
            draw_talwar(f, hx=9 + lean, hy=15 + bob, angle='idle')
        else:
            # Right arm forward holding talwar, left arm back
            f.set(11 + lean, 13 + bob, 'kurta_sh')
            f.set(10 + lean, 14 + bob, 'skin')
            f.set(19 + lean, 13 + bob, 'kurta_lit')
            f.set(20 + lean, 14 + bob, 'skin')
            draw_talwar(f, hx=21 + lean, hy=15 + bob, angle='ready_low')

        # Head & Face
        draw_head(f, hx=15 + lean, hy=7 + bob, facing_right=True)

        f.add_outline()
        frames.append(f)
    return frames


def generate_jump_frames():
    """4 Frames: Launch crouch, upward thrust, apex rise, apex hang."""
    frames = []

    # Frame 0: Crouch launch
    f0 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f0, lx=(10, 14), ly=(22, 28), rx=(16, 20), ry=(22, 28), state='crouch')
    draw_juti(f0, x=11, y=29, facing_right=True)
    draw_juti(f0, x=18, y=29, facing_right=True)
    draw_kurta_skirt(f0, tx=15, ty=18, spread=2)
    draw_kamarband(f0, tx=15, ty=17)
    draw_kurta_torso(f0, tx=15, ty=12)
    draw_head(f0, hx=15, hy=8)
    draw_talwar(f0, hx=22, hy=17, angle='idle')
    f0.add_outline()
    frames.append(f0)

    # Frame 1: Upward propel (stretch)
    f1 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f1, lx=(12, 15), ly=(20, 27), rx=(16, 19), ry=(21, 28), billow=-1)
    draw_juti(f1, x=13, y=28, facing_right=True)
    draw_juti(f1, x=17, y=29, facing_right=True)
    draw_kurta_skirt(f1, tx=15, ty=16, sway=-1)
    draw_kamarband(f1, tx=15, ty=15)
    draw_kurta_torso(f1, tx=15, ty=10)
    # Arms reaching up
    f1.set(11, 10, 'kurta_sh'); f1.set(10, 9, 'skin')
    f1.set(19, 10, 'kurta_lit'); f1.set(20, 9, 'skin')
    draw_head(f1, hx=15, hy=6)
    draw_talwar(f1, hx=21, hy=10, angle='overhead_raise')
    f1.add_outline()
    frames.append(f1)

    # Frame 2: High jump rise (knees tucked)
    f2 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f2, lx=(11, 15), ly=(18, 25), rx=(16, 20), ry=(19, 25), billow=-2)
    draw_juti(f2, x=12, y=26, facing_right=True)
    draw_juti(f2, x=18, y=26, facing_right=True)
    draw_kurta_skirt(f2, tx=15, ty=15, spread=1)
    draw_kamarband(f2, tx=15, ty=14)
    draw_kurta_torso(f2, tx=15, ty=9)
    draw_head(f2, hx=15, hy=5)
    draw_talwar(f2, hx=22, hy=12, angle='ready_low')
    f2.add_outline()
    frames.append(f2)

    # Frame 3: Apex float
    f3 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f3, lx=(11, 15), ly=(19, 26), rx=(16, 20), ry=(19, 26), billow=-1)
    draw_juti(f3, x=12, y=27, facing_right=True)
    draw_juti(f3, x=18, y=27, facing_right=True)
    draw_kurta_skirt(f3, tx=15, ty=16)
    draw_kamarband(f3, tx=15, ty=15)
    draw_kurta_torso(f3, tx=15, ty=10)
    draw_head(f3, hx=15, hy=6)
    draw_talwar(f3, hx=22, hy=14, angle='idle')
    f3.add_outline()
    frames.append(f3)

    return frames


def generate_fall_frames():
    """2 Frames: Air descent, dhoti & kurta billowing upward due to wind."""
    frames = []

    # Frame 0: Transition to fall
    f0 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f0, lx=(11, 15), ly=(18, 26), rx=(17, 21), ry=(18, 26), billow=2)
    draw_juti(f0, x=12, y=27, facing_right=True)
    draw_juti(f0, x=19, y=27, facing_right=True)
    draw_kurta_skirt(f0, tx=15, ty=16, spread=2) # Hem flutters up
    draw_kamarband(f0, tx=15, ty=15, sway=1)
    draw_kurta_torso(f0, tx=15, ty=10)
    # Arms out for balance
    f0.set(10, 11, 'kurta_sh'); f0.set(9, 10, 'skin')
    f0.set(20, 11, 'kurta_lit'); f0.set(21, 10, 'skin')
    draw_head(f0, hx=15, hy=6)
    draw_talwar(f0, hx=22, hy=12, angle='ready_low')
    f0.add_outline()
    frames.append(f0)

    # Frame 1: Full rapid drop
    f1 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f1, lx=(10, 14), ly=(17, 26), rx=(17, 21), ry=(17, 26), billow=3)
    draw_juti(f1, x=11, y=27, facing_right=True)
    draw_juti(f1, x=19, y=27, facing_right=True)
    draw_kurta_skirt(f1, tx=15, ty=15, spread=3)
    draw_kamarband(f1, tx=15, ty=14, sway=2)
    draw_kurta_torso(f1, tx=15, ty=9)
    # Arms raised
    f1.set(10, 10, 'kurta_sh'); f1.set(9, 9, 'skin')
    f1.set(20, 10, 'kurta_lit'); f1.set(21, 9, 'skin')
    draw_head(f1, hx=15, hy=5)
    draw_talwar(f1, hx=22, hy=11, angle='ready_low')
    f1.add_outline()
    frames.append(f1)

    return frames


def generate_attack1_frames():
    """6 Frames: Quick Talwar Slash - Windup, Step & Swing, Full Arc Impact, Follow-through, Recovery, Return."""
    frames = []

    # Frame 0: Windup / Coil back
    f0 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f0, lx=(10, 14), ly=(20, 27), rx=(15, 19), ry=(20, 27))
    draw_juti(f0, x=11, y=28, facing_right=True)
    draw_juti(f0, x=16, y=28, facing_right=True)
    draw_kurta_skirt(f0, tx=14, ty=17, sway=-1)
    draw_kamarband(f0, tx=14, ty=16)
    draw_kurta_torso(f0, tx=14, ty=11, lean=-1)
    draw_head(f0, hx=14, hy=7)
    # Talwar drawn back over shoulder
    draw_talwar(f0, hx=9, hy=12, angle='windup_back')
    f0.add_outline()
    frames.append(f0)

    # Frame 1: Lunge start / Swing forward
    f1 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f1, lx=(9, 13), ly=(21, 28), rx=(16, 21), ry=(21, 28))
    draw_juti(f1, x=10, y=29, facing_right=True)
    draw_juti(f1, x=20, y=29, facing_right=True)
    draw_kurta_skirt(f1, tx=16, ty=18, sway=-1)
    draw_kamarband(f1, tx=16, ty=17)
    draw_kurta_torso(f1, tx=16, ty=12, lean=2)
    draw_head(f1, hx=16, hy=8)
    draw_talwar(f1, hx=19, hy=14, angle='slash_horizontal')
    f1.add_outline()
    frames.append(f1)

    # Frame 2: Full Slash Impact with glowing arc
    f2 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f2, lx=(8, 12), ly=(22, 28), rx=(17, 23), ry=(22, 28))
    draw_juti(f2, x=9, y=29, facing_right=True)
    draw_juti(f2, x=22, y=29, facing_right=True)
    draw_kurta_skirt(f2, tx=17, ty=19, sway=-2)
    draw_kamarband(f2, tx=17, ty=18)
    draw_kurta_torso(f2, tx=17, ty=13, lean=3)
    draw_head(f2, hx=17, hy=9)
    draw_talwar(f2, hx=22, hy=15, angle='slash_horizontal')
    draw_slash_fx(f2, fx_type='horizontal', stage=1)
    f2.add_outline()
    frames.append(f2)

    # Frame 3: Follow-through & Sparks
    f3 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f3, lx=(8, 12), ly=(22, 28), rx=(17, 23), ry=(22, 28))
    draw_juti(f3, x=9, y=29, facing_right=True)
    draw_juti(f3, x=22, y=29, facing_right=True)
    draw_kurta_skirt(f3, tx=17, ty=19, sway=-1)
    draw_kamarband(f3, tx=17, ty=18)
    draw_kurta_torso(f3, tx=17, ty=13, lean=2)
    draw_head(f3, hx=17, hy=9)
    draw_talwar(f3, hx=23, hy=16, angle='ready_low')
    draw_slash_fx(f3, fx_type='horizontal', stage=2)
    f3.add_outline()
    frames.append(f3)

    # Frame 4: Recovery step
    f4 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f4, lx=(9, 13), ly=(21, 28), rx=(16, 21), ry=(21, 28))
    draw_juti(f4, x=10, y=29, facing_right=True)
    draw_juti(f4, x=19, y=29, facing_right=True)
    draw_kurta_skirt(f4, tx=16, ty=18)
    draw_kamarband(f4, tx=16, ty=17)
    draw_kurta_torso(f4, tx=16, ty=12, lean=1)
    draw_head(f4, hx=16, hy=8)
    draw_talwar(f4, hx=22, hy=16, angle='ready_low')
    f4.add_outline()
    frames.append(f4)

    # Frame 5: Return to combat stance
    f5 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f5, lx=(11, 14), ly=(20, 27), rx=(16, 19), ry=(20, 27))
    draw_juti(f5, x=12, y=28, facing_right=True)
    draw_juti(f5, x=17, y=28, facing_right=True)
    draw_kurta_skirt(f5, tx=15, ty=17)
    draw_kamarband(f5, tx=15, ty=16)
    draw_kurta_torso(f5, tx=15, ty=11)
    draw_head(f5, hx=15, hy=7)
    draw_talwar(f5, hx=22, hy=15, angle='idle')
    f5.add_outline()
    frames.append(f5)

    return frames


def generate_attack2_frames():
    """6 Frames: Overhead Heavy Talwar Cleave - High Raise, Windup Peak, Downward Strike, Ground Impact, Lift, Return."""
    frames = []

    # Frame 0: High Raise
    f0 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f0, lx=(11, 14), ly=(20, 27), rx=(16, 19), ry=(20, 27))
    draw_juti(f0, x=12, y=28, facing_right=True)
    draw_juti(f0, x=17, y=28, facing_right=True)
    draw_kurta_skirt(f0, tx=15, ty=17)
    draw_kamarband(f0, tx=15, ty=16)
    draw_kurta_torso(f0, tx=15, ty=11)
    draw_head(f0, hx=15, hy=7)
    # Talwar raised high
    draw_talwar(f0, hx=17, hy=7, angle='overhead_raise')
    f0.add_outline()
    frames.append(f0)

    # Frame 1: Windup Peak
    f1 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f1, lx=(10, 14), ly=(20, 27), rx=(15, 19), ry=(20, 27))
    draw_juti(f1, x=11, y=28, facing_right=True)
    draw_juti(f1, x=16, y=28, facing_right=True)
    draw_kurta_skirt(f1, tx=15, ty=17, sway=-1)
    draw_kamarband(f1, tx=15, ty=16)
    draw_kurta_torso(f1, tx=15, ty=11, lean=-1)
    draw_head(f1, hx=15, hy=7)
    draw_talwar(f1, hx=15, hy=5, angle='overhead_raise', glint=True)
    f1.add_outline()
    frames.append(f1)

    # Frame 2: Downward Strike & Vertical Arc
    f2 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f2, lx=(8, 12), ly=(22, 28), rx=(17, 23), ry=(22, 28))
    draw_juti(f2, x=9, y=29, facing_right=True)
    draw_juti(f2, x=22, y=29, facing_right=True)
    draw_kurta_skirt(f2, tx=17, ty=19)
    draw_kamarband(f2, tx=17, ty=18)
    draw_kurta_torso(f2, tx=17, ty=13, lean=2)
    draw_head(f2, hx=17, hy=9)
    draw_talwar(f2, hx=20, hy=19, angle='downward_cleave')
    draw_slash_fx(f2, fx_type='overhead', stage=1)
    f2.add_outline()
    frames.append(f2)

    # Frame 3: Ground Impact & Shockwave
    f3 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f3, lx=(8, 12), ly=(22, 28), rx=(17, 23), ry=(22, 28))
    draw_juti(f3, x=9, y=29, facing_right=True)
    draw_juti(f3, x=22, y=29, facing_right=True)
    draw_kurta_skirt(f3, tx=17, ty=19)
    draw_kamarband(f3, tx=17, ty=18)
    draw_kurta_torso(f3, tx=17, ty=13, lean=2)
    draw_head(f3, hx=17, hy=9)
    draw_talwar(f3, hx=21, hy=21, angle='downward_cleave')
    draw_slash_fx(f3, fx_type='overhead', stage=2)
    f3.add_outline()
    frames.append(f3)

    # Frame 4: Pull back / Recover
    f4 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f4, lx=(9, 13), ly=(21, 28), rx=(16, 21), ry=(21, 28))
    draw_juti(f4, x=10, y=29, facing_right=True)
    draw_juti(f4, x=19, y=29, facing_right=True)
    draw_kurta_skirt(f4, tx=16, ty=18)
    draw_kamarband(f4, tx=16, ty=17)
    draw_kurta_torso(f4, tx=16, ty=12)
    draw_head(f4, hx=16, hy=8)
    draw_talwar(f4, hx=21, hy=17, angle='ready_low')
    f4.add_outline()
    frames.append(f4)

    # Frame 5: Return to ready stance
    f5 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f5, lx=(11, 14), ly=(20, 27), rx=(16, 19), ry=(20, 27))
    draw_juti(f5, x=12, y=28, facing_right=True)
    draw_juti(f5, x=17, y=28, facing_right=True)
    draw_kurta_skirt(f5, tx=15, ty=17)
    draw_kamarband(f5, tx=15, ty=16)
    draw_kurta_torso(f5, tx=15, ty=11)
    draw_head(f5, hx=15, hy=7)
    draw_talwar(f5, hx=22, hy=15, angle='idle')
    f5.add_outline()
    frames.append(f5)

    return frames


def generate_hit_frames():
    """3 Frames: Hurt / Recoil - Impact shock, knockback stagger, recovery."""
    frames = []

    # Frame 0: Impact shock (flash, head knocked back)
    f0 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f0, lx=(9, 13), ly=(21, 28), rx=(15, 19), ry=(20, 27))
    draw_juti(f0, x=10, y=29, facing_right=True)
    draw_juti(f0, x=16, y=28, facing_right=True)
    draw_kurta_skirt(f0, tx=14, ty=17, sway=2)
    draw_kamarband(f0, tx=14, ty=16, sway=1)
    draw_kurta_torso(f0, tx=14, ty=11, lean=-2)
    draw_head(f0, hx=13, hy=7, blink=True) # Eyes clamped shut in pain
    # Hurt flash on chest
    f0.blend(14, 12, 'slash_hi')
    f0.blend(15, 12, 'slash_hi')
    draw_talwar(f0, hx=20, hy=16, angle='ready_low')
    f0.add_outline()
    frames.append(f0)

    # Frame 1: Knockback stagger
    f1 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f1, lx=(8, 12), ly=(21, 28), rx=(14, 18), ry=(20, 27))
    draw_juti(f1, x=9, y=29, facing_right=True)
    draw_juti(f1, x=15, y=28, facing_right=True)
    draw_kurta_skirt(f1, tx=13, ty=17, sway=1)
    draw_kamarband(f1, tx=13, ty=16)
    draw_kurta_torso(f1, tx=13, ty=11, lean=-2)
    draw_head(f1, hx=12, hy=7, blink=True)
    draw_talwar(f1, hx=19, hy=17, angle='ready_low')
    f1.add_outline()
    frames.append(f1)

    # Frame 2: Recovery step
    f2 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f2, lx=(10, 14), ly=(20, 27), rx=(16, 19), ry=(20, 27))
    draw_juti(f2, x=11, y=28, facing_right=True)
    draw_juti(f2, x=17, y=28, facing_right=True)
    draw_kurta_skirt(f2, tx=14, ty=17)
    draw_kamarband(f2, tx=14, ty=16)
    draw_kurta_torso(f2, tx=14, ty=11, lean=-1)
    draw_head(f2, hx=14, hy=7, blink=False)
    draw_talwar(f2, hx=21, hy=16, angle='idle')
    f2.add_outline()
    frames.append(f2)

    return frames


def generate_death_frames():
    """8 Frames: Fallen Hero sequence - stagger, knees buckle, collapse, resting on ground."""
    frames = []

    # Frame 0: Heavy lethal blow recoil
    f0 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f0, lx=(9, 13), ly=(20, 27), rx=(15, 19), ry=(20, 27))
    draw_juti(f0, x=10, y=28, facing_right=True)
    draw_juti(f0, x=16, y=28, facing_right=True)
    draw_kurta_skirt(f0, tx=14, ty=17)
    draw_kamarband(f0, tx=14, ty=16)
    draw_kurta_torso(f0, tx=14, ty=11, lean=-2)
    draw_head(f0, hx=13, hy=7, blink=True)
    draw_talwar(f0, hx=20, hy=16, angle='ready_low')
    f0.add_outline()
    frames.append(f0)

    # Frame 1: Staggering backward, clutching chest
    f1 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f1, lx=(9, 13), ly=(21, 28), rx=(15, 19), ry=(21, 28))
    draw_juti(f1, x=10, y=29, facing_right=True)
    draw_juti(f1, x=16, y=29, facing_right=True)
    draw_kurta_skirt(f1, tx=14, ty=18)
    draw_kamarband(f1, tx=14, ty=17)
    draw_kurta_torso(f1, tx=14, ty=12, lean=-1)
    # Hand to chest
    f1.set(15, 14, 'skin')
    draw_head(f1, hx=14, hy=8, blink=True)
    draw_talwar(f1, hx=20, hy=18, angle='ready_low')
    f1.add_outline()
    frames.append(f1)

    # Frame 2: Knees buckling, sinking down
    f2 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f2, lx=(9, 14), ly=(23, 28), rx=(15, 20), ry=(23, 28))
    draw_juti(f2, x=10, y=29, facing_right=True)
    draw_juti(f2, x=16, y=29, facing_right=True)
    draw_kurta_skirt(f2, tx=14, ty=19)
    draw_kamarband(f2, tx=14, ty=18)
    draw_kurta_torso(f2, tx=14, ty=13)
    draw_head(f2, hx=14, hy=9, blink=True)
    # Talwar slipping from hand
    draw_talwar(f2, hx=21, hy=20, angle='ready_low')
    f2.add_outline()
    frames.append(f2)

    # Frame 3: Both knees hit ground
    f3 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f3, lx=(8, 14), ly=(24, 28), rx=(15, 21), ry=(24, 28))
    draw_juti(f3, x=9, y=29, facing_right=True)
    draw_juti(f3, x=16, y=29, facing_right=True)
    draw_kurta_skirt(f3, tx=14, ty=20)
    draw_kamarband(f3, tx=14, ty=19)
    draw_kurta_torso(f3, tx=14, ty=15)
    draw_head(f3, hx=14, hy=11, blink=True)
    # Dropped talwar on ground
    draw_talwar(f3, hx=22, hy=23, angle='ready_low')
    f3.add_outline()
    frames.append(f3)

    # Frame 4: Torso bowing / slumping forward
    f4 = Frame(WIDTH, HEIGHT)
    draw_dhoti(f4, lx=(8, 15), ly=(25, 29), rx=(16, 22), ry=(25, 29))
    draw_kurta_skirt(f4, tx=15, ty=22)
    draw_kamarband(f4, tx=15, ty=21)
    draw_kurta_torso(f4, tx=15, ty=17, lean=2)
    draw_head(f4, hx=18, hy=14, blink=True)
    draw_talwar(f4, hx=23, hy=24, angle='ready_low')
    f4.add_outline()
    frames.append(f4)

    # Frame 5: Tipping over to the ground
    f5 = Frame(WIDTH, HEIGHT)
    # Body settling horizontally
    for x in range(6, 26):
        f5.set(x, 28, 'dhoti')
        f5.set(x, 27, 'dhoti_sh')
    for x in range(10, 19):
        f5.set(x, 26, 'kurta')
        f5.set(x, 25, 'kurta_sh')
    f5.set(13, 26, 'sash')
    f5.set(14, 26, 'sash')
    # Head near ground
    for y in range(24, 28):
        for x in range(19, 25):
            f5.set(x, y, 'skin')
    for x in range(20, 26): f5.set(x, 24, 'hair')
    # Talwar on ground
    draw_talwar(f5, hx=25, hy=26, angle='ready_low')
    f5.add_outline()
    frames.append(f5)

    # Frame 6: Dhoti and Kurta draping flat
    f6 = Frame(WIDTH, HEIGHT)
    for x in range(5, 27):
        f6.set(x, 29, 'dhoti_sh')
        f6.set(x, 28, 'dhoti')
    for x in range(9, 18):
        f6.set(x, 27, 'kurta')
        f6.set(x, 26, 'kurta_lit')
    f6.set(12, 27, 'sash')
    f6.set(13, 27, 'sash')
    for y in range(25, 29):
        for x in range(19, 25):
            f6.set(x, y, 'skin')
    for x in range(20, 26): f6.set(x, 25, 'hair')
    draw_talwar(f6, hx=25, hy=27, angle='ready_low')
    f6.add_outline()
    frames.append(f6)

    # Frame 7: Resting peacefully on the ground (final loop hold)
    f7 = Frame(WIDTH, HEIGHT)
    for x in range(5, 27):
        f7.set(x, 29, 'dhoti_sh')
        f7.set(x, 28, 'dhoti')
    for x in range(9, 18):
        f7.set(x, 27, 'kurta')
        f7.set(x, 26, 'kurta_lit')
    f7.set(12, 27, 'sash')
    f7.set(13, 27, 'sash')
    for y in range(25, 29):
        for x in range(19, 25):
            f7.set(x, y, 'skin')
    for x in range(20, 26): f7.set(x, 25, 'hair')
    draw_talwar(f7, hx=25, hy=27, angle='ready_low')
    f7.add_outline()
    frames.append(f7)

    return frames


# =========================================================================
# MASTER SPRITE SHEET & GODOT EXPORT
# =========================================================================

def build_all_assets():
    base_dir = "assets/images/player_32x32"
    frames_dir = os.path.join(base_dir, "frames")
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(frames_dir, exist_ok=True)

    attack1_f = generate_attack1_frames()
    animations = {
        'Idle':    (generate_idle_frames(), 5.0, True),
        'Run':     (generate_run_frames(), 10.0, True),
        'Jump':    (generate_jump_frames(), 6.0, False),
        'Fall':    (generate_fall_frames(), 6.0, True),
        'Attack':  (attack1_f, 8.0, False),
        'Attack1': (attack1_f, 8.0, False),
        'Attack2': (generate_attack2_frames(), 8.0, False),
        'Hit':     (generate_hit_frames(), 6.0, False),
        'Death':   (generate_death_frames(), 5.0, False),
    }

    # 1. Save horizontal sprite sheets matching Godot AnimatedSprite2D layout
    for anim_name, (frames, speed, loop) in animations.items():
        sheet_path = os.path.join(base_dir, f"{anim_name}.png")
        save_spritesheet(frames, sheet_path)

        # Save individual frames as well
        anim_frames_dir = os.path.join(frames_dir, anim_name.lower())
        os.makedirs(anim_frames_dir, exist_ok=True)
        for idx, frame in enumerate(frames):
            frame_path = os.path.join(anim_frames_dir, f"{anim_name.lower()}_{idx}.png")
            with open(frame_path, 'wb') as fp:
                fp.write(frame.to_png_bytes())

    # 2. Save unified Master Sprite Sheet (Grid)
    # Rows: 8 animations, Max columns: 8 frames
    master_cols = 8
    master_rows = len(animations)
    master_w = master_cols * WIDTH
    master_h = master_rows * HEIGHT
    master_sheet = Frame(master_w, master_h)

    for row_idx, (anim_name, (frames, _, _)) in enumerate(animations.items()):
        oy = row_idx * HEIGHT
        for col_idx, f in enumerate(frames):
            ox = col_idx * WIDTH
            for y in range(HEIGHT):
                for x in range(WIDTH):
                    master_sheet.set(ox + x, oy + y, f.data[y][x])

    master_path = os.path.join(base_dir, "HeritageQuest_Hero_Master_Sheet.png")
    with open(master_path, 'wb') as fp:
        fp.write(master_sheet.to_png_bytes())
    print(f"Saved Master Sheet: {master_path} ({master_w}x{master_h})")

    # 3. Generate Godot 4 SpriteFrames .tres resource
    generate_godot_sprite_frames(animations, base_dir)

    # 4. Generate Interactive HTML Preview Visualizer
    generate_html_preview(animations, base_dir)


def generate_godot_sprite_frames(animations, base_dir):
    """Creates a ready-to-load Godot 4 SpriteFrames resource file (.tres)."""
    tres_path = os.path.join(base_dir, "hero_sprite_frames.tres")
    
    lines = []
    lines.append('[gd_resource type="SpriteFrames" load_steps=50 format=3]')
    lines.append('')
    
    # ExtResources for the horizontal texture sheets
    ext_id = 1
    ext_map = {}
    for anim_name in animations.keys():
        lines.append(f'[ext_resource type="Texture2D" path="res://assets/images/player_32x32/{anim_name}.png" id="{ext_id}_{anim_name.lower()}"]')
        ext_map[anim_name] = f'{ext_id}_{anim_name.lower()}'
        ext_id += 1
    lines.append('')

    # SubResources for each frame (AtlasTexture)
    atlas_map = {}
    sub_id = 1
    for anim_name, (frames, _, _) in animations.items():
        atlas_map[anim_name] = []
        tex_id = ext_map[anim_name]
        for f_idx in range(len(frames)):
            sub_name = f"AtlasTexture_{anim_name.lower()}_{f_idx}"
            lines.append(f'[sub_resource type="AtlasTexture" id="{sub_name}"]')
            lines.append(f'atlas = ExtResource("{tex_id}")')
            lines.append(f'region = Rect2({f_idx * 32}, 0, 32, 32)')
            lines.append('')
            atlas_map[anim_name].append(sub_name)
            sub_id += 1

    # SpriteFrames resource definition
    lines.append('[resource]')
    lines.append('animations = [{')
    
    anim_blocks = []
    for anim_name, (frames, speed, loop) in animations.items():
        block = []
        block.append(f'"frames": [')
        frame_entries = []
        for sub_name in atlas_map[anim_name]:
            frame_entries.append('{\n"duration": 1.0,\n"texture": SubResource("' + sub_name + '")\n}')
        block.append(', '.join(frame_entries))
        block.append('],')
        block.append(f'"loop": {"true" if loop else "false"},')
        block.append(f'"name": &"{anim_name}",')
        block.append(f'"speed": {speed}')
        anim_blocks.append('{\n' + '\n'.join(block) + '\n}')

    lines.append(', '.join(anim_blocks))
    lines.append('}]')

    with open(tres_path, 'w', encoding='utf-8') as fp:
        fp.write('\n'.join(lines))
    print(f"Generated Godot SpriteFrames: {tres_path}")


def generate_html_preview(animations, base_dir):
    """Generates a rich interactive visualizer HTML file."""
    html_path = os.path.join(base_dir, "character_preview.html")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Heritage Quest - Hero 32x32 Character Preview</title>
<style>
  :root {{
    --bg: #0f172a;
    --card: #1e293b;
    --accent: #f59e0b;
    --text: #f8fafc;
    --muted: #94a3b8;
  }}
  body {{
    margin: 0;
    padding: 24px;
    background: var(--bg);
    color: var(--text);
    font-family: system-ui, -apple-system, sans-serif;
  }}
  h1 {{
    color: var(--accent);
    margin: 0 0 8px 0;
  }}
  .subtitle {{
    color: var(--muted);
    margin-bottom: 24px;
  }}
  .container {{
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
  }}
  .preview-card {{
    background: var(--card);
    border-radius: 12px;
    padding: 20px;
    border: 1px solid #334155;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  }}
  .canvas-box {{
    background: #182234;
    border: 2px solid #475569;
    border-radius: 8px;
    padding: 16px;
    display: flex;
    justify-content: center;
    align-items: center;
    background-image: 
      linear-gradient(45deg, #131b2a 25%, transparent 25%), 
      linear-gradient(-45deg, #131b2a 25%, transparent 25%), 
      linear-gradient(45deg, transparent 75%, #131b2a 75%), 
      linear-gradient(-45deg, transparent 75%, #131b2a 75%);
    background-size: 16px 16px;
    background-position: 0 0, 0 8px, 8px -8px, -8px 0px;
  }}
  canvas {{
    image-rendering: pixelated;
    image-rendering: crisp-edges;
  }}
  .controls {{
    margin-top: 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }}
  .btn-group {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }}
  button {{
    background: #334155;
    border: 1px solid #64748b;
    color: #f8fafc;
    padding: 8px 14px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.15s ease;
  }}
  button:hover {{
    background: #475569;
  }}
  button.active {{
    background: var(--accent);
    color: #0f172a;
    border-color: #fbbf24;
    font-weight: bold;
  }}
  .info-tag {{
    display: inline-block;
    padding: 4px 8px;
    border-radius: 4px;
    background: #0284c7;
    color: white;
    font-size: 12px;
    font-weight: 600;
  }}
  .slider-row {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 14px;
  }}
  .master-sheet-view {{
    margin-top: 32px;
    background: var(--card);
    border-radius: 12px;
    padding: 20px;
    border: 1px solid #334155;
  }}
  .master-sheet-view img {{
    image-rendering: pixelated;
    width: 512px;
    border: 1px solid #475569;
    border-radius: 4px;
    margin-top: 12px;
  }}
</style>
</head>
<body>

<h1>Heritage Quest - Hero 32x32 Character Preview</h1>
<p class="subtitle">Indian Ethnicity &bull; Authentic Golden Yellow Kurta &bull; Pleated White Dhoti &bull; Crimson Sash &bull; Curved Talwar</p>

<div class="container">
  <div class="preview-card" style="flex: 1; min-width: 340px; max-width: 440px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
      <h2 id="current-anim-name" style="margin: 0; font-size: 20px; color: var(--accent);">Idle</h2>
      <span id="frame-counter" class="info-tag">Frame 0 / 6</span>
    </div>

    <div class="canvas-box">
      <canvas id="view-canvas" width="256" height="256"></canvas>
    </div>

    <div class="controls">
      <div>
        <label style="font-size: 13px; color: var(--muted); margin-bottom: 6px; display: block;">Select Animation:</label>
        <div class="btn-group" id="anim-buttons">
          <button class="active" onclick="switchAnim('Idle')">Idle</button>
          <button onclick="switchAnim('Run')">Run</button>
          <button onclick="switchAnim('Jump')">Jump</button>
          <button onclick="switchAnim('Fall')">Fall</button>
          <button onclick="switchAnim('Attack')">Attack (Slash)</button>
          <button onclick="switchAnim('Attack2')">Attack2 (Cleave)</button>
          <button onclick="switchAnim('Hit')">Hit</button>
          <button onclick="switchAnim('Death')">Death</button>
        </div>
      </div>

      <div class="slider-row">
        <span>Zoom:</span>
        <button onclick="setZoom(4)" id="zoom-4">4x (128px)</button>
        <button class="active" onclick="setZoom(8)" id="zoom-8">8x (256px)</button>
        <button onclick="setZoom(12)" id="zoom-12">12x (384px)</button>
      </div>

      <div class="slider-row">
        <span>Speed:</span>
        <input type="range" id="speed-slider" min="1" max="24" value="6" oninput="updateSpeed(this.value)">
        <span id="speed-label">6 FPS</span>
      </div>

      <div class="btn-group">
        <button id="play-pause-btn" onclick="togglePlay()">Pause</button>
        <button onclick="stepFrame(-1)">&larr; Prev Frame</button>
        <button onclick="stepFrame(1)">Next Frame &rarr;</button>
      </div>
    </div>
  </div>

  <div class="preview-card" style="flex: 1; min-width: 400px;">
    <h2 style="margin-top: 0; color: var(--accent);">Character Design & Lore Specs</h2>
    <table style="width: 100%; border-collapse: collapse; font-size: 14px; line-height: 1.8;">
      <tr><td style="color: var(--muted); width: 140px;">Character:</td><td>Hero of <em>Heritage Quest</em></td></tr>
      <tr><td style="color: var(--muted);">Ethnicity:</td><td>Indian (warm golden-brown complexion, regal mustache, warrior hair)</td></tr>
      <tr><td style="color: var(--muted);">Upper Garment:</td><td>Authentic <strong>Yellow Kurta</strong> with Mandarin collar, gold buttons, and hip chaaks (side slits)</td></tr>
      <tr><td style="color: var(--muted);">Lower Garment:</td><td>Authentic <strong>White Dhoti</strong> with pleated central drape (kachha fold)</td></tr>
      <tr><td style="color: var(--muted);">Waist Sash:</td><td>Crimson Kamarband / Patka with dangling gold-fringed ends</td></tr>
      <tr><td style="color: var(--muted);">Footwear:</td><td>Traditional Leather Mojris / Jutis with pointed curled toes</td></tr>
      <tr><td style="color: var(--muted);">Primary Weapon:</td><td>Curved Indian <strong>Talwar</strong> with burnished brass disc pommel (katori)</td></tr>
      <tr><td style="color: var(--muted);">Resolution:</td><td>32x32 pixels per frame (pixel-perfect sprite alignment)</td></tr>
      <tr><td style="color: var(--muted);">Godot Engine:</td><td>Ready for <code>AnimatedSprite2D</code> or <code>SpriteFrames</code> (.tres included)</td></tr>
    </table>

    <div style="margin-top: 20px; padding: 12px; background: #0f172a; border-radius: 8px; border: 1px solid #334155; font-size: 13px;">
      <strong style="color: #38bdf8;">Animation Frame Breakdown:</strong>
      <ul style="margin: 8px 0 0 18px; padding: 0;">
        <li><strong>Idle:</strong> 6 frames &bull; Subtle chest breathing &bull; Eye blink &bull; Blade gleam</li>
        <li><strong>Run:</strong> 8 frames &bull; Full platformer cycle &bull; Dhoti billow &bull; Kurta flutter</li>
        <li><strong>Jump:</strong> 4 frames &bull; Launch crouch &bull; Rocket rise &bull; Apex tuck</li>
        <li><strong>Fall:</strong> 2 frames &bull; Upward wind cloth fluttering &bull; Landing ready</li>
        <li><strong>Attack:</strong> 6 frames &bull; Horizontal Talwar slash &bull; Curved cyan/gold energy arc</li>
        <li><strong>Attack2:</strong> 6 frames &bull; Overhead Talwar cleave &bull; Vertical shockwave arc</li>
        <li><strong>Hit:</strong> 3 frames &bull; Recoil shock &bull; Knockback stagger &bull; Recovery</li>
        <li><strong>Death:</strong> 8 frames &bull; Buckling knees &bull; Weapon drop &bull; Honorable fallen rest</li>
      </ul>
    </div>
  </div>
</div>

<div class="master-sheet-view">
  <h2 style="margin: 0 0 8px 0; color: var(--accent);">Master Sprite Sheet (All Animations)</h2>
  <p style="color: var(--muted); margin: 0 0 12px 0;">All 8 animation sequences consolidated into an 8x8 32x32 grid sheet (256x256 px):</p>
  <img src="HeritageQuest_Hero_Master_Sheet.png" alt="Master Sheet">
</div>

<script>
const animData = {{
  'Idle': {{ count: 6, speed: 6, loop: true, img: 'Idle.png' }},
  'Run': {{ count: 8, speed: 10, loop: true, img: 'Run.png' }},
  'Jump': {{ count: 4, speed: 6, loop: false, img: 'Jump.png' }},
  'Fall': {{ count: 2, speed: 6, loop: true, img: 'Fall.png' }},
  'Attack': {{ count: 6, speed: 8, loop: false, img: 'Attack.png' }},
  'Attack2': {{ count: 6, speed: 8, loop: false, img: 'Attack2.png' }},
  'Hit': {{ count: 3, speed: 6, loop: false, img: 'Hit.png' }},
  'Death': {{ count: 8, speed: 5, loop: false, img: 'Death.png' }},
}};

let currentAnim = 'Idle';
let currentFrame = 0;
let isPlaying = true;
let zoom = 8;
let images = {{}};
let timer = null;

const canvas = document.getElementById('view-canvas');
const ctx = canvas.getContext('2d');
ctx.imageSmoothingEnabled = false;

// Preload spritesheets
Object.keys(animData).forEach(key => {{
  const img = new Image();
  img.src = animData[key].img;
  images[key] = img;
}});

function switchAnim(name) {{
  currentAnim = name;
  currentFrame = 0;
  document.getElementById('current-anim-name').innerText = name;
  document.querySelectorAll('#anim-buttons button').forEach(btn => {{
    btn.classList.toggle('active', btn.innerText.includes(name));
  }});
  document.getElementById('speed-slider').value = animData[name].speed;
  document.getElementById('speed-label').innerText = animData[name].speed + ' FPS';
  resetTimer();
  render();
}}

function setZoom(z) {{
  zoom = z;
  const size = 32 * zoom;
  canvas.width = size;
  canvas.height = size;
  ctx.imageSmoothingEnabled = false;
  document.querySelectorAll('.slider-row button').forEach(btn => btn.classList.remove('active'));
  document.getElementById('zoom-' + z).classList.add('active');
  render();
}}

function updateSpeed(val) {{
  document.getElementById('speed-label').innerText = val + ' FPS';
  resetTimer();
}}

function togglePlay() {{
  isPlaying = !isPlaying;
  document.getElementById('play-pause-btn').innerText = isPlaying ? 'Pause' : 'Play';
  if (isPlaying) resetTimer();
  else clearInterval(timer);
}}

function stepFrame(delta) {{
  isPlaying = false;
  document.getElementById('play-pause-btn').innerText = 'Play';
  clearInterval(timer);
  const total = animData[currentAnim].count;
  currentFrame = (currentFrame + delta + total) % total;
  render();
}}

function resetTimer() {{
  clearInterval(timer);
  if (!isPlaying) return;
  const fps = parseInt(document.getElementById('speed-slider').value);
  timer = setInterval(() => {{
    const total = animData[currentAnim].count;
    const loop = animData[currentAnim].loop;
    if (currentFrame + 1 >= total) {{
      if (loop) currentFrame = 0;
    }} else {{
      currentFrame++;
    }}
    render();
  }}, 1000 / fps);
}}

function render() {{
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const img = images[currentAnim];
  if (!img || !img.complete) {{
    setTimeout(render, 50);
    return;
  }}
  const sx = currentFrame * 32;
  ctx.drawImage(img, sx, 0, 32, 32, 0, 0, canvas.width, canvas.height);
  document.getElementById('frame-counter').innerText = 'Frame ' + currentFrame + ' / ' + animData[currentAnim].count;
}}

images['Idle'].onload = () => {{
  setZoom(8);
  resetTimer();
}};
</script>

</body>
</html>
"""
    with open(html_path, 'w', encoding='utf-8') as fp:
        fp.write(html_content)
    print(f"Generated HTML preview: {html_path}")


if __name__ == '__main__':
    print("Building Heritage Quest 32x32 Character Assets...")
    build_all_assets()
    print("All assets successfully built!")
