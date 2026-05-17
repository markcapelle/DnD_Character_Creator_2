from app import app, db
from models import ReferenceSkill, ReferenceRace, RaceTrait, RaceModifier, ReferenceBackground, BackgroundProficiency, ReferenceClass, ClassFeature, ClassSkill, ClassAbility, ClassSave, ReferenceSpell
from sqlalchemy import text

# Running script
# run from python: python seed_script.py



# DICTIONARIES
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
            "Fey Ancestry: Elves have advantage on saving throws against being charmed, and magic cannot put them to sleep.",
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



CLASSES = {
    "fighter": {
        "name": "Fighter",
        "description": "Fighters are masters of martial combat, skilled with weapons and armour.",
        "features": [
            {
                "name": "Second Wind",
                "description": "The fighter can use a bonus action to regain hit points equal to 1d10 + fighter level. Once used, a short or long rest is required before it can be used again."
            }
        ],
        "primary_abilities": ["strength", "constitution"],
        "saving_throws": ["strength", "constitution"],
        "base_hp": 10,
        "hit_die": "d10",
        "skill_choices": 2,
        "skill_list": [
            "acrobatics",
            "animal handling",
            "athletics",
            "history",
            "insight",
            "intimidation",
            "perception",
            "survival"
        ],
        "spellcaster": False,
        "spellbook": None,
        "spellslots": None
    },

    "rogue": {
        "name": "Rogue",
        "description": "Rogues are stealthy experts who excel at precision, agility, and cunning.",
        "features": [
            {
                "name": "Sneak Attack",
                "description": "Once per turn, the rogue can deal an extra 1d6 damage to a creature they hit with an attack if they have advantage on the attack roll. The attack must use a finesse or ranged weapon."
            }
        ],
        "primary_abilities": ["dexterity", "intelligence"],
        "saving_throws": ["dexterity", "intelligence"],
        "base_hp": 8,
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
            "sleight of hand",
            "stealth"
        ],
        "spellcaster": False,
        "spellbook": None,
        "spellslots": None
    },

    "wizard": {
        "name": "Wizard",
        "description": "Wizards are scholars of arcane magic who rely on intellect and study.",
        "features": [
            {
                "name": "Spellcaster",
                "description": "Using their spellbook, the wizard can cast spells."
            }
        ],
        "primary_abilities": ["intelligence"],
        "saving_throws": ["intelligence", "wisdom"],
        "base_hp": 6,
        "hit_die": "d6",
        "skill_choices": 2,
        "skill_list": [
            "arcana",
            "history",
            "insight",
            "investigation",
            "medicine",
            "religion"
        ],
        "spellcaster": True,
        "spellbook": "WIZARD_SPELLBOOK",
        "spellslots": 2
    },

    "cleric": {
        "name": "Cleric",
        "description": "Clerics are divine spellcasters who channel the power of their deity to heal allies, smite foes, and shape the battlefield through sacred magic.",
        "features": [
            {
                "name": "Spellcaster",
                "description": "Calling upon their faith, a cleric can cast spells."
            },
            {
                "name": "Turn Undead",
                "description": "Presenting their holy symbol, a cleric causes every undead within 30 feet to flee on a failed Wisdom save."
            }
        ],
        "primary_abilities": ["wisdom"],
        "saving_throws": ["charisma", "wisdom"],
        "base_hp": 8,
        "hit_die": "d8",
        "skill_choices": 2,
        "skill_list": [
            "history",
            "insight",
            "medicine",
            "persuasion",
            "religion"
        ],
        "spellcaster": True,
        "spellbook": "CLERIC_SPELLBOOK",
        "spellslots": 2
    }
}



