extends Area2D

# Heritage Quest - Expanded Fullscreen Lore & Artifact System

@onready var canvas_layer: CanvasLayer = $CanvasLayer if has_node("CanvasLayer") else null
@onready var color_rect: ColorRect = find_child("ColorRect", true, false) as ColorRect

@onready var title_label: Label = find_child("TitleLabel", true, false) as Label
@onready var lore_label: RichTextLabel = find_child("LoreLabel", true, false) as RichTextLabel
@onready var artifacts_container: VBoxContainer = find_child("ArtifactsContainer", true, false) as VBoxContainer

# Right-side Preview Elements
@onready var right_panel: PanelContainer = find_child("RightPanel", true, false) as PanelContainer
@onready var preview_texture: TextureRect = find_child("ArtifactLargeTexture", true, false) as TextureRect
@onready var preview_title: Label = find_child("PreviewTitleLabel", true, false) as Label
@onready var preview_desc: Label = find_child("ArtifactDescriptionLabel", true, false) as Label

# Navigation Buttons
@onready var next_button: Button = find_child("NextLevelButton", true, false) as Button
@onready var menu_button: Button = find_child("MenuButton", true, false) as Button

# -----------------------------------------------------------------------------
# EXPANDED HISTORICAL LORE (BBCode Formatted)
# -----------------------------------------------------------------------------
const LEVEL_LORE: Dictionary = {
	"Level1_RedFort": {
		"title": "Level Complete: Red Fort (Lal Qila) — Old Delhi",
		"lore": "[color=#F5C242][b]ARCHITECTURAL MARVEL OF THE MUGHAL ERA[/b][/color]\nCommissioned in 1638 by Emperor Shah Jahan upon shifting the empire's capital from Agra to Shahjahanabad, the Red Fort stands as an enduring symbol of Indian sovereignty. Constructed from massive blocks of red sandstone along the Yamuna River, its octagonal wall spans over 2.4 kilometers.\n\n[color=#E0A82E][b]Key Historical Features:[/b][/color]\n• [color=#FFFFFF]Lahori Gate:[/color] The grand ceremonial entrance facing the city of Delhi.\n• [color=#FFFFFF]Diwan-i-Aam & Diwan-i-Khas:[/color] Halls of public and private audience, once housing the legendary Peacock Throne.\n• [color=#FFFFFF]Architectural Fusion:[/color] A masterwork blending Islamic, Persian, Timurid, and traditional Hindu craftsmanship."
	},
	"Level2_Hampi": {
		"title": "Level Complete: Hampi — Vijayanagara, Karnataka",
		"lore": "[color=#F5C242][b]THE LOST METROPOLIS OF STONE[/b][/color]\nNestled among rugged boulder-strewn hills along the Tungabhadra River, Hampi was the thriving capital of the Vijayanagara Empire during the 14th to 16th centuries. At its height, it was one of the wealthiest and largest cities in the ancient world.\n\n[color=#E0A82E][b]Key Historical Features:[/b][/color]\n• [color=#FFFFFF]Vittala Temple Stone Chariot:[/color] An iconic monolithic shrine dedicated to Garuda.\n• [color=#FFFFFF]Virupaksha Temple:[/color] A towering 9-tiered gopuram dedicated to Lord Shiva that remains an active place of worship today.\n• [color=#FFFFFF]Elephant Stables & Aqueducts:[/color] Demonstrating sophisticated Indo-Islamic royal architecture and hydro-engineering."
	},
	"Level3_Raigad": {
		"title": "Level Complete: Raigad Fort — Sahyadri Mountains, Maharashtra",
		"lore": "[color=#F5C242][b]THE GIBRALTAR OF THE EAST[/b][/color]\nPerched 820 meters high in the Sahyadri mountain range, Raigad Fort served as the capital of the Maratha Empire under Chhatrapati Shivaji Maharaj, who was crowned here in 1674 as the Chhatrapati.\n\n[color=#E0A82E][b]Key Historical Features:[/b][/color]\n• [color=#FFFFFF]Maha Darwaja:[/color] A massive defensive gateway flanked by two natural bastion towers.\n• [color=#FFFFFF]Raj Sabha (Royal Court):[/color] Designed with acoustic engineering allowing whispered commands to echo across the throne hall.\n• [color=#FFFFFF]Hirakani Buruj:[/color] A legendary sheer cliff face named after a mother's bravery."
	},
	"Level4_Ujjain": {
		"title": "Level Complete: Ujjain — Shipra River, Madhya Pradesh",
		"lore": "[color=#F5C242][b]ANCIENT SEAT OF ASTRONOMY & FAITH[/b][/color]\nOne of the four sacred Kumbh Mela sites, Ujjain is one of India's oldest continuously inhabited cities. Under the reign of King Vikramaditya, it flourished as the premier center for ancient Indian mathematics, astronomy, and literature.\n\n[color=#E0A82E][b]Key Historical Features:[/b][/color]\n• [color=#FFFFFF]Mahakaleshwar Temple:[/color] Home to one of the 12 sacred Jyotirlingas, featuring a south-facing deity.\n• [color=#FFFFFF]Ancient Meridian Prime:[/color] Considered the Greenwich of ancient Indian astronomers for calculating planetary cycles.\n• [color=#FFFFFF]Vedh Shala Observatory:[/color] Constructed to measure celestial movements and precise timekeeping."
	}
}

