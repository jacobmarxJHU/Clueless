"""
This is where all the database table models are stored in the Flask project. I've added a table for each one outlined
in the schema with primary and foreign keys. Please tweak as needed.
"""

from app import db


class Users(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    sessionInfo = db.Column(db.String)


# ActiveGames Table
class ActiveGames(db.Model):
    __tablename__ = 'ActiveGames'
    id = db.Column(db.Integer, primary_key=True)
    gameStatus = db.Column(db.Integer, db.ForeignKey('GameStatus.id'))
    playerCount = db.Column(db.Integer)
    gameCode = db.Column(db.String)
    currentPlayer = db.Column(db.Integer, db.ForeignKey('ActivePlayers.id'))


# GameStatus Table
class GameStatus(db.Model):
    __tablename__ = 'GameStatus'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String)


# PlayerOrder Table
class PlayerOrder(db.Model):
    __tablename__ = 'PlayerOrder'
    id = db.Column(db.Integer, primary_key=True)
    gameId = db.Column(db.Integer, db.ForeignKey('ActiveGames.id'))
    playerId = db.Column(db.Integer, db.ForeignKey('ActivePlayers.id'))
    turn = db.Column(db.Integer)


# PlayerLocations Table
class PlayerLocations(db.Model):
    __tablename__ = 'PlayerLocations'
    gameId = db.Column(db.Integer, db.ForeignKey('ActiveGames.id'), primary_key=True)
    playerId = db.Column(db.Integer, db.ForeignKey('ActivePlayers.id'), primary_key=True)
    characterId = db.Column(db.Integer, db.ForeignKey('Characters.id'))
    locationId = db.Column(db.Integer, db.ForeignKey('Locations.id'))


# ActivePlayers Table
class ActivePlayers(db.Model):
    __tablename__ = 'ActivePlayers'
    id = db.Column(db.Integer, primary_key=True)
    playerName = db.Column(db.String)
    playerCode = db.Column(db.String)


# Characters Table
class Characters(db.Model):
    __tablename__ = 'Characters'
    id = db.Column(db.Integer, primary_key=True)
    character = db.Column(db.String)


# Locations Table
class Locations(db.Model):
    __tablename__ = 'Locations'
    id = db.Column(db.Integer, primary_key=True)
    locationName = db.Column(db.String)


# Solutions Table
class Solutions(db.Model):
    __tablename__ = 'Solutions'
    id = db.Column(db.Integer, primary_key=True)
    characterId = db.Column(db.Integer, db.ForeignKey('Characters.id'))
    gameId = db.Column(db.Integer, db.ForeignKey('ActiveGames.id'))
    roomId = db.Column(db.Integer, db.ForeignKey('Rooms.id'))
    weaponId = db.Column(db.Integer, db.ForeignKey('Weapons.id'))


# Guesses Table
class Guesses(db.Model):
    __tablename__ = 'Guesses'
    id = db.Column(db.Integer, primary_key=True)
    characterId = db.Column(db.Integer, db.ForeignKey('Characters.id'))
    gameId = db.Column(db.Integer, db.ForeignKey('ActiveGames.id'))
    roomId = db.Column(db.Integer, db.ForeignKey('Rooms.id'))
    weaponId = db.Column(db.Integer, db.ForeignKey('Weapons.id'))
    playerId = db.Column(db.Integer, db.ForeignKey('ActivePlayers.id'))


# Rooms Table
class Rooms(db.Model):
    __tablename__ = 'Rooms'
    id = db.Column(db.Integer, primary_key=True)
    roomName = db.Column(db.String)


# Weapons Table
class Weapons(db.Model):
    __tablename__ = 'Weapons'
    id = db.Column(db.Integer, primary_key=True)
    weaponName = db.Column(db.String)


# Paths Table
class Paths(db.Model):
    __tablename__ = 'Paths'
    id = db.Column(db.Integer, primary_key=True)
    locationId1 = db.Column(db.Integer, db.ForeignKey('Locations.id'))
    locationId2 = db.Column(db.Integer, db.ForeignKey('Locations.id'))
