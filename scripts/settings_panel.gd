extends CanvasLayer

# Heritage Quest - Settings Panel (Volume Controls)

@onready var master_slider: HSlider = $CenterContainer/PanelContainer/VBoxContainer/MasterRow/MasterSlider
@onready var music_slider: HSlider = $CenterContainer/PanelContainer/VBoxContainer/MusicRow/MusicSlider
@onready var sfx_slider: HSlider = $CenterContainer/PanelContainer/VBoxContainer/SFXRow/SFXSlider
@onready var master_value_label: Label = $CenterContainer/PanelContainer/VBoxContainer/MasterRow/MasterValue
@onready var music_value_label: Label = $CenterContainer/PanelContainer/VBoxContainer/MusicRow/MusicValue
@onready var sfx_value_label: Label = $CenterContainer/PanelContainer/VBoxContainer/SFXRow/SFXValue
@onready var back_button: Button = $CenterContainer/PanelContainer/VBoxContainer/BackButton

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	visible = false
	
	var gm = get_node_or_null("/root/GameManager")
	if gm:
		master_slider.value = gm.master_volume * 100.0
		music_slider.value = gm.music_volume * 100.0
		sfx_slider.value = gm.sfx_volume * 100.0
	
	master_slider.value_changed.connect(_on_master_changed)
	music_slider.value_changed.connect(_on_music_changed)
	sfx_slider.value_changed.connect(_on_sfx_changed)
	back_button.pressed.connect(_on_back_pressed)
	
	_update_labels()

func show_settings() -> void:
	visible = true

func hide_settings() -> void:
	visible = false

func _on_master_changed(value: float) -> void:
	var gm = get_node_or_null("/root/GameManager")
	if gm:
		gm.set_master_volume(value / 100.0)
	_update_labels()

func _on_music_changed(value: float) -> void:
	var gm = get_node_or_null("/root/GameManager")
	if gm:
		gm.set_music_volume(value / 100.0)
	_update_labels()

func _on_sfx_changed(value: float) -> void:
	var gm = get_node_or_null("/root/GameManager")
	if gm:
		gm.set_sfx_volume(value / 100.0)
	_update_labels()

func _on_back_pressed() -> void:
	hide_settings()

func _update_labels() -> void:
	if master_value_label:
		master_value_label.text = "%d%%" % int(master_slider.value)
	if music_value_label:
		music_value_label.text = "%d%%" % int(music_slider.value)
	if sfx_value_label:
		sfx_value_label.text = "%d%%" % int(sfx_slider.value)
