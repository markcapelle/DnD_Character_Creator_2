from flask import Flask, render_template, request, session, jsonify

app = Flask(__name__)
app.secret_key = "dev-key"


# Character class
class Character:
    def __init__(self):
        self.points_pool = 24
        self.proficiency = 2 #Proficiency modifier, starts at +2
        
        self.race = None
        self.char_class = None
        self.background = None

        self.abilities = {
            "strength": 8,
            "dexterity": 8,
            "constitution": 8,
            "intelligence": 8,
            "wisdom": 8,
            "charisma": 8
        }

        self.skills = {
            "acrobatics": False,
            "animal_handling": False,
            "arcana": False,
            "athletics": False,
            "deception": False,
            "history": False,
            "insight": False,
            "intimidation": False,
            "investigation": False,
            "medicine": False,
            "nature": False,
            "perception": False,
            "performance": False,
            "persuasion": False,
            "religion": False,
            "sleight_of_hand": False,
            "stealth": False,
            "survival": False
        }
    
    def increase(self, ability):
        if self.points_pool > 0: #If there are points available
            self.abilities[ability] += 1 #Increase selected ability by 1
            self.points_pool -= 1 #Reduce available points by 1
    
    def decrease(self, ability):
        if self.abilities[ability] > 8: #If selected ability is not 8 (minimum)
            self.abilities[ability] -= 1 #Reduce selected ability by 1
            self.points_pool += 1 #Increase available points by 1

    def calculate_modifiers(self):
        self.modifiers = {}
        for ability, score in self.abilities.items():
            self.modifiers[ability] = (score - 10) // 2

    def calculate_skill_bonuses(self):
        skill_bonuses = {}

        for skill, ability in SKILLS.items():
            mod = self.modifiers.get(ability, 0)
            proficient = self.skills.get(skill, False)
            bonus = mod + (self.proficiency if proficient else 0)
            skill_bonuses[skill] = bonus

        return skill_bonuses

    def apply_background(self, background_data):
        for prof in background_data.get("proficiencies", []):
            self.skills[prof] = True

    @classmethod
    def from_dict(cls, data):
        c = cls()
        c.points_pool = data.get("points_pool", 27)
        c.proficiency = data.get("proficiency", c.proficiency)
        c.race = data.get("race")
        c.char_class = data.get("char_class")
        c.background = data.get("background")
        c.abilities = data.get("abilities", {}).copy()
        c.skills = data.get("skills", {}).copy()
        return c

    def to_dict(self):
        return {
            "abilities": self.abilities,
            "points_pool": self.points_pool,
            "proficiency": self.proficiency,
            "race": self.race,
            "char_class": self.char_class,
            "background": self.background,
            "skills": self.skills
        }
#============ End Character Class ============



