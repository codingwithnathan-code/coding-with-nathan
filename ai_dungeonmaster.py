import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import ollama
import json
import os
import random
from datetime import datetime

# ==================== COLORS ====================
BG_COLOR = "#1e1e2e"
TITLE_COLOR = "#cdd6f4"
TEXT_COLOR = "#cdd6f4"
ACCENT_COLOR = "#89b4fa"
SUCCESS_COLOR = "#a6e3a1"
DANGER_COLOR = "#f38ba8"
BUTTON_COLOR = "#313244"
ENTRY_BG = "#313244"

SAVE_FILE = "rpg_save.json"


class AIDungeonMaster:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Dungeon Master RPG - Coding With Nathan")
        self.root.geometry("1100x800")
        self.root.configure(bg=BG_COLOR)

        self.player = {
            "name": "Hero",
            "class": "Warrior",
            "hp": 100,
            "max_hp": 100,
            "attack": 12,
            "defense": 8,
            "gold": 20,
            "level": 1,
            "xp": 0,
        }

        self.inventory = ["Rusty Sword", "Health Potion"]
        self.story_history = []
        self.in_combat = False
        self.current_enemy = None
        self.game_started = False

        # === Procedural Dungeon ===
        self.dungeon = {}  # room_id → room data
        self.current_room_id = None
        self.room_counter = 0

        self.create_widgets()
        self.show_welcome()

    # ------------------------------------------------------------------
    # PROCEDURAL DUNGEON GENERATION
    # ------------------------------------------------------------------
    def generate_room(self, room_type=None):
        """Generate a new procedural room and return its ID"""
        self.room_counter += 1
        room_id = f"room_{self.room_counter}"

        room_types = ["corridor", "chamber", "hall", "cave", "ruins", "crypt"]
        if not room_type:
            room_type = random.choice(room_types)

        adjectives = [
            "dark",
            "damp",
            "ancient",
            "crumbling",
            "torch-lit",
            "echoing",
            "forgotten",
            "blood-stained",
        ]
        features = [
            "old bones scattered on the floor",
            "strange symbols carved into the walls",
            "a broken statue in the corner",
            "pools of stagnant water",
            "webs covering the ceiling",
            "faded murals on the walls",
            "a collapsed pillar",
            "scorch marks on the ground",
        ]

        exits = random.sample(
            ["north", "south", "east", "west"], k=random.randint(1, 3)
        )

        # Chance of an encounter or loot
        has_enemy = random.random() < 0.35
        has_loot = random.random() < 0.25

        room = {
            "id": room_id,
            "type": room_type,
            "description": f"A {random.choice(adjectives)} {room_type} with {random.choice(features)}.",
            "exits": exits,
            "visited": False,
            "has_enemy": has_enemy,
            "has_loot": has_loot,
            "enemy_name": None,
            "loot_item": None,
        }

        if has_enemy:
            enemies = [
                "Goblin Scout",
                "Skeleton Warrior",
                "Giant Spider",
                "Dark Wolf",
                "Cave Bat Swarm",
                "Bandit",
                "Slime",
                "Cursed Knight",
            ]
            room["enemy_name"] = random.choice(enemies)

        if has_loot:
            items = [
                "Health Potion",
                "Gold Pouch",
                "Iron Dagger",
                "Magic Dust",
                "Old Map Fragment",
                "Silver Ring",
                "Torch",
            ]
            room["loot_item"] = random.choice(items)

        self.dungeon[room_id] = room
        return room_id

    def get_current_room(self):
        return self.dungeon.get(self.current_room_id)

    def move_to_direction(self, direction):
        """Try to move in a direction. Create a new room if needed."""
        room = self.get_current_room()
        if not room:
            return False, "You are not in a valid room."

        if direction not in room["exits"]:
            return False, f"There is no exit to the {direction}."

        # Create a new room in that direction
        new_room_id = self.generate_room()
        self.current_room_id = new_room_id
        new_room = self.get_current_room()
        new_room["visited"] = True

        return True, new_room

    # ------------------------------------------------------------------
    # GUI
    # ------------------------------------------------------------------
    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="⚔️ AI Dungeon Master RPG",
            font=("Arial", 24, "bold"),
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        )
        title.pack(pady=12)

        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True, padx=20)

        # Left - Story
        left_frame = tk.Frame(main_frame, bg=BG_COLOR)
        left_frame.pack(side=tk.LEFT, fill="both", expand=True)

        self.story_display = scrolledtext.ScrolledText(
            left_frame,
            font=("Consolas", 11),
            bg="#181825",
            fg=TEXT_COLOR,
            wrap=tk.WORD,
            height=28,
            state="disabled",
        )
        self.story_display.pack(fill="both", expand=True, pady=5)

        input_frame = tk.Frame(left_frame, bg=BG_COLOR)
        input_frame.pack(fill="x", pady=8)

        self.action_entry = tk.Entry(
            input_frame,
            font=("Arial", 13),
            bg=ENTRY_BG,
            fg=TEXT_COLOR,
            insertbackground="white",
        )
        self.action_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 8))
        self.action_entry.bind("<Return>", lambda e: self.send_action())

        tk.Button(
            input_frame,
            text="Act",
            font=("Arial", 12, "bold"),
            bg=ACCENT_COLOR,
            fg="#1e1e2e",
            command=self.send_action,
            width=8,
        ).pack(side=tk.LEFT)

        # Right - Stats
        right_frame = tk.Frame(main_frame, bg="#181825", width=280)
        right_frame.pack(side=tk.RIGHT, fill="y", padx=(15, 0))
        right_frame.pack_propagate(False)

        tk.Label(
            right_frame,
            text="CHARACTER",
            font=("Arial", 13, "bold"),
            bg="#181825",
            fg=ACCENT_COLOR,
        ).pack(pady=(15, 8))

        self.stats_label = tk.Label(
            right_frame,
            text="",
            font=("Consolas", 11),
            bg="#181825",
            fg=TEXT_COLOR,
            justify="left",
        )
        self.stats_label.pack(pady=5, padx=15, anchor="w")

        tk.Label(
            right_frame,
            text="INVENTORY",
            font=("Arial", 12, "bold"),
            bg="#181825",
            fg=ACCENT_COLOR,
        ).pack(pady=(20, 5))

        self.inventory_listbox = tk.Listbox(
            right_frame,
            font=("Arial", 10),
            bg="#313244",
            fg=TEXT_COLOR,
            height=7,
            selectbackground=ACCENT_COLOR,
        )
        self.inventory_listbox.pack(padx=15, fill="x")

        # Room info
        tk.Label(
            right_frame,
            text="CURRENT ROOM",
            font=("Arial", 12, "bold"),
            bg="#181825",
            fg=ACCENT_COLOR,
        ).pack(pady=(15, 5))

        self.room_label = tk.Label(
            right_frame,
            text="Not in dungeon",
            font=("Arial", 10),
            bg="#181825",
            fg="#a6adc8",
            wraplength=240,
            justify="left",
        )
        self.room_label.pack(padx=15, anchor="w")

        btn_frame = tk.Frame(right_frame, bg="#181825")
        btn_frame.pack(pady=15)

        tk.Button(
            btn_frame,
            text="New Game",
            font=("Arial", 11, "bold"),
            bg=SUCCESS_COLOR,
            fg="#1e1e2e",
            width=18,
            command=self.new_game,
        ).pack(pady=3)
        tk.Button(
            btn_frame,
            text="Save Game",
            font=("Arial", 10),
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            width=18,
            command=self.save_game,
        ).pack(pady=3)
        tk.Button(
            btn_frame,
            text="Load Game",
            font=("Arial", 10),
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            width=18,
            command=self.load_game,
        ).pack(pady=3)
        tk.Button(
            btn_frame,
            text="Use Potion",
            font=("Arial", 10),
            bg=DANGER_COLOR,
            fg="white",
            width=18,
            command=self.use_potion,
        ).pack(pady=3)

        self.status_label = tk.Label(
            self.root, text="Ready", bg=BG_COLOR, fg="#6c7086", font=("Arial", 10)
        )
        self.status_label.pack(pady=5)

        self.update_stats_display()

    def update_stats_display(self):
        p = self.player
        text = (
            f"Name : {p['name']}\nClass: {p['class']}\nLevel: {p['level']}\n"
            f"HP   : {p['hp']}/{p['max_hp']}\nATK  : {p['attack']}\n"
            f"DEF  : {p['defense']}\nGold : {p['gold']}\nXP   : {p['xp']}"
        )
        self.stats_label.config(text=text)

        self.inventory_listbox.delete(0, tk.END)
        for item in self.inventory:
            self.inventory_listbox.insert(tk.END, item)

        room = self.get_current_room()
        if room:
            exits = ", ".join(room["exits"])
            self.room_label.config(text=f"{room['type'].title()}\nExits: {exits}")
        else:
            self.room_label.config(text="Not in dungeon")

    def append_story(self, text, tag="narrator"):
        self.story_display.config(state="normal")
        if tag == "player":
            self.story_display.insert(tk.END, f"\n> {text}\n", "player")
        elif tag == "combat":
            self.story_display.insert(tk.END, f"\n{text}\n", "combat")
        else:
            self.story_display.insert(tk.END, f"\n{text}\n", "narrator")

        self.story_display.tag_config("player", foreground="#89b4fa")
        self.story_display.tag_config("narrator", foreground="#cdd6f4")
        self.story_display.tag_config("combat", foreground="#f9e2af")
        self.story_display.see(tk.END)
        self.story_display.config(state="disabled")

    def show_welcome(self):
        welcome = """Welcome, adventurer!

This version features procedural dungeon generation.

• The dungeon is created as you explore
• Each room has exits, possible enemies, and loot
• Type actions like "go north", "look around", "search the room", "attack"
• The local Llama AI acts as your Dungeon Master

Click "New Game" to begin!"""
        self.append_story(welcome)

    def new_game(self):
        name = simpledialog.askstring("Character Name", "What is your name?")
        if not name:
            name = "Hero"

        class_choice = simpledialog.askstring(
            "Choose Class", "1. Warrior\n2. Rogue\n3. Mage\n\nType the class name:"
        )
        if class_choice and class_choice.lower() in ["warrior", "rogue", "mage"]:
            class_choice = class_choice.capitalize()
        else:
            class_choice = "Warrior"

        if class_choice == "Warrior":
            hp, atk, defense = 120, 14, 10
        elif class_choice == "Rogue":
            hp, atk, defense = 90, 13, 7
        else:
            hp, atk, defense = 70, 16, 5

        self.player = {
            "name": name,
            "class": class_choice,
            "hp": hp,
            "max_hp": hp,
            "attack": atk,
            "defense": defense,
            "gold": 25,
            "level": 1,
            "xp": 0,
        }

        self.inventory = ["Starter Weapon", "Health Potion", "Health Potion"]
        self.story_history = []
        self.in_combat = False
        self.current_enemy = None
        self.game_started = True

        # Generate starting room
        self.dungeon = {}
        self.room_counter = 0
        self.current_room_id = self.generate_room(room_type="entrance hall")
        self.get_current_room()["visited"] = True
        self.get_current_room()["has_enemy"] = False  # Safe starting room

        self.story_display.config(state="normal")
        self.story_display.delete(1.0, tk.END)
        self.story_display.config(state="disabled")

        room = self.get_current_room()
        opening = f"""You enter the ancient dungeon as a level 1 {class_choice} named {name}.

{room['description']}
Exits: {', '.join(room['exits'])}

The air is cold and heavy with the smell of damp stone. Your adventure begins here.

What do you do?"""

        self.append_story(opening)
        self.story_history.append({"role": "assistant", "content": opening})
        self.update_stats_display()
        self.status_label.config(text=f"Playing as {name} the {class_choice}")

    def send_action(self):
        if not self.game_started:
            messagebox.showinfo("Start Game", "Please start a New Game first.")
            return

        action = self.action_entry.get().strip()
        if not action:
            return

        self.action_entry.delete(0, tk.END)
        self.append_story(action, tag="player")
        self.status_label.config(text="Dungeon Master is thinking...")

        if self.in_combat:
            self.handle_combat_action(action)
            return

        # Handle movement commands directly with procedural generation
        action_lower = action.lower()
        moved = False
        for direction in ["north", "south", "east", "west"]:
            if (
                f"go {direction}" in action_lower
                or f"move {direction}" in action_lower
                or action_lower == direction
            ):
                success, result = self.move_to_direction(direction)
                if success:
                    room = result
                    desc = f"You move {direction}.\n\n{room['description']}\nExits: {', '.join(room['exits'])}"

                    if room["has_enemy"] and not room.get("enemy_defeated", False):
                        desc += f"\n\nA {room['enemy_name']} is here!"
                        self.append_story(desc)
                        self.start_combat(room["enemy_name"])
                    else:
                        if room["has_loot"] and room["loot_item"]:
                            desc += f"\n\nYou notice something: {room['loot_item']} (type 'take {room['loot_item'].lower()}' to pick it up)"
                        self.append_story(desc)

                    self.update_stats_display()
                    moved = True
                    break
                else:
                    self.append_story(result)
                    moved = True
                    break

        if moved:
            self.status_label.config(text=f"Room: {self.get_current_room()['type']}")
            return

        # Handle taking loot
        room = self.get_current_room()
        if room and room.get("loot_item") and "take" in action_lower:
            item = room["loot_item"]
            self.inventory.append(item)
            room["loot_item"] = None
            room["has_loot"] = False
            self.append_story(f"You pick up the {item}.")
            self.update_stats_display()
            return

        # Otherwise let the AI handle the action
        self.ask_dungeon_master(action)

    def ask_dungeon_master(self, action):
        room = self.get_current_room()
        room_info = ""
        if room:
            room_info = f"""Current Room Type: {room['type']}
Room Description: {room['description']}
Available Exits: {', '.join(room['exits'])}
Has Enemy: {room['has_enemy']}
Loot Available: {room.get('loot_item', 'None')}"""

        system_prompt = f"""You are an expert Dungeon Master.

Player: {self.player['name']} the {self.player['class']} (Level {self.player['level']})
HP: {self.player['hp']}/{self.player['max_hp']} | ATK: {self.player['attack']} | DEF: {self.player['defense']}
Gold: {self.player['gold']} | Inventory: {', '.join(self.inventory)}

{room_info}

Rules:
- Respond in 2-4 short paragraphs.
- Be immersive.
- If the player triggers a fight, end with: [COMBAT_START: Monster Name]
- Never break character.
- Keep responses concise."""

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.story_history[-8:])
        messages.append({"role": "user", "content": action})

        try:
            response = ollama.chat(model="llama3.1", messages=messages)
            reply = response["message"]["content"].strip()

            if "[COMBAT_START:" in reply:
                start = reply.find("[COMBAT_START:") + len("[COMBAT_START:")
                end = reply.find("]", start)
                monster_name = reply[start:end].strip()
                reply = reply.replace(f"[COMBAT_START: {monster_name}]", "").strip()
                self.append_story(reply)
                self.start_combat(monster_name)
            else:
                self.append_story(reply)

            self.story_history.append({"role": "user", "content": action})
            self.story_history.append({"role": "assistant", "content": reply})
            self.status_label.config(text="Ready")

        except Exception as e:
            messagebox.showerror(
                "Ollama Error", f"Make sure Ollama is running with llama3.1\n\n{e}"
            )
            self.status_label.config(text="Error")

    def start_combat(self, monster_name):
        self.in_combat = True
        base_hp = 25 + (self.player["level"] * 12)
        self.current_enemy = {
            "name": monster_name,
            "hp": base_hp,
            "max_hp": base_hp,
            "attack": 7 + self.player["level"] * 2,
        }
        self.append_story(
            f"⚔️ COMBAT!\n\nA {monster_name} appears!\nEnemy HP: {base_hp}\n\nType: attack / defend / use potion / flee",
            tag="combat",
        )

    def handle_combat_action(self, action):
        action = action.lower()
        enemy = self.current_enemy
        player = self.player

        if "attack" in action:
            damage = max(1, player["attack"] + random.randint(-3, 4))
            enemy["hp"] -= damage
            result = f"You hit the {enemy['name']} for {damage} damage!"

            if enemy["hp"] <= 0:
                self.win_combat()
                return

            enemy_dmg = max(
                1, enemy["attack"] + random.randint(-2, 3) - player["defense"] // 3
            )
            player["hp"] -= enemy_dmg
            result += f"\nThe {enemy['name']} strikes you for {enemy_dmg} damage!"

            if player["hp"] <= 0:
                self.player_died()
                return

        elif "defend" in action:
            enemy_dmg = max(1, enemy["attack"] // 2)
            player["hp"] -= enemy_dmg
            result = f"You defend. The {enemy['name']} hits you for {enemy_dmg} damage."

        elif "potion" in action:
            if "Health Potion" in self.inventory:
                self.inventory.remove("Health Potion")
                heal = random.randint(25, 40)
                player["hp"] = min(player["max_hp"], player["hp"] + heal)
                result = f"You heal for {heal} HP!"
            else:
                result = "No Health Potions left!"

        elif "flee" in action:
            if random.random() > 0.4:
                self.in_combat = False
                self.current_enemy = None
                self.append_story("You successfully flee!", tag="combat")
                self.update_stats_display()
                return
            else:
                enemy_dmg = max(1, enemy["attack"] // 2)
                player["hp"] -= enemy_dmg
                result = f"Failed to flee! You take {enemy_dmg} damage."
        else:
            result = "Combat commands: attack, defend, use potion, flee"

        result += f"\n\nEnemy HP: {max(0, enemy['hp'])} | Your HP: {player['hp']}/{player['max_hp']}"
        self.append_story(result, tag="combat")
        self.update_stats_display()

    def win_combat(self):
        enemy_name = self.current_enemy["name"]
        xp_gain = 12 + self.player["level"] * 7
        gold_gain = random.randint(6, 18)

        self.player["xp"] += xp_gain
        self.player["gold"] += gold_gain

        level_up_text = ""
        if self.player["xp"] >= self.player["level"] * 45:
            self.player["level"] += 1
            self.player["max_hp"] += 12
            self.player["hp"] = self.player["max_hp"]
            self.player["attack"] += 2
            self.player["defense"] += 1
            level_up_text = f"\n🎉 LEVEL UP! You are now level {self.player['level']}!"

        # Mark enemy as defeated in current room
        room = self.get_current_room()
        if room:
            room["has_enemy"] = False
            room["enemy_defeated"] = True

        result = f"You defeated the {enemy_name}!\n+{xp_gain} XP | +{gold_gain} Gold{level_up_text}"
        self.append_story(result, tag="combat")
        self.in_combat = False
        self.current_enemy = None
        self.update_stats_display()

    def player_died(self):
        self.append_story(
            f"\n💀 {self.player['name']} has fallen...\n\nGame Over.", tag="combat"
        )
        self.game_started = False
        self.in_combat = False

    def use_potion(self):
        if "Health Potion" in self.inventory:
            self.inventory.remove("Health Potion")
            heal = random.randint(25, 40)
            self.player["hp"] = min(self.player["max_hp"], self.player["hp"] + heal)
            self.append_story(f"You recover {heal} HP.")
            self.update_stats_display()
        else:
            messagebox.showinfo("No Potion", "You have no Health Potions.")

    def save_game(self):
        if not self.game_started:
            return
        data = {
            "player": self.player,
            "inventory": self.inventory,
            "dungeon": self.dungeon,
            "current_room_id": self.current_room_id,
            "room_counter": self.room_counter,
            "story_history": self.story_history[-15:],
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=2)
        messagebox.showinfo("Saved", "Game saved!")

    def load_game(self):
        if not os.path.exists(SAVE_FILE):
            messagebox.showinfo("Load", "No save found.")
            return
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)

        self.player = data["player"]
        self.inventory = data["inventory"]
        self.dungeon = data["dungeon"]
        self.current_room_id = data["current_room_id"]
        self.room_counter = data["room_counter"]
        self.story_history = data.get("story_history", [])
        self.game_started = True
        self.in_combat = False

        self.story_display.config(state="normal")
        self.story_display.delete(1.0, tk.END)
        self.story_display.config(state="disabled")

        for msg in self.story_history[-6:]:
            if msg["role"] == "user":
                self.append_story(msg["content"], tag="player")
            else:
                self.append_story(msg["content"])

        self.update_stats_display()
        messagebox.showinfo("Loaded", "Game loaded!")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AIDungeonMaster()
    app.run()
