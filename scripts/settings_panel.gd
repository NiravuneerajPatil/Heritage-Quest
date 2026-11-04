extends Control

# Heritage Quest - Main Menu Script

@onready var play_button: Button = $MarginContainer/VBoxContainer/MainButtons/PlayButton if has_node("$MarginContainer/VBoxContainer/MainButtons/PlayButton") else null
@onready var settings_button: Button = $MarginContainer/VBoxContainer/MainButtons/SettingsButton if has_node("$MarginContainer/VBoxContainer/MainButtons/SettingsButton") else null
@onready var exit_button: Button = $MarginContainer/VBoxContainer/MainButtons/ExitButton if has_node("$MarginContainer/VBoxContainer/MainButtons/ExitButton") else null

@onready var settings_panel: Control = $SettingsLayer/SettingsPanel if has_node("SettingsLayer/SettingsPanel") else $SettingsPanel

func _ready() -> void:
	# Hide Settings panel by default on load
	if settings_panel:
		settings_panel.hide()

	if play_button:
		play_button.pressed.connect(_on_play_pressed)
	if settings_button:
		settings_button.pressed.connect(_on_settings_pressed)
	if exit_button:
		exit_button.pressed.connect(_on_exit_pressed)

func _on_play_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/levels/Level1_RedFort.tscn")

func _on_settings_pressed() -> void:
	if settings_panel:
		settings_panel.show()

func _on_exit_pressed() -> void:
	get_tree().quit()
