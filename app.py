from flask import Flask, render_template, request, session, jsonify
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











@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


if __name__ == "__main__":
    app.run()