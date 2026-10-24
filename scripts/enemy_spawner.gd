extends Node2D

@export var enemy_scene: PackedScene = preload("res://scenes/components/Enemy.tscn")
@export var spawn_interval: float = 4.0
@export var max_enemies: int = 5

var timer: Timer
var current_enemies: int = 0

func _ready() -> void:
	timer = Timer.new()
	timer.wait_time = spawn_interval
	timer.autostart = true
	timer.timeout.connect(_spawn_enemy)
	add_child(timer)

func _spawn_enemy() -> void:
	if current_enemies >= max_enemies or not enemy_scene:
		return

	var enemy = enemy_scene.instantiate()
	enemy.global_position = global_position
	enemy.tree_exited.connect(func(): current_enemies -= 1)
	get_parent().add_child(enemy)
	current_enemies += 1
