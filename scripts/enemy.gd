extends CharacterBody2D

@export var speed: float = 100.0
@export var patrol_distance: float = 150.0
@export var damage: int = 1

var start_x: float
var direction: int = 1

@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D if has_node("AnimatedSprite2D") else null

func _ready() -> void:
	start_x = global_position.x

func _physics_process(delta: float) -> void:
	# Explicit boundary checks prevent oscillation jitter
	if global_position.x >= start_x + patrol_distance:
		direction = -1
	elif global_position.x <= start_x - patrol_distance:
		direction = 1

	if animated_sprite:
		animated_sprite.flip_h = direction < 0

	velocity.x = direction * speed
	move_and_slide()

func _on_hitbox_body_entered(body: Node2D) -> void:
	if body.has_method("take_damage"):
		body.take_damage(damage)
