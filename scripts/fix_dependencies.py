import os

def get_uid_from_file(path):
    if not os.path.exists(path):
        return ""
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if line.startswith('uid="'):
                return line.split('uid="')[1].split('"')[0]
            elif line.startswith('uid://'):
                return line
    return ""

def get_texture_uid(texture_path):
    import_path = texture_path + '.import'
    return get_uid_from_file(import_path)

def get_script_uid(script_path):
    uid_file = script_path + '.uid'
    return get_uid_from_file(uid_file)

# -------------------------------------------------------------------------
# 1. FIX HERO SPRITE FRAMES (.tres)
# -------------------------------------------------------------------------
def generate_hero_tres():
    path = "assets/images/player_32x32/hero_sprite_frames.tres"
    
    anims = [
        ("Idle", "Idle.png", 6, 1, 5.0),
        ("Run", "Run.png", 8, 1, 10.0),
        ("Jump", "Jump.png", 4, 0, 6.0),
        ("Fall", "Fall.png", 2, 1, 6.0),
        ("Attack", "Attack.png", 6, 0, 8.0),
        ("Attack1", "Attack1.png", 6, 0, 8.0),
        ("Attack2", "Attack2.png", 6, 0, 8.0),
        ("Hit", "Hit.png", 3, 0, 6.0),
        ("Death", "Death.png", 8, 0, 5.0),
    ]
    
    total_sub = sum(count for _, _, count, _, _ in anims)
    total_ext = len(anims)
    load_steps = total_ext + total_sub + 1
    
    lines = []
    lines.append(f'[gd_resource type="SpriteFrames" load_steps={load_steps} format=3]')
    lines.append('')
    
    # ExtResources
    for idx, (anim_name, file_name, _, _, _) in enumerate(anims):
        tex_path = f"assets/images/player_32x32/{file_name}"
        uid = get_texture_uid(tex_path)
        uid_attr = f' uid="{uid}"' if uid else ""
        ext_id = f"{idx + 1}_{anim_name.lower()}"
        lines.append(f'[ext_resource type="Texture2D"{uid_attr} path="res://{tex_path}" id="{ext_id}"]')
    lines.append('')
    
    # SubResources (AtlasTexture)
    for idx, (anim_name, file_name, count, _, _) in enumerate(anims):
        ext_id = f"{idx + 1}_{anim_name.lower()}"
        for f in range(count):
            sub_id = f"AtlasTexture_{anim_name.lower()}_{f}"
            lines.append(f'[sub_resource type="AtlasTexture" id="{sub_id}"]')
            lines.append(f'atlas = ExtResource("{ext_id}")')
            lines.append(f'region = Rect2({f * 32}, 0, 32, 32)')
            lines.append('')
            
    # Resource
    lines.append('[resource]')
    lines.append('animations = [{')
    
    anim_blocks = []
    for idx, (anim_name, file_name, count, loop, speed) in enumerate(anims):
        b = []
        b.append('"frames": [{')
        frame_items = []
        for f in range(count):
            sub_id = f"AtlasTexture_{anim_name.lower()}_{f}"
            frame_items.append(f'"duration": 1.0,\n"texture": SubResource("{sub_id}")')
        b.append('\n}, {\n'.join(frame_items))
        b.append('}],')
        b.append(f'"loop": {loop},')
        b.append(f'"name": &"{anim_name}",')
        b.append(f'"speed": {speed}')
        anim_blocks.append('\n'.join(b))
        
    lines.append('\n}, {\n'.join(anim_blocks))
    lines.append('}]')
    
    content = '\n'.join(lines) + '\n'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed: {path} ({load_steps} load steps, valid Godot 4 syntax)")

