extends Area2D

# Heritage Quest - Level Exit & Summary Controller

@export var next_level_path: String = "res://scenes/levels/Level2_Hampi.tscn"
@export var level_title: String = "Level Cleared!"
@export var level_index: int = 1

@onready var canvas_layer: CanvasLayer = $CanvasLayer
@onready var background: ColorRect = $CanvasLayer/Background
@onready var level_title_label: Label = $CanvasLayer/Background/CenterContainer/PanelContainer/MarginContainer/VBoxContainer/LevelTitleLabel
@onready var artifacts_container: VBoxContainer = $CanvasLayer/Background/CenterContainer/PanelContainer/MarginContainer/VBoxContainer/ScrollContainer/ArtifactsContainer
@onready var next_level_button: Button = $CanvasLayer/Background/CenterContainer/PanelContainer/MarginContainer/VBoxContainer/ButtonContainer/NextLevelButton
@onready var menu_button: Button = $CanvasLayer/Background/CenterContainer/PanelContainer/MarginContainer/VBoxContainer/ButtonContainer/MenuButton

var is_triggered: bool = false

func _ready() -> void:
	body_entered.connect(_on_body_entered)
	
	if canvas_layer:
		canvas_layer.visible = false
		
	if next_level_button:
		next_level_button.pressed.connect(_on_next_level_pressed)
		
	if menu_button:
		menu_button.pressed.connect(_on_menu_pressed)

func _on_body_entered(body: Node2D) -> void:
	if is_triggered:
		return
		
	if body.name == "Player" or body.is_in_group("player"):
		is_triggered = true
		show_completion_summary()

func show_completion_summary() -> void:
	get_tree().paused = true
	
	if level_title_label:
		level_title_label.text = level_title
		
	# Clear static editor placeholders in ArtifactsContainer
	for child in artifacts_container.get_children():
		child.queue_free()
		
	# Fetch collected items from GameManager for this level
	var gm = get_node_or_null("/root/GameManager")
	var collected_list: Array = []
	var current_score: int = 0
	
	if gm:
		if gm.has_method("get_level_collected_artifacts"):
			collected_list = gm.get_level_collected_artifacts(level_index)
		if "score" in gm:
			current_score = gm.score

	# Populate UI with collected items
	if collected_list.is_empty():
		var empty_lbl = Label.new()
		empty_lbl.text = "No artifacts collected in this area."
		empty_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		artifacts_container.add_child(empty_lbl)
	else:
		for item in collected_list:
			# Horizontal container to place text on the LEFT and image on the RIGHT
			var item_row = HBoxContainer.new()
			item_row.add_theme_constant_override("separation", 16)
			
			# 1. VBoxContainer for Text Info (Left Side - Expands to fill available space)
			var info_box = VBoxContainer.new()
			info_box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
			
			# Item Title
			var title_lbl = Label.new()
			title_lbl.text = "• %s" % item.get("name", "Artifact")
			title_lbl.add_theme_font_size_override("font_size", 18)
			info_box.add_child(title_lbl)
			
			# Description & Powerup Boost info
			var desc_lbl = Label.new()
			var desc_text = item.get("description", "")
			if item.has("boost"):
				desc_text += " [Boost: %s]" % item.get("boost")
			desc_lbl.text = desc_text
			desc_lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
			desc_lbl.add_theme_font_size_override("font_size", 12)
			desc_lbl.modulate = Color(0.85, 0.85, 0.85)
			info_box.add_child(desc_lbl)
			
			# Historical Era & Origin details
			if item.has("era") and item.has("origin"):
				var meta_lbl = Label.new()
				meta_lbl.text = "Era: %s | Origin: %s" % [item.get("era"), item.get("origin")]
				meta_lbl.add_theme_font_size_override("font_size", 11)
				meta_lbl.modulate = Color(0.98, 0.75, 0.14) # Gold trim tint
				info_box.add_child(meta_lbl)
				
			item_row.add_child(info_box)
			
			# 2. TextureRect for the Pixel Art Icon (Right Side - Larger Single Frame Cutout)
			var texture_rect = TextureRect.new()
			texture_rect.custom_minimum_size = Vector2(80, 80) # Increased icon display size
			texture_rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
			texture_rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
			texture_rect.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST # Preserves crisp pixel art
			
			var item_id = item.get("id", "")
			var tex_path = "res://assets/images/artifacts/%s.png" % item_id
			
			if ResourceLoader.exists(tex_path):
				var full_tex: Texture2D = load(tex_path)
				# Extract frame 0 (32x32) from the horizontal sprite sheet
				var atlas_tex = AtlasTexture.new()
				atlas_tex.atlas = full_tex
				atlas_tex.region = Rect2(0, 0, 32, 32)
				texture_rect.texture = atlas_tex
			
			item_row.add_child(texture_rect)
			
			# Add row to main container
			artifacts_container.add_child(item_row)
			
			# Separator between items
			var sep = HSeparator.new()
			artifacts_container.add_child(sep)

		# Append Total Score at the end of the scroll list
		var score_lbl = Label.new()
		score_lbl.text = "\nTotal Score: %d" % current_score
		score_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		score_lbl.add_theme_font_size_override("font_size", 18)
		artifacts_container.add_child(score_lbl)

	# Show popup layer with entry animation
	if canvas_layer:
		canvas_layer.visible = true
		if background:
			background.modulate.a = 0.0
			var tween = create_tween()
			tween.set_pause_mode(Tween.TWEEN_PAUSE_PROCESS)
			tween.tween_property(background, "modulate:a", 1.0, 0.3)
func _on_next_level_pressed() -> void:
	get_tree().paused = false
	if next_level_path != "":
		get_tree().change_scene_to_file(next_level_path)

func _on_menu_pressed() -> void:
	get_tree().paused = false
	get_tree().change_scene_to_file("res://scenes/main.tscn")
