extends Area2D

# Heritage Quest - Level Transition Portal / Heritage Gate

@export var next_level_path: String = ""
@export var level_title: String = "Heritage Site Completed!"
@export var level_index: int = 1

var is_triggered: bool = false

func _ready() -> void:
	body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node2D) -> void:
	if is_triggered:
		return
	if body.name == "Player" or body.is_in_group("player"):
		is_triggered = true
		print("Reached Level Goal: ", level_title)
		
		var gm = get_node_or_null("/root/GameManager")
		if gm:
			gm.level_completed.emit(level_title)
			gm.current_level_path = next_level_path
			gm.current_level_index = level_index
		
		# Show level complete screen instead of immediately transitioning
		var level_complete = get_tree().current_scene.get_node_or_null("LevelCompleteScreen")
		if level_complete and level_complete.has_method("show_level_complete"):
			level_complete.show_level_complete(level_title, level_index, next_level_path)
		else:
			# Fallback to direct transition
			if next_level_path != "":
				var tween = create_tween()
				tween.tween_property(self, "modulate:a", 0.0, 0.5)
				tween.chain().tween_callback(func():
					get_tree().change_scene_to_file(next_level_path)
				)
