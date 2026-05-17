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

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

    name = db.Column(db.String(100), nullable=False)
    race = db.Column(db.String(50))
    char_class = db.Column(db.String(50))
    hit_die = db.Column(db.String(10))
    max_hp = db.Column(db.Integer)
    background_id = db.Column(db.String(50))  # simple text for now

class Abilities(db.Model):
    __tablename__ = "abilities"

    character_id = db.Column(db.String(36), db.ForeignKey("characters.id"), primary_key=True)

    strength = db.Column(db.Integer)
    dexterity = db.Column(db.Integer)
    constitution = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    wisdom = db.Column(db.Integer)
    charisma = db.Column(db.Integer)

    character = db.relationship("Character", backref="abilities")

class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.String(36), db.ForeignKey("characters.id"), nullable=False)

    skill_name = db.Column(db.String(50), nullable=False)
    is_proficient = db.Column(db.Boolean, default=False)

    character = db.relationship("Character", backref="skills")

class State(db.Model):
    __tablename__ = "states"

    character_id = db.Column(db.String(36), db.ForeignKey("characters.id"), primary_key=True)

    current_hp = db.Column(db.Integer)
    hit_dice_remaining = db.Column(db.Integer)
    exhaustion = db.Column(db.Integer)
    deathroll_successes = db.Column(db.Integer)
    deathroll_failures = db.Column(db.Integer)

    character = db.relationship("Character", backref="state")

class Notebook(db.Model):
    __tablename__ = "notebooks"

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.String(36), db.ForeignKey("characters.id"), nullable=False)

    title = db.Column(db.String(100))
    content = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    character = db.relationship("Character", backref="notes")

# ************************************************************************************************************
# ************************************************************************************************************


