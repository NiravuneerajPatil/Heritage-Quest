extends Area2D

# Heritage Quest - Level Transition Portal / Heritage Gate

@export var next_level_path: String = ""
@export var level_title: String = "Heritage Site Completed!"

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
			
		if next_level_path != "":
			var tween = create_tween()
			tween.tween_property(self, "modulate:a", 0.0, 0.5)
			tween.chain().tween_callback(func():
				get_tree().change_scene_to_file(next_level_path)
			)
