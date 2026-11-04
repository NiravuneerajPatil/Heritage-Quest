extends CharacterBody2D

# Heritage Quest - Enemy Logic
enum State { PATROL, CHASE }
var current_state: State = State.PATROL
var target_player: Node2D = null

@export var chase_speed: float = 130.0
@export var speed: float = 100.0
@export var patrol_distance: float = 150.0
@export var damage: int = 1
@export var max_health: int = 2

var start_x: float
var direction: int = 1
var current_health: int = 2
var is_dead: bool = false

@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D if has_node("AnimatedSprite2D") else null
@onready var sprite: CanvasItem = $Sprite if has_node("Sprite") else null
@onready var hitbox_area: Area2D = $Hitbox if has_node("Hitbox") else null
@onready var ledge_check: RayCast2D = $LedgeCheck if has_node("LedgeCheck") else null

func _ready() -> void:
	start_x = global_position.x
	current_health = max_health
	
	if ledge_check:
		ledge_check.add_exception(self) # Prevent self-collision lock
	
	if hitbox_area and not hitbox_area.body_entered.is_connected(_on_hitbox_body_entered):
		hitbox_area.body_entered.connect(_on_hitbox_body_entered)

func _physics_process(delta: float) -> void:
	if is_dead:
		return

	# State Machine Switching
	match current_state:
		State.PATROL:
			_process_patrol(delta)
		State.CHASE:
			_process_chase(delta)

	# Apply Gravity
	if not is_on_floor():
		velocity.y += 980.0 * delta

	move_and_slide()

func _process_patrol(_delta: float) -> void:
	var hit_patrol_limit = (global_position.x >= start_x + patrol_distance and direction == 1) or \
						   (global_position.x <= start_x - patrol_distance and direction == -1)
	
	# Check ledge only if ledge_check node exists
	var lost_ledge = false
	if ledge_check and is_on_floor():
		lost_ledge = not ledge_check.is_colliding()

	if is_on_wall() or lost_ledge or hit_patrol_limit:
		_flip_direction()

	velocity.x = direction * speed

func _process_chase(_delta: float) -> void:
	if not is_instance_valid(target_player):
		current_state = State.PATROL
		return

	var diff_x = target_player.global_position.x - global_position.x
	
	if abs(diff_x) < 8.0:
		velocity.x = 0.0
		return

	var desired_direction = 1 if diff_x > 0 else -1
	if desired_direction != direction:
		direction = desired_direction
		_update_facing_direction()

	var wall_hit = is_on_wall()
	var lost_ledge = false
	if ledge_check and is_on_floor():
		lost_ledge = not ledge_check.is_colliding()

	if wall_hit or lost_ledge:
		velocity.x = 0.0
	else:
		velocity.x = direction * chase_speed

func _flip_direction() -> void:
	direction *= -1
	_update_facing_direction()

func _update_facing_direction() -> void:
	if ledge_check:
		ledge_check.position.x = abs(ledge_check.position.x if ledge_check.position.x != 0 else 12.0) * direction
		ledge_check.force_raycast_update()

	if animated_sprite:
		animated_sprite.flip_h = direction < 0
	elif sprite and "flip_h" in sprite:
		sprite.flip_h = direction < 0

func _on_hitbox_body_entered(body: Node2D) -> void:
	if is_dead:
		return
	if body.name == "Player" or body.is_in_group("player"):
		if body.has_method("take_damage"):
			body.take_damage(damage)

func take_damage(amount: int) -> void:
	if is_dead:
		return
		
	current_health -= amount
	
	var target_visual = animated_sprite if animated_sprite else sprite
	if target_visual:
		var tween = create_tween()
		tween.tween_property(target_visual, "modulate", Color.RED, 0.1)
		tween.tween_property(target_visual, "modulate", Color.WHITE, 0.1)
		
	if current_health <= 0:
		die()

func die() -> void:
	is_dead = true
	velocity = Vector2.ZERO
	
	set_collision_layer_value(3, false)
	set_collision_mask_value(1, false)
	
	if hitbox_area:
		hitbox_area.set_deferred("monitoring", false)
		hitbox_area.set_deferred("monitorable", false)
		
	var target_visual: CanvasItem = animated_sprite if animated_sprite else sprite
	var tween = create_tween()
	tween.set_parallel(true)
	if target_visual:
		tween.tween_property(target_visual, "scale", Vector2(1.3, 1.3), 0.15)
		tween.tween_property(target_visual, "modulate:a", 0.0, 0.25)
	tween.chain().tween_callback(queue_free)

func _on_detection_area_body_entered(body: Node2D) -> void:
	if body.name == "Player" or body.is_in_group("player"):
		target_player = body
		current_state = State.CHASE

func _on_detection_area_body_exited(body: Node2D) -> void:
	if body == target_player:
		target_player = null
		current_state = State.PATROL