# -------------------------------------------------------------------------
# 2. FIX ARTIFACTS SPRITE FRAMES (.tres)
# -------------------------------------------------------------------------
def generate_artifacts_tres():
    path = "assets/images/artifacts/artifacts_sprite_frames.tres"
    
    items = [
        ("artifact_kohinoor", 4, 1, 5.0),
        ("artifact_nataraja", 4, 1, 5.0),
        ("artifact_ashoka_seal", 4, 1, 5.0),
        ("artifact_shivrai_coin", 6, 1, 6.0),
        ("artifact_manuscript", 4, 1, 5.0),
        ("powerup_turban", 4, 1, 5.0),
        ("powerup_angavastram", 4, 1, 5.0),
        ("powerup_vambrace", 4, 1, 5.0),
    ]
    
    total_sub = sum(count for _, count, _, _ in items)
    total_ext = len(items)
    load_steps = total_ext + total_sub + 1
    
    lines = []
    lines.append(f'[gd_resource type="SpriteFrames" load_steps={load_steps} format=3]')
    lines.append('')
    
    for idx, (item_name, _, _, _) in enumerate(items):
        tex_path = f"assets/images/artifacts/{item_name}.png"
        uid = get_texture_uid(tex_path)
        uid_attr = f' uid="{uid}"' if uid else ""
        ext_id = f"{idx + 1}_{item_name}"
        lines.append(f'[ext_resource type="Texture2D"{uid_attr} path="res://{tex_path}" id="{ext_id}"]')
    lines.append('')
    
    for idx, (item_name, count, _, _) in enumerate(items):
        ext_id = f"{idx + 1}_{item_name}"
        for f in range(count):
            sub_id = f"AtlasTexture_{item_name}_{f}"
            lines.append(f'[sub_resource type="AtlasTexture" id="{sub_id}"]')
            lines.append(f'atlas = ExtResource("{ext_id}")')
            lines.append(f'region = Rect2({f * 32}, 0, 32, 32)')
            lines.append('')
            
    lines.append('[resource]')
    lines.append('animations = [{')
    
    blocks = []
    for idx, (item_name, count, loop, speed) in enumerate(items):
        b = []
        b.append('"frames": [{')
        frame_items = []
        for f in range(count):
            sub_id = f"AtlasTexture_{item_name}_{f}"
            frame_items.append(f'"duration": 1.0,\n"texture": SubResource("{sub_id}")')
        b.append('\n}, {\n'.join(frame_items))
        b.append('}],')
        b.append(f'"loop": {loop},')
        b.append(f'"name": &"{item_name}",')
        b.append(f'"speed": {speed}')
        blocks.append('\n'.join(b))
        
    lines.append('\n}, {\n'.join(blocks))
    lines.append('}]')
    
    content = '\n'.join(lines) + '\n'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed: {path} ({load_steps} load steps, valid Godot 4 syntax)")

# -------------------------------------------------------------------------
# 3. FIX SCENES WITH UIDS
# -------------------------------------------------------------------------
def fix_player_scene():
    path = "scenes/Player.tscn"
    script_uid = get_script_uid("scripts/player.gd")
    script_uid_attr = f' uid="{script_uid}"' if script_uid else ""
    
    content = f"""[gd_scene format=3]

[ext_resource type="Script"{script_uid_attr} path="res://scripts/player.gd" id="1_player_script"]
[ext_resource type="SpriteFrames" path="res://assets/images/player_32x32/hero_sprite_frames.tres" id="2_player_frames"]

[sub_resource type="RectangleShape2D" id="RectangleShape2D_hero"]
size = Vector2(14, 26)

[node name="Player" type="CharacterBody2D"]
collision_layer = 1
collision_mask = 1
script = ExtResource("1_player_script")

[node name="AnimatedSprite2D" type="AnimatedSprite2D" parent="."]
texture_filter = 1
sprite_frames = ExtResource("2_player_frames")
animation = &"Idle"
autoplay = "Idle"

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
position = Vector2(0, 2)
shape = SubResource("RectangleShape2D_hero")
"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed: {path}")

def fix_artifact_scene():
    path = "scenes/components/Artifact.tscn"
    script_uid = get_script_uid("scripts/artifact.gd")
    script_uid_attr = f' uid="{script_uid}"' if script_uid else ""
    
    content = f"""[gd_scene format=3]

[ext_resource type="Script"{script_uid_attr} path="res://scripts/artifact.gd" id="1_script"]
[ext_resource type="SpriteFrames" path="res://assets/images/artifacts/artifacts_sprite_frames.tres" id="2_frames"]

[sub_resource type="CircleShape2D" id="CircleShape2D_item"]
radius = 12.0

[node name="Artifact" type="Area2D"]
collision_layer = 2
collision_mask = 1
script = ExtResource("1_script")

[node name="AnimatedSprite2D" type="AnimatedSprite2D" parent="."]
texture_filter = 1
sprite_frames = ExtResource("2_frames")
animation = &"artifact_kohinoor"
autoplay = "artifact_kohinoor"

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("CircleShape2D_item")

