extends CharacterBody2D

# Heritage Quest - Player Controller
# Features authentic 32x32 Indian Hero with Talwar combat & collectible clothing power-ups

@onready var animated_sprite_2d: AnimatedSprite2D = $AnimatedSprite2D

const BASE_SPEED = 300.0
const JUMP_VELOCITY = -600.0
const FALL_DEATH_Y = 1200.0  # Y position below which player dies

var speed: float = BASE_SPEED
var is_attacking: bool = false
var can_double_jump: bool = false
var has_double_jump_powerup: bool = false
var attack_multiplier: float = 1.0
var max_health: int = 3
var current_health: int = 3
var is_dead: bool = false
var is_invincible: bool = false
var invincibility_timer: float = 0.0
const INVINCIBILITY_DURATION: float = 1.5

# Attack hitbox
var attack_area: Area2D = null

func _ready() -> void:
	add_to_group("player")
	if animated_sprite_2d:
		animated_sprite_2d.animation_finished.connect(_on_animation_finished)
	
	# Create attack hitbox area
	_setup_attack_hitbox()
	
	# Apply any existing powerups from GameManager
	var gm = get_node_or_null("/root/GameManager")
	if gm:
		if gm.has_powerup("vitality"):
			max_health += 1
			current_health = max_health
		if gm.has_powerup("double_jump"):
			has_double_jump_powerup = true
			can_double_jump = true
			speed = BASE_SPEED * 1.15
		if gm.has_powerup("attack_boost"):
			attack_multiplier = 1.75
		if gm.has_powerup("speed_boost"):
			speed = BASE_SPEED * 1.30
		# Full attire bonus
		if gm.full_attire_bonus_active:
			max_health += 2
			current_health = max_health
			speed *= 1.25
			attack_multiplier *= 1.25

func _setup_attack_hitbox() -> void:
	attack_area = Area2D.new()
	attack_area.name = "AttackHitbox"
	attack_area.collision_layer = 0
	attack_area.collision_mask = 4  # Enemy layer
	attack_area.monitoring = false  # Only active during attacks
	
	var shape = CollisionShape2D.new()
	var rect = RectangleShape2D.new()
	rect.size = Vector2(30, 20)
	shape.shape = rect
	shape.position = Vector2(18, 0)  # In front of player
	attack_area.add_child(shape)
	add_child(attack_area)
	
	attack_area.body_entered.connect(_on_attack_hit)

func _physics_process(delta: float) -> void:
	if is_dead:
		return
	
	# Handle invincibility frames
	if is_invincible:
		invincibility_timer -= delta
		if invincibility_timer <= 0:
			is_invincible = false
			modulate.a = 1.0
		else:
			# Flashing effect
			modulate.a = 0.5 + 0.5 * sin(invincibility_timer * 20.0)
	
	# Add gravity
	if not is_on_floor():
		velocity += get_gravity() * delta
	else:
		# Reset double jump when on floor
		can_double_jump = has_double_jump_powerup

	# Handle attack inputs
	if Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and not is_attacking:
		trigger_attack("Attack1")
	if Input.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT) and not is_attacking:
		trigger_attack("Attack2")

	# Handle jump input & double jump
	if Input.is_action_just_pressed("jump"):
		if is_on_floor():
			velocity.y = JUMP_VELOCITY
		elif can_double_jump:
			# Double Jump (Agility power-up from Zari Angavastram)
			velocity.y = JUMP_VELOCITY * 0.9
			can_double_jump = false
			if animated_sprite_2d:
				animated_sprite_2d.play("Jump")

	# Handle horizontal movement
	var direction := Input.get_axis("left", "right")
	
	# Stop movement if attacking on the ground
	if is_attacking and is_on_floor():
		direction = 0 
		
	if direction:
		velocity.x = direction * speed
		if not is_attacking:
			animated_sprite_2d.flip_h = (direction < 0)
			# Update attack hitbox direction
			if attack_area:
				var shape_node = attack_area.get_child(0) as CollisionShape2D
				if shape_node:
					shape_node.position.x = -18 if direction < 0 else 18
	else:
		velocity.x = move_toward(velocity.x, 0, speed)
		
	# Update animations based on movement state
	if not is_attacking:
		update_animation()

	move_and_slide()
	
	# Check for fall death
	if global_position.y > FALL_DEATH_Y:
		die()

