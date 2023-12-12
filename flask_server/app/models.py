"""
This is where all the database table models are stored in the Flask project. I've added a table for each one outlined
in the schema with primary and foreign keys. Please tweak as needed.
"""

from app import db
from sqlalchemy import Integer, ForeignKey, String, Column, Boolean, CheckConstraint
from random import choice, sample
from string import ascii_uppercase
from .utility import commit_changes, emptyDict

# TODO: Format with SQLAlchemy ORM format (decalarative base and mapped)
# TODO: Add repr methods to each class
# TODO: Add Cascade delete to foreign keys where appropriate


# Characters Table
class Character(db.Model):
    __tablename__ = 'Characters'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    character = Column(String(20), nullable=False)
    color = Column(String[10])

    @classmethod
    def getCharacterId(cls, cName):
        return Character.query.filter_by(character=cName).first().id
    
    @classmethod
    def getAllCharacters(cls):

        out = []
        chars = Character.query.all()
        for c in chars:
            out.append(c.character)
        
        return out

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

    @classmethod
    def getString(cls, cardId):

        card = db.session.get(Card, cardId)

        if card.locationId:
            location = db.session.get(Location, card.locationId)
            return location.locationName if location else None

        elif card.characterId:
            character = db.session.get(Character, card.characterId)
            return character.character if character else None

        elif card.weaponId:
            weapon = db.session.get(Weapon, card.weaponId)
            return weapon.weaponName if weapon else None

        return None  # Return None if no card type matches

    @classmethod
    def getCardId(cls, cid=None, lid=None, wid=None):

        if cid:
            return Card.query.filter_by(characterId=cid).first().id
        elif lid:
            if not Location.checkIsRoom(lid=lid):
                raise("Attempting to get a card with a hallway location")
            return Card.query.filter_by(locationId=lid).first().id
        elif wid:
            return Card.query.filter_by(weaponId=wid).first().id
        else:
            print("ERROR")
            return

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

        user_set = []
        for u in users:
            user_set.append(u.id)

        return user_set
    
    @classmethod
    def getGamecode_username(cls, username):
        return User.query.filter_by(username=username).join(
            Game, Game.id==User.activeGame).add_columns(Game.gameCode).first()[1]

    @classmethod
    def getGameId(cls, gamecode):
        return Game.query.filter_by(gameCode=gamecode).first().id

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

    @classmethod
    def addGuess(cls, gamecode, username, location, character, weapon):
        
        gid = Game.getGameId(gamecode)
        uid = User.getUserId(username)
        lid = Location.getLocId(location)
        wid = Weapon.getWeaponId(weapon)
        cid = Character.getCharacterId(character)

        guess = Guess(characterId=cid, weaponId=wid, locationId=lid, playerId=uid, gameId=gid)
        db.session.add(guess)
        commit_changes()
        return

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
    gameId = Column(Integer, ForeignKey('cs.Games.id'), nullable=False)

    @classmethod
    def generateHand(cls, gamecode: str):
        gid = Game.getGameId(gamecode)
        pis = PlayerInfo.query.filter_by(gameId=gid).all()
        sol = Solution.query.filter_by(gameId=gid).first()

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
                hand = Hand(cardId=cardId, playerInfo=p.id, gameId=gid)
                db.session.add(hand)
                commit_changes()

    @classmethod
    def retrieveHand(cls, gamecode: str) -> dict:
        game = Game.query.filter_by(gameCode=gamecode).first()
        pis = PlayerInfo.query.filter_by(gameId=game.id).join(
            User, User.id==PlayerInfo.playerId).add_columns(User.username, User.sessionInfo).all()
        
        outDict = {}
        for pi in pis:
            hand = Hand.query.filter_by(playerInfo=pi[0].id).all()
            hList = []
            for h in hand:
                card = db.session.get(Card, h.cardId)
                hList.append(card.getItem())

            outDict[pi[1]] = hList
        
        return outDict

    @classmethod
    def disprove(cls, gamecode, character, weapon, location):

        print(gamecode)
        print(location)
        print(weapon)
        print(character)

        cid = Character.getCharacterId(character)
        wid = Weapon.getWeaponId(weapon)
        lid = Location.getLocId(location)

        cCard = Card.getCardId(cid=cid)
        wCard = Card.getCardId(wid=wid)
        lCard = Card.getCardId(lid=lid)
        
        hands = Hand.query.filter_by(gameId=Game.getGameId(gamecode)).all()
        handList = []

        for h in hands:
            handList.append(h.cardId)
        
        if cCard in handList:
            return Card.getString(cCard)
        elif wCard in handList:
            return Card.getString(wCard)
        elif lCard in handList:
            return Card.getString(lCard)
        else:
            return None


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

    @classmethod
    def getLocId(cls, lName):
        return Location.query.filter_by(locationName=lName).first().id

    @classmethod
    def checkIsRoom(cls, lid=None, lName=None):
        if lid:
            return Location.query.filter_by(id=lid).first().isRoom
        elif lName:
            return Location.query.filter_by(locationName=lName).first().isRoom
        else:
            raise("calling Location.checkIsRoom with no arguments")

    def __repr__(self) -> str:
        return f"<Location {self.locationName}, room: {self.isRoom}>"


