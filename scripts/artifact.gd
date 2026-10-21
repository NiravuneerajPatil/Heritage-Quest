extends Area2D

# Heritage Quest - Collectible Artifact & Clothing Power-Up

@export var item_id: String = "artifact_kohinoor"
@export var item_display_name: String = "Koh-i-Noor Diamond"
@export var points: int = 150

@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var label: Label = $Label

var initial_y: float = 0.0
var elapsed_time: float = 0.0
var is_collected: bool = false

func _ready() -> void:
	initial_y = position.y
	body_entered.connect(_on_body_entered)
	
	if animated_sprite and animated_sprite.sprite_frames:
		if animated_sprite.sprite_frames.has_animation(item_id):
			animated_sprite.play(item_id)
	
	if label:
		label.text = item_display_name
		label.visible = false

func _process(delta: float) -> void:
	if not is_collected:
		elapsed_time += delta
		# Gentle hover float
		position.y = initial_y + sin(elapsed_time * 3.5) * 5.0

func _on_body_entered(body: Node2D) -> void:
	if is_collected:
		return
	if body.name == "Player" or body.is_in_group("player"):
		is_collected = true
		
		# Notify player or game manager
		var gm = get_node_or_null("/root/GameManager")
		if gm:
			gm.collect_item(item_display_name, item_id, points)
		
		if body.has_method("apply_powerup"):
			body.apply_powerup(item_id)
			
		# Visual pickup pop animation
		var tween = create_tween()
		tween.set_parallel(true)
		tween.tween_property(self, "scale", Vector2(1.6, 1.6), 0.25).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
		tween.tween_property(self, "modulate:a", 0.0, 0.25)
		tween.tween_property(self, "position:y", position.y - 20.0, 0.25)
		tween.chain().tween_callback(queue_free)
