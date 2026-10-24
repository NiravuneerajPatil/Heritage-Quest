extends CanvasLayer

# Heritage Quest - Level Complete Screen
# Shows artifact details and outfit completion progress

@onready var title_label: Label = $CenterContainer/PanelContainer/ScrollContainer/VBoxContainer/TitleLabel
@onready var artifacts_container: VBoxContainer = $CenterContainer/PanelContainer/ScrollContainer/VBoxContainer/ArtifactsContainer
@onready var outfit_title: Label = $CenterContainer/PanelContainer/ScrollContainer/VBoxContainer/OutfitTitle
@onready var outfit_progress_bar: ProgressBar = $CenterContainer/PanelContainer/ScrollContainer/VBoxContainer/OutfitProgressBar
@onready var outfit_percent_label: Label = $CenterContainer/PanelContainer/ScrollContainer/VBoxContainer/OutfitPercentLabel
@onready var outfit_details: VBoxContainer = $CenterContainer/PanelContainer/ScrollContainer/VBoxContainer/OutfitDetails
@onready var bonus_label: Label = $CenterContainer/PanelContainer/ScrollContainer/VBoxContainer/BonusLabel
@onready var continue_button: Button = $CenterContainer/PanelContainer/ScrollContainer/VBoxContainer/ContinueButton

var next_level_path: String = ""

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	visible = false
	continue_button.pressed.connect(_on_continue_pressed)

func show_level_complete(level_title: String, level_index: int, next_path: String) -> void:
	next_level_path = next_path
	visible = true
	get_tree().paused = true
	
	var gm = get_node_or_null("/root/GameManager")
	if not gm:
		return
	
	# Set title
	title_label.text = level_title
	
	# Clear previous artifacts
	for child in artifacts_container.get_children():
		child.queue_free()
	
	# Display collected artifacts with historical info
	var collected = gm.get_level_collected_artifacts(level_index)
	if collected.size() == 0:
		var no_items = Label.new()
		no_items.text = "No artifacts collected in this level."
		no_items.add_theme_color_override("font_color", Color(0.7, 0.7, 0.7))
		no_items.add_theme_font_size_override("font_size", 13)
		artifacts_container.add_child(no_items)
	else:
		for art in collected:
			_add_artifact_entry(art)
	
	# Update outfit progress
	var completion = gm.get_outfit_completion_percentage()
	outfit_progress_bar.value = completion
	outfit_percent_label.text = "Outfit Completion: %d%% (%d / %d pieces)" % [
		int(completion), gm.get_collected_outfit_count(), gm.outfit_pieces.size()
	]
	
	# Show outfit piece details
	for child in outfit_details.get_children():
		child.queue_free()
	
	for key in gm.outfit_pieces:
		var piece = gm.outfit_pieces[key]
		var row = HBoxContainer.new()
		row.add_theme_constant_override("separation", 8)
		
		var status_icon = Label.new()
		status_icon.text = "✓" if piece["collected"] else "✗"
		status_icon.add_theme_color_override("font_color", Color(0.2, 0.9, 0.3) if piece["collected"] else Color(0.5, 0.5, 0.5))
		status_icon.add_theme_font_size_override("font_size", 14)
		row.add_child(status_icon)
		
		var slot_label = Label.new()
		slot_label.text = "[%s]" % piece["slot"]
		slot_label.add_theme_color_override("font_color", Color(0.6, 0.6, 0.6))
		slot_label.add_theme_font_size_override("font_size", 11)
		slot_label.custom_minimum_size.x = 70
		row.add_child(slot_label)
		
		var name_label = Label.new()
		name_label.text = piece["name"]
		name_label.add_theme_color_override("font_color", Color(0.98, 0.75, 0.14) if piece["collected"] else Color(0.45, 0.45, 0.45))
		name_label.add_theme_font_size_override("font_size", 12)
		row.add_child(name_label)
		
		var boost_label_item = Label.new()
		boost_label_item.text = " — " + piece["boost"]
		boost_label_item.add_theme_color_override("font_color", Color(0.5, 0.8, 1.0) if piece["collected"] else Color(0.35, 0.35, 0.35))
		boost_label_item.add_theme_font_size_override("font_size", 11)
		row.add_child(boost_label_item)
		
		outfit_details.add_child(row)
	
	# Show bonus label if full attire
	if gm.is_full_attire_complete():
		bonus_label.text = "🏆 FULL HERITAGE GUARDIAN ATTIRE COMPLETE!\nBonus: +25% All Stats, Shield Aura, Heritage Glow Effect"
		bonus_label.visible = true
	else:
		var remaining = gm.outfit_pieces.size() - gm.get_collected_outfit_count()
		bonus_label.text = "Collect %d more piece(s) to unlock the Heritage Guardian powers!" % remaining
		bonus_label.visible = true

func _add_artifact_entry(art: Dictionary) -> void:
	var container = VBoxContainer.new()
	container.add_theme_constant_override("separation", 4)
	
	# Separator
	var sep = HSeparator.new()
	sep.add_theme_color_override("separator", Color(0.98, 0.75, 0.14, 0.3))
	container.add_child(sep)
	
	# Name
	var name_lbl = Label.new()
	name_lbl.text = art.get("name", "Unknown Artifact")
	name_lbl.add_theme_color_override("font_color", Color(0.98, 0.75, 0.14))
	name_lbl.add_theme_font_size_override("font_size", 15)
	container.add_child(name_lbl)
	
	# Description
	var desc_lbl = Label.new()
	desc_lbl.text = art.get("description", "")
	desc_lbl.add_theme_color_override("font_color", Color(0.85, 0.85, 0.85))
	desc_lbl.add_theme_font_size_override("font_size", 11)
	desc_lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	desc_lbl.custom_minimum_size.x = 500
	container.add_child(desc_lbl)
	
	# Era & origin (for historical artifacts)
	if art.has("era"):
		var era_lbl = Label.new()
		era_lbl.text = "Era: %s  |  Origin: %s" % [art["era"], art.get("origin", "Unknown")]
		era_lbl.add_theme_color_override("font_color", Color(0.6, 0.75, 0.9))
		era_lbl.add_theme_font_size_override("font_size", 10)
		container.add_child(era_lbl)
	
	if art.has("significance"):
		var sig_lbl = Label.new()
		sig_lbl.text = "Historical Significance: " + art["significance"]
		sig_lbl.add_theme_color_override("font_color", Color(0.7, 0.9, 0.7))
		sig_lbl.add_theme_font_size_override("font_size", 10)
		sig_lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		sig_lbl.custom_minimum_size.x = 500
		container.add_child(sig_lbl)
	
	# Boost info (for outfit pieces)
	if art.has("boost"):
		var boost_lbl = Label.new()
		boost_lbl.text = "Power: " + art["boost"]
		boost_lbl.add_theme_color_override("font_color", Color(0.5, 0.8, 1.0))
		boost_lbl.add_theme_font_size_override("font_size", 11)
		container.add_child(boost_lbl)
	
	artifacts_container.add_child(container)

func _on_continue_pressed() -> void:
	get_tree().paused = false
	if next_level_path != "":
		get_tree().change_scene_to_file(next_level_path)
	else:
		get_tree().change_scene_to_file("res://scenes/main.tscn")