[node name="Label" type="Label" parent="."]
visible = false
offset_left = -60.0
offset_top = -24.0
offset_right = 60.0
offset_bottom = -8.0
theme_override_font_sizes/font_size = 10
horizontal_alignment = 1
"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed: {path}")

def fix_level1_scene():
    path = "scenes/levels/Level1_RedFort.tscn"
    sky_uid = get_texture_uid("assets/images/backgrounds/red_fort/sky.png")
    far_uid = get_texture_uid("assets/images/backgrounds/red_fort/monuments_far.png")
    mid_uid = get_texture_uid("assets/images/backgrounds/red_fort/fort_mid.png")
    tileset_uid = get_texture_uid("assets/images/tilesets/red_fort_sandstone.png")
    
    def uid_str(u): return f' uid="{u}"' if u else ""
    
    content = f"""[gd_scene format=3]

[ext_resource type="Texture2D"{uid_str(sky_uid)} path="res://assets/images/backgrounds/red_fort/sky.png" id="1_sky"]
[ext_resource type="Texture2D"{uid_str(far_uid)} path="res://assets/images/backgrounds/red_fort/monuments_far.png" id="2_far"]
[ext_resource type="Texture2D"{uid_str(mid_uid)} path="res://assets/images/backgrounds/red_fort/fort_mid.png" id="3_mid"]
[ext_resource type="PackedScene" path="res://scenes/Player.tscn" id="4_player"]
[ext_resource type="PackedScene" path="res://scenes/components/Artifact.tscn" id="5_artifact"]
[ext_resource type="PackedScene" path="res://scenes/components/LevelExit.tscn" id="6_exit"]
[ext_resource type="PackedScene" path="res://scenes/components/HUD.tscn" id="7_hud"]
[ext_resource type="Texture2D"{uid_str(tileset_uid)} path="res://assets/images/tilesets/red_fort_sandstone.png" id="8_tileset"]

[sub_resource type="RectangleShape2D" id="RectangleShape2D_ground"]
size = Vector2(2000, 108)

[sub_resource type="RectangleShape2D" id="RectangleShape2D_p1"]
size = Vector2(180, 20)

[sub_resource type="RectangleShape2D" id="RectangleShape2D_p2"]
size = Vector2(200, 20)

[sub_resource type="RectangleShape2D" id="RectangleShape2D_p3"]
size = Vector2(220, 20)

[sub_resource type="RectangleShape2D" id="RectangleShape2D_p4"]
size = Vector2(180, 20)

[sub_resource type="RectangleShape2D" id="RectangleShape2D_wall_l"]
size = Vector2(40, 800)

[sub_resource type="RectangleShape2D" id="RectangleShape2D_wall_r"]
size = Vector2(40, 800)

[node name="Level1_RedFort" type="Node2D"]

[node name="HUD" parent="." instance=ExtResource("7_hud")]

[node name="ParallaxBackground" type="ParallaxBackground" parent="."]

[node name="SkyLayer" type="ParallaxLayer" parent="ParallaxBackground"]
motion_scale = Vector2(0.1, 0.1)
motion_mirroring = Vector2(1152, 0)

[node name="SkySprite" type="Sprite2D" parent="ParallaxBackground/SkyLayer"]
texture_filter = 1
scale = Vector2(2, 2)
texture = ExtResource("1_sky")
centered = false

[node name="FarLayer" type="ParallaxLayer" parent="ParallaxBackground"]
motion_scale = Vector2(0.3, 0.2)
motion_mirroring = Vector2(1152, 0)

[node name="FarSprite" type="Sprite2D" parent="ParallaxBackground/FarLayer"]
texture_filter = 1
scale = Vector2(2, 2)
texture = ExtResource("2_far")
centered = false

[node name="MidLayer" type="ParallaxLayer" parent="ParallaxBackground"]
motion_scale = Vector2(0.6, 0.4)
motion_mirroring = Vector2(1152, 0)

[node name="MidSprite" type="Sprite2D" parent="ParallaxBackground/MidLayer"]
texture_filter = 1
scale = Vector2(2, 2)
texture = ExtResource("3_mid")
centered = false

[node name="Platforms" type="Node2D" parent="."]

[node name="Ground" type="StaticBody2D" parent="Platforms"]
position = Vector2(0, 540)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/Ground"]
position = Vector2(1000, 54)
shape = SubResource("RectangleShape2D_ground")

[node name="SandstoneGround" type="ColorRect" parent="Platforms/Ground"]
offset_right = 2000.0
offset_bottom = 108.0
color = Color(0.72549, 0.109804, 0.109804, 1)

[node name="CorniceTrim" type="ColorRect" parent="Platforms/Ground"]
offset_right = 2000.0
offset_bottom = 8.0
color = Color(0.984314, 0.74902, 0.141176, 1)

[node name="Platform1" type="StaticBody2D" parent="Platforms"]
position = Vector2(280, 440)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/Platform1"]
position = Vector2(90, 10)
shape = SubResource("RectangleShape2D_p1")

[node name="Visual" type="ColorRect" parent="Platforms/Platform1"]
offset_right = 180.0
offset_bottom = 20.0
color = Color(0.862745, 0.14902, 0.14902, 1)

[node name="GoldTrim" type="ColorRect" parent="Platforms/Platform1"]
offset_right = 180.0
offset_bottom = 4.0
color = Color(0.984314, 0.74902, 0.141176, 1)

[node name="Platform2" type="StaticBody2D" parent="Platforms"]
position = Vector2(540, 350)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/Platform2"]
position = Vector2(100, 10)
shape = SubResource("RectangleShape2D_p2")

[node name="Visual" type="ColorRect" parent="Platforms/Platform2"]
offset_right = 200.0
offset_bottom = 20.0
color = Color(0.862745, 0.14902, 0.14902, 1)

[node name="GoldTrim" type="ColorRect" parent="Platforms/Platform2"]
offset_right = 200.0
offset_bottom = 4.0
color = Color(0.984314, 0.74902, 0.141176, 1)

[node name="Platform3_DiwanIKhas" type="StaticBody2D" parent="Platforms"]
position = Vector2(820, 250)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/Platform3_DiwanIKhas"]
position = Vector2(110, 10)
shape = SubResource("RectangleShape2D_p3")

[node name="Visual" type="ColorRect" parent="Platforms/Platform3_DiwanIKhas"]
offset_right = 220.0
offset_bottom = 20.0
color = Color(0.95, 0.95, 0.98, 1)

[node name="GoldTrim" type="ColorRect" parent="Platforms/Platform3_DiwanIKhas"]
offset_right = 220.0
offset_bottom = 4.0
color = Color(0.984314, 0.74902, 0.141176, 1)

[node name="Platform4" type="StaticBody2D" parent="Platforms"]
position = Vector2(1180, 380)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/Platform4"]
position = Vector2(90, 10)
shape = SubResource("RectangleShape2D_p4")

[node name="Visual" type="ColorRect" parent="Platforms/Platform4"]
offset_right = 180.0
offset_bottom = 20.0
color = Color(0.862745, 0.14902, 0.14902, 1)

[node name="GoldTrim" type="ColorRect" parent="Platforms/Platform4"]
offset_right = 180.0
offset_bottom = 4.0
color = Color(0.984314, 0.74902, 0.141176, 1)

[node name="LeftBoundary" type="StaticBody2D" parent="Platforms"]
position = Vector2(-20, 300)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/LeftBoundary"]
shape = SubResource("RectangleShape2D_wall_l")

[node name="RightBoundary" type="StaticBody2D" parent="Platforms"]
position = Vector2(1920, 300)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/RightBoundary"]
shape = SubResource("RectangleShape2D_wall_r")

[node name="Collectibles" type="Node2D" parent="."]

[node name="Artifact_Turban" parent="Collectibles" instance=ExtResource("5_artifact")]
position = Vector2(370, 400)
item_id = "powerup_turban"
item_display_name = "Saffron Pagri (+1 HP)"
points = 200

[node name="Artifact_Manuscript" parent="Collectibles" instance=ExtResource("5_artifact")]
position = Vector2(640, 310)
item_id = "artifact_manuscript"
item_display_name = "Martial Arts Manuscript"
points = 300

[node name="Artifact_Kohinoor" parent="Collectibles" instance=ExtResource("5_artifact")]
position = Vector2(930, 200)
item_id = "artifact_kohinoor"
item_display_name = "Koh-i-Noor Diamond"
points = 1000

[node name="LevelExit" parent="." instance=ExtResource("6_exit")]
position = Vector2(1740, 540)
next_level_path = "res://scenes/levels/Level2_Hampi.tscn"
level_title = "Lal Qila (Red Fort) Cleared!"

[node name="Player" parent="." instance=ExtResource("4_player")]
position = Vector2(100, 480)
scale = Vector2(1.5, 1.5)

[node name="Camera2D" type="Camera2D" parent="Player"]
position = Vector2(0, -40)
limit_left = 0
limit_top = 0
limit_right = 1920
limit_bottom = 648
position_smoothing_enabled = true
"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed: {path}")

def fix_level2_scene():
    path = "scenes/levels/Level2_Hampi.tscn"
    sky_uid = get_texture_uid("assets/images/backgrounds/hampi/sky.png")
    far_uid = get_texture_uid("assets/images/backgrounds/hampi/hills_far.png")
    mid_uid = get_texture_uid("assets/images/backgrounds/hampi/temple_mid.png")
    
    def uid_str(u): return f' uid="{u}"' if u else ""
    
    content = f"""[gd_scene format=3]