# Map Spots Table
class MapSpot(db.Model):
    __tablename__ = 'MapSpots'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    row = Column(Integer, nullable=False)
    col = Column(Integer, nullable=False)
    locationId = Column(Integer, ForeignKey('cs.Locations.id'), nullable=False)
    occupied = Column(Boolean, nullable=False)

    @classmethod
    def getMapDict(cls, game_code):
        gid = Game.getGameId(game_code)
        test1 = PlayerInfo.query.filter_by(gameId=gid).all()

        locDict = {}

        for t in test1:
            lid = str(t.locationId)
            color = Character.query.filter_by(id=t.characterId).first().color

            if (lid in locDict):
                tempArr = locDict[lid]
                tempArr.append(color)
                locDict[lid] = tempArr
            else:
                locDict[lid] = [color]
            
        mapDict = emptyDict()

        for key in locDict:
            spots = MapSpot.query.filter_by(locationId=int(key)).all()
            tempArr = locDict[key]

            for i in range(0, len(tempArr)):
                color = tempArr[i]
                spot = spots[i]
                tempRow = spot.row
                tempCol = spot.col
                rowStr = f"row{tempRow}"
                mapDict[rowStr][tempCol] = color
        
        return mapDict

    def __repr__(self) -> str:
        return f"<MapSpot {self.id}, row: {self.row}, col: {self.col}, lid: {self.locationId}>"



