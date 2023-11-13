"""
This is where all the database table models are stored in the Flask project. I've added a table for each one outlined
in the schema with primary and foreign keys. Please tweak as needed.
"""

from app import db
from sqlalchemy import Integer, ForeignKey, String, Column, Boolean, CheckConstraint
from random import choice, sample
from string import ascii_uppercase

# TODO: Format with SQLAlchemy ORM format (decalarative base and mapped)
# TODO: Add repr methods to each class
# TODO: Add Cascade delete to foreign keys where appropriate


# Characters Table
class Character(db.Model):
    __tablename__ = 'Characters'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    character = Column(String(20), nullable=False)

    def __repr__(self):
        return '<Character {}>'.format(self.character)


# Cards Table
class Card(db.Model):
    # TODO: Add method to get the associated character, location, or weapon string

    __tablename__ = 'Cards'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    locationId = Column(Integer, ForeignKey('cs.Locations.id'))
    characterId = Column(Integer, ForeignKey('cs.Characters.id'))
    weaponId = Column(Integer, ForeignKey('cs.Weapons.id'))

    def __repr__(self):
        return '<Card char: {}, weap: {}, loc: {}>'.format(self.characterId, self.weaponId, self.locationId)


# Games Table
class Game(db.Model):

    __tablename__ = 'Games'
    __table_args__ = {'schema': 'cs'}


    def createGameCode(self):
        """
        creates a 6 character (ascii uppercase) string that is not already in the gameCode in the games table.
        """
        codeLength = 6
        
        #TODO: upgrade this to another algorithm (scaleability)
        currentGames = Game.query.all()
        currentCodes = []

        for game in currentGames:
            currentCodes.append(game.gameCode)
        
        while True:
            newCode = ''
            for _ in range(codeLength):
                newCode += choice(ascii_uppercase)

            if newCode not in currentCodes:
                break
        
        return newCode

    id = Column(Integer, primary_key=True)
    gameStatus = Column(Integer, ForeignKey('cs.GameStatus.id'), default=2, nullable=True)
    playerCount = Column(Integer, CheckConstraint('playerCount >= 0 and playerCount <= 6'), default=0, nullable=False)
    gameCode = Column(String(6), nullable=False, default=createGameCode, unique=True)

    @classmethod
    def getUsers(cls, gamecode):
        
        game = Game.query.filter_by(gameCode=gamecode).first()
        users = User.query.filter_by(activeGame=game.id).all()

        user_set = set()
        for u in users:
            user_set.add(u.id)

        return user_set

    def __repr__(self):
        return '<Game id: {}, status: {}, player count: {}, gameCode: {}>'.format(self.id, self.gameStatus, self.playerCount, self.gameCode)


# GameStatus Table
class GameStatus(db.Model):
    __tablename__ = 'GameStatus'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    status = Column(String(20), nullable=False)

    def __repr__(self):
        return '<GameStatus status: {}>'.format(self.status)


# Guesses Table
class Guess(db.Model):
    __tablename__ = 'Guesses'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    characterId = Column(Integer, ForeignKey('cs.Characters.id'), nullable=False)
    gameId = Column(Integer, ForeignKey('cs.Games.id'), nullable=False)
    locationId = Column(Integer, ForeignKey('cs.Locations.id'), nullable=False)
    weaponId = Column(Integer, ForeignKey('cs.Weapons.id'), nullable=False)
    playerId = Column(Integer, ForeignKey('cs.Users.id'), nullable=False)

    def __repr__(self):
        return '<Guess {}>'.format(self.id)


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

    @classmethod
    def initializeGame(cls, gamecode:str):
        game = Game.query.filter_by(gameCode=gamecode).first()
        usersInGame = Game.getUsers('TDSOLK')
        startLocs = StartLocation.getStartIds()

        for i in range(len(usersInGame)):
            userId = sample(usersInGame, 1)[0]
            usersInGame.remove(userId)
            charId = startLocs[i][0]
            locId = startLocs[i][1]
            pi = PlayerInfo(gameId=game.id, characterId=charId, locationId=locId, playerId=userId)
            db.session.add(pi)
            db.session.commit()
            print(pi)
        
        return

    @classmethod
    def getGameState(cls, gamecode):
        game = Game.query.filter_by(gameCode=gamecode).first()
        pis = PlayerInfo.query.filter_by(gameId=game.id).join(User).add_column(User.username).join(Character).add_column(Character.character).join(Location).add_column(Location.locationName).all()

        state = {}

        for p in pis:
            state[p[1]] = {'character': p[2], 'location': p[3]}
        
        return state

    def __repr__(self) -> str:

        user = User.query.filter_by(id=self.playerId).first()
        game = Game.query.filter_by(id=self.gameId).first()
        char = Character.query.filter_by(id=self.characterId).first()
        loc = Location.query.filter_by(id=self.locationId).first()

        return f"<PlayerInfo id: {self.id}, player: {user.username}, game: {game.gameCode}, char: {char.character}, loc: {loc.locationName}, isEliminated: {self.isEliminated}>"



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


# CharacterStart table - for initial character starting location
class StartLocation(db.Model):
    # TODO: add a class method to output locations as dict 
    #   (json format) 
    #   (maybe input is character names?)

    __tablename__ = 'StartLocations'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    characterId = Column(Integer, ForeignKey('cs.Characters.id'), nullable=False)
    locationId = Column(Integer, ForeignKey('cs.Locations.id'), nullable=False)

    @classmethod
    def getStartNames(cls):
        pStart = StartLocation.query.join(Character, StartLocation.characterId==Character.id).join(Location, StartLocation.locationId==Location.id).add_column(Character.character).add_column(Location.locationName)
        startLocs = {}
        for p in pStart:
            startLocs[p[1]] = p[2]
        
        return startLocs
    
    @classmethod
    def getStartIds(cls):
        pStart = StartLocation.query.all()
        startLocs = []
        for p in pStart:
            startLocs.append([p.characterId, p.locationId])
        
        return startLocs

    def __repr__(self) -> str:
        
        char = Character.query.filter_by(id=self.characterId).first()
        loc = Location.query.filter_by(id=self.locationId).first()

        return f"<StartLocation char: {char.character}, loc: {loc.locationName}>"


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

    def createPlayerCode(self):
        """
        creates a 6 character (ascii uppercase) string that is not already in the Users playerCode table.
        """
        codeLength = 6
        
        #TODO: upgrade this to another algorithm (scaleability)
        currentUsers = User.query.all()
        currentCodes = []

        for user in currentUsers:
            currentCodes.append(user.playerCode)
        
        print(currentCodes)
        
        while True:
            newCode = ''
            for _ in range(codeLength):
                newCode += choice(ascii_uppercase)

            if newCode not in currentCodes:
                break
        
        return newCode

    __tablename__ = 'Users'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    sessionInfo = Column(String(20))
    playerCode = Column(String(6), default=createPlayerCode, unique=True, nullable=False) # default creates a unique 6 character string not already in the column
    username = Column(String, nullable=False, unique=True)
    playerStatus = Column(Integer, ForeignKey('cs.PlayerStatus.id'), default=2, nullable=False) # defaults to inactive
    isLeader = Column(Boolean, default=False, nullable=False)
    activeGame = Column(Integer, ForeignKey('cs.Games.id'))

    def __repr__(self):
        return f"<User id: {self.id}, username: {self.username}, playerStatus: {self.playerStatus}, playerCode: {self.playerCode}, sessionInfo: {self.sessionInfo}, activeGame: {self.activeGame}>"


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
    gameId = Column(Integer, ForeignKey('cs.Games.id'), nullable=False, unique=True)