[ext_resource type="Texture2D"{uid_str(sky_uid)} path="res://assets/images/backgrounds/hampi/sky.png" id="1_sky"]
[ext_resource type="Texture2D"{uid_str(far_uid)} path="res://assets/images/backgrounds/hampi/hills_far.png" id="2_far"]
[ext_resource type="Texture2D"{uid_str(mid_uid)} path="res://assets/images/backgrounds/hampi/temple_mid.png" id="3_mid"]
[ext_resource type="PackedScene" path="res://scenes/Player.tscn" id="4_player"]
[ext_resource type="PackedScene" path="res://scenes/components/Artifact.tscn" id="5_artifact"]
[ext_resource type="PackedScene" path="res://scenes/components/LevelExit.tscn" id="6_exit"]
[ext_resource type="PackedScene" path="res://scenes/components/HUD.tscn" id="7_hud"]

[sub_resource type="RectangleShape2D" id="RectangleShape2D_ground"]
size = Vector2(2100, 108)

[sub_resource type="RectangleShape2D" id="RectangleShape2D_p1"]
size = Vector2(180, 20)

[sub_resource type="RectangleShape2D" id="RectangleShape2D_p2"]
size = Vector2(200, 20)

[sub_resource type="RectangleShape2D" id="RectangleShape2D_p3"]
size = Vector2(220, 20)

