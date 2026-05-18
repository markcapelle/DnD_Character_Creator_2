from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import uuid

db = SQLAlchemy()

def generate_uuid():
    return str(uuid.uuid4())

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship: one user -> many characters
    characters = db.relationship("Character", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"



# ************************************************************************************************************
# Models for storing the User's Characters
# ************************************************************************************************************

class Character(db.Model):
    __tablename__ = "characters"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

    name = db.Column(db.String(100), nullable=False)
    
    race_id = db.Column(db.Integer, db.ForeignKey("reference_races.id"))
    race = db.relationship("ReferenceRace")
    
    class_id = db.Column(db.Integer, db.ForeignKey("reference_classes.id"))
    class_ref = db.relationship("ReferenceClass")

    hit_die = db.Column(db.String(10))
    max_hp = db.Column(db.Integer)

    background_id = db.Column(db.Integer, db.ForeignKey("reference_backgrounds.id"))
    background = db.relationship("ReferenceBackground")



class CharacterAbilities(db.Model):
    __tablename__ = "character_abilities"

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.String(36), db.ForeignKey("characters.id"), unique=True)

    strength = db.Column(db.Integer)
    dexterity = db.Column(db.Integer)
    constitution = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    wisdom = db.Column(db.Integer)
    charisma = db.Column(db.Integer)

    character = db.relationship("Character", backref=db.backref("abilities", lazy=True))

class CharacterSkill(db.Model):
    __tablename__ = "character_skills"

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.String(36), db.ForeignKey("characters.id"), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey("reference_skills.id"), nullable=False)
    is_proficient = db.Column(db.Boolean, default=False)

    __table_args__ = (
        db.UniqueConstraint("character_id", "skill_id", name="uq_character_skill"),
    )

    character = db.relationship("Character", backref=db.backref("skills", lazy=True))
    reference_skill = db.relationship("ReferenceSkill", lazy=True)

class CharacterState(db.Model):
    __tablename__ = "character_states"

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.String(36), db.ForeignKey("characters.id"), unique=True)

    current_hp = db.Column(db.Integer)
    hit_dice_remaining = db.Column(db.Integer)
    exhaustion = db.Column(db.Integer)
    deathroll_successes = db.Column(db.Integer)
    deathroll_failures = db.Column(db.Integer)

    character = db.relationship("Character", backref=db.backref("state", lazy=True))

class CharacterNotebook(db.Model):
    __tablename__ = "character_notebooks"

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.String(36), db.ForeignKey("characters.id"), nullable=False)

    title = db.Column(db.String(100))
    content = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    character = db.relationship("Character", backref=db.backref("notes", lazy=True))


# ************************************************************************************************************
# ************************************************************************************************************


# ************************************************************************************************************
# Reference Models
# ************************************************************************************************************

class ReferenceSkill(db.Model): # Skills - reference model
    __tablename__ = "reference_skills"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    ability = db.Column(db.String(20), nullable=False) 

# *************************************************

class ReferenceRace(db.Model): # Races - base model
    __tablename__ = "reference_races"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    traits = db.relationship("RaceTrait", backref="race", lazy=True, cascade="all, delete-orphan")
    modifiers = db.relationship("RaceModifier", backref="race", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Race {self.name}>"

class RaceTrait(db.Model): # Races - traits model
    __tablename__ = "race_traits"

    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey("reference_races.id"), nullable=False)
    trait_text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<RaceTrait {self.trait_text[:20]}>"

class RaceModifier(db.Model): # Races - ability modifiers model
    __tablename__ = "race_modifiers"

    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey("reference_races.id"), nullable=False)
    ability = db.Column(db.String(20), nullable=False) 
    value = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<RaceModifier {self.ability} +{self.value}>"

# *************************************************

class ReferenceBackground(db.Model): # Backgrounds - base model
    __tablename__ = "reference_backgrounds"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    proficiencies = db.relationship(
        "BackgroundProficiency",
        backref="background",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Background {self.name}>"

class BackgroundProficiency(db.Model): # Backgrounds - proficiencies model
    __tablename__ = "background_proficiencies"

    id = db.Column(db.Integer, primary_key=True)
    background_id = db.Column(db.Integer, db.ForeignKey("reference_backgrounds.id"), nullable=False)

    proficiency_type = db.Column(db.String(20), nullable=False)  

    def __repr__(self):
        return f"<BackgroundProf {self.proficiency_type}: {self.proficiency_value}>"

# *************************************************

class ReferenceClass(db.Model): # Classes - base model
    __tablename__ = "reference_classes"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    base_hp = db.Column(db.Integer, nullable=False)
    hit_die = db.Column(db.String(10), nullable=False)

    skill_choices = db.Column(db.Integer, nullable=False)  # how many skills the class can choose

    spellcaster = db.Column(db.Boolean, default=False)
    spellbook = db.Column(db.String(50))  # link to spellbook.class
    spellslots = db.Column(db.Integer, nullable=True)  # only for full casters

    # Relationships
    features = db.relationship(
        "ClassFeature",
        backref="class_ref",
        lazy=True,
        cascade="all, delete-orphan"
    )

    skills = db.relationship(
        "ClassSkill",
        backref="class_ref",
        lazy=True,
        cascade="all, delete-orphan"
    )

    abilities = db.relationship(
        "ClassAbility",
        backref="class_ref",
        lazy=True,
        cascade="all, delete-orphan"
    )

    saves = db.relationship(
        "ClassSave",
        backref="class_ref",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Class {self.name}>"

class ClassFeature(db.Model): # Classes - class features
    __tablename__ = "class_features"

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey("reference_classes.id"), nullable=False)

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<ClassFeature {self.name}>"

class ClassSkill(db.Model): # Classes - available skills
    __tablename__ = "class_skills"

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey("reference_classes.id"), nullable=False)

    skill = db.Column(db.String(50), nullable=False)  # e.g., "Athletics"

    def __repr__(self):
        return f"<ClassSkill {self.skill}>"

class ClassAbility(db.Model): # Classes - main class abilities
    __tablename__ = "class_abilities"

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey("reference_classes.id"), nullable=False)

    ability = db.Column(db.String(20), nullable=False)  # e.g., "strength"

    def __repr__(self):
        return f"<ClassAbility {self.ability}>"

class ClassSave(db.Model): # Classes - save roll abilities
    __tablename__ = "class_saves"

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey("reference_classes.id"), nullable=False)

    ability = db.Column(db.String(20), nullable=False)  # e.g., "constitution"

    def __repr__(self):
        return f"<ClassSave {self.ability}>"

# *************************************************

class ReferenceSpell(db.Model): # Spellbook
    __tablename__ = "reference_spellbook"

    id = db.Column(db.Integer, primary_key=True)

    class_key = db.Column(db.String(50), nullable=False)
    # e.g., "wizard", "cleric", "druid", "paladin"

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    level = db.Column(db.Integer, nullable=False)  # 0 = cantrip
    casting_time = db.Column(db.String(50), nullable=False)
    components = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Spell {self.name} (Level {self.level})>"
