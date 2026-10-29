# Heritage Quest 🚩

**Heritage Quest** is a 2D action-platformer built in Godot 4. It blends historical and cultural themes across iconic Indian landmarks with fast-paced combat, exploration, artifact collection, and adaptive enemy AI.

---

## 🎮 Game Features

- **Dynamic Player Mechanics:**
  - Smooth 2D platforming physics (running, jumping, ledge traversal).
  - Multi-directional attack combos (`Attack1`, `Attack2`) with active hitbox management.
  - Power-up system including agility buffs (Double Jump via *Zari Angavastram*) and health boosts.
  - Invincibility frames (i-frames) with visual alpha flashing upon taking damage.

- **Smart Enemy AI State Machine:**
  - State-driven behavior: **PATROL** and **CHASE** modes.
  - Ledge-awareness protection using `RayCast2D` checks (`LedgeCheck`) to prevent enemies from falling off platform edges.
  - Detection area triggers (`Area2D`) with targeted body tracking and deadzone buffers to eliminate direction jitter.
  - Smooth visual scaling and alpha-fade death sequences.

- **Level & Progression System:**
  - Cultural artifacts and collectibles (*Ashoka Lion Capital Seal*, *Bronze Nataraja Idol*, etc.) with real-time HUD updates.
  - Multiple themed levels (*Lal Qila / Red Fort*, *Hampi*, *Raigad*).
  - Dedicated Main Menu UI with responsive resolution scaling (`canvas_items` mode).

---

## 🛠️ Project Structure

```text
Heritage Quest/
├── assets/                  # Textures, sprites, and UI art
├── levels/                  # Level scenes (Level1_RedFort.tscn, etc.)
├── res/
│   ├── scenes/
│   │   ├── Player.tscn      # Player character body, animations & hitboxes
│   │   ├── Enemy.tscn       # Enemy AI character, LedgeCheck & detection
│   │   ├── main.tscn        # Main Menu & Settings UI
│   │   ├── HUD.tscn         # Health and score overlay
│   │   └── LevelExit.tscn   # Scene transition triggers
│   └── scripts/
│       ├── player.gd        # Player movement, combat & animation handler
│       ├── enemy.gd         # Enemy state machine (PATROL / CHASE)
│       └── main.gd          # UI & game management
└── project.godot            # Godot 4 engine configuration
```

---

## 🧠 Core Enemy AI Architecture (`enemy.gd`)

The enemy relies on a delegate-based Finite State Machine (FSM):

```gdscript
enum State { PATROL, CHASE }
var current_state: State = State.PATROL
```

- **Patrol Mode:** Traverses a set distance (`patrol_distance`) and flips direction when encountering walls, patrol bounds, or platform ledges via `LedgeCheck`.
- **Chase Mode:** Initiated via `_on_detection_area_body_entered`. Targets the player's X position with increased speed (`chase_speed`) while enforcing ledge safety so the enemy won't plunge off cliffs during pursuit.

---

## 🏃 Player Control Scheme (`player.gd`)

| Action | Control | Description |
| :--- | :--- | :--- |
| **Move Left / Right** | `A` / `D` or `Left Arrow` / `Right Arrow` | Walk / Run across terrain |
| **Jump** | `Spacebar` | Single jump or Double Jump (if unlocked) |
| **Primary Attack** | `Left Mouse Button` | Performs `Attack1` strike |
| **Secondary Attack** | `Right Mouse Button` | Performs `Attack2` strike |

---

## 🚀 Setup & Running the Game

1. **Prerequisites:** Download and install [Godot Engine 4.x](https://godotengine.org/).
2. **Clone / Open:**
   - Clone or copy this repository to your local machine.
   - Open Godot 4, click **Import**, and select the `project.godot` file in the repository root.
3. **Run Game:**
   - Press **`F5`** (or click the **Play** button at top right) to launch the game from the Main Menu (`main.tscn`).
   - Press **`F6`** to test individual levels directly.

---

## 📝 Future Improvements & Roadmap

- [ ] Boss encounter logic for stage completions.
- [ ] Additional cultural artifact collectibles and lore encyclopedia menu.
- [ ] Controller / Gamepad support for player movement and combat.