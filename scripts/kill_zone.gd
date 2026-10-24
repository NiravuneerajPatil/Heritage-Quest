extends Area2D

# Heritage Quest - Kill Zone (Fall Death Detector)
# When the player enters this area, they die

func _ready() -> void:
	body_entered.connect(_on_body_entered)
	# Make sure monitoring is on
	monitoring = true

func _on_body_entered(body: Node2D) -> void:
	if body.is_in_group("player") and body.has_method("die"):
		body.die()