SPELLBOOKS = {
    "cleric": [
        # --- Cantrips (level 0) ---
        {
            "level": 0,
            "name": "Spare the Dying",
            "description": "You touch a living creature that has 0 hit points. The creature becomes stable. This spell has no effect on undead or constructs.",
            "casting_time": "1 action",
            "range": "Touch",
            "components": "V, S",
            "duration": "Instantaneous"
        },
        {
            "level": 0,
            "name": "Light",
            "description": "You touch one object no larger than 10 feet in any dimension. It sheds bright light in a 20-foot radius and dim light for another 20 feet.",
            "casting_time": "1 action",
            "range": "Touch",
            "components": "V, M",
            "duration": "1 hour"
        },
        {
            "level": 0,
            "name": "Sacred Flame",
            "description": "Flame-like radiance descends on a creature you can see. Dex save or take 1d8 radiant damage. No benefit from cover.",
            "casting_time": "1 action",
            "range": "60 feet",
            "components": "V, S",
            "duration": "Instantaneous"
        },

        # --- Level 1 ---
        {
            "level": 1,
            "name": "Bless",
            "description": "Up to three creatures gain +1d4 to attack rolls and saving throws.",
            "casting_time": "1 action",
            "range": "30 feet",
            "components": "V, S, M",
            "duration": "Concentration, up to 1 minute"
        },
        {
            "level": 1,
            "name": "Cure Wounds",
            "description": "A creature you touch regains 1d8 + spellcasting modifier HP.",
            "casting_time": "1 action",
            "range": "Touch",
            "components": "V, S",
            "duration": "Instantaneous"
        }
    ],

    "wizard": [
        # --- Cantrips (level 0) ---
        {
            "level": 0,
            "name": "Fire Bolt",
            "description": "You hurl a mote of fire at a creature or object. On a hit, it takes 1d10 fire damage.",
            "casting_time": "1 action",
            "range": "120 feet",
            "components": "V, S",
            "duration": "Instantaneous"
        },
        {
            "level": 0,
            "name": "Mage Hand",
            "description": "A spectral hand appears within range. It can manipulate objects but not attack.",
            "casting_time": "1 action",
            "range": "30 feet",
            "components": "V, S",
            "duration": "1 minute"
        },
        {
            "level": 0,
            "name": "Light",
            "description": "Object sheds bright light in a 20-foot radius and dim light for another 20 feet.",
            "casting_time": "1 action",
            "range": "Touch",
            "components": "V, M",
            "duration": "1 hour"
        },

        # --- Level 1 ---
        {
            "level": 1,
            "name": "Magic Missile",
            "description": "Three darts of force automatically hit for 1d4+1 each.",
            "casting_time": "1 action",
            "range": "120 feet",
            "components": "V, S",
            "duration": "Instantaneous"
        },
        {
            "level": 1,
            "name": "Shield",
            "description": "You gain +5 AC until the start of your next turn. No damage from Magic Missile.",
            "casting_time": "1 reaction",
            "range": "Self",
            "components": "V, S",
            "duration": "1 round"
        }
    ]
}



# Seeding Functions
def seed_reference_skills():
    print("Seeding reference_skills...")

    # Always wipe the table first
    ReferenceSkill.query.delete()

    skills = [
        ("Acrobatics", "dexterity"),
        ("Animal Handling", "wisdom"),
        ("Arcana", "intelligence"),
        ("Athletics", "strength"),
        ("Deception", "charisma"),
        ("History", "intelligence"),
        ("Insight", "wisdom"),
        ("Intimidation", "charisma"),
        ("Investigation", "intelligence"),
        ("Medicine", "wisdom"),
        ("Nature", "intelligence"),
        ("Perception", "wisdom"),
        ("Performance", "charisma"),
        ("Persuasion", "charisma"),
        ("Religion", "intelligence"),
        ("Sleight of Hand", "dexterity"),
        ("Stealth", "dexterity"),
        ("Survival", "wisdom"),
    ]

    for name, ability in skills:
        db.session.add(ReferenceSkill(name=name, ability=ability))

    db.session.commit()
    print("reference_skills seeded successfully.")


