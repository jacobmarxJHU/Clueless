from app import db
from .models import (
    Game, PlayerOrder, WeaponLocation, Path, Hand, PlayerInfo, Solution
)
import random
import json
from .utility import commit_changes
from .extensions import socketio
from flask_socketio import emit


# Master initialize board function to pass initialized game state to front end
def initialize_board(gamecode: str):
    # CONFIRM GAME IS EMPTY and change to active
    game = Game.query.filter_by(gameCode=gamecode).first()

    pi = PlayerInfo.query.filter_by(gameId=game.id).first()

    if pi:
        print("ERROR: GAME ALREADY EXISTS")
        return
    else:
        game.gameStatus = 4
        commit_changes()

    # GAME GENERATION
    # generates user characters and starting locations
    PlayerInfo.initializeGame(gamecode)
    # generates starting location for weapons
    WeaponLocation.initializeGame(gamecode)
    # generates solution
    Solution.generate(gamecode)
    # generates hands
    Hand.generateHand(gamecode)
    # generate player order
    PlayerOrder.generate(gamecode)
    
    # GETTING INFO TO BE PASSED TO USER
    startingUser = PlayerOrder.getStart(gamecode)
    
    # PASSING GAME STATE TO FRONT END
    emitState(gamecode)
    emitHands(gamecode)
    
    # PASSING PLAYER THAT IS STARTING THE GAME
    emitTurnInfo(gamecode, startingUser)


def emitTurnInfo(gamecode: str, username: str = None):

    if not username:
        username = PlayerOrder.getNext(gamecode)

    paths = Path.findConnected(gamecode, username)
    
    emitPackage = {username: paths}
    print(emitPackage)

    # emit("start_turn", emitPackage, to=gamecode)
    emit("start_turn", emitPackage)


def emitHands(gamecode):
    hands = Hand.retrieveHand(gamecode)
    
    #TODO: Emit to single player; I think this should work
    # emit("pop_hand", hands, to=gamecode)
    print('Here are the hands: ')
    print(hands)
    emit("pop_hand", hands)


def emitState(gamecode: str):
    state = generateGameState(gamecode)
    print(state)
    # emit("pop_locations", state, to=gamecode)
    emit("pop_locations", state)


def generateGameState(gamecode):
    playerState = PlayerInfo.getGameState(gamecode)
    weaponState = WeaponLocation.getWeaponState(gamecode)
    
    return {"userState": playerState, "weaponState": weaponState}


