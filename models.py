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
    race = db.Column(db.String(50))
    char_class = db.Column(db.String(50))
    hit_die = db.Column(db.String(10))
    max_hp = db.Column(db.Integer)
    background_id = db.Column(db.String(50))  # simple text for now

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

class ReferenceSkill(db.Model):
    __tablename__ = "reference_skills"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    ability = db.Column(db.String(20), nullable=False)  # e.g., "dexterity", "wisdom"

