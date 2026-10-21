extends CharacterBody2D

# Heritage Quest - Player Controller
# Features authentic 32x32 Indian Hero with Talwar combat & collectible clothing power-ups

@onready var animated_sprite_2d: AnimatedSprite2D = $AnimatedSprite2D

const BASE_SPEED = 300.0
const JUMP_VELOCITY = -600.0

var speed: float = BASE_SPEED
var is_attacking: bool = false
var can_double_jump: bool = false
var has_double_jump_powerup: bool = false
var attack_multiplier: float = 1.0
var max_health: int = 3
var current_health: int = 3

func _ready() -> void:
	add_to_group("player")
	if animated_sprite_2d:
		animated_sprite_2d.animation_finished.connect(_on_animation_finished)

func _physics_process(delta: float) -> void:
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
			# Play jump sound / puff effect if available
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
	else:
		velocity.x = move_toward(velocity.x, 0, speed)
		
	# Update animations based on movement state
	if not is_attacking:
		update_animation()

	move_and_slide()

func trigger_attack(anim_name: String) -> void:
	is_attacking = true
	# Play Attack1 or fallback to Attack if Attack1 is named Attack
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

func apply_powerup(powerup_id: String) -> void:
	print("Player equipped powerup: ", powerup_id)
	if powerup_id == "powerup_turban":
		# Saffron Pagri: Vitality boost
		max_health += 1
		current_health = max_health
	elif powerup_id == "powerup_angavastram":
		# Zari Angavastram: Double Jump & Agility
		has_double_jump_powerup = true
		can_double_jump = true
		speed = BASE_SPEED * 1.15
	elif powerup_id == "powerup_vambrace":
		# Mavala Vambrace: Attack damage boost
		attack_multiplier = 1.75
