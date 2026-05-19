from flask import Flask, render_template, request, redirect, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Character # Import all models
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





@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

if __name__ == "__main__":
    app.run()