# -----------------------------------------------------------------------------
# EXPANDED ARTIFACT CATALOG (Single-Frame Sliced Preview)
# -----------------------------------------------------------------------------
const ARTIFACT_DATA: Dictionary = {
	"powerup_turban": {
		"name": "Saffron Pagri",
		"subtitle": "Maratha Royal Headwear",
		"desc": "A vibrant saffron turban symbolizing valor, honor, and resilience. Worn by warrior-king commanders across the Deccan terrain.\n\n[color=#F5C242]Gameplay Perk:[/color] +1 Maximum Health Point & Stun Resistance.",
		"icon": "res://assets/images/artifacts/powerup_turban.png",
		"frame_size": Vector2(32, 32)
	},
	"artifact_manuscript": {
		"name": "Vedic Palm-Leaf Manuscript",
		"subtitle": "Ancient Astronomical Treatise",
		"desc": "Inscribed on treated palm leaves using a metal stylus, this rare manuscript preserves ancient mathematical formulas, seasonal crop calendars, and stellar alignments from Ujjain.\n\n[color=#F5C242]Gameplay Perk:[/color] Grants +500 Wisdom Score Points.",
		"icon": "res://assets/images/artifacts/artifact_manuscript.png",
		"frame_size": Vector2(32, 32)
	},
	"artifact_kohinoor": {
		"name": "Royal Crown Gem",
		"subtitle": "Jewel of Imperial Heritage",
		"desc": "Mined from the ancient Golconda region, this luminous uncut gemstone passed through imperial dynasties as an emblem of ultimate sovereignty and cultural pride.\n\n[color=#F5C242]Gameplay Perk:[/color] Unlocks 2x Score Multiplier.",
		"icon": "res://assets/images/artifacts/artifact_kohinoor.png",
		"frame_size": Vector2(32, 32)
	},
	"powerup_mojri": {
		"name": "Royal Gold Mojris",
		"subtitle": "Embroidered Heritage Footwear",
		"desc": "Handcrafted leather footwear woven with gold zari thread, designed for swift movement across temple courtyards and stone fortresses.\n\n[color=#F5C242]Gameplay Perk:[/color] Increases Movement Speed by 20%.",
		"icon": "res://assets/images/artifacts/powerup_mojri.png",
		"frame_size": Vector2(32, 32)
	}
}

var current_level_name: String = ""

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	if canvas_layer:
		canvas_layer.process_mode = Node.PROCESS_MODE_ALWAYS
		canvas_layer.hide()

	if not body_entered.is_connected(_on_body_entered):
		body_entered.connect(_on_body_entered)

	if next_button and not next_button.pressed.is_connected(_on_next_pressed):
		next_button.pressed.connect(_on_next_pressed)
	if menu_button and not menu_button.pressed.is_connected(_on_menu_pressed):
		menu_button.pressed.connect(_on_menu_pressed)

	_apply_fullscreen_theme()

func _on_body_entered(body: Node2D) -> void:
	if body.is_in_group("Player") or "Player" in body.name or body is CharacterBody2D:
		show_exit_summary()

func show_exit_summary() -> void:
	current_level_name = get_tree().current_scene.scene_file_path.get_file().get_basename()

	if LEVEL_LORE.has(current_level_name):
		var data = LEVEL_LORE[current_level_name]
		if title_label: 
			title_label.text = data["title"]
			title_label.add_theme_color_override("font_color", Color(0.98, 0.85, 0.42))
		if lore_label:
			lore_label.bbcode_enabled = true
			lore_label.text = data["lore"]
			lore_label.add_theme_color_override("default_color", Color(0.94, 0.95, 0.98))
			lore_label.custom_minimum_size = Vector2(0, 160)

	_populate_artifacts()

	if canvas_layer:
		canvas_layer.show()

	get_tree().paused = true

