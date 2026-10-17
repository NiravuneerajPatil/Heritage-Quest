extends CharacterBody2D

@onready var animated_sprite_2d: AnimatedSprite2D = $AnimatedSprite2D

const SPEED = 300.0
const JUMP_VELOCITY = -600.0

# Track if the player is currently attacking
var is_attacking: bool = false

func _ready() -> void:
	# Connect the animation finished signal so we know when to stop attacking
	animated_sprite_2d.animation_finished.connect(_on_animation_finished)

func _physics_process(delta: float) -> void:
	# Add gravity.
	if not is_on_floor():
		velocity += get_gravity() * delta

	# Handle attack input.
	if Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and not is_attacking:
		is_attacking = true
		animated_sprite_2d.play("Attack")
	if Input.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT) and not is_attacking:
		is_attacking = true
		animated_sprite_2d.play("Attack2")

	# Handle jump input 
	if Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = JUMP_VELOCITY

	# Handle horizontal movement.
	var direction := Input.get_axis("left", "right")
	
	# OVERRIDE DIRECTION: Stop moving if attacking on the ground
	if is_attacking and is_on_floor():
		direction = 0 
		
	if direction:
		velocity.x = direction * SPEED
		if not is_attacking:
			animated_sprite_2d.flip_h = (direction < 0)
	else:
		velocity.x = move_toward(velocity.x, 0, SPEED)
		
	# Update animations based on state
	if not is_attacking:
		update_animation()

	move_and_slide()

func update_animation() -> void:
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
	if animated_sprite_2d.animation == "Attack":
		is_attacking = false
	if animated_sprite_2d.animation=="Attack2":
		is_attacking=false
