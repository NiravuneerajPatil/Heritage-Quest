extends Node

# Heritage Quest - Global Game Manager
# Tracks collected historical artifacts, active clothing power-ups, and level transitions.

signal artifact_collected(artifact_name: String, artifact_type: String)
signal level_completed(level_name: String)

var score: int = 0
var collected_artifacts: Array[String] = []
var active_powerups: Dictionary = {
	"vitality": false,     # Saffron Pagri (+1 Max HP)
	"double_jump": false,  # Zari Angavastram (Agility & Double Jump)
	"attack_boost": false, # Mavala Vambrace (Increased Talwar Damage)
	"speed_boost": false   # Royal Mojris (Sprint Agility)
}

func collect_item(item_name: String, item_type: String, points: int = 100) -> void:
	score += points
	if not collected_artifacts.has(item_name):
		collected_artifacts.append(item_name)
	
	# Apply clothing power-ups
	if item_type == "powerup_turban":
		active_powerups["vitality"] = true
	elif item_type == "powerup_angavastram":
		active_powerups["double_jump"] = true
	elif item_type == "powerup_vambrace":
		active_powerups["attack_boost"] = true
	
	artifact_collected.emit(item_name, item_type)
	print("Collected: ", item_name, " (+", points, " pts). Total Score: ", score)

func has_powerup(powerup_name: String) -> bool:
	return active_powerups.get(powerup_name, false)

func reset_progress() -> void:
	score = 0
	collected_artifacts.clear()
	for k in active_powerups.keys():
		active_powerups[k] = false
