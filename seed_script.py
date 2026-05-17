from app import app, db
from models import ReferenceSkill

# Running script
# run from python: python seed_script.py


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


def run_all_seeds():
    """Call all seed functions here."""
    seed_reference_skills()

    # Future seeds:
    # seed_races()
    # seed_race_traits()
    # seed_classes()
    # seed_class_features()
    # seed_backgrounds()
    # seed_spellbook()

    print("All seeds completed.")


if __name__ == "__main__":
    with app.app_context():
        run_all_seeds()
