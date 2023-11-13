from app import db
from .models import PlayerInfo, WeaponLocation


def generateGameState(gamecode):
    playerState = PlayerInfo.getGameState(gamecode)
    weaponState = WeaponLocation.getWeaponState(gamecode)
    
    return {"userState": playerState, "weaponState": weaponState}


# Utility function to commit changes to database as they're made
def commit_changes():
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e