func _populate_artifacts() -> void:
	if not artifacts_container: return

	for child in artifacts_container.get_children():
		child.queue_free()

	var gm = get_node_or_null("/root/GameManager")
	var raw_items = gm.collected_artifacts if gm and "collected_artifacts" in gm else ["powerup_turban", "artifact_manuscript", "artifact_kohinoor"]

	var first_item_loaded = false

	for item_key in raw_items:
		var item_str = str(item_key)
		var info = ARTIFACT_DATA.get(item_str, {
			"name": item_str.capitalize().replace("_", " "),
			"subtitle": "Ancient Relic",
			"desc": "A preserved historical artifact recovered during your quest.",
			"icon": "res://assets/images/artifacts/%s.png" % item_str,
			"frame_size": Vector2(32, 32)
		})

		# Row Button
		var row = Button.new()
		row.custom_minimum_size = Vector2(0, 48)
		row.alignment = HorizontalAlignment.HORIZONTAL_ALIGNMENT_LEFT

		var row_style = StyleBoxFlat.new()
		row_style.bg_color = Color(0.16, 0.17, 0.24, 0.8)
		row_style.border_color = Color(0.85, 0.65, 0.20, 0.5)
		row_style.set_border_width_all(1)
		row_style.set_corner_radius_all(6)
		row_style.content_margin_left = 12
		row.add_theme_stylebox_override("normal", row_style)
		row.text = "  ✦  " + info["name"] + "  (" + info["subtitle"] + ")"
		row.add_theme_color_override("font_color", Color(0.92, 0.94, 0.98))

		# Hover & Selection update right-side preview
		row.mouse_entered.connect(func(): _update_preview(info))
		row.pressed.connect(func(): _update_preview(info))

		artifacts_container.add_child(row)

		if not first_item_loaded:
			_update_preview(info)
			first_item_loaded = true

func _update_preview(info: Dictionary) -> void:
	if preview_title:
		preview_title.text = info["name"].to_upper()
		preview_title.add_theme_color_override("font_color", Color(0.98, 0.85, 0.42))
	if preview_desc:
		preview_desc.text = info["desc"]
		preview_desc.autowrap_mode = TextServer.AUTOWRAP_WORD

	var icon_path = info["icon"]
	var frame_size = info.get("frame_size", Vector2(32, 32))

	if preview_texture:
		if ResourceLoader.exists(icon_path):
			var full_tex = load(icon_path) as Texture2D
			
			# Slice single 32x32 pixel frame from spritesheet to prevent grid rendering
			var atlas = AtlasTexture.new()
			atlas.atlas = full_tex
			atlas.region = Rect2(Vector2.ZERO, frame_size)

			preview_texture.texture = atlas
			preview_texture.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
			preview_texture.custom_minimum_size = Vector2(200, 200)
			preview_texture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
			preview_texture.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		else:
			preview_texture.texture = null

func _apply_fullscreen_theme() -> void:
	if color_rect:
		color_rect.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		color_rect.color = Color(0.06, 0.07, 0.10, 0.96)

	if right_panel:
		var panel_style = StyleBoxFlat.new()
		panel_style.bg_color = Color(0.11, 0.12, 0.17, 0.95)
		panel_style.border_color = Color(0.95, 0.72, 0.22, 1.0) # Saffron Gold
		panel_style.set_border_width_all(3)
		panel_style.set_corner_radius_all(12)
		panel_style.content_margin_left = 24
		panel_style.content_margin_right = 24
		panel_style.content_margin_top = 24
		panel_style.content_margin_bottom = 24
		right_panel.add_theme_stylebox_override("panel", panel_style)

	for btn in [next_button, menu_button]:
		if btn:
			btn.custom_minimum_size = Vector2(200, 48)
			var b_style = StyleBoxFlat.new()
			b_style.bg_color = Color(0.24, 0.20, 0.14)
			b_style.border_color = Color(0.95, 0.72, 0.22)
			b_style.set_border_width_all(2)
			b_style.set_corner_radius_all(8)
			btn.add_theme_stylebox_override("normal", b_style)
			btn.add_theme_color_override("font_color", Color(1.0, 0.95, 0.80))

func _on_next_pressed() -> void:
	get_tree().paused = false
	match current_level_name:
		"Level1_RedFort": get_tree().change_scene_to_file("res://scenes/levels/Level2_Hampi.tscn")
		"Level2_Hampi": get_tree().change_scene_to_file("res://scenes/levels/Level3_Raigad.tscn")
		"Level3_Raigad": get_tree().change_scene_to_file("res://scenes/levels/Level4_Ujjain.tscn")
		_: get_tree().change_scene_to_file("res://scenes/main.tscn")

func _on_menu_pressed() -> void:
	get_tree().paused = false
	get_tree().change_scene_to_file("res://scenes/main.tscn")