#============ Libraries ============
RACES = {
    "human": {
        "name": "Human",
        "description": "In the reckonings of most worlds, humans are the youngest of the common races, late to arrive on the world scene and short-lived in comparison to dwarves, elves and dragons."
            " Perhaps it is because of their shorter lives that they strive to achieve as much as they can in the years they are given."
            " Or maybe they feel they have something to prove to the elder races, and that's why they build their mighty empires on the foundation of conquest and trade."
            " Whatever drives them, humans are the innovators, the achievers, and the pioneers of the worlds.",
        "traits": [
            "Fast Learners: Human ability scores all increase by 1.",
        ],
        "modifiers": {
            "strength": 1,
            "dexterity": 1,
            "constitution": 1,
            "intelligence": 1,
            "wisdom": 1,
            "charisma": 1
        }
    },

    "elf": {
        "name": "Elf",
        "description": "Elves are a magical people of otherworldly grace, living in the world but not entirely part of it."
            " They live in places of ethereal beauty, in the midst of ancient forests or in silvery spires glittering with faerie lights,"
                " where soft music drifts through the air and gentle fragrances waft on the breeze."
            " Elves love nature and magic, art and artistry, music and poetry, and the good things of the world.",
        "traits": [
            "Darkvision: Elves are accustomed to twilit forests and the night sky. They have superior vision in dark and dim conditions."
                " They can see in dim light within 60 feet ahead as if it were bright light, and in darkness as if it were dim light."
                " They cannot discern colour in darkness, only shades of grey.",
            "Fey Ancestry: Elves have advantage on saving throws agiasnt being charmed, and magic cannot put them to sleep.",
            "Trance: Elves do not need to sleep, and can instead meditate for 4 hours a day. Meditating gives the same benefit as 8 hours of sleep."
        ],
        "modifiers": {
            "dexterity": 2
        }
    },

    "dwarf": {
        "name": "Dwarf",
        "description": "Kingdoms rich in ancient grandeur, halls carved into the roots of mountains, the echoing of picks and hammers in deep mines and blazing forges,"
            " a commitment to clan and tradition, and a burning hatred of goblins and orcs - these common threads unite all dwarves.",
        "traits": [
            "Darkvision: Accustomed to life underground, Dwarves have superior vision in dark and dim conditions."
                " They can see in dim light within 60 feet ahead as if it were bright light, and in darkness as if it were dim light."
                " They cannot discern colour in darkness, only shades of grey.",
            "Dwarven Resilience: Dwarves have advantage on saving throws against poison, and have a resistance against poison damage.",
            "Dwarven Combat Training: Movement speed is not reduced by wearing heavy armour and dwarves have proficiency with battleaxes, handaxes, light hammers and warhammers."
        ],
        "modifiers": {
            "constitution": 2
        }
    },

    "dragonborn": {
        "name": "Dragonborn",
        "description": "Born of dragons, as their name proclaims, the dragonborn walk proudly through a world that greets them with fearful incomprehension."
            " Shaped by draconic gods or the dragons themselves, dragonborn originally hatched from dragon eggs as a unique race, combining the best attributes of dragons and humanoids."
            " Some dragonborn are faithful servants to true dragons, others form the ranks of soldiers in great wars, and still others find themselves adrift, with no clear calling in life.",
        "traits": [
            "Damage Resistance: A dragonborn is resistant to fire damage.",
            "Fire Breath: Dragonborn can breathe fire in a 5 by 30 foot line. Targets in its path must make a saving throw vs 8 + Con + Proficiency. A failed save deals 2d6 fire damage. A successful save deals half damage."
        ],
        "modifiers": {
            "strength": 2,
            "charisma": 1
        }
    }
}

CLASSES = {
    "fighter": {
        "name": "Fighter",
        "description": "Fighters are masters of martial combat, skilled with weapons and armour.",
        "class_features": [
            "Second Wind: The fighter can use a bonus action to regain hit points equal to 1d10 + fighter level. Once the feature is used a short or long rest must be taken before it can be used again."
        ],
        "primary_abilities": ["strength", "constitution"],
        "saving_throws": ["strength", "constitution"],
        "hit_points": 10,
        "hit_die": "d10",
        "skill_choices": 2,
        "skill_list": [
            "acrobatics",
            "animal_handling",
            "athletics",
            "history",
            "insight",
            "intimidation",
            "perception",
            "survival"
        ],
        "spellcaster": False,
        "spellbook": None,
        "spell_slots": None
    },

    "rogue": {
        "name": "Rogue",
        "description": "Rogues are stealthy experts who excel at precision, agility, and cunning.",
        "class_features": [
            "Sneak Attack: Once per turn the rogue can deal an extra 1d6 damage to one creature they hit with an attack if you have advantage on the attack roll."
            " The attack must use a finesse or ranged weapon."
        ],
        "primary_abilities": ["dexterity", "intelligence"],
        "saving_throws": ["dexterity", "intelligence"],
        "hit_points": 8,
        "hit_die": "d8",
        "skill_choices": 4,
        "skill_list": [
            "acrobatics",
            "athletics",
            "deception",
            "insight",
            "intimidation",
            "investigation",
            "perception",
            "performance",
            "persuasion",
            "sleight_of_hand",
            "stealth"
        ],
        "spellcaster": False,
        "spellbook": None,
        "spell_slots": None
    },

    "wizard": {
        "name": "Wizard",
        "description": "Wizards are scholars of arcane magic who rely on intellect and study.",
        "class_features": [
            "Spellcaster: Using their spellbook, the wizard can cast spells."
        ],
        "primary_abilities": ["intelligence"],
        "saving_throws": ["intelligence", "wisdom"],
        "hit_points": 6,
        "hit_die": "d6",
        "skill_choices": 2,
        "skill_list": [
            "arcana",
            "history",
            "insight",
            "investigation",
            "medicine",
            "religion",
        ],
        "spellcaster": True,
        "spellbook": "WIZARD_SPELLBOOK",
        "spell_slots": 2
    },

    "cleric": {
        "name": "Cleric",
        "description": "Clerics are divine spellcasters who channel the power of their deity to heal allies, smite foes, and shape the battlefield through sacred magic.",
        "class_features": [
            "Spellcaster: Calling upon their faith, a cleric can cast spells.",
            "Turn Undead: Presenting their holy symbol, a cleric causes every undead within 30 feet to flee on a failed wisdom save."
        ],
        "primary_abilities": ["wisdom"],
        "saving_throws": ["charisma", "wisdom"],
        "hit_points": 8,
        "hit_die": "d8",
        "skill_choices": 2,
        "skill_list": [
            "history",
            "insight",
            "medicine",
            "persuasion",
            "religion",
        ],
        "spellcaster": True,
        "spellbook": "CLERIC_SPELLBOOK",
        "spell_slots": 2
    }
}