# Paths Table
class Path(db.Model):
    __tablename__ = 'Paths'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    locationId1 = Column(Integer, ForeignKey('cs.Locations.id'), nullable=False)
    locationId2 = Column(Integer, ForeignKey('cs.Locations.id'), nullable=False)
    isSecret = Column(Boolean, default=False)

    @classmethod
    def findConnected(cls, gamecode: str, username: str):
        uid = User.query.filter_by(username=username).first().id
        gid = Game.query.filter_by(gameCode=gamecode).first().id
        loc = PlayerInfo.query.filter_by(playerId=uid, gameId=gid).join(
            Location, Location.id==PlayerInfo.locationId).add_columns(Location.isRoom).first()

        currLoc = loc[0].locationId
        room = loc[1]

        paths1 = Path.query.filter_by(locationId1=currLoc).join(
            Location, Location.id==Path.locationId2).add_columns(
                Location.locationName, Location.isRoom).all()

        paths2 = Path.query.filter_by(locationId2=currLoc).join(
            Location, Location.id==Path.locationId1).add_columns(
                Location.locationName, Location.isRoom).all()

        # Get locations of all other players in the game
        occupied_locations = PlayerInfo.query.filter(
            PlayerInfo.gameId == gid,
            PlayerInfo.playerId != uid
        ).all()

        occupied_locations = [p.locationId for p in occupied_locations]

        newLocs = []

        if paths1:
            print("paths2")
            for p in paths1:
                loc_id = p[0].locationId2
                if p[0].isSecret:
                    secretPath = p[1] + " (Secret Path)"
                    newLocs.append(secretPath)
                else:
                    # Skip occupied hallways
                    if loc_id in occupied_locations and not p[2]:
                        continue

                    newLocs.append(p[1])

        if paths2:
            print("paths1")
            for p in paths2:
                loc_id = p[0].locationId1
                if p[0].isSecret:
                    secretPath = p[1] + " (Secret Path)"
                    newLocs.append(secretPath)
                else:
                    # Skip occupied hallways
                    if loc_id in occupied_locations and not p[2]:
                        continue

                    newLocs.append(p[1])

        pathInfo = {"inRoom": room, 'locations': newLocs}

        return pathInfo

    def __repr__(self) -> str:

        loc1 = Location.query.filter_by(id=self.locationId1).first()
        loc2 = Location.query.filter_by(id=self.locationId2).first()

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
    mapSpotId = Column(Integer, ForeignKey('cs.MapSpots.id'))

    @classmethod
    def initializeGame(cls, gamecode:str):
        game = Game.query.filter_by(gameCode=gamecode).first()
        usersInGame = Game.getUsers(gamecode)
        startLocs = StartLocation.getStartIds()

        for i in range(len(usersInGame)):
            userId = choice(usersInGame)
            usersInGame.remove(userId)
            charId = startLocs[i][0]
            locId = startLocs[i][1]
            pi = PlayerInfo(gameId=game.id, characterId=charId, locationId=locId, playerId=userId)
            db.session.add(pi)
            commit_changes()
        
        return

    @classmethod
    def getGameState(cls, gamecode):
        game = Game.query.filter_by(gameCode=gamecode).first()
        pis = PlayerInfo.query.filter_by(gameId=game.id).join(
            User, User.id==PlayerInfo.playerId).join(
                Character, Character.id==PlayerInfo.characterId).join(
                    Location, Location.id==PlayerInfo.locationId
                ).add_columns(User.username, Character.character, Location.locationName).all()

        state = {}

        for p in pis:
            state[p[1]] = {'character': p[2], 'location': p[3]}
        
        return state
    
    @classmethod
    def getPlayerLocationId(cls, gamecode, username):
        userId = User.getUserId(username)
        gameId = Game.getGameId(gamecode)

        return PlayerInfo.query.filter_by(gameId=gameId, playerId=userId).first().locationId
    
    @classmethod
    def getPlayerLocation(cls, gamecode, username):
        userId = User.getUserId(username)
        gameId = Game.getGameId(gamecode)

        return PlayerInfo.query.filter_by(gameId=gameId, playerId=userId).join(
            Location, Location.id==PlayerInfo.locationId
        ).add_columns(Location.locationName).first()[1]

    @classmethod
    def setEliminated(cls, gamecode, username):
        pi = PlayerInfo.query.filter_by(gameId=Game.getGameId(gamecode), playerId=User.getUserId(username)).first()
        pi.isEliminated = True
        commit_changes()

    @classmethod
    def movePlayer(cls, gamecode, newLocation, character=None, username=None):

        gid = Game.getGameId(gamecode)
        nlid = Location.getLocId(newLocation)

        if character is not None:
            cid = Character.getCharacterId(character)
            pi = PlayerInfo.query.filter_by(gameId=gid, characterId=cid).first()
        elif username is not None:
            uid = User.getUserId(username)
            pi = PlayerInfo.query.filter_by(gameId=gid, playerId=uid).first()
            pi.locationId = nlid
        else:
            raise("PlayerInfo.movePlayer -> No character or user identifier")
        
        if pi is not None:
            pi.locationId = nlid
        commit_changes()
        return

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
    isEliminated = Column(Boolean, default=False)

    @classmethod
    def getCurrSid(cls, gamecode):
        return PlayerOrder.query.filter_by(gameId=Game.getGameId(gamecode), activeTurn=True).join(
            User, User.id==PlayerOrder.playerId).add_columns(User.sessionInfo).first()[1]

    @classmethod
    def generate(cls, gamecode: str):
        game=Game.query.filter_by(gameCode=gamecode).first()

        users = PlayerInfo.query.filter_by(gameId=game.id).join(Character, Character.id==PlayerInfo.characterId).add_columns(Character.character).all()

        uList = []
        characters = []
        for u in users:
            uList.append(u[0].playerId)
            characters.append(u[1])

        # if Miss Scarlet is selected, have her entered as the first turn
        startTurn = 1
        if 'Miss Scarlet' in characters:
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

        pos = PlayerOrder.query.filter_by(gameId=game.id).join(User, User.id==PlayerOrder.playerId).add_columns(User.username).all()
        
        for po in pos:
            if po[0].turn == firstTurn:
                po[0].activeTurn = True
                startUser = po[1]
            else:
                po[0].activeTurn = False
        commit_changes()
        
        return startUser
    
    @classmethod
    def getNext(cls, gamecode: str) -> int:
        game = Game.query.filter_by(gameCode=gamecode).first()

        poCurrent = PlayerOrder.query.filter_by(gameId=game.id, activeTurn=True).first()

        nextTurn = poCurrent.turn + 1

        poNext = PlayerOrder.query.filter_by(gameId=game.id, turn=nextTurn).join(User, User.id==PlayerOrder.playerId).add_columns(User.username).first()

        # If the next player doesn't exist, reset to the first turn
        if not poNext:
            nextTurn = 1

        # Loop to find the next player who is not eliminated
        while True:
            poNext = PlayerOrder.query.filter_by(gameId=game.id, turn=nextTurn).join(User, User.id == PlayerOrder.playerId).add_columns(User.username, PlayerOrder.isEliminated).first()

            # If poNext is None, it means we have reached the end of the order, so start from the beginning
            if not poNext:
                nextTurn = 1
            elif not poNext.isEliminated:
                break
            else:
                nextTurn += 1

        # Assign new active turn
        poCurrent.activeTurn = False
        poNext[0].activeTurn = True

        commit_changes()

        return poNext[1]
    
    @classmethod
    def setEliminated(cls, gamecode, username):
        po = PlayerOrder.query.filter_by(gameId=Game.getGameId(gamecode), playerId=User.getUserId(username)).first()
        po.isEliminated = True
        commit_changes()

    @classmethod
    def getLast(cls, gamecode):
        last = PlayerOrder.query.filter_by(gameId=Game.getGameId(gamecode), isEliminated=False).join(
            User, User.id==PlayerOrder.playerId).add_columns(User.username).first()

        return last[1]

    @classmethod
    def countLeft(cls, gamecode):
        count = PlayerOrder.query.filter_by(gameId=Game.getGameId(gamecode), isEliminated=False).count()
        return count
    
    @classmethod
    def getCurrentUsername(cls, gamecode):
        return PlayerOrder.query.filter_by(gameId=Game.getGameId(gamecode), activeTurn=True).join(
            User, User.id==PlayerOrder.playerId).add_columns(User.username).first()[1]

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
    
    @classmethod
    def getSolution(cls, gamecode):
        gameId = Game.getGameId(gamecode)
        return Solution.query.filter_by(gameId=gameId).first()

    @classmethod
    def checkSol(cls, gamecode, location, weapon, character):

        lid = Location.getLocId(location)
        wid = Weapon.getWeaponId(weapon)
        cid = Character.getCharacterId(character)

        wCard = Card.getCardId(wid=wid)
        cCard = Card.getCardId(cid=cid)
        lCard = Card.getCardId(lid=lid)

        sol = Solution.query.filter_by(gameId=Game.getGameId(gamecode), locationCard=lCard, characterCard=cCard, weaponCard=wCard).first()
        if sol is None:
            return False
        else:
            return True


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

    @classmethod
    def getUserId(cls, username):
        return User.query.filter_by(username=username).first().id
    
    @classmethod
    def getSess(cls, username):
        return User.query.filter_by(username=username).first().sessionInfo

    @classmethod
    def getGid(cls, username):
        return User.query.filter_by(username=username).first().activeGame
    
    @classmethod
    def getUsernameFromSession(cls, sid):
        return User.query.filter_by(sessionInfo=sid).first().username

    def __repr__(self):
        return f"<User id: {self.id}, username: {self.username}, playerStatus: {self.playerStatus}, playerCode: {self.playerCode}, sessionInfo: {self.sessionInfo}, activeGame: {self.activeGame}>"


