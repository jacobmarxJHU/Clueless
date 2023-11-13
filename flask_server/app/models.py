"""
This is where all the database table models are stored in the Flask project. I've added a table for each one outlined
in the schema with primary and foreign keys. Please tweak as needed.
"""

from app import db
from sqlalchemy import Integer, ForeignKey, String, Column, Boolean, CheckConstraint
from random import choice, sample
from string import ascii_uppercase
from .utility import commit_changes

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

    __tablename__ = 'Cards'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    locationId = Column(Integer, ForeignKey('cs.Locations.id'))
    characterId = Column(Integer, ForeignKey('cs.Characters.id'))
    weaponId = Column(Integer, ForeignKey('cs.Weapons.id'))
    
    def getItem(self):
        if self.locationId:
            location = db.session.get(Location, self.locationId)
            return location.locationName if location else None

        elif self.characterId:
            character = db.session.get(Character, self.characterId)
            return character.character if character else None

        elif self.weaponId:
            weapon = db.session.get(Weapon, self.weaponId)
            return weapon.weaponName if weapon else None

        return None  # Return None if no card type matches
            
    def __repr__(self):

        if self.locationId:
            loc = db.session.get(Location, self.locationId)
            string = f"location: {loc.locationName}"
        elif self.characterId:
            ch = db.session.get(Character, self.characterId)
            string = f"character: {ch.character}"
        elif self.weaponId:
            wep = db.session.get(Weapon, self.weaponId)
            string = f"weapon: {wep.weaponName}"

        return f'<Card {string}>'


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

    @classmethod
    def generateHand(cls, gamecode: str):
        game = Game.query.filter_by(gameCode=gamecode).first()
        pis = PlayerInfo.query.filter_by(gameId=game.id).all()
        sol = Solution.query.filter_by(gameId=game.id).first()

        badIds = [sol.characterCard, sol.locationCard, sol.weaponCard]

        # generate hand
        if not sol:
            print("Error: this game does not have an associated solution")
            return

        cards = Card.query.filter(Card.id != badIds[0]).filter(Card.id != badIds[1]).filter(Card.id != badIds[2]).all()
        
        cardList = []
        for c in cards:
            cardList.append(c.id)

        i = 0
        while len(cardList) > 0 and i <= 18:
            for p in pis:
                if len(cardList) == 0:
                    break

                cardId = choice(cardList)
                cardList.remove(cardId)
                hand = Hand(cardId=cardId, playerInfo=p.id)
                db.session.add(hand)
                commit_changes()

    @classmethod
    def retrieveHand(cls, gamecode: str) -> dict:
        game = Game.query.filter_by(gameCode=gamecode).first()
        pis = PlayerInfo.query.filter_by(gameId=game.id).join(User, User.id==PlayerInfo.playerId).add_columns(User.username).all()
        
        outDict = {}
        for pi in pis:
            hand = Hand.query.filter_by(playerInfo=pi[0].id).all()
            hList = []
            for h in hand:
                card = db.session.get(Card, h.cardId)
                hList.append(card.getItem())

            outDict[pi[1]] = hList
        
        return outDict


    def __repr__(self) -> str:
        card = db.session.get(Card, self.cardId)
        pis = PlayerInfo.query.filter_by(id=self.playerInfo).join(Game, Game.id==PlayerInfo.gameId).join(User, User.id==PlayerInfo.playerId).add_columns(User.username, Game.gameCode).first()

        gamecode = pis[2]
        username = pis[1]

        return f"<Hand card: {card.getItem()}, user: {username}, game: {gamecode}>"


# Locations Table
class Location(db.Model):
    __tablename__ = 'Locations'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    locationName = Column(String(55), nullable=False)
    isRoom = Column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f"<Location {self.locationName}, room: {self.isRoom}>"


# Paths Table
class Path(db.Model):
    __tablename__ = 'Paths'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    locationId1 = Column(Integer, ForeignKey('cs.Locations.id'), nullable=False)
    locationId2 = Column(Integer, ForeignKey('cs.Locations.id'), nullable=False)
    isSecret = Column(Boolean, default=False)

    def __repr__(self) -> str:

        loc1 = Location.query.filter_by(self.locationId1).first()
        loc2 = Location.query.filter_by(self.locationId2).first()

        return f"<Path loc1: {loc1.locationName}, loc2: {loc2.locationName}, secret={self.isSecret}>"


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
            commit_changes()
            print(pi)
        
        return

    @classmethod
    def getGameState(cls, gamecode):
        game = Game.query.filter_by(gameCode=gamecode).first()
        pis = PlayerInfo.query.filter_by(gameId=game.id).join(User, User.id==PlayerInfo.playerId).join(Character, Character.id==PlayerInfo.characterId).join(Location, Location.id==PlayerInfo.id).add_columns(User.username, Character.character, Location.locationName).all()

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

    @classmethod
    def generate(cls, gamecode: str):
        game=Game.query.filter_by(gameCode=gamecode).first()
        print(game)

        users = PlayerInfo.query.filter_by(gameId=game.id).join(Character, Character.id==PlayerInfo.characterId).add_columns(Character.character).all()

        uList = []
        characters = []
        for u in users:
            uList.append(u[0].playerId)
            characters.append(u[1])

        # if Miss Scarlet is selected, have her entered as the first turn
        startTurn = 1
        if 'Miss Scarlet' in characters:
            print("Miss Scarlet found")
            scarletIndex = characters.index('Miss Scarlet')
            po = PlayerOrder(gameId=game.id, playerId=uList[scarletIndex], turn=startTurn)
            db.session.add(po)
            commit_changes()

            uList.pop(scarletIndex)
            startTurn += 1
        
        for i in range(startTurn, len(uList) + startTurn):
            u = choice(uList)
            uList.remove(u)
            po = PlayerOrder(gameId=game.id, playerId=u, turn=i)
            db.session.add(po)
            commit_changes()
        
        return

    @classmethod
    def getStart(cls, gamecode: str) -> int:
        game = Game.query.filter_by(gameCode=gamecode).first()

        firstTurn = 1

        po = PlayerOrder.query.filter_by(gameId=game.id, turn=firstTurn).first()

        po.activeTurn = True
        commit_changes()
        
        return po.playerId
    
    @classmethod
    def getNext(cls, gamecode: str) -> int:
        game = Game.query.filter_by(gameCode=gamecode).first()

        poCurrent = PlayerOrder.query.filter_by(gameId=game.id, activeTurn=True).first()

        nextTurn = poCurrent.turn + 1

        poNext = PlayerOrder.query.filter_by(gameId=game.id, turn=nextTurn).first()

        if not poNext:
            nextTurn = 1
            poNext = PlayerOrder.query.filter_by(gameId=game.id, turn=nextTurn).first()

        poCurrent.activeTurn = False
        poNext.activeTurn = True

        commit_changes()

        return poNext.playerId

    def __repr__(self) -> str:

        game = db.session.get(Game, self.gameId)
        user = db.session.get(User, self.playerId)
        return f"<PlayerOrder game: {game.gameCode}, user: {user.username}, turn: {self.turn}, activeTurn: {self.activeTurn}>"