def seed_reference_races():
    print("Seeding reference_races...")

    # Wipe tables and reset identity counters
    db.session.execute(text("TRUNCATE reference_races RESTART IDENTITY CASCADE;"))
    db.session.execute(text("TRUNCATE race_traits RESTART IDENTITY CASCADE;"))
    db.session.execute(text("TRUNCATE race_modifiers RESTART IDENTITY CASCADE;"))

    for key, data in RACES.items():
        race = ReferenceRace(
            key=key,
            name=data["name"],
            description=data["description"]
        )
        db.session.add(race)
        db.session.flush()  # ensures race.id is available

        # Traits
        for trait_text in data.get("traits", []):
            db.session.add(RaceTrait(race_id=race.id, trait_text=trait_text))

        # Ability modifiers
        for ability, value in data.get("modifiers", {}).items():
            db.session.add(RaceModifier(race_id=race.id, ability=ability, value=value))

    db.session.commit()
    print("reference_races seeded successfully.")


def seed_reference_backgrounds():
    print("Seeding reference_backgrounds...")

    db.session.execute(text("TRUNCATE reference_backgrounds RESTART IDENTITY CASCADE;"))
    db.session.execute(text("TRUNCATE background_proficiencies RESTART IDENTITY CASCADE;"))

    for key, data in BACKGROUNDS.items():
        background = ReferenceBackground(
            key=key,
            name=data["name"],
            description=data["description"]
        )
        db.session.add(background)
        db.session.flush()

        # Store each skill directly in proficiency_type
        for skill in data.get("proficiencies", []):
            db.session.add(
                BackgroundProficiency(
                    background_id=background.id,
                    proficiency_type=skill
                )
            )

    db.session.commit()
    print("reference_backgrounds seeded successfully.")


def seed_reference_classes():
    print("Seeding reference_classes...")

    db.session.execute(text("TRUNCATE reference_classes RESTART IDENTITY CASCADE;"))
    db.session.execute(text("TRUNCATE class_features RESTART IDENTITY CASCADE;"))
    db.session.execute(text("TRUNCATE class_skills RESTART IDENTITY CASCADE;"))
    db.session.execute(text("TRUNCATE class_abilities RESTART IDENTITY CASCADE;"))
    db.session.execute(text("TRUNCATE class_saves RESTART IDENTITY CASCADE;"))

    for key, data in CLASSES.items():
        class_entry = ReferenceClass(
            key=key,
            name=data["name"],
            description=data["description"],
            base_hp=data["base_hp"],
            hit_die=data["hit_die"],
            skill_choices=data["skill_choices"],
            spellcaster=data["spellcaster"],
            spellbook=data["spellbook"],
            spellslots=data["spellslots"]
        )
        db.session.add(class_entry)
        db.session.flush()

        # Features
        for feature in data.get("features", []):
            db.session.add(ClassFeature(
                class_id=class_entry.id,
                name=feature["name"],
                description=feature["description"]
            ))

        # Primary abilities
        for ability in data.get("primary_abilities", []):
            db.session.add(ClassAbility(
                class_id=class_entry.id,
                ability=ability
            ))

        # Saving throws
        for save in data.get("saving_throws", []):
            db.session.add(ClassSave(
                class_id=class_entry.id,
                ability=save
            ))

        # Skill list
        for skill in data.get("skill_list", []):
            db.session.add(ClassSkill(
                class_id=class_entry.id,
                skill=skill
            ))

    db.session.commit()
    print("reference_classes seeded successfully.")



def seed_spellbook():
    print("Seeding reference_spellbook...")

    # Wipe table and reset identity counter
    db.session.execute(text("TRUNCATE reference_spellbook RESTART IDENTITY CASCADE;"))

    for class_key, spells in SPELLBOOKS.items():
        for spell in spells:
            db.session.add(
                ReferenceSpell(
                    class_key=class_key,
                    name=spell["name"],
                    description=spell["description"],
                    level=spell["level"],
                    casting_time=spell["casting_time"],
                    components=spell["components"],
                    duration=spell["duration"]
                )
            )

    db.session.commit()
    print("reference_spellbook seeded successfully.")



def run_all_seeds():
    seed_reference_skills()
    seed_reference_races()
    seed_reference_backgrounds()
    seed_reference_classes()
    seed_spellbook()

    print("All seeds completed.")


if __name__ == "__main__":
    with app.app_context():
        run_all_seeds()