[sub_resource type="RectangleShape2D" id="RectangleShape2D_p4"]
size = Vector2(180, 20)

[sub_resource type="RectangleShape2D" id="RectangleShape2D_wall_l"]
size = Vector2(40, 800)

[sub_resource type="RectangleShape2D" id="RectangleShape2D_wall_r"]
size = Vector2(40, 800)

[node name="Level2_Hampi" type="Node2D"]

[node name="HUD" parent="." instance=ExtResource("7_hud")]

[node name="ParallaxBackground" type="ParallaxBackground" parent="."]

[node name="SkyLayer" type="ParallaxLayer" parent="ParallaxBackground"]
motion_scale = Vector2(0.1, 0.1)
motion_mirroring = Vector2(1152, 0)

[node name="SkySprite" type="Sprite2D" parent="ParallaxBackground/SkyLayer"]
texture_filter = 1
scale = Vector2(2, 2)
texture = ExtResource("1_sky")
centered = false

[node name="FarLayer" type="ParallaxLayer" parent="ParallaxBackground"]
motion_scale = Vector2(0.3, 0.2)
motion_mirroring = Vector2(1152, 0)

[node name="FarSprite" type="Sprite2D" parent="ParallaxBackground/FarLayer"]
texture_filter = 1
scale = Vector2(2, 2)
texture = ExtResource("2_far")
centered = false

[node name="MidLayer" type="ParallaxLayer" parent="ParallaxBackground"]
motion_scale = Vector2(0.6, 0.4)
motion_mirroring = Vector2(1152, 0)

[node name="MidSprite" type="Sprite2D" parent="ParallaxBackground/MidLayer"]
texture_filter = 1
scale = Vector2(2, 2)
texture = ExtResource("3_mid")
centered = false

[node name="Platforms" type="Node2D" parent="."]

[node name="Ground" type="StaticBody2D" parent="Platforms"]
position = Vector2(0, 540)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/Ground"]
position = Vector2(1050, 54)
shape = SubResource("RectangleShape2D_ground")

[node name="GraniteGround" type="ColorRect" parent="Platforms/Ground"]
offset_right = 2100.0
offset_bottom = 108.0
color = Color(0.470588, 0.45098, 0.435294, 1)

[node name="MossTrim" type="ColorRect" parent="Platforms/Ground"]
offset_right = 2100.0
offset_bottom = 6.0
color = Color(0.290196, 0.509804, 0.235294, 1)

