"""
This is where all the database table models are stored in the Flask project. I've added a table for each one outlined
in the schema with primary and foreign keys. Please tweak as needed.
"""

from app import db


class Users(db.Model):
    __tablename__ = 'Users'
    __table_args__ = {'schema': 'cs'}

    id = db.Column(db.Integer, primary_key=True)
    sessionInfo = db.Column(db.String)
    username = db.Column(db.String, unique=True, nullable=False)

# GameStatus Table
class GameStatus(db.Model):
    __tablename__ = 'GameStatus'
    __table_args__ = {'schema': 'cs'}

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String)


# ActivePlayers Table
class ActivePlayers(db.Model):
    __tablename__ = 'ActivePlayers'
    __table_args__ = {'schema': 'cs'}

    id = db.Column(db.Integer, primary_key=True)
    playerName = db.Column(db.String)
    playerCode = db.Column(db.String)


# ActiveGames Table
class ActiveGames(db.Model):
    __tablename__ = 'ActiveGames'
    __table_args__ = {'schema': 'cs'}

    id = db.Column(db.Integer, primary_key=True)
    gameStatus = db.Column(db.Integer, db.ForeignKey('cs.GameStatus.id'))
    playerCount = db.Column(db.Integer)
    gameCode = db.Column(db.String)
    currentPlayer = db.Column(db.Integer, db.ForeignKey('cs.ActivePlayers.id'))

# PlayerOrder Table
class PlayerOrder(db.Model):
    __tablename__ = 'PlayerOrder'
    __table_args__ = {'schema': 'cs'}

    id = db.Column(db.Integer, primary_key=True)
    gameId = db.Column(db.Integer, db.ForeignKey('cs.ActiveGames.id'))
    playerId = db.Column(db.Integer, db.ForeignKey('cs.ActivePlayers.id'))
    turn = db.Column(db.Integer)


# Characters Table
class Characters(db.Model):
    __tablename__ = 'Characters'
    __table_args__ = {'schema': 'cs'}

    id = db.Column(db.Integer, primary_key=True)
    character = db.Column(db.String)


# Locations Table
class Locations(db.Model):
    __tablename__ = 'Locations'
    __table_args__ = {'schema': 'cs'}

    id = db.Column(db.Integer, primary_key=True)
    locationName = db.Column(db.String)


# PlayerLocations Table
class PlayerLocations(db.Model):
    __tablename__ = 'PlayerLocations'
    __table_args__ = {'schema': 'cs'}

    gameId = db.Column(db.Integer, db.ForeignKey('cs.ActiveGames.id'), primary_key=True)
    playerId = db.Column(db.Integer, db.ForeignKey('cs.ActivePlayers.id'), primary_key=True)
    characterId = db.Column(db.Integer, db.ForeignKey('cs.Characters.id'))
    locationId = db.Column(db.Integer, db.ForeignKey('cs.Locations.id'))


# Rooms Table
class Rooms(db.Model):
    __tablename__ = 'Rooms'
    __table_args__ = {'schema': 'cs'}

    id = db.Column(db.Integer, primary_key=True)
    roomName = db.Column(db.String)


# Weapons Table
class Weapons(db.Model):
    __tablename__ = 'Weapons'
    __table_args__ = {'schema': 'cs'}

    id = db.Column(db.Integer, primary_key=True)
    weaponName = db.Column(db.String)


# Paths Table
class Paths(db.Model):
    __tablename__ = 'Paths'
    __table_args__ = {'schema': 'cs'}

    id = db.Column(db.Integer, primary_key=True)
    locationId1 = db.Column(db.Integer, db.ForeignKey('cs.Locations.id'))
    locationId2 = db.Column(db.Integer, db.ForeignKey('cs.Locations.id'))


# Solutions Table
class Solutions(db.Model):
    __tablename__ = 'Solutions'
    __table_args__ = {'schema': 'cs'}

    id = db.Column(db.Integer, primary_key=True)
    characterId = db.Column(db.Integer, db.ForeignKey('cs.Characters.id'))
    gameId = db.Column(db.Integer, db.ForeignKey('cs.ActiveGames.id'))
    roomId = db.Column(db.Integer, db.ForeignKey('cs.Rooms.id'))
    weaponId = db.Column(db.Integer, db.ForeignKey('cs.Weapons.id'))


# Guesses Table
class Guesses(db.Model):
    __tablename__ = 'Guesses'
    __table_args__ = {'schema': 'cs'}

    id = db.Column(db.Integer, primary_key=True)
    characterId = db.Column(db.Integer, db.ForeignKey('cs.Characters.id'))
    gameId = db.Column(db.Integer, db.ForeignKey('cs.ActiveGames.id'))
    roomId = db.Column(db.Integer, db.ForeignKey('cs.Rooms.id'))
    weaponId = db.Column(db.Integer, db.ForeignKey('cs.Weapons.id'))
    playerId = db.Column(db.Integer, db.ForeignKey('cs.ActivePlayers.id'))