# PlayerStatus table
class PlayerStatus(db.Model):

    __tablename__ = 'PlayerStatus'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    status = Column(String(20), nullable=False)

    def __repr__(self) -> str:
        return f"<PlayerStatus status: {self.status}>"


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
        pStart = StartLocation.query.join(Character, StartLocation.characterId==Character.id).join(Location, StartLocation.locationId==Location.id).add_columns(Character.character, Location.locationName)
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
    characterCard = Column(Integer, ForeignKey('cs.Cards.id'), nullable=False)
    gameId = Column(Integer, ForeignKey('cs.Games.id'), nullable=False, unique=True)
    locationCard = Column(Integer, ForeignKey('cs.Cards.id'), nullable=False)
    weaponCard = Column(Integer, ForeignKey('cs.Cards.id'), nullable=False)

    def generate(gamecode: str):
        gameId = Game.query.filter_by(gameCode=gamecode).first().id

        locations = Card.query.filter(Card.locationId.isnot(None)).all()
        characters = Card.query.filter(Card.characterId.isnot(None)).all()
        weapons = Card.query.filter(Card.weaponId.isnot(None)).all()

        
        locId = choice(locations).id
        wepId = choice(weapons).id
        charId = choice(characters).id
        
        sol = Solution(gameId=gameId, weaponCard=wepId, characterCard=charId, locationCard=locId)
        db.session.add(sol)
        commit_changes()
    
        return

    def __repr__(self) -> str:
        
        game = Game.query.filter_by(id=self.gameId).first()
        cCard = db.session.get(Card, self.characterCard)
        wCard = db.session.get(Card, self.weaponCard)
        lCard = db.session.get(Card, self.locationCard)

        return f"<Solution game: {game.id}, character: {cCard.getItem()}, location: {lCard.getItem()}, weapon: {wCard.getItem()}>"

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

    def __repr__(self) -> str:
        return f"<Weapon {self.weaponName}>" 


class WeaponLocation(db.Model):
    # TODO: Add class method to populate initial locations per game
    # TODO: Add class method to output the weapon locations as a dictionary (formatted for a json object)

    __tablename__ = 'WeaponLocations'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    locationId = Column(Integer, ForeignKey('cs.Locations.id'), nullable=False)
    gameId = Column(Integer, ForeignKey('cs.Games.id'), nullable=False)
    weapondId = Column(Integer, ForeignKey('cs.Weapons.id'), nullable=False)

    @classmethod
    def initializeGame(cls, gamecode):
        game = Game.query.filter_by(gameCode=gamecode).first()

        # randomly place weapons in rooms
        weapons = Weapon.query.all()
        locs = Location.query.filter_by(isRoom=True).all()

        lList = []
        for l in locs:
            lList.append(l.id)

        for w in weapons:
            locId = choice(lList)
            lList.remove(locId)
            wl = WeaponLocation(locationId=locId, weapondId=w.id, gameId=game.id)
            db.session.add(wl)
            commit_changes()
        
        return
    
    @classmethod
    def getWeaponState(cls, gamecode: str):
        game = Game.query.filter_by(gameCode=gamecode).first()
        wls = WeaponLocation.query.filter_by(gameId=game.id).join(Weapon, Weapon.id==WeaponLocation.weapondId).join(Location, Location.id==WeaponLocation.locationId).add_columns(Weapon.weaponName, Location.locationName).all()

        weaponState = {}
        for wl in wls:
            weaponState[wl[1]] =  wl[2]
        
        return weaponState

    def __repr__(self) -> str:
        
        game = Game.query.filter_by(id=self.gameId).first()
        wep = Weapon.query.filter_by(id=self.weapondId).first()
        loc = Location.query.filter_by(id=self.locationId).first()

        return f"<WeaponLocation game: {game.gameCode}, location: {loc.locationName}, weapon: {wep.weaponName}"
    

# Winners table
class Winner(db.Model):
    # TODO: make gameId unique

    __tablename__ = 'Winners'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    playerId = Column(Integer, ForeignKey('cs.Users.id'), nullable=False)
    gameId = Column(Integer, ForeignKey('cs.Games.id'), nullable=False, unique=True)
