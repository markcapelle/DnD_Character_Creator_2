from flask import Flask, render_template, request, redirect, session, jsonify
from werkzeug.security import generate_password_hash
from models import db, User # Import all models
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
    return render_template("register.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        pw1 = request.form.get("password1")
        pw2 = request.form.get("password2")

        if pw1 != pw2:
            return "Passwords do not match"

        # Create user
        new_user = User(
            email=email,
            password_hash=generate_password_hash(pw1)
        )

        db.session.add(new_user)
        db.session.commit()

        return "User registered!"

    return render_template("register.html")








@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

if __name__ == "__main__":
    app.run()