SKILLS = {
    "acrobatics": "dexterity",
    "animal_handling": "wisdom",
    "arcana": "intelligence",
    "athletics": "strength",
    "deception": "charisma",
    "history": "intelligence",
    "insight": "wisdom",
    "intimidation": "charisma",
    "investigation": "intelligence",
    "medicine": "wisdom",
    "nature": "intelligence",
    "perception": "wisdom",
    "performance": "charisma",
    "persuasion": "charisma",
    "religion": "intelligence",
    "sleight_of_hand": "dexterity",
    "stealth": "dexterity",
    "survival": "wisdom"
}

BACKGROUNDS = {
    "acolyte": {
        "name": "Acolyte",
        "description": "The Acolyte has spent years in service to a temple or sacred order, shaped by ritual, study, and unwavering devotion to a higher power.",
        "proficiencies": ["insight", "religion"]
    },

    "criminal": {
        "name": "Criminal",
        "description": "The Criminal has lived a life shaped by shadows, deception, and illicit dealings, relying on quick wits and a talent for slipping past notice.",
        "proficiencies": ["deception", "stealth"]
    },

    "folk_hero": {
        "name": "Folk Hero",
        "description": "The Folk Hero has risen from humble origins, earning the admiration of common people through acts of bravery, compassion, and defiance against injustice.",
        "proficiencies": ["animal_handling", "survival"]
    },

    "noble": {
        "name": "Noble",
        "description": "The Noble was raised among wealth and influence, shaped by formal education, courtly expectations, and the responsibilities of a distinguished lineage.",
        "proficiencies": ["history", "persuasion"]
    },

    "sage": {
        "name": "Sage",
        "description": "The Sage has spent years in study and research, driven by an insatiable curiosity and a deep desire to uncover the truths of the world.",
        "proficiencies": ["arcana", "history"]
    },

    "soldier": {
        "name": "Soldier",
        "description": "The Soldier has been forged by discipline, drill, and the harsh realities of battle, serving in organized ranks and learning the demands of command and obedience alike.",
        "proficiencies": ["athletics", "intimidation"]
    }
}



# Spellbook libraries
WIZARD_SPELLBOOK = {
    "cantrips": [
        {
            "name": "Fire Bolt",
            "description": "You hurl a mote of fire at a creature or object within range. You make a ranged spell attack agiasnt the target."
                " On a hit, the target takes 1d10 fire damage. A flammable object hit by this spell ignites if it isn't beign worn or carried.",
            "casting_time": "1 action",
            "range": "120 feet",
            "components": "V, S",
            "duration": "Instantaneous"
        },
        {
            "name": "Mage Hand",
            "description": "A spectral, floating hand appears at a point you choose within range. The hand can't attack, activate magic items, or carry more than 10 pounds.",
            "casting_time": "1 action",
            "range": "30 feet",
            "components": "V, S",
            "duration": "1 minute"
        },
        {
            "name": "Light",
            "description": "You touch one object that is no larger than 10 feet in any dimension. Until the spell ends, the object sheds bright light in a 20-foot radius and dim light for an additional 20 feet.",
            "casting_time": "1 action",
            "range": "Touch",
            "components": "V, M",
            "duration": "1 hour"
        }
    ],
    "level_1": [
        {
            "name": "Magic Missile",
            "description": "You create three glowing darts of magical force. Each dart hits a creature of your choice that you can see within range."
                " A dart deals 1d4 + 1 force damage to its target. The darts all strike simultaneously, and you can direct them to hit one creature or several.",
            "casting_time": "1 action",
            "range": "120 feet",
            "components": "V, S",
            "duration": "Instantaneous"
        },
        {
            "name": "Shield",
            "description": "An invisible barrier of magical force appears and protects you."
                " Until the start of your next turn, you have a +5 bonus to AC, including agiasnt the triggering attack, and you take no damage from magic missile.",
            "casting_time": "1 reaction",
            "range": "Self",
            "components": "V, S",
            "duration": "1 round"
        }
    ]
}

