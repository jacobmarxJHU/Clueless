"""
This is where all the database table models are stored in the Flask project. I've added a table for each one outlined
in the schema with primary and foreign keys. Please tweak as needed.
"""

from app import db
from sqlalchemy import Integer, ForeignKey, String, Column, Boolean

# TODO: Format with SQLAlchemy ORM format (decalarative base and mapped)
# TODO: Add repr methods to each class


# Characters Table
class Character(db.Model):
    __tablename__ = 'Characters'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    character = Column(String(20), nullable=False)


# Cards Table
class Cards(db.Model):
    # TODO: Add method to get the associated character, location, or weapon string

    __tablename__ = 'Cards'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    locationId = Column(Integer, ForeignKey('cs.Locations.id'))
    characterId = Column(Integer, ForeignKey('cs.Characters.id'))
    weaponId = Column(Integer, ForeignKey('cs.Weapons.id'))


# Games Table
class Game(db.Model):
    # TODO: add max player constarint to playerCount (set to 6)
    # TODO: add min player constraint to playerCount (set to 0)
    # TODO: add default gameCode (random 6 character string)
    # TODO: make game status not nullable
    # TODO: add default value for gameStatus

    __tablename__ = 'Games'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    gameStatus = Column(Integer, ForeignKey('cs.GameStatus.id'))
    playerCount = Column(Integer, default=0, nullable=False)
    gameCode = Column(String(6), nullable=False)


# GameStatus Table
class GameStatus(db.Model):
    __tablename__ = 'GameStatus'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    status = Column(String(20), nullable=False)


# Guesses Table
class Guesse(db.Model):
    __tablename__ = 'Guesses'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    characterId = Column(Integer, ForeignKey('cs.Characters.id'), nullable=False)
    gameId = Column(Integer, ForeignKey('cs.Games.id'), nullable=False)
    locationId = Column(Integer, ForeignKey('cs.Locations.id'), nullable=False)
    weaponId = Column(Integer, ForeignKey('cs.Weapons.id'), nullable=False)
    playerId = Column(Integer, ForeignKey('cs.Users.id'), nullable=False)


# Hands Table
class Hand(db.Model):
    # TODO: add class method to generate hands at the start of the game
    # TODO: add a class method to return all cards in a users hand as dictionary

    __tablename__ = 'Hands'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    cardId = Column(Integer, ForeignKey('cs.Cards.id'), nullable=False)
    playerInfo = Column(Integer, ForeignKey('cs.PlayerInfos.id'), nullable=False)


# Locations Table
class Location(db.Model):
    __tablename__ = 'Locations'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    locationName = Column(String(55), nullable=False)
    isRoom = Column(Boolean, default=False, nullable=False)


# Paths Table
class Path(db.Model):
    __tablename__ = 'Paths'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    locationId1 = Column(Integer, ForeignKey('cs.Locations.id'), nullable=False)
    locationId2 = Column(Integer, ForeignKey('cs.Locations.id'), nullable=False)
    isSecret = Column(Boolean, default=False)


# PlayerInfo
class PlayerInfo(db.Model):

    __tablename__ = 'PlayerInfos'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    gameId = Column(Integer, ForeignKey('cs.Games.id'), nullable=False)
    characterId = Column(Integer, ForeignKey('cs.Characters.id'), nullable=False)
    locationId = Column(Integer, ForeignKey('cs.Locations.id'), nullable=False)
    isEliminated = Column(Boolean, default=False, nullable=False)
    playerId = Column(Integer, ForeignKey('cs.Users.id'), nullable=False)


# PlayerOrder Table
class PlayerOrder(db.Model):
    #TODO: update default of turn to be an increment of the current max in the playerOrder table or just remove?

    __tablename__ = 'PlayerOrder'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    gameId = Column(Integer, ForeignKey('cs.Games.id'), nullable=False)
    playerId = Column(Integer, ForeignKey('cs.Users.id'), nullable=False)
    turn = Column(Integer, default=-1, nullable=False)
    activeTurn = Column(Boolean, default=False, nullable=False)


# PlayerStatus table
class PlayerStatus(db.Model):

    __tablename__ = 'PlayerStatus'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    status = Column(String(20), nullable=False)


# StartLocations table - for initial character starting location
class StartLocation():
    # TODO: add a class method to output locations as dict 
    #   (json format) 
    #   (maybe input is character names?)

    __tablename__ = 'StartLocations'
    __table_args__ = {'schema': 'cs'}

    characterId = Column(Integer, ForeignKey('cs.Characters.id'), nullable=False)
    locationId = Column(Integer, ForeignKey('cs.Locations.id'), nullable=False)


# Solutions Table
class Solution(db.Model):
    # make gameId unique

    __tablename__ = 'Solutions'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    characterId = Column(Integer, ForeignKey('cs.Characters.id'), nullable=False)
    gameId = Column(Integer, ForeignKey('cs.Games.id'), nullable=False)
    locationId = Column(Integer, ForeignKey('cs.Locations.id'), nullable=False)
    weaponId = Column(Integer, ForeignKey('cs.Weapons.id'), nullable=False)

# Users table
class User(db.Model):
    # TODO: add default function for populated a unique 4 character playerCode
    # TODO: add default value to playerStatus (set to inactive)
    # TODO: make playerCode not nullable
    # TODO: add default to playerStatus
    # TODO: make player status not nullable
    # TODO: make playerCode, Username unique

    __tablename__ = 'Users'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    sessionInfo = Column(String(20))
    playerCode = Column(String(6))
    username = Column(String, nullable=False)
    playerStatus = Column(Integer, ForeignKey('cs.PlayerStatus.id'))


# Weapons Table
class Weapon(db.Model):
    __tablename__ = 'Weapons'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    weaponName = Column(String(20))


class WeaponLocation(db.Model):
    # TODO: Add class method to populate initial locations per game
    # TODO: Add class method to output the weapon locations as a dictionary (formatted for a json object)

    __tablename__ = 'WeaponLocations'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    locationId = Column(Integer, ForeignKey('cs.Locations.id'), nullable=False)
    gameId = Column(Integer, ForeignKey('cs.Games.id'), nullable=False)
    weapondId = Column(Integer, ForeignKey('cs.Weapons.id'), nullable=False)


# Winners table
class Winner(db.Model):
    # TODO: make gameId unique

    __tablename__ = 'Winners'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    playerId = Column(Integer, ForeignKey('cs.Users.id'), nullable=False)
    gameId = Column(Integer, ForeignKey('cs.Games.id'), nullable=False)

