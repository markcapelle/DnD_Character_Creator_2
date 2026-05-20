from flask import Flask, render_template, request, redirect, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Character, CharacterState # Import all models
from dotenv import load_dotenv
import os

load_dotenv() # Load the .env file

app = Flask(__name__)
app.secret_key = "dev-key"


# Load Neon DB URL from .env
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Register app with SQLAlchemy
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()


# FUNCTIONS
def ability_mod(score): # Calc modifiers
    return (score - 10) // 2

app.jinja_env.globals.update(ability_mod=ability_mod)

# ROUTING
@app.route("/") # Default Route
def home():
    if "user_id" in session:
        return redirect("/index")
    
    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"]) # Login Route - should be the first page users arrive on upon opening the app
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Look up user
        user = User.query.filter_by(email=email).first()

        if not user:
            return render_template("login.html", error="User email not recognised")

        # Check password
        if not check_password_hash(user.password_hash, password):
            return render_template("login.html", error="Password is incorrect")

        # Log user in
        session["user_id"] = user.id

        return redirect("/index")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"]) # User Registration Route
def register():
    if request.method == "POST":
        email = request.form.get("email")
        pw1 = request.form.get("password1")
        pw2 = request.form.get("password2")

        if pw1 != pw2:
            return render_template("register.html", error="Passwords do not match")

        # Create user
        new_user = User(
            email=email,
            password_hash=generate_password_hash(pw1)
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect("/login?registered=1")

    return render_template("register.html")


@app.route("/index") # User Dashboard
def index():
    user_id = session.get("user_id")

    if not user_id:
        return redirect("/login")
    
    user = User.query.get(user_id)
    characters = Character.query.filter_by(user_id=user_id).all()

    return render_template("index.html", user=user, characters=characters)


@app.route("/logout") # Logout route
def logout():
    session.clear()
    return redirect("/login")


@app.route("/delete_character/<character_id>", methods=["DELETE"]) # Character deletion route
def delete_character(character_id):
    from models import (
        Character, CharacterAbilities, CharacterSkill,
        CharacterState, CharacterNotebook, db
    )

    # Delete children first (CASCADE is optional but safe)
    CharacterNotebook.query.filter_by(character_id=character_id).delete()
    CharacterState.query.filter_by(character_id=character_id).delete()
    CharacterSkill.query.filter_by(character_id=character_id).delete()
    CharacterAbilities.query.filter_by(character_id=character_id).delete()

    # Delete the character
    Character.query.filter_by(id=character_id).delete()

    db.session.commit()

    return {"success": True}



@app.route("/character/<character_id>") # Character Sheet route
def load_character(character_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    # Load character and ensure it belongs to the logged-in user
    character = Character.query.filter_by(id=character_id, user_id=user_id).first()
    if not character:
        return "Character not found or unauthorized", 404

    # Store active character in session to modify states live
    session["character_id"] = character_id

    # Load related data
    abilities = character.abilities[0] if character.abilities else None
    skills = character.skills
    state = character.state[0] if character.state else None
    notes = character.notes

    return render_template(
        "character_sheet.html",
        character=character,
        abilities=abilities,
        skills=skills,
        state=state,
        notes=notes
    )



@app.route("/spellbook/<character_id>") # Spellbook route
def spellbook(character_id):
    from models import Character, ReferenceSpell

    character = Character.query.get(character_id)
    if not character:
        return "Character not found", 404

    # Get the spellbook key from the character's class
    class_key = character.class_ref.spellbook

    # If the class has no spellbook assigned, show empty list
    if not class_key:
        spellbook = {}
        return render_template("spellbook.html", character=character, spellbook=spellbook)

    # Pull all spells for this class
    spells = ReferenceSpell.query.filter_by(class_key=class_key).order_by(ReferenceSpell.level).all()

    # Group spells by level
    spellbook = {}
    for spell in spells:
        spellbook.setdefault(spell.level, []).append(spell)

    return render_template("spellbook.html", character=character, spellbook=spellbook)



@app.route("/dice") # Dicebox route
def dice():
    return render_template("dice.html")


@app.post("/hp/<direction>") # Adjust HP - route updates the current_HP value on screen and in database real time (without refreshing)
def change_hp(direction):
    character_id = session.get("character_id")
    if not character_id:
        return {"error": "No character loaded"}, 400

    state = CharacterState.query.filter_by(character_id=character_id).first()
    character = Character.query.get(character_id)

    if not state or not character:
        return {"error": "Character not found"}, 404

    if direction == "plus":
        state.current_hp = min(state.current_hp + 1, character.max_hp)
    elif direction == "minus":
        state.current_hp = max(state.current_hp - 1, 0)
    else:
        return {"error": "Invalid direction"}, 400

    db.session.commit()

    return {
        "current_hp": state.current_hp,
        "max_hp": character.max_hp
    }



@app.post("/hitdice/toggle") # Hit Dice tracker route
def toggle_hit_dice():
    character_id = session.get("character_id")
    if not character_id:
        return {"error": "No character loaded"}, 400

    state = CharacterState.query.filter_by(character_id=character_id).first()

    # Toggle between 0 and 1 for now
    if state.hit_dice_remaining > 0:
        state.hit_dice_remaining = 0
    else:
        state.hit_dice_remaining = 1

    db.session.commit()

    return {"hit_dice_remaining": state.hit_dice_remaining}



@app.post("/deathsave/<type>/<int:index>") # Death Saves tracker route
def update_death_save(type, index):
    character_id = session.get("character_id")
    if not character_id:
        return {"error": "No character loaded"}, 400

    state = CharacterState.query.filter_by(character_id=character_id).first()

    # Clamp index between 1 and 3
    index = max(1, min(index, 3))

    if type == "success":
        # Toggle logic
        if state.deathroll_successes == index:
            state.deathroll_successes = 0
        else:
            state.deathroll_successes = index

    elif type == "fail":
        # Toggle logic
        if state.deathroll_failures == index:
            state.deathroll_failures = 0
        else:
            state.deathroll_failures = index

    else:
        return {"error": "Invalid type"}, 400

    db.session.commit()

    return {
        "successes": state.deathroll_successes,
        "failures": state.deathroll_failures
    }



@app.post("/exhaustion/<int:index>") # Exhaustion tracker route
def update_exhaustion(index):
    character_id = session.get("character_id")
    if not character_id:
        return {"error": "No character loaded"}, 400

    state = CharacterState.query.filter_by(character_id=character_id).first()

    # Clamp 0–6
    index = max(0, min(index, 6))

    # Toggle logic
    if state.exhaustion == index:
        state.exhaustion = 0
    else:
        state.exhaustion = index

    db.session.commit()

    return {"exhaustion": state.exhaustion}



@app.post("/spellslot/<int:index>") # Spellslots tracker route
def update_spellslot(index):
    character_id = session.get("character_id")
    if not character_id:
        return {"error": "No character loaded"}, 400

    state = CharacterState.query.filter_by(character_id=character_id).first()

    # Clamp between 1 and max slots
    max_slots = state.character.class_ref.spellslots or 0
    index = max(1, min(index, max_slots))

    # Toggle logic
    if state.current_spellslots == index:
        state.current_spellslots = 0
    else:
        state.current_spellslots = index

    db.session.commit()

    return {"current_spellslots": state.current_spellslots}





@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

if __name__ == "__main__":
    app.run()