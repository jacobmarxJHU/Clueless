from app import db
from .models import PlayerInfo, Character, Weapon, Location


def genLocationObject(gameCode: str) -> dict:
    pass


# Utility function to commit changes to database as they're made
def commit_changes():
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e