func trigger_attack(anim_name: String) -> void:
	is_attacking = true
	# Enable attack hitbox
	if attack_area:
		attack_area.monitoring = true
	
	# Play Attack1 or fallback to Attack
	if animated_sprite_2d:
		if animated_sprite_2d.sprite_frames.has_animation(anim_name):
			animated_sprite_2d.play(anim_name)
		elif animated_sprite_2d.sprite_frames.has_animation("Attack"):
			animated_sprite_2d.play("Attack")
		elif animated_sprite_2d.sprite_frames.has_animation("Attack2"):
			animated_sprite_2d.play("Attack2")

func update_animation() -> void:
	if not animated_sprite_2d:
		return
	if not is_on_floor():
		if velocity.y < 0:
			animated_sprite_2d.play("Jump")
		else:
			animated_sprite_2d.play("Fall")
	else:
		if abs(velocity.x) > 1:
			animated_sprite_2d.play("Run")
		else:
			animated_sprite_2d.play("Idle")

func _on_animation_finished() -> void:
	if animated_sprite_2d.animation in ["Attack", "Attack1", "Attack2"]:
		is_attacking = false
		# Disable attack hitbox
		if attack_area:
			attack_area.monitoring = false

func _on_attack_hit(body: Node2D) -> void:
	if body.is_in_group("enemies") and body.has_method("take_damage"):
		body.take_damage(int(attack_multiplier))

func take_damage(amount: int = 1) -> void:
	if is_dead or is_invincible:
		return
	
	current_health -= amount
	
	# Play hit animation if available
	if animated_sprite_2d and animated_sprite_2d.sprite_frames.has_animation("Hit"):
		animated_sprite_2d.play("Hit")
	
	# Update HUD
	_update_hud_health()
	
	if current_health <= 0:
		die()
	else:
		# Start invincibility frames
		is_invincible = true
		invincibility_timer = INVINCIBILITY_DURATION
		
		# Knockback
		velocity.y = -300.0
		velocity.x = -sign(velocity.x) * 200.0 if abs(velocity.x) > 0 else -200.0

func die() -> void:
	if is_dead:
		return
	is_dead = true
	
	if animated_sprite_2d and animated_sprite_2d.sprite_frames.has_animation("Death"):
		animated_sprite_2d.play("Death")
	
	set_physics_process(false)
	
	var gm = get_node_or_null("/root/GameManager")
	if gm:
		gm.player_died.emit()
	
	var death_screen = get_tree().current_scene.get_node_or_null("DeathScreen")
	if death_screen and death_screen.has_method("show_death_screen"):
		var level_path = get_tree().current_scene.scene_file_path
		death_screen.show_death_screen(level_path)
	else:
		var tween = create_tween()
		tween.tween_interval(1.5)
		tween.tween_callback(func():
			get_tree().reload_current_scene()
		)

func _update_hud_health() -> void:
	var hud = get_tree().current_scene.get_node_or_null("HUD")
	if hud and hud.has_method("update_health"):
		hud.update_health(current_health, max_health)

func apply_powerup(powerup_id: String) -> void:
	print("Player equipped powerup: ", powerup_id)
	if powerup_id == "powerup_turban":
		max_health += 1
		current_health = max_health
	elif powerup_id == "powerup_angavastram":
		has_double_jump_powerup = true
		can_double_jump = true
		speed = BASE_SPEED * 1.15
	elif powerup_id == "powerup_vambrace":
		attack_multiplier = 1.75
	elif powerup_id == "powerup_mojris":
		speed = BASE_SPEED * 1.30
	
	_update_hud_health()

func has_powerup(powerup_id: String) -> bool:
	var gm = get_node_or_null("/root/GameManager")
	if gm and gm.has_method("has_powerup"):
		var key_map = {
			"powerup_turban": "vitality",
			"powerup_angavastram": "double_jump",
			"powerup_vambrace": "attack_boost",
			"powerup_mojris": "speed_boost"
		}
		var gm_key = key_map.get(powerup_id, powerup_id)
		if gm.has_powerup(gm_key):
			return true

	match powerup_id:
		"powerup_turban", "vitality":
			return max_health > 3
		"powerup_angavastram", "double_jump":
			return has_double_jump_powerup
		"powerup_vambrace", "attack_boost":
			return attack_multiplier > 1.0
		"powerup_mojris", "speed_boost":
			return speed > BASE_SPEED
		_:
			return false
