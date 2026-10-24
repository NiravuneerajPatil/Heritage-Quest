extends CanvasLayer

# Heritage Quest - Death Screen ("You Died")

@onready var retry_button: Button = %RetryButton if has_node("%RetryButton") else $PanelContainer/VBoxContainer/RetryButton
@onready var menu_button: Button = %MenuButton if has_node("%MenuButton") else $PanelContainer/VBoxContainer/MenuButton
@onready var panel: PanelContainer = $PanelContainer if has_node("PanelContainer") else $CenterContainer

var current_level_path: String = ""

func _ready() -> void:
	if retry_button:
		retry_button.pressed.connect(_on_retry_pressed)
	if menu_button:
		menu_button.pressed.connect(_on_menu_pressed)
	
	visible = false
	process_mode = Node.PROCESS_MODE_ALWAYS

func show_death_screen(level_path: String) -> void:
	current_level_path = level_path
	visible = true
	get_tree().paused = true
	
	if panel:
		panel.modulate.a = 0.0
		panel.scale = Vector2(0.8, 0.8)
		var tween = create_tween()
		tween.set_pause_mode(Tween.TWEEN_PAUSE_PROCESS)
		tween.set_parallel(true)
		tween.tween_property(panel, "modulate:a", 1.0, 0.4)
		tween.tween_property(panel, "scale", Vector2(1.0, 1.0), 0.3).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)

func _on_retry_pressed() -> void:
	get_tree().paused = false
	if current_level_path != "":
		get_tree().change_scene_to_file(current_level_path)
	else:
		get_tree().reload_current_scene()

func _on_menu_pressed() -> void:
	get_tree().paused = false
	get_tree().change_scene_to_file("res://scenes/main.tscn")