CLERIC_SPELLBOOK = {
    "cantrips": [
        {
            "name": "Spare the Dying",
            "description": "You touch a living creature that has 0 hit points. The creature becomes stable. This spell has no effect on undead or constructs.",
            "casting_time": "1 action",
            "range": "Touch",
            "components": "V, S",
            "duration": "Instantaneous"
        },
        {
            "name": "Light",
            "description": "You touch one object that is no larger than 10 feet in any dimension. Until the spell ends, the object sheds bright light in a 20-foot radius and dim light for an additional 20 feet.",
            "casting_time": "1 action",
            "range": "Touch",
            "components": "V, M",
            "duration": "1 hour"
        },
        {
            "name": "Sacred Flame",
            "description": "Flame-like radiance descends on a creature that you can see within range. The target must succeed on a dexterity saving throw or take 1d8 radiant damage. The target gains no benefit from taking cover.",
            "casting_time": "1 action",
            "range": "60 feet",
            "components": "V, S",
            "duration": "Instantaneous"
        }
    ],
    "level_1": [
        {
            "name": "Bless",
            "description": "You bless up to three creatures of your choice within range. Whenever a target makes an attack roll or a saving throw before the spell ends, the target can roll a d4 and add the number rolled to the attack roll or saving throw.",
            "casting_time": "1 action",
            "range": "30 feet",
            "components": "V, S, M",
            "duration": "Concentration, up to 1 minute"
        },
        {
            "name": "Cure Wounds",
            "description": "A creature you touch regains a number of hit points equal to 1d8 + your spellcasting ability modifier. This spell has no effect on undead or constructs.",
            "casting_time": "1 action",
            "range": "Touch",
            "components": "V, S",
            "duration": "Instantaneous"
        }
    ]
}

def get_character():
    if "character" not in session:
        session["character"] = Character().to_dict()
    return session["character"]

def save_character(char_dict):
    session["character"] = char_dict




# =======================
# RENDER Pages
# =======================

@app.route("/") #Render the landing page
def index():
    character = get_character()
    return render_template("abilities.html", character=character, races=RACES, classes=CLASSES)

@app.route("/skills") #Render skills selection page
def skills():
    sheet = session.get("character_sheet", {})
    class_data = CLASSES.get(sheet.get("class"), {})

    return render_template(
        "skills.html",
        sheet=sheet,
        skills=SKILLS,
        allowed_skills=class_data.get("skill_list", []),
        max_choices=class_data.get("skill_choices", 0)
    )

@app.route("/background") #Render the background selection page
def background():
    return render_template("background.html", backgrounds=BACKGROUNDS)

@app.route("/index")
def home():
    sheet = build_character_sheet()
    if sheet is None:
        sheet = {}
    return render_template("index.html", sheet=sheet)

@app.route("/dice") #Render dicebox window
def dice():
    return render_template("dice.html")

@app.route("/spellbook") #Render spellbook window
def spellbook_page():
    sheet = session.get("character_sheet", {})
    spellbook_name = sheet.get("spellbook")

    # Load the correct spellbook dict
    spellbook = globals().get(spellbook_name, {})

    return render_template("spellbook.html", spellbook=spellbook)


# =======================
# ROUTES
# =======================

@app.route("/increase", methods=["POST"]) #Increase ability
def increase():
    ability = request.json.get("ability")

    char = Character()
    char.__dict__.update(get_character())

    char.increase(ability)
    save_character(char.to_dict())

    return jsonify(char.to_dict())

@app.route("/decrease", methods=["POST"]) #Decrease ability
def decrease():
    ability = request.json.get("ability")

    char = Character()
    char.__dict__.update(get_character())

    char.decrease(ability)
    save_character(char.to_dict())

    return jsonify(char.to_dict())

