extends Node

# Heritage Quest - Global Game Manager (Autoload)

@warning_ignore("unused_signal")
signal artifact_collected(artifact_name: String, artifact_type: String)
@warning_ignore("unused_signal")
signal level_completed(level_name: String)
@warning_ignore("unused_signal")
signal player_died

var score: int = 0
var collected_artifacts: Array[String] = []
var active_powerups: Dictionary = {
	"vitality": false,
	"double_jump": false,
	"attack_boost": false,
	"speed_boost": false
}

# --- Volume Settings ---
var master_volume: float = 1.0
var music_volume: float = 1.0
var sfx_volume: float = 1.0

# --- Current level tracking ---
var current_level_path: String = ""
var current_level_index: int = 1
var current_level_name: String = ""

# --- Outfit / Attire System ---
var outfit_pieces: Dictionary = {
	"powerup_turban": {
		"name": "Saffron Pagri",
		"description": "A traditional saffron turban worn by Maratha warriors, symbolizing courage and sacrifice. It provides divine vitality to its wearer.",
		"boost": "+1 Max Health",
		"collected": false,
		"slot": "Head"
	},
	"powerup_angavastram": {
		"name": "Zari Angavastram",
		"description": "A resplendent silk shoulder cloth woven with golden zari threads from the looms of Hampi. Grants the wearer supernatural agility and the ability to leap twice in the air.",
		"boost": "Double Jump & +15% Speed",
		"collected": false,
		"slot": "Shoulder"
	},
	"powerup_vambrace": {
		"name": "Mavala Steel Vambrace",
		"description": "Forged in the legendary Maratha armories of Raigad Fort, this steel arm guard channels the warrior spirit of Chhatrapati Shivaji Maharaj, greatly amplifying combat prowess.",
		"boost": "+75% Attack Damage",
		"collected": false,
		"slot": "Arms"
	},
	"powerup_mojris": {
		"name": "Royal Mojris",
		"description": "Exquisite leather footwear adorned with intricate embroidery, once worn by Mughal nobility. These enchanted shoes allow the wearer to move with unmatched swiftness.",
		"boost": "+30% Movement Speed",
		"collected": false,
		"slot": "Feet"
	}
}

# --- Artifact Historical Data ---
var artifact_data: Dictionary = {
	"artifact_kohinoor": {
		"name": "Koh-i-Noor Diamond",
		"description": "One of the largest cut diamonds in the world, the Koh-i-Noor ('Mountain of Light') has a history spanning centuries. Originally mined in India's Golconda mines, it passed through the hands of Mughal emperors, Persian invaders, and Afghan rulers before being acquired by the British East India Company in 1849. It was presented to Queen Victoria and is now part of the British Crown Jewels.",
		"era": "14th Century onwards",
		"origin": "Golconda Mines, Deccan Plateau",
		"significance": "Symbol of imperial power and the complex colonial history of India's cultural treasures."
	},
	"artifact_manuscript": {
		"name": "Martial Arts Manuscript",
		"description": "An ancient illustrated manuscript detailing the martial art forms practiced within the Red Fort's training grounds. These documents preserve the combat techniques of the Mughal imperial guard, including swordsmanship (talwarbaazi), wrestling (kushti), and archery (teerandaazi). Such texts were closely guarded military secrets.",
		"era": "17th Century, Mughal Period",
		"origin": "Diwan-i-Khas, Red Fort, Delhi",
		"significance": "Preserves ancient Indian martial traditions and military strategy of the Mughal Empire."
	},
	"artifact_ashoka_seal": {
		"name": "Ashoka Lion Capital Seal",
		"description": "A ceremonial seal inspired by the Lion Capital of Ashoka at Sarnath. Emperor Ashoka erected pillars across the Indian subcontinent in the 3rd century BCE, inscribed with his edicts promoting dharma (righteousness), non-violence, and moral governance. The four-lion capital became the emblem of the Republic of India.",
		"era": "3rd Century BCE, Maurya Empire",
		"origin": "Sarnath, Uttar Pradesh",
		"significance": "Embodies the ideals of truth, non-violence, and justice that form the philosophical foundation of the Indian Republic."
	},
	"artifact_nataraja": {
		"name": "Bronze Nataraja Idol",
		"description": "A masterpiece of Chola bronze casting, the Nataraja depicts Lord Shiva as the cosmic dancer performing the Tandava — the dance of creation and destruction. The ring of fire (prabhavali) represents the cycle of samsara, while the crushed demon Apasmara symbolizes triumph over ignorance. Hampi's Vijayanagara Empire was renowned for patronizing such artistic traditions.",
		"era": "11th-14th Century, Chola & Vijayanagara Period",
		"origin": "Hampi, Karnataka",
		"significance": "Represents the pinnacle of Indian bronze sculpture and the deep spiritual philosophy of cosmic cycles."
	},
	"artifact_shivrai_coin": {
		"name": "Gold Shivrai Coin",
		"description": "The Shivrai was a gold coin issued by Chhatrapati Shivaji Maharaj after his coronation at Raigad Fort in 1674 CE. The coin bore Sanskrit inscriptions and represented the economic sovereignty of the newly established Maratha Empire. It was one of the first acts of declaring independence from Mughal suzerainty.",
		"era": "1674 CE, Maratha Empire",
		"origin": "Raigad Fort, Maharashtra",
		"significance": "Symbol of Maratha sovereignty and Shivaji Maharaj's vision of Swarajya (self-rule)."
	}
}

