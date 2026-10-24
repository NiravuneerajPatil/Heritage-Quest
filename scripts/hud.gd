extends CanvasLayer

# Heritage Quest - In-Game HUD

@onready var level_label: Label = $MarginContainer/VBoxContainer/TopRow/LevelLabel
@onready var score_label: Label = $MarginContainer/VBoxContainer/TopRow/ScoreLabel
@onready var artifacts_label: Label = $MarginContainer/VBoxContainer/BottomRow/ArtifactsLabel
@onready var powerups_container: HBoxContainer = $MarginContainer/VBoxContainer/BottomRow/PowerupsContainer
@onready var banner: PanelContainer = $BannerContainer
@onready var health_container: HBoxContainer = $MarginContainer/VBoxContainer/TopRow/HealthContainer

var level_name: String = "Heritage Site"

func _ready() -> void:
	var gm = get_node_or_null("/root/GameManager")
	if gm:
		gm.artifact_collected.connect(_on_artifact_collected)
		gm.level_completed.connect(_on_level_completed)
		update_display()
	
	if banner:
		banner.modulate.a = 0.0
		# Show initial level banner
		show_banner(level_name)

func set_level_name(new_name: String) -> void:
	level_name = new_name
	if level_label:
		level_label.text = new_name
	show_banner(new_name)

func show_banner(text: String) -> void:
	if not banner: return
	var lbl = banner.get_node_or_null("BannerLabel")
	if lbl:
		lbl.text = text
	var tween = create_tween()
	tween.tween_property(banner, "modulate:a", 1.0, 0.4)
	tween.tween_interval(2.0)
	tween.tween_property(banner, "modulate:a", 0.0, 0.6)

func update_display() -> void:
	var gm = get_node_or_null("/root/GameManager")
	if not gm: return
	
	if score_label:
		score_label.text = "SCORE: %05d" % gm.score
		
	if artifacts_label:
		artifacts_label.text = "ARTIFACTS: %d" % gm.collected_artifacts.size()
		
	if powerups_container:
		for child in powerups_container.get_children():
			child.queue_free()
		
		# Display active power-up badges
		if gm.has_powerup("vitality"):
			add_powerup_badge("PAGRI (+1 HP)")
		if gm.has_powerup("double_jump"):
			add_powerup_badge("ZARI (2X JUMP)")
		if gm.has_powerup("attack_boost"):
			add_powerup_badge("VAMBRACE (+ATK)")

func add_powerup_badge(text: String) -> void:
	var tag = Label.new()
	tag.text = "[" + text + "]"
	tag.add_theme_color_override("font_color", Color(0.98, 0.75, 0.14))
	tag.add_theme_font_size_override("font_size", 11)
	powerups_container.add_child(tag)

func update_health(current: int, max_hp: int) -> void:
	if not health_container:
		return
	# Clear existing hearts
	for child in health_container.get_children():
		child.queue_free()
	# Add hearts
	for i in range(max_hp):
		var heart = Label.new()
		if i < current:
			heart.text = "♥"
			heart.add_theme_color_override("font_color", Color(0.9, 0.15, 0.15))
		else:
			heart.text = "♡"
			heart.add_theme_color_override("font_color", Color(0.4, 0.4, 0.4))
		heart.add_theme_font_size_override("font_size", 18)
		health_container.add_child(heart)

func _on_artifact_collected(item_name: String, item_type: String) -> void:
	update_display()
	show_banner("COLLECTED: " + item_name.to_upper())

func _on_level_completed(title: String) -> void:
	show_banner("HERITAGE SITE CLEARED!\n" + title)