# Weapons Table
class Weapon(db.Model):
    __tablename__ = 'Weapons'
    __table_args__ = {'schema': 'cs'}

    id = Column(Integer, primary_key=True)
    weaponName = Column(String(20))

    @classmethod
    def getWeaponId(cls, wName):
        return Weapon.query.filter_by(weaponName=wName).first().id

    @classmethod
    def getAllWeapons(cls):

        out = []
        weps = Weapon.query.all()
        for w in weps:
            out.append(w.weaponName)
        
        return out


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

    @classmethod
    def moveWeapon(cls, gamecode, weapon, newLocation):
        lid = Location.getLocId(newLocation)
        wid = Weapon.getWeaponId(weapon)
        gid = Game.getGameId(gamecode)

        print(lid)
        print(wid)
        print(gid)

        if not Location.checkIsRoom(lid=lid):
            print("WeaponLocation.moveWeapon -> Trying to move a weapon to a hallway")
        
        wl = WeaponLocation.query.filter_by(gameId=gid, weapondId=wid).first()
        wl.locationId = lid
        commit_changes()

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

    @classmethod
    def addWinner(cls, username, gamecode):
        win = Winner(playerId=User.getUserId(username), gameId=Game.getGameId(gamecode))
        db.session.add(win)
        commit_changes()