@app.route("/select_race", methods=["POST"]) #Select and store race
def select_race():
    race = request.json.get("race")

    char = Character()
    char.__dict__.update(get_character())

    char.race = race
    save_character(char.to_dict())

    race_data = RACES.get(race, {})

    return jsonify({
        "race": race,
        "description": race_data.get("description", ""),
        "traits": race_data.get("traits", []),
        "modifiers": race_data.get("modifiers", {})
    })

@app.route("/select_class", methods=["POST"]) #Select and store class
def select_class():
    class_name = request.json.get("class")

    char = Character()
    char.__dict__.update(get_character())

    char.char_class = class_name
    save_character(char.to_dict())

    class_data = CLASSES.get(class_name, {})

    return jsonify({
        "class": class_name,
        "description": class_data.get("description", ""),
        "class_features": class_data.get("class_features", ""),
        "primary_abilities": class_data.get("primary_abilities", []),
        "saving_throws": class_data.get("saving_throws", []),
        "hit_die": class_data.get("hit_die", ""),
        "spellcaster": class_data.get("spellcaster", False),
        "spellbook": class_data.get("spellbook", None)
    })

#Check first page is ready to proceed
@app.route("/is_ready", methods=["GET"])
def is_ready():
    char = get_character()

    race_ok = bool(char.get("race"))
    class_ok = bool(char.get("char_class"))
    points_ok = char.get("points_pool", 0) == 0

    return jsonify({
        "ready": race_ok and class_ok and points_ok,
        "race_ok": race_ok,
        "class_ok": class_ok,
        "points_ok": points_ok
    })

#Build complete character sheet
def build_character_sheet():
    char_data = get_character()
    if not char_data:
        return None

    character = Character.from_dict(char_data)

    # Apply race modifiers
    race_data = RACES.get(character.race, {})
    race_mods = race_data.get("modifiers", {})

    final_abilities = {}
    for ability, score in character.abilities.items():
        final_abilities[ability] = score + race_mods.get(ability, 0)

    character.abilities = final_abilities
    character.calculate_modifiers()

    # Background
    background_key = character.background
    background_data = BACKGROUNDS.get(background_key, {})
    character.apply_background(background_data)

    # Skills
    skill_bonuses = character.calculate_skill_bonuses()

    # Class
    class_data = CLASSES.get(character.char_class, {})

    # Calculate hit points
    hit_points = class_data.get("hit_points", 0)
    con_mod = character.modifiers.get("constitution", 0)
    max_hp = hit_points + con_mod

    # Spellcasting stats, if any
    if class_data.get("spellcaster"):
        spell_ability = class_data["primary_abilities"][0]  # e.g. intelligence for wizard, wisdom for cleric
        spell_mod = character.modifiers.get(spell_ability, 0)

        spell_save_dc = 8 + character.proficiency + spell_mod
        spell_attack_bonus = character.proficiency + spell_mod
    else:
        spell_ability = None
        spell_mod = None
        spell_save_dc = None
        spell_attack_bonus = None

    character_sheet = {
        "race": character.race,
        "race_name": race_data.get("name", ""),
        "class": character.char_class,
        "class_name": class_data.get("name", ""),
        "class_features": class_data.get("class_features", ""),
        "spellcaster": class_data.get("spellcaster", False),
        "spellbook": class_data.get("spellbook", None),
        "spell_slots_used": 0,
        "max_spell_slots": class_data.get("spell_slots", None),
        "spellcasting_ability": spell_ability,
        "spell_save_dc": spell_save_dc,
        "spell_attack_bonus": spell_attack_bonus,
        "proficiency": character.proficiency,
        "abilities": final_abilities,
        "ability_modifiers": character.modifiers,
        "skill_proficiencies": character.skills,
        "skills": skill_bonuses,
        "hit_die": class_data.get("hit_die", ""),
        "hit_dice_used": 0,
        "death_rolls_success": 0,
        "death_rolls_fails": 0,
        "max_hp": max_hp,
        "current_hp": max_hp,
        "primary_abilities": class_data.get("primary_abilities", []),
        "saving_throws": class_data.get("saving_throws", []),
        "traits": race_data.get("traits", []),
        "description": {
            "race": race_data.get("description", ""),
            "class": class_data.get("description", "")
        },
        "background": background_key,
        "background_name": background_data.get("name", ""),
        "background_description": background_data.get("description", ""),
        "background_proficiencies": background_data.get("proficiencies", []),
    }

    session["character_sheet"] = character_sheet
    return character_sheet


