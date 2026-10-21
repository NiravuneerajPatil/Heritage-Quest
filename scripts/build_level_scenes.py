"""
Heritage Quest - Level Scenes Generator
Generates full Godot 4 Level scenes with multi-layer ParallaxBackgrounds,
authentic platform terrain, instanced Player, Camera2D, animated Artifacts, and HUD.

Levels:
1. scenes/levels/Level1_RedFort.tscn (Lal Qila, Delhi)
2. scenes/levels/Level2_Hampi.tscn (Vijayanagara Empire, Karnataka)
3. scenes/levels/Level3_Raigad.tscn (Maratha Empire, Maharashtra)
"""

import os

def create_platform_str(name, pos_x, pos_y, width, height, color_hex="b91c1c"):
    return f"""[node name="{name}" type="StaticBody2D" parent="Platforms"]
position = Vector2({pos_x}, {pos_y})

[node name="CollisionShape2D" type="CollisionShape2D" parent="Platforms/{name}"]
position = Vector2({width / 2.0}, {height / 2.0})
shape = SubResource("RectangleShape2D_plat_{name}")

[node name="ColorRect" type="ColorRect" parent="Platforms/{name}"]
offset_right = {width}.0
offset_bottom = {height}.0
color = Color({color_hex})
"""

def generate_level1():
    path = "scenes/levels/Level1_RedFort.tscn"
    content = """[gd_scene format=3]

[ext_resource type="Texture2D" path="res://assets/images/backgrounds/red_fort/sky.png" id="1_sky"]
[ext_resource type="Texture2D" path="res://assets/images/backgrounds/red_fort/monuments_far.png" id="2_far"]
[ext_resource type="Texture2D" path="res://assets/images/backgrounds/red_fort/fort_mid.png" id="3_mid"]
[ext_resource type="PackedScene" path="res://scenes/Player.tscn" id="4_player"]
[ext_resource type="PackedScene" path="res://scenes/components/Artifact.tscn" id="5_artifact"]
[ext_resource type="PackedScene" path="res://scenes/components/LevelExit.tscn" id="6_exit"]
[ext_resource type="PackedScene" path="res://scenes/components/HUD.tscn" id="7_hud"]
[ext_resource type="Texture2D" path="res://assets/images/tilesets/red_fort_sandstone.png" id="8_tileset"]

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
    with open(path, 'w', encoding='utf-8') as fp:
        fp.write(content)
    print(f"Generated Level 1: {path}")


def generate_level2():
    path = "scenes/levels/Level2_Hampi.tscn"
    content = """[gd_scene format=3]

[ext_resource type="Texture2D" path="res://assets/images/backgrounds/hampi/sky.png" id="1_sky"]
[ext_resource type="Texture2D" path="res://assets/images/backgrounds/hampi/hills_far.png" id="2_far"]
[ext_resource type="Texture2D" path="res://assets/images/backgrounds/hampi/temple_mid.png" id="3_mid"]
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
    with open(path, 'w', encoding='utf-8') as fp:
        fp.write(content)
    print(f"Generated Level 2: {path}")


def generate_level3():
    path = "scenes/levels/Level3_Raigad.tscn"
    content = """[gd_scene format=3]

[ext_resource type="Texture2D" path="res://assets/images/backgrounds/raigad/sky.png" id="1_sky"]
[ext_resource type="Texture2D" path="res://assets/images/backgrounds/raigad/cliffs_far.png" id="2_far"]
[ext_resource type="Texture2D" path="res://assets/images/backgrounds/raigad/citadel_mid.png" id="3_mid"]
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
    with open(path, 'w', encoding='utf-8') as fp:
        fp.write(content)
    print(f"Generated Level 3: {path}")


if __name__ == '__main__':
    print("Building Heritage Quest Level Scenes...")
    generate_level1()
    generate_level2()
    generate_level3()
    print("All level scenes generated successfully!")