# --- Level artifact mapping ---
var level_artifacts: Dictionary = {
	1: ["powerup_turban", "artifact_manuscript", "artifact_kohinoor"],
	2: ["powerup_angavastram", "artifact_ashoka_seal", "artifact_nataraja"],
	3: ["powerup_vambrace", "artifact_shivrai_coin", "artifact_ashoka_seal"]
}

var full_attire_bonus_active: bool = false

func _ready() -> void:
	_apply_volume_settings()

func collect_item(item_name: String, item_type: String, points: int = 100) -> void:
	score += points
	if not collected_artifacts.has(item_type):
		collected_artifacts.append(item_type)
	
	if item_type == "powerup_turban":
		active_powerups["vitality"] = true
		outfit_pieces["powerup_turban"]["collected"] = true
	elif item_type == "powerup_angavastram":
		active_powerups["double_jump"] = true
		outfit_pieces["powerup_angavastram"]["collected"] = true
	elif item_type == "powerup_vambrace":
		active_powerups["attack_boost"] = true
		outfit_pieces["powerup_vambrace"]["collected"] = true
	elif item_type == "powerup_mojris":
		active_powerups["speed_boost"] = true
		outfit_pieces["powerup_mojris"]["collected"] = true
	
	artifact_collected.emit(item_name, item_type)
	print("Collected: ", item_name, " (+", points, " pts). Total Score: ", score)
	_check_full_attire()

func has_powerup(powerup_name: String) -> bool:
	return active_powerups.get(powerup_name, false)

func get_level_collected_artifacts(level_idx: int) -> Array:
	var level_arts = level_artifacts.get(level_idx, [])
	var result := []
	for art_id in level_arts:
		if collected_artifacts.has(art_id):
			if artifact_data.has(art_id):
				var data = artifact_data[art_id].duplicate()
				data["id"] = art_id
				result.append(data)
			elif outfit_pieces.has(art_id):
				var data = outfit_pieces[art_id].duplicate()
				data["id"] = art_id
				result.append(data)
	return result

func complete_level(title: String) -> void:
	level_completed.emit(title)

func notify_player_died() -> void:
	player_died.emit()

func reset_progress() -> void:
	score = 0
	collected_artifacts.clear()
	for k in active_powerups.keys():
		active_powerups[k] = false
	for k in outfit_pieces.keys():
		outfit_pieces[k]["collected"] = false
	full_attire_bonus_active = false

func is_full_attire_complete() -> bool:
	for key in outfit_pieces:
		if not outfit_pieces[key]["collected"]:
			return false
	return true

func _check_full_attire() -> void:
	if is_full_attire_complete() and not full_attire_bonus_active:
		full_attire_bonus_active = true
		print("🏆 FULL ATTIRE COMPLETE!")

func set_master_volume(value: float) -> void:
	master_volume = value
	_apply_volume_settings()

func set_music_volume(value: float) -> void:
	music_volume = value
	_apply_volume_settings()

func set_sfx_volume(value: float) -> void:
	sfx_volume = value
	_apply_volume_settings()

func _apply_volume_settings() -> void:
	var master_idx = AudioServer.get_bus_index("Master")
	if master_idx >= 0:
		AudioServer.set_bus_volume_db(master_idx, linear_to_db(master_volume))
		AudioServer.set_bus_mute(master_idx, master_volume <= 0.01)
	
	var music_idx = AudioServer.get_bus_index("Music")
	if music_idx >= 0:
		AudioServer.set_bus_volume_db(music_idx, linear_to_db(music_volume))
		AudioServer.set_bus_mute(music_idx, music_volume <= 0.01)
	
	var sfx_idx = AudioServer.get_bus_index("SFX")
	if sfx_idx >= 0:
		AudioServer.set_bus_volume_db(sfx_idx, linear_to_db(sfx_volume))
		AudioServer.set_bus_mute(sfx_idx, sfx_volume <= 0.01)
