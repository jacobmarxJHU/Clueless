from app import db
from .models import PlayerInfo, Character, Weapon, Location, WeaponLocation, Game


def genLocationObject(gameCode: str) -> dict:

    # get game
    game = Game.query.filter_by(gameCode=gameCode).first()


    # TODO: change this to a join statement
    # get weapon locations -> create dictionary of weapons:locations <- both full text
    weaponLocs = WeaponLocation.query.filter_by(gameId=game.id).all()
    weaponDict = {}

    for wl in weaponLocs:
        wep = Weapon.query.filter_by(id=wl.id).first()
        loc = Location.query.filter_by(id=wl.id).first()
        weaponDict[wep.weaponName] = loc.locationName

    print(weaponDict)

    # get user locations -> create dictionary of usernames:locations <- both full text
    player = PlayerInfo.query.filter_by(gameId=game.id).all()
    userDict = {}

    for ul in player:
        pass


# Utility function to commit changes to database as they're made
def commit_changes():
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e