[node name="Platform1_Monolith" type="StaticBody2D" parent="Platforms"]
position = Vector2(260, 430)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/Platform1_Monolith"]
position = Vector2(90, 10)
shape = SubResource("RectangleShape2D_p1")

[node name="Visual" type="ColorRect" parent="Platforms/Platform1_Monolith"]
offset_right = 180.0
offset_bottom = 20.0
color = Color(0.55, 0.53, 0.51, 1)

[node name="Moss" type="ColorRect" parent="Platforms/Platform1_Monolith"]
offset_right = 180.0
offset_bottom = 4.0
color = Color(0.29, 0.51, 0.24, 1)

[node name="Platform2_Mandapa" type="StaticBody2D" parent="Platforms"]
position = Vector2(520, 330)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/Platform2_Mandapa"]
position = Vector2(100, 10)
shape = SubResource("RectangleShape2D_p2")

[node name="Visual" type="ColorRect" parent="Platforms/Platform2_Mandapa"]
offset_right = 200.0
offset_bottom = 20.0
color = Color(0.55, 0.53, 0.51, 1)

[node name="Platform3_GopuramApex" type="StaticBody2D" parent="Platforms"]
position = Vector2(820, 220)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/Platform3_GopuramApex"]
position = Vector2(110, 10)
shape = SubResource("RectangleShape2D_p3")

[node name="Visual" type="ColorRect" parent="Platforms/Platform3_GopuramApex"]
offset_right = 220.0
offset_bottom = 20.0
color = Color(0.65, 0.63, 0.61, 1)

[node name="GoldTrim" type="ColorRect" parent="Platforms/Platform3_GopuramApex"]
offset_right = 220.0
offset_bottom = 4.0
color = Color(0.984314, 0.74902, 0.141176, 1)

[node name="Platform4_StoneChariot" type="StaticBody2D" parent="Platforms"]
position = Vector2(1160, 360)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/Platform4_StoneChariot"]
position = Vector2(90, 10)
shape = SubResource("RectangleShape2D_p4")

[node name="Visual" type="ColorRect" parent="Platforms/Platform4_StoneChariot"]
offset_right = 180.0
offset_bottom = 20.0
color = Color(0.55, 0.53, 0.51, 1)

[node name="LeftBoundary" type="StaticBody2D" parent="Platforms"]
position = Vector2(-20, 300)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/LeftBoundary"]
shape = SubResource("RectangleShape2D_wall_l")

[node name="RightBoundary" type="StaticBody2D" parent="Platforms"]
position = Vector2(1960, 300)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/RightBoundary"]
shape = SubResource("RectangleShape2D_wall_r")

[node name="Collectibles" type="Node2D" parent="."]

[node name="Artifact_Angavastram" parent="Collectibles" instance=ExtResource("5_artifact")]
position = Vector2(350, 390)
item_id = "powerup_angavastram"
item_display_name = "Zari Angavastram (Double Jump)"
points = 350

[node name="Artifact_AshokaSeal" parent="Collectibles" instance=ExtResource("5_artifact")]
position = Vector2(620, 290)
item_id = "artifact_ashoka_seal"
item_display_name = "Ashoka Lion Capital Seal"
points = 400

[node name="Artifact_Nataraja" parent="Collectibles" instance=ExtResource("5_artifact")]
position = Vector2(930, 170)
item_id = "artifact_nataraja"
item_display_name = "Bronze Nataraja Idol"
points = 1000

[node name="LevelExit" parent="." instance=ExtResource("6_exit")]
position = Vector2(1820, 540)
next_level_path = "res://scenes/levels/Level3_Raigad.tscn"
level_title = "Hampi Ruins Cleared!"

[node name="Player" parent="." instance=ExtResource("4_player")]
position = Vector2(100, 480)
scale = Vector2(1.5, 1.5)

[node name="Camera2D" type="Camera2D" parent="Player"]
position = Vector2(0, -40)
limit_left = 0
limit_top = 0
limit_right = 1960
limit_bottom = 648
position_smoothing_enabled = true
"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed: {path}")