#Commit abilities.html to character
@app.route("/commit_character", methods=["POST"])
def commit_character():
    sheet = build_character_sheet()
    if sheet is None:
        return jsonify({"success": False, "error": "No character in session"})
    return jsonify({"success": True})


# Add the skills to the character sheet
@app.route("/set_skills", methods=["POST"])
def set_skills():
    data = request.json
    selected_skills = data.get("skills", [])

    character = session.get("character")
    if not character:
        return {"success": False, "error": "No character in session"}

    # Ensure skills dict exists
    skills = character.get("skills", {})

    # Reset all skills
    for skill in skills:
        skills[skill] = False

    # Apply selected skills
    for skill in selected_skills:
        if skill in skills:
            skills[skill] = True

    character["skills"] = skills
    session["character"] = character

    return {"success": True}



@app.route("/background_ready")
def background_ready():
    char = get_character()
    if not char:
        return jsonify({"ready": False})

    background = char["background"] if isinstance(char, dict) else char.background

    return jsonify({"ready": bool(background)})



@app.route("/set_background", methods=["POST"])
def set_background():
    data = request.get_json()
    selected = data.get("background")

    if not selected or selected not in BACKGROUNDS:
        return jsonify({"success": False, "error": "Invalid background"})

    char = get_character()
    if not char:
        return jsonify({"success": False, "error": "No character in session"})

    # Handle both dict and Character object
    if isinstance(char, dict):
        char["background"] = selected
    else:
        char.background = selected
        char = char.to_dict()  # normalize for session storage

    session["character"] = char

    return jsonify({"success": True})

# Adjust character health
@app.route("/hp/<action>", methods=["POST"])
def modify_hp(action):
    sheet = session.get("character_sheet", {})

    current = sheet.get("current_hp", 0)
    max_hp = sheet.get("max_hp", 0)

    if action == "up":
        current = min(current + 1, max_hp)
    elif action == "down":
        current = max(current - 1, 0)

    sheet["current_hp"] = current
    session["character_sheet"] = sheet

    return {"current_hp": current, "max_hp": max_hp}

# Track the character's hit dice useage.
@app.route("/hitdice/update", methods=["POST"])
def update_hitdice():
    sheet = session.get("character_sheet", {})

    count = int(request.json.get("count", 0))
    # clamp between 0 and 3 for now — can be scaled for levels
    count = max(0, min(count, 3))

    sheet["hit_dice_used"] = count
    session["character_sheet"] = sheet

    return {"hit_dice_used": count}

# Track the character's death rolls (successes and fails).
@app.route("/deathroll/update", methods=["POST"])
def update_deathroll():
    sheet = session.get("character_sheet", {})

    roll_type = request.json.get("type")      # "success" or "fail"
    delta = int(request.json.get("delta", 0)) # +1 or -1

    if roll_type not in ("success", "fail"):
        return {"error": "Invalid roll type"}, 400

    key = "death_rolls_success" if roll_type == "success" else "death_rolls_fails"

    # Update and clamp 0–3
    current = sheet.get(key, 0)
    current = max(0, min(3, current + delta))
    sheet[key] = current

    session["character_sheet"] = sheet

    return {
        "success": sheet.get("death_rolls_success", 0),
        "fails": sheet.get("death_rolls_fails", 0)
    }

# Track spellcaster's spell slots
@app.route("/spellslots/update", methods=["POST"])
def update_spellslots():
    sheet = session.get("character_sheet", {})

    max_slots = sheet.get("max_spell_slots")
    if max_slots is None:
        return {"error": "Class has no spell slots"}, 400

    try:
        count = int(request.json.get("count"))
    except (TypeError, ValueError):
        return {"error": "Invalid count"}, 400

    # clamp
    count = max(0, min(count, max_slots))

    sheet["spell_slots_used"] = count
    session["character_sheet"] = sheet

    return {"spell_slots_used": count}


@app.route("/reset", methods=["POST"])
def reset():
    session.clear()  # wipes ALL session data
    return {"success": True}




@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


if __name__ == "__main__":
    app.run()