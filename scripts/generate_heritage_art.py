"""
Heritage Quest - Indian Heritage Sites Backdrops & Themed Tilesets Generator
Generates pixel-perfect panoramic parallax backdrops and themed 32x32 tilesets for:
1. Red Fort / Lal Qila (Delhi) - Mughal Sandstone Citadel
2. Hampi / Vijayanagara (Karnataka) - Ancient Granite Temples & Monoliths
3. Raigad Fort (Maharashtra) - Sahyadri Mountain Cliffside Citadel
"""

import os
import math
import zlib
import struct

def create_png(width, height, rgba_data):
    def chunk(chunk_type, data):
        return struct.pack('>I', len(data)) + chunk_type + data + struct.pack('>I', zlib.crc32(chunk_type + data) & 0xffffffff)

    raw = bytearray()
    for y in range(height):
        raw.append(0) # None filter
        for x in range(width):
            r, g, b, a = rgba_data[y * width + x]
            raw.extend((r, g, b, a))

    compressed = zlib.compress(bytes(raw), 9)
    ihdr = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', compressed) + chunk(b'IEND', b'')


class Canvas:
    def __init__(self, w, h, bg=(0,0,0,0)):
        self.w = w
        self.h = h
        self.pixels = [bg for _ in range(w * h)]

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.pixels[y * self.w + x] = color

    def get(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.pixels[y * self.w + x]
        return (0, 0, 0, 0)

    def blend(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            sr, sg, sb, sa = color
            if sa == 0: return
            if sa == 255:
                self.pixels[y * self.w + x] = color
                return
            idx = y * self.w + x
            dr, dg, db, da = self.pixels[idx]
            alpha = sa / 255.0
            inv = 1.0 - alpha
            nr = int(sr * alpha + dr * inv)
            ng = int(sg * alpha + dg * inv)
            nb = int(sb * alpha + db * inv)
            na = min(255, int(sa + da * inv))
            self.pixels[idx] = (nr, ng, nb, na)

    def rect(self, x1, y1, x2, y2, color):
        for y in range(max(0, y1), min(self.h, y2 + 1)):
            for x in range(max(0, x1), min(self.w, x2 + 1)):
                self.set(x, y, color)

    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as fp:
            fp.write(create_png(self.w, self.h, self.pixels))
        print(f"Saved: {path} ({self.w}x{self.h})")


# =========================================================================
# BACKDROP GENERATION (576 x 324)
# =========================================================================

def lerp_color(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
        int(c1[3] + (c2[3] - c1[3]) * t)
    )

# -------------------------------------------------------------------------
# LEVEL 1: RED FORT (DELHI)
# -------------------------------------------------------------------------
def generate_red_fort_backdrop():
    w, h = 576, 324
    base_dir = "assets/images/backgrounds/red_fort"
    os.makedirs(base_dir, exist_ok=True)

    # 1. Sky Layer (Twilight Sunset Gradient + Glowing Sun + Cloud Strata)
    sky = Canvas(w, h)
    col_top = (46, 16, 101, 255)     # Deep twilight purple
    col_mid1 = (194, 65, 12, 255)    # Fiery orange-red
    col_mid2 = (245, 158, 11, 255)   # Amber gold
    col_bot = (254, 240, 138, 255)   # Golden haze at horizon

    for y in range(h):
        t = y / float(h)
        if t < 0.35:
            c = lerp_color(col_top, col_mid1, t / 0.35)
        elif t < 0.7:
            c = lerp_color(col_mid1, col_mid2, (t - 0.35) / 0.35)
        else:
            c = lerp_color(col_mid2, col_bot, (t - 0.7) / 0.3)
        # Subtle dithering
        for x in range(w):
            dither = ((x ^ y) & 1) * 3 - 1
            rc = (max(0, min(255, c[0] + dither)), max(0, min(255, c[1] + dither)), max(0, min(255, c[2] + dither)), 255)
            sky.set(x, y, rc)

    # Golden Sun setting near horizon (x=410, y=190)
    sun_x, sun_y = 410, 190
    for y in range(sun_y - 28, sun_y + 29):
        for x in range(sun_x - 28, sun_x + 29):
            d = math.hypot(x - sun_x, y - sun_y)
            if d < 18:
                sky.set(x, y, (255, 255, 230, 255))
            elif d < 28:
                alpha = int((1.0 - (d - 18) / 10.0) * 180)
                sky.blend(x, y, (254, 215, 170, alpha))

    # Twilight clouds
    for cx, cy, clen in [(80, 70, 110), (280, 110, 140), (450, 60, 90), (160, 140, 100)]:
        for dx in range(-clen // 2, clen // 2):
            factor = 1.0 - (2 * abs(dx) / clen)**2
            ch = int(5 * factor)
            for dy in range(-ch, ch + 1):
                sky.blend(cx + dx, cy + dy, (120, 30, 80, 120))
                if dy == ch:
                    sky.blend(cx + dx, cy + dy, (245, 158, 11, 160)) # Golden under-lighting!

    sky.save(f"{base_dir}/sky.png")

    # 2. Far Layer: Distant Shahjahanabad Skyline (Domes, Jama Masjid, Minarets)
    far = Canvas(w, h)
    far_color = (136, 19, 55, 210)       # Dark rose / maroon silhouette
    far_color_sh = (100, 12, 40, 230)
    far_highlight = (244, 63, 94, 210)

    # Distant fortress wall baseline
    base_y = 195
    for x in range(w):
        # Rolling citadel wall
        wall_h = int(15 + 4 * math.sin(x * 0.03))
        for y in range(base_y - wall_h, h):
            far.set(x, y, far_color)

    # Monuments in distance:
    # Jama Masjid style double minarets & domes at x=140
    def draw_far_dome(can, cx, cy, radius, col):
        for y in range(cy - radius, cy + 1):
            dy = cy - y
            dx = int(math.sqrt(max(0, radius*radius - dy*dy)))
            for x in range(cx - dx, cx + dx + 1):
                can.set(x, y, col)
        # Finial (Kalash spire)
        for y in range(cy - radius - 5, cy - radius):
            can.set(cx, y, far_highlight)

    def draw_far_minaret(can, cx, base_y, top_y, width, col):
        can.rect(cx - width // 2, top_y, cx + width // 2, base_y, col)
        # Chhatri dome on top
        draw_far_dome(can, cx, top_y, width + 1, far_highlight)

    # Jama Masjid domes & minarets at x=140
    draw_far_minaret(far, 110, base_y, 130, 5, far_color_sh)
    draw_far_dome(far, 130, 160, 12, far_color_sh)
    draw_far_dome(far, 150, 150, 16, far_color_sh) # Central great dome
    draw_far_dome(far, 170, 160, 12, far_color_sh)
    draw_far_minaret(far, 190, base_y, 130, 5, far_color_sh)

    # Distant Red Fort Chhatris & Watchtowers at x=320, x=480
    draw_far_minaret(far, 310, base_y, 155, 6, far_color)
    draw_far_minaret(far, 360, base_y, 160, 6, far_color)
    draw_far_minaret(far, 470, base_y, 150, 7, far_color)
    draw_far_minaret(far, 530, base_y, 165, 5, far_color)

    # Distant battlements crenellations (merlons)
    for x in range(0, w, 8):
        far.rect(x, base_y - 20, x + 4, base_y - 15, far_color)

    far.save(f"{base_dir}/monuments_far.png")

    # 3. Midground Layer: Red Fort Ramparts, Lahori Gate & Ornate Arches
    mid = Canvas(w, h)
    c_stone = (185, 28, 28, 255)       # Red Sandstone
    c_stone_hi = (220, 38, 38, 255)    # Sandstone Sunlit
    c_stone_sh = (127, 29, 29, 255)    # Sandstone Shadow
    c_marble = (248, 250, 252, 255)    # White Marble Pavilions
    c_gold = (251, 191, 36, 255)       # Gilded Spire

    # High Red Sandstone Wall across middle
    wall_top = 220
    for x in range(w):
        for y in range(wall_top, h):
            # Brick pattern
            brick_row = (y - wall_top) // 6
            brick_col = (x + (3 if brick_row % 2 == 1 else 0)) // 12
            if (y - wall_top) % 6 == 0 or (x + (3 if brick_row % 2 == 1 else 0)) % 12 == 0:
                mid.set(x, y, c_stone_sh)
            else:
                mid.set(x, y, c_stone)

    # Wall stringcourse / trim molding
    for x in range(w):
        mid.set(x, wall_top - 1, c_stone_hi)
        mid.set(x, wall_top, c_stone_hi)
        mid.set(x, wall_top + 1, c_stone_sh)

    # Red Sandstone Merlons / Battlements (Crenellations)
    for x in range(0, w, 16):
        # Pointed arched merlons
        mid.rect(x + 2, wall_top - 10, x + 10, wall_top - 2, c_stone)
        # Pointed top tip
        mid.rect(x + 4, wall_top - 13, x + 8, wall_top - 11, c_stone_hi)
        mid.set(x + 6, wall_top - 14, c_stone_hi)
        # Arrow slit in merlon
        mid.set(x + 6, wall_top - 7, (24, 20, 18, 255))
        mid.set(x + 6, wall_top - 6, (24, 20, 18, 255))

    # Octagonal Bastion Towers at x=120 and x=420
    for bx in [120, 420]:
        mid.rect(bx - 24, wall_top - 30, bx + 24, h, c_stone)
        # Shading
        mid.rect(bx - 24, wall_top - 30, bx - 14, h, c_stone_sh)
        mid.rect(bx + 14, wall_top - 30, bx + 24, h, c_stone_hi)
        # White Marble Diwan-i-Khas style Chhatri on top of the Bastion
        # Pillars
        for px in [bx - 16, bx - 6, bx + 6, bx + 16]:
            mid.rect(px - 1, wall_top - 52, px + 1, wall_top - 30, c_marble)
        # Marble dome
        for y in range(wall_top - 65, wall_top - 52):
            dy = (wall_top - 52) - y
            rx = int(math.sqrt(max(0, 14*14 - dy*dy * 1.1)))
            mid.rect(bx - rx, y, bx + rx, y, c_marble)
        # Gold finial
        for y in range(wall_top - 72, wall_top - 65):
            mid.set(bx, y, c_gold)

    # Grand Mughal Cusped Arched Gate at x=270 (Lahori Gate)
    gx = 270
    gy = wall_top + 10
    # Outer gate frame
    mid.rect(gx - 28, gy - 20, gx + 28, h, c_stone_hi)
    # Deep inner arched opening
    for y in range(gy - 5, h):
        for x in range(gx - 18, gx + 19):
            if y < gy + 15:
                # Cusped arch curve
                dy = (gy + 15) - y
                rx = int(18 - dy * 0.7)
                if abs(x - gx) <= rx:
                    mid.set(x, y, (30, 10, 10, 255))
            else:
                mid.set(x, y, (20, 5, 5, 255))

    # Flying Swallowtail Banners / Flags on bastions
    for fx in [144, 444]:
        for y in range(wall_top - 80, wall_top - 60):
            mid.set(fx, y, (120, 53, 15, 255)) # Staff
        # Crimson & gold flag fluttering
        for dx in range(1, 14):
            mid.set(fx + dx, wall_top - 80 + int(math.sin(dx * 0.6) * 2), (220, 38, 38, 255))
            mid.set(fx + dx, wall_top - 79 + int(math.sin(dx * 0.6) * 2), (251, 191, 36, 255))

    mid.save(f"{base_dir}/fort_mid.png")


# -------------------------------------------------------------------------
# LEVEL 2: HAMPI (VIJAYANAGARA)
# -------------------------------------------------------------------------
def generate_hampi_backdrop():
    w, h = 576, 324
    base_dir = "assets/images/backgrounds/hampi"
    os.makedirs(base_dir, exist_ok=True)

    # 1. Sky Layer (Golden Dawn over Tungabhadra river)
    sky = Canvas(w, h)
    c_dawn1 = (74, 4, 78, 255)       # Deep purple dawn
    c_dawn2 = (194, 65, 12, 255)     # Saffron rose
    c_dawn3 = (251, 146, 60, 255)    # Morning gold
    c_dawn4 = (254, 240, 138, 255)   # Mist radiance

    for y in range(h):
        t = y / float(h)
        if t < 0.4:
            c = lerp_color(c_dawn1, c_dawn2, t / 0.4)
        elif t < 0.75:
            c = lerp_color(c_dawn2, c_dawn3, (t - 0.4) / 0.35)
        else:
            c = lerp_color(c_dawn3, c_dawn4, (t - 0.75) / 0.25)
        for x in range(w):
            dither = ((x ^ y) & 1) * 2 - 1
            rc = (max(0, min(255, c[0] + dither)), max(0, min(255, c[1] + dither)), max(0, min(255, c[2] + dither)), 255)
            sky.set(x, y, rc)

    sky.save(f"{base_dir}/sky.png")

    # 2. Far Layer: Boulders, Matanga Hill & River Tungabhadra
    far = Canvas(w, h)
    c_boulder_far = (133, 77, 60, 210)
    c_boulder_sh = (92, 50, 40, 230)
    c_water = (253, 186, 116, 220)   # River reflection of dawn

    # River strip at horizon (y=200 to 225)
    for y in range(200, 225):
        for x in range(w):
            far.set(x, y, c_water)

    # Giant Granite Boulder Hills (Matanga & Hemakuta Hills)
    # Series of rounded huge rocks stacked on each other
    def draw_far_boulder(can, cx, cy, rx, ry, col):
        for y in range(cy - ry, cy + ry + 1):
            dy = (y - cy) / float(ry)
            if abs(dy) <= 1.0:
                dx = int(rx * math.sqrt(1.0 - dy*dy))
                for x in range(cx - dx, cx + dx + 1):
                    can.set(x, y, col)

    # Distant rocky peaks
    for bx, by, rx, ry in [
        (80, 180, 70, 45), (140, 175, 55, 40), (220, 185, 80, 40),
        (340, 170, 95, 55), (420, 180, 60, 35), (500, 175, 75, 50)
    ]:
        draw_far_boulder(far, bx, by, rx, ry, c_boulder_far)

    # Boulder shading & highlights
    for bx, by, rx, ry in [
        (80, 180, 70, 45), (340, 170, 95, 55), (500, 175, 75, 50)
    ]:
        draw_far_boulder(far, bx - 8, by - 4, rx - 8, ry - 6, c_boulder_sh)

    # Distant small mandapas on hilltops
    for tx in [130, 340]:
        far.rect(tx - 6, 120, tx + 6, 130, c_boulder_sh)
        far.rect(tx - 8, 117, tx + 8, 120, c_boulder_sh)
        far.set(tx, 115, (254, 240, 138, 255))

    far.save(f"{base_dir}/hills_far.png")

    # 3. Midground Layer: Virupaksha Gopuram (Temple Tower), Monolithic Pillars & Coconut Palms
    mid = Canvas(w, h)
    c_granite = (168, 162, 158, 255)
    c_granite_sh = (120, 113, 108, 255)
    c_granite_hi = (214, 211, 209, 255)
    c_palm_trunk = (120, 53, 15, 255)
    c_palm_frond = (34, 130, 56, 255)
    c_palm_hi = (74, 222, 128, 255)

    # Great Dravidian Gopuram (Pyramidal Temple Tower) at x=200
    gox = 200
    base_gopuram_y = 260
    tiers = 7
    tier_w = 48
    tier_h = 16
    for t in range(tiers):
        ty = base_gopuram_y - (t + 1) * tier_h
        cw = int(tier_w * (1.0 - t * 0.09))
        mid.rect(gox - cw, ty, gox + cw, ty + tier_h, c_granite)
        # Tier horizontal shelf
        mid.rect(gox - cw - 2, ty, gox + cw + 2, ty + 2, c_granite_hi)
        # Carved deity relief niches
        for nx in range(gox - cw + 4, gox + cw - 4, 8):
            mid.rect(nx, ty + 4, nx + 4, ty + tier_h - 2, c_granite_sh)
            mid.set(nx + 2, ty + 6, c_granite_hi) # Mini sculpted idol
    # Kalash barrel roof (Shikhara / Stupika) on top of Gopuram
    shikhara_y = base_gopuram_y - (tiers) * tier_h - 10
    mid.rect(gox - 18, shikhara_y, gox + 18, shikhara_y + 10, c_granite_hi)
    for kx in range(gox - 12, gox + 13, 6):
        mid.rect(kx - 1, shikhara_y - 6, kx + 1, shikhara_y, (251, 191, 36, 255)) # Golden Kalash pot!

    # Monolithic Carved Dravidian Stone Pillars (Kalyana Mandapa)
    for px in [60, 110, 320, 370, 440, 510]:
        py = 230
        # Pillar base
        mid.rect(px - 5, py + 25, px + 5, py + 30, c_granite_sh)
        # Shaft
        mid.rect(px - 3, py - 15, px + 3, py + 25, c_granite)
        mid.rect(px - 3, py - 15, px - 2, py + 25, c_granite_hi)
        # Carved Yali (mythical lion-elephant) bracket capital
        mid.rect(px - 7, py - 20, px + 7, py - 15, c_granite_hi)
        mid.set(px - 6, py - 18, c_granite_sh)
        mid.set(px + 6, py - 18, c_granite_sh)
        # Architrave stone beam across pillars
        mid.rect(px - 26, py - 24, px + 26, py - 20, c_granite_hi)

    # Stone Chariot (Kallina Ratha) silhouette at x=370
    rcx = 370
    rcy = 235
    # Chariot wheels
    for wx in [rcx - 14, rcx + 14]:
        for dy in range(-7, 8):
            for dx in range(-7, 8):
                if 5 <= dx*dx + dy*dy <= 49:
                    mid.set(wx + dx, rcy + 15 + dy, c_granite_sh)
                elif dx*dx + dy*dy <= 4:
                    mid.set(wx + dx, rcy + 15 + dy, c_granite_hi)
    # Chariot shrine body
    mid.rect(rcx - 18, rcy - 10, rcx + 18, rcy + 14, c_granite)
    mid.rect(rcx - 12, rcy - 22, rcx + 12, rcy - 10, c_granite_hi)

    # Lush Coconut Palm Trees framing the scene at x=30, x=480, x=550
    def draw_palm(can, px, py, height):
        # Trunk
        for y in range(py - height, py):
            dx = int(math.sin((py - y) * 0.05) * 5)
            can.set(px + dx, y, c_palm_trunk)
            can.set(px + dx + 1, y, c_palm_trunk)
        # Crown fronds
        top_x = px + int(math.sin(height * 0.05) * 5)
        top_y = py - height
        for angle_deg in [-140, -100, -60, -30, 0, 30, 60, 100, 140]:
            rad = math.radians(angle_deg)
            for r in range(4, 28):
                fx = int(top_x + r * math.cos(rad))
                fy = int(top_y + r * math.sin(rad) + (r * 0.25)**2 * 0.1) # Drooping curve
                can.set(fx, fy, c_palm_frond)
                if r % 3 == 0: can.set(fx, fy - 1, c_palm_hi)

    draw_palm(mid, 24, 270, 95)
    draw_palm(mid, 40, 270, 80)
    draw_palm(mid, 480, 260, 85)
    draw_palm(mid, 550, 270, 90)

    mid.save(f"{base_dir}/temple_mid.png")


# -------------------------------------------------------------------------
# LEVEL 3: RAIGAD FORT (SAHYADRI / MARATHA)
# -------------------------------------------------------------------------
def generate_raigad_backdrop():
    w, h = 576, 324
    base_dir = "assets/images/backgrounds/raigad"
    os.makedirs(base_dir, exist_ok=True)

    # 1. Sky Layer (Stormy Sahyadri Mountain Mist & Twilight Sky)
    sky = Canvas(w, h)
    c_sky1 = (15, 23, 42, 255)       # Slate navy
    c_sky2 = (30, 41, 59, 255)       # Sahyadri dark indigo
    c_sky3 = (56, 189, 248, 255)     # Glowing mountain dawn cleft
    c_mist = (224, 242, 254, 255)    # Swirling mountain fog

    for y in range(h):
        t = y / float(h)
        if t < 0.5:
            c = lerp_color(c_sky1, c_sky2, t / 0.5)
        elif t < 0.8:
            c = lerp_color(c_sky2, c_sky3, (t - 0.5) / 0.3)
        else:
            c = lerp_color(c_sky3, c_mist, (t - 0.8) / 0.2)
        for x in range(w):
            dither = ((x ^ y) & 1) * 3 - 1
            rc = (max(0, min(255, c[0] + dither)), max(0, min(255, c[1] + dither)), max(0, min(255, c[2] + dither)), 255)
            sky.set(x, y, rc)

    sky.save(f"{base_dir}/sky.png")

    # 2. Far Layer: Rugged Jagged Sahyadri Mountain Peaks in Deep Mist
    far = Canvas(w, h)
    c_cliff_far = (51, 65, 85, 220)
    c_cliff_sh = (30, 41, 59, 240)
    c_cliff_hi = (100, 116, 139, 220)

    # Mountain ridges with sheer vertical drops (typical Deccan Traps basalt cliffs)
    for x in range(w):
        # Stepped plateau basalt mountain profile
        px = x / 40.0
        m_h = int(100 + 40 * math.sin(px * 1.2) + 20 * math.cos(px * 3.4))
        # Basalt cliff steps
        m_h = (m_h // 12) * 12
        for y in range(h - m_h, h):
            far.set(x, y, c_cliff_far)

    # Add dramatic jagged pinnacle peaks (e.g. Lingana pinnacle next to Raigad)
    lingana_x = 380
    for y in range(90, h):
        w_l = int(max(0, 18 - (y - 90) * 0.15))
        far.rect(lingana_x - w_l, y, lingana_x + w_l, y, c_cliff_sh)
        far.set(lingana_x - w_l, y, c_cliff_hi)

    # Mist layers drifting between ridges
    for my in range(160, 240, 25):
        for x in range(w):
            mist_alpha = int(70 + 40 * math.sin(x * 0.04 + my))
            far.blend(x, my, (241, 245, 249, mist_alpha))
            far.blend(x, my + 1, (241, 245, 249, mist_alpha // 2))

    far.save(f"{base_dir}/cliffs_far.png")

    # 3. Midground Layer: Raigad Citadel Ramparts, Maha Darwaja & Saffron Bhagwa Dhwaj
    mid = Canvas(w, h)
    c_basalt = (71, 85, 105, 255)
    c_basalt_sh = (30, 41, 59, 255)
    c_basalt_hi = (148, 163, 184, 255)
    c_saffron = (249, 115, 22, 255)

    # Massive fortified stone mountain ramparts at base
    wall_y = 205
    for x in range(w):
        wy = wall_y + int(6 * math.sin(x * 0.025))
        for y in range(wy, h):
            # Basalt stone brick pattern
            r_idx = (y - wy) // 8
            c_idx = (x + (4 if r_idx % 2 == 1 else 0)) // 16
            if (y - wy) % 8 == 0 or (x + (4 if r_idx % 2 == 1 else 0)) % 16 == 0:
                mid.set(x, y, c_basalt_sh)
            else:
                mid.set(x, y, c_basalt)

    # Bastion watchtowers jutting over the cliff at x=100 and x=450
    for bx in [100, 450]:
        mid.rect(bx - 26, wall_y - 25, bx + 26, h, c_basalt)
        mid.rect(bx - 26, wall_y - 25, bx - 14, h, c_basalt_sh)
        mid.rect(bx + 14, wall_y - 25, bx + 26, h, c_basalt_hi)
        # Rounded watchtower roof
        for dy in range(1, 12):
            rw = int(26 - dy * 1.5)
            mid.rect(bx - rw, wall_y - 25 - dy, bx + rw, wall_y - 25 - dy, c_basalt_hi)

    # Grand Maha Darwaja (Great Gate flanked by twin massive bastions) at x=280
    mid.rect(255, wall_y - 15, 305, h, c_basalt_hi)
    # Iron-studded wooden gateway
    for y in range(wall_y - 5, h):
        for x in range(268, 292):
            if y < wall_y + 10:
                dy = (wall_y + 10) - y
                rx = int(12 - dy * 0.8)
                if abs(x - 280) <= rx:
                    mid.set(x, y, (20, 15, 10, 255))
            else:
                mid.set(x, y, (15, 10, 5, 255))
                # Brass door spikes
                if x in [272, 280, 288] and y % 8 == 0:
                    mid.set(x, y, (251, 191, 36, 255))

    # Proud Saffron Maratha Flags (Bhagwa Dhwaj - Swallowtail) on high towers
    for fx in [100, 280, 450]:
        fy = wall_y - 40
        # Flagpole
        for y in range(fy - 32, fy):
            mid.set(fx, y, (226, 232, 240, 255))
        # Swallowtail double-triangle saffron flag fluttering
        for dx in range(1, 20):
            flag_y = fy - 32 + int(math.sin(dx * 0.5) * 3)
            # Top triangle
            mid.set(fx + dx, flag_y, c_saffron)
            mid.set(fx + dx, flag_y + 1, c_saffron)
            if dx < 14:
                mid.set(fx + dx, flag_y + 2, c_saffron)
                mid.set(fx + dx, flag_y + 3, c_saffron)
            # Bottom swallowtail triangle
            if dx < 17:
                mid.set(fx + dx, flag_y + 5, c_saffron)
                mid.set(fx + dx, flag_y + 6, c_saffron)

    mid.save(f"{base_dir}/citadel_mid.png")


# =========================================================================
# THEMED TILESETS (256 x 256, 32x32 Tiles = 8x8 Grid)
# =========================================================================

def generate_tilesets():
    base_dir = "assets/images/tilesets"
    os.makedirs(base_dir, exist_ok=True)

    # 1. Red Fort Sandstone Citadel Tileset
    ts_red = Canvas(256, 256)
    c_red_base = (185, 28, 28, 255)
    c_red_hi = (239, 68, 68, 255)
    c_red_lit = (220, 38, 38, 255)
    c_red_sh = (127, 29, 29, 255)
    c_red_dk = (69, 10, 10, 255)
    c_gold = (251, 191, 36, 255)
    c_brass = (217, 119, 6, 255)

    def draw_sandstone_block(can, tx, ty, block_type):
        ox = tx * 32
        oy = ty * 32
        # Base fill
        for y in range(32):
            for x in range(32):
                can.set(ox + x, oy + y, c_red_base)
                # Subtle sandstone grain texture
                if (x + y * 3) % 7 == 0:
                    can.set(ox + x, oy + y, c_red_lit)
                elif (x * 2 + y) % 9 == 0:
                    can.set(ox + x, oy + y, c_red_sh)

        # Brick mortar lines (carved stone ashlar masonry)
        can.rect(ox, oy, ox + 31, oy, c_red_hi)
        can.rect(ox, oy + 15, ox + 31, oy + 15, c_red_sh)
        can.rect(ox, oy + 31, ox + 31, oy + 31, c_red_dk)
        # Vertical joint
        can.rect(ox + 16, oy, ox + 16, oy + 15, c_red_sh)
        can.rect(ox, oy + 16, ox, oy + 31, c_red_sh)

        if block_type == 'top':
            # Ornate floral relief / carved cornice trim
            for x in range(32):
                can.set(ox + x, oy, c_gold)
                can.set(ox + x, oy + 1, c_red_hi)
                can.set(ox + x, oy + 2, c_red_lit)
                # Lotus petal molding
                if x % 4 == 0: can.set(ox + x, oy + 3, c_gold)

        elif block_type == 'left':
            for y in range(32):
                can.set(ox, oy + y, c_red_hi)
                can.set(ox + 1, oy + y, c_red_lit)

        elif block_type == 'right':
            for y in range(32):
                can.set(ox + 31, oy + y, c_red_dk)
                can.set(ox + 30, oy + y, c_red_sh)

        elif block_type == 'platform':
            # Thin floating sandstone slab (10px high)
            for y in range(12, 32):
                for x in range(32): can.set(ox + x, oy + y, (0,0,0,0))
            for x in range(32):
                can.set(ox + x, oy, c_gold)
                can.set(ox + x, oy + 1, c_red_hi)
                can.set(ox + x, oy + 11, c_red_dk)

        elif block_type == 'crenellation':
            # Fort battlement merlon
            for y in range(0, 16):
                for x in range(0, 8): can.set(ox + x, oy + y, (0,0,0,0))
                for x in range(24, 32): can.set(ox + x, oy + y, (0,0,0,0))
            # Arrow loop slit
            can.rect(ox + 15, oy + 6, ox + 16, oy + 18, (24, 20, 18, 255))

        elif block_type == 'arch':
            # Mughal cusped archway
            for y in range(32):
                for x in range(32):
                    dy = 31 - y
                    curve = int(14.0 * math.sin(x * math.pi / 31.0))
                    if dy < curve:
                        can.set(ox + x, oy + y, (0,0,0,0))
                    elif dy == curve:
                        can.set(ox + x, oy + y, c_gold)

        elif block_type == 'pillar':
            # Sandstone carved pillar
            for y in range(32):
                for x in range(32): can.set(ox + x, oy + y, (0,0,0,0))
            can.rect(ox + 10, oy, ox + 21, oy + 31, c_red_base)
            can.rect(ox + 10, oy, ox + 12, oy + 31, c_red_hi)
            can.rect(ox + 19, oy, ox + 21, oy + 31, c_red_sh)
            # Lotus capital at top
            can.rect(ox + 6, oy, ox + 25, oy + 4, c_gold)

        elif block_type == 'lantern':
            # Hanging Mughal brass oil lamp / diya
            for y in range(32):
                for x in range(32): can.set(ox + x, oy + y, (0,0,0,0))
            # Chain
            for y in range(0, 12): can.set(ox + 16, oy + y, c_gold)
            # Lamp vessel
            can.rect(ox + 12, oy + 12, ox + 20, oy + 18, c_brass)
            can.rect(ox + 14, oy + 19, ox + 18, oy + 21, c_gold)
            # Glowing flame
            can.set(ox + 16, oy + 10, (255, 255, 255, 255))
            can.set(ox + 16, oy + 11, (254, 240, 138, 255))
            can.blend(ox + 15, oy + 11, (249, 115, 22, 200))
            can.blend(ox + 17, oy + 11, (249, 115, 22, 200))

    # Layout Sandstone Grid:
    draw_sandstone_block(ts_red, 0, 0, 'top')
    draw_sandstone_block(ts_red, 1, 0, 'top')
    draw_sandstone_block(ts_red, 2, 0, 'top')
    draw_sandstone_block(ts_red, 0, 1, 'left')
    draw_sandstone_block(ts_red, 1, 1, 'fill')
    draw_sandstone_block(ts_red, 2, 1, 'right')
    draw_sandstone_block(ts_red, 3, 0, 'platform')
    draw_sandstone_block(ts_red, 4, 0, 'platform')
    draw_sandstone_block(ts_red, 5, 0, 'platform')
    draw_sandstone_block(ts_red, 0, 2, 'crenellation')
    draw_sandstone_block(ts_red, 1, 2, 'arch')
    draw_sandstone_block(ts_red, 2, 2, 'pillar')
    draw_sandstone_block(ts_red, 3, 2, 'lantern')

    ts_red.save(f"{base_dir}/red_fort_sandstone.png")

    # 2. Hampi Granite Monolith & Temple Ruins Tileset
    ts_hampi = Canvas(256, 256)
    c_grn_base = (140, 134, 130, 255)
    c_grn_hi = (185, 180, 175, 255)
    c_grn_sh = (100, 95, 90, 255)
    c_grn_dk = (60, 56, 54, 255)
    c_moss = (74, 130, 60, 255)
    c_moss_hi = (110, 180, 80, 255)

    def draw_granite_block(can, tx, ty, block_type):
        ox = tx * 32
        oy = ty * 32
        for y in range(32):
            for x in range(32):
                can.set(ox + x, oy + y, c_grn_base)
                # Rough granite speckle texture
                if (x * 5 + y * 7) % 11 == 0:
                    can.set(ox + x, oy + y, c_grn_hi)
                elif (x * 3 + y * 2) % 13 == 0:
                    can.set(ox + x, oy + y, c_grn_sh)

        # Heavy monolithic joint lines
        can.rect(ox, oy, ox + 31, oy, c_grn_hi)
        can.rect(ox, oy + 31, ox + 31, oy + 31, c_grn_dk)
        can.rect(ox, oy, ox, oy + 31, c_grn_sh)
        can.rect(ox + 31, oy, ox + 31, oy + 31, c_grn_dk)

        if block_type == 'top':
            # Ancient weathered stone top with green moss patches
            for x in range(32):
                can.set(ox + x, oy, c_grn_hi)
                if (x % 7 < 4):
                    can.set(ox + x, oy, c_moss)
                    can.set(ox + x, oy + 1, c_moss_hi)
                    can.set(ox + x, oy + 2, c_moss)

        elif block_type == 'platform':
            for y in range(12, 32):
                for x in range(32): can.set(ox + x, oy + y, (0,0,0,0))
            for x in range(32):
                can.set(ox + x, oy, c_grn_hi)
                can.set(ox + x, oy + 11, c_grn_dk)
                if x % 5 < 3: can.set(ox + x, oy, c_moss_hi)

        elif block_type == 'pillar':
            for y in range(32):
                for x in range(32): can.set(ox + x, oy + y, (0,0,0,0))
            # Monolithic Dravidian carved pillar with central medallion
            can.rect(ox + 9, oy, ox + 22, oy + 31, c_grn_base)
            can.rect(ox + 9, oy, ox + 11, oy + 31, c_grn_hi)
            can.rect(ox + 20, oy, ox + 22, oy + 31, c_grn_sh)
            # Medallion in center
            can.rect(ox + 12, oy + 12, ox + 19, oy + 19, c_grn_hi)
            can.set(ox + 15, oy + 15, c_grn_dk)
            can.set(ox + 16, oy + 15, c_grn_dk)

        elif block_type == 'urn':
            # Ancient Sacred Terracotta / Brass Kalash Pot
            for y in range(32):
                for x in range(32): can.set(ox + x, oy + y, (0,0,0,0))
            can.rect(ox + 10, oy + 12, ox + 21, oy + 26, (194, 65, 12, 255))
            can.rect(ox + 12, oy + 8, ox + 19, oy + 11, (234, 88, 12, 255))
            # Mango leaves & coconut on top
            can.set(ox + 15, oy + 4, (120, 53, 15, 255))
            can.set(ox + 16, oy + 4, (120, 53, 15, 255))
            can.set(ox + 13, oy + 6, c_moss_hi)
            can.set(ox + 18, oy + 6, c_moss_hi)

    draw_granite_block(ts_hampi, 0, 0, 'top')
    draw_granite_block(ts_hampi, 1, 0, 'top')
    draw_granite_block(ts_hampi, 2, 0, 'top')
    draw_granite_block(ts_hampi, 0, 1, 'fill')
    draw_granite_block(ts_hampi, 1, 1, 'fill')
    draw_granite_block(ts_hampi, 2, 1, 'fill')
    draw_granite_block(ts_hampi, 3, 0, 'platform')
    draw_granite_block(ts_hampi, 4, 0, 'platform')
    draw_granite_block(ts_hampi, 5, 0, 'platform')
    draw_granite_block(ts_hampi, 0, 2, 'pillar')
    draw_granite_block(ts_hampi, 1, 2, 'urn')

    ts_hampi.save(f"{base_dir}/hampi_granite.png")

    # 3. Raigad Basalt Mountain Fortress Tileset
    ts_raigad = Canvas(256, 256)
    c_bas_base = (71, 85, 105, 255)
    c_bas_hi = (148, 163, 184, 255)
    c_bas_sh = (30, 41, 59, 255)
    c_bas_dk = (15, 23, 42, 255)
    c_wood = (120, 53, 15, 255)
    c_iron = (203, 213, 225, 255)

    def draw_basalt_block(can, tx, ty, block_type):
        ox = tx * 32
        oy = ty * 32
        for y in range(32):
            for x in range(32):
                can.set(ox + x, oy + y, c_bas_base)
                if (x + y * 2) % 8 == 0: can.set(ox + x, oy + y, c_bas_sh)
                elif (x * 2 + y) % 9 == 0: can.set(ox + x, oy + y, c_bas_hi)

        can.rect(ox, oy, ox + 31, oy, c_bas_hi)
        can.rect(ox, oy + 31, ox + 31, oy + 31, c_bas_dk)
        can.rect(ox, oy, ox, oy + 31, c_bas_sh)
        can.rect(ox + 31, oy, ox + 31, oy + 31, c_bas_dk)

        if block_type == 'top':
            for x in range(32):
                can.set(ox + x, oy, c_bas_hi)
                can.set(ox + x, oy + 1, c_bas_hi)

        elif block_type == 'platform':
            for y in range(12, 32):
                for x in range(32): can.set(ox + x, oy + y, (0,0,0,0))
            for x in range(32):
                can.set(ox + x, oy, c_bas_hi)
                can.set(ox + x, oy + 11, c_bas_dk)

        elif block_type == 'torch':
            for y in range(32):
                for x in range(32): can.set(ox + x, oy + y, (0,0,0,0))
            # Iron torch sconce on fort wall
            can.rect(ox + 14, oy + 14, ox + 18, oy + 28, c_wood)
            can.rect(ox + 12, oy + 12, ox + 20, oy + 15, c_iron)
            # Blazing torch fire
            can.set(ox + 16, oy + 6, (255, 255, 255, 255))
            can.set(ox + 16, oy + 7, (254, 240, 138, 255))
            can.rect(ox + 14, oy + 8, ox + 18, oy + 11, (249, 115, 22, 255))

    draw_basalt_block(ts_raigad, 0, 0, 'top')
    draw_basalt_block(ts_raigad, 1, 0, 'top')
    draw_basalt_block(ts_raigad, 2, 0, 'top')
    draw_basalt_block(ts_raigad, 0, 1, 'fill')
    draw_basalt_block(ts_raigad, 1, 1, 'fill')
    draw_basalt_block(ts_raigad, 2, 1, 'fill')
    draw_basalt_block(ts_raigad, 3, 0, 'platform')
    draw_basalt_block(ts_raigad, 4, 0, 'platform')
    draw_basalt_block(ts_raigad, 5, 0, 'platform')
    draw_basalt_block(ts_raigad, 0, 2, 'torch')

    ts_raigad.save(f"{base_dir}/raigad_basalt.png")


if __name__ == '__main__':
    print("Generating Indian Heritage Sites Parallax Backdrops...")
    generate_red_fort_backdrop()
    generate_hampi_backdrop()
    generate_raigad_backdrop()
    print("Generating Themed 32x32 Architectural Tilesets...")
    generate_tilesets()
    print("All backdrops and tilesets successfully generated!")