def fix_level3_scene():
    path = "scenes/levels/Level3_Raigad.tscn"
    sky_uid = get_texture_uid("assets/images/backgrounds/raigad/sky.png")
    far_uid = get_texture_uid("assets/images/backgrounds/raigad/cliffs_far.png")
    mid_uid = get_texture_uid("assets/images/backgrounds/raigad/citadel_mid.png")
    
    def uid_str(u): return f' uid="{u}"' if u else ""
    
    content = f"""[gd_scene format=3]

[ext_resource type="Texture2D"{uid_str(sky_uid)} path="res://assets/images/backgrounds/raigad/sky.png" id="1_sky"]
[ext_resource type="Texture2D"{uid_str(far_uid)} path="res://assets/images/backgrounds/raigad/cliffs_far.png" id="2_far"]
[ext_resource type="Texture2D"{uid_str(mid_uid)} path="res://assets/images/backgrounds/raigad/citadel_mid.png" id="3_mid"]
[ext_resource type="PackedScene" path="res://scenes/Player.tscn" id="4_player"]
[ext_resource type="PackedScene" path="res://scenes/components/Artifact.tscn" id="5_artifact"]
[ext_resource type="PackedScene" path="res://scenes/components/LevelExit.tscn" id="6_exit"]
[ext_resource type="PackedScene" path="res://scenes/components/HUD.tscn" id="7_hud"]

[sub_resource type="RectangleShape2D" id="RectangleShape2D_ground_a"]
size = Vector2(700, 108)

[sub_resource type="RectangleShape2D" id="RectangleShape2D_ground_b"]
size = Vector2(1000, 108)

[sub_resource type="RectangleShape2D" id="RectangleShape2D_p1"]
size = Vector2(180, 20)

[sub_resource type="RectangleShape2D" id="RectangleShape2D_p2"]
size = Vector2(160, 20)

[sub_resource type="RectangleShape2D" id="RectangleShape2D_p3"]
size = Vector2(220, 20)

[sub_resource type="RectangleShape2D" id="RectangleShape2D_p4"]
size = Vector2(180, 20)

[sub_resource type="RectangleShape2D" id="RectangleShape2D_wall_l"]
size = Vector2(40, 800)

[sub_resource type="RectangleShape2D" id="RectangleShape2D_wall_r"]
size = Vector2(40, 800)

[node name="Level3_Raigad" type="Node2D"]

[node name="HUD" parent="." instance=ExtResource("7_hud")]

[node name="ParallaxBackground" type="ParallaxBackground" parent="."]

[node name="SkyLayer" type="ParallaxLayer" parent="ParallaxBackground"]
motion_scale = Vector2(0.1, 0.1)
motion_mirroring = Vector2(1152, 0)

[node name="SkySprite" type="Sprite2D" parent="ParallaxBackground/SkyLayer"]
texture_filter = 1
scale = Vector2(2, 2)
texture = ExtResource("1_sky")
centered = false

[node name="FarLayer" type="ParallaxLayer" parent="ParallaxBackground"]
motion_scale = Vector2(0.3, 0.2)
motion_mirroring = Vector2(1152, 0)

[node name="FarSprite" type="Sprite2D" parent="ParallaxBackground/FarLayer"]
texture_filter = 1
scale = Vector2(2, 2)
texture = ExtResource("2_far")
centered = false

[node name="MidLayer" type="ParallaxLayer" parent="ParallaxBackground"]
motion_scale = Vector2(0.6, 0.4)
motion_mirroring = Vector2(1152, 0)

[node name="MidSprite" type="Sprite2D" parent="ParallaxBackground/MidLayer"]
texture_filter = 1
scale = Vector2(2, 2)
texture = ExtResource("3_mid")
centered = false

[node name="Platforms" type="Node2D" parent="."]

[node name="GroundA" type="StaticBody2D" parent="Platforms"]
position = Vector2(0, 540)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/GroundA"]
position = Vector2(350, 54)
shape = SubResource("RectangleShape2D_ground_a")

[node name="BasaltGround" type="ColorRect" parent="Platforms/GroundA"]
offset_right = 700.0
offset_bottom = 108.0
color = Color(0.278431, 0.333333, 0.411765, 1)

[node name="GroundB" type="StaticBody2D" parent="Platforms"]
position = Vector2(950, 540)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/GroundB"]
position = Vector2(500, 54)
shape = SubResource("RectangleShape2D_ground_b")

[node name="BasaltGround" type="ColorRect" parent="Platforms/GroundB"]
offset_right = 1000.0
offset_bottom = 108.0
color = Color(0.278431, 0.333333, 0.411765, 1)

[node name="Platform1_Watchtower" type="StaticBody2D" parent="Platforms"]
position = Vector2(320, 420)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/Platform1_Watchtower"]
position = Vector2(90, 10)
shape = SubResource("RectangleShape2D_p1")

[node name="Visual" type="ColorRect" parent="Platforms/Platform1_Watchtower"]
offset_right = 180.0
offset_bottom = 20.0
color = Color(0.35, 0.42, 0.52, 1)

[node name="Platform2_ChasmCross" type="StaticBody2D" parent="Platforms"]
position = Vector2(680, 380)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/Platform2_ChasmCross"]
position = Vector2(80, 10)
shape = SubResource("RectangleShape2D_p2")

[node name="Visual" type="ColorRect" parent="Platforms/Platform2_ChasmCross"]
offset_right = 160.0
offset_bottom = 20.0
color = Color(0.35, 0.42, 0.52, 1)

[node name="Platform3_MahaDarwaja" type="StaticBody2D" parent="Platforms"]
position = Vector2(980, 260)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/Platform3_MahaDarwaja"]
position = Vector2(110, 10)
shape = SubResource("RectangleShape2D_p3")

[node name="Visual" type="ColorRect" parent="Platforms/Platform3_MahaDarwaja"]
offset_right = 220.0
offset_bottom = 20.0
color = Color(0.42, 0.50, 0.60, 1)

[node name="SaffronBanner" type="ColorRect" parent="Platforms/Platform3_MahaDarwaja"]
offset_right = 220.0
offset_bottom = 4.0
color = Color(0.976471, 0.45098, 0.0862745, 1)

[node name="Platform4_Nagarkhana" type="StaticBody2D" parent="Platforms"]
position = Vector2(1350, 360)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/Platform4_Nagarkhana"]
position = Vector2(90, 10)
shape = SubResource("RectangleShape2D_p4")

[node name="Visual" type="ColorRect" parent="Platforms/Platform4_Nagarkhana"]
offset_right = 180.0
offset_bottom = 20.0
color = Color(0.35, 0.42, 0.52, 1)

[node name="LeftBoundary" type="StaticBody2D" parent="Platforms"]
position = Vector2(-20, 300)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/LeftBoundary"]
shape = SubResource("RectangleShape2D_wall_l")

[node name="RightBoundary" type="StaticBody2D" parent="Platforms"]
position = Vector2(2000, 300)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/RightBoundary"]
shape = SubResource("RectangleShape2D_wall_r")

[node name="Collectibles" type="Node2D" parent="."]

[node name="Artifact_Vambrace" parent="Collectibles" instance=ExtResource("5_artifact")]
position = Vector2(410, 370)
item_id = "powerup_vambrace"
item_display_name = "Mavala Steel Vambrace (+Attack)"
points = 400

[node name="Artifact_Shivrai1" parent="Collectibles" instance=ExtResource("5_artifact")]
position = Vector2(760, 330)
item_id = "artifact_shivrai_coin"
item_display_name = "Gold Shivrai Coin"
points = 250

[node name="Artifact_Shivrai2" parent="Collectibles" instance=ExtResource("5_artifact")]
position = Vector2(1090, 210)
item_id = "artifact_shivrai_coin"
item_display_name = "Gold Shivrai Coin"
points = 250

[node name="Artifact_AshokaSeal" parent="Collectibles" instance=ExtResource("5_artifact")]
position = Vector2(1440, 310)
item_id = "artifact_ashoka_seal"
item_display_name = "Royal Seal of Sovereignty"
points = 1000

[node name="LevelExit" parent="." instance=ExtResource("6_exit")]
position = Vector2(1850, 540)
next_level_path = "res://scenes/levels/Level1_RedFort.tscn"
level_title = "Raigad Fort Cleared! All Heritage Sites Liberated!"

[node name="Player" parent="." instance=ExtResource("4_player")]
position = Vector2(100, 480)
scale = Vector2(1.5, 1.5)

[node name="Camera2D" type="Camera2D" parent="Player"]
position = Vector2(0, -40)
limit_left = 0
limit_top = 0
limit_right = 2000
limit_bottom = 648
position_smoothing_enabled = true
"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed: {path}")

if __name__ == '__main__':
    print("Regenerating all dependencies with proper Godot 4 syntax and UIDs...")
    generate_hero_tres()
    generate_artifacts_tres()
    fix_player_scene()
    fix_artifact_scene()
    fix_level1_scene()
    fix_level2_scene()
    fix_level3_scene()
    print("All dependencies successfully repaired!")
