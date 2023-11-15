from flask import request
from flask_socketio import emit, join_room
from .models import User, Game, db, Path, PlayerInfo, Character, Winner, WeaponLocation, Location, Weapon, Guess, Solution, Hand, PlayerOrder
from .board_manipulation import initialize_board, emitTurnInfo, emitState
import json
from .utility import commit_changes
from .gameplay import next_turn

from .extensions import socketio


@socketio.on("connect")
def handle_connect():
    print("Client Connected")


@socketio.on("user_join")
def handle_user_join(data):

    # data = json.loads(data)
    name = data['username']
    gameIn = data['gameCode']

    print("User joined")
    print(f"attempted join with username: {name}, gameCode: {gameIn}")

    try:
        print('attempt now')
        user = User.query.filter_by(username=name).first()
        user.sessionInfo = request.sid
        user.playerStatus = 1
        user.isLeader = False
        commit_changes()
        print(user)
    except:
        raise("Error locating the user")


    if gameIn:
        # game code provided, check if new game or existing
        game = Game.query.filter_by(gameCode=gameIn).first()
        print("game code provided")
        print(game)

        if game:
            print("game exists")
            # exists check if in lobby or inactive
            if game.playerCount >= 6:
                print("trying to join a full lobby")
                return
            elif game.gameStatus == 2:
                # 2 -> inactive
                print("inactive")
                game.gameStatus = 1
                user.isLeader = True
                user.activeGame = game.id
                commit_changes()
                print(game)

            elif game.gameStatus == 1:
                # 1 -> lobby
                print("lobby")
                commit_changes()
                print(game)

            else:
                print("trying to join in progress game")
                return
        else:
            # create a new game with that code
            print("Creating game from gamecode")
            game = Game(gameCode=gameIn, gameStatus=1)
            db.session.add(game)
            commit_changes()

            user.isLeader = True
            commit_changes()


    else:
        print("no game code provided: create a new one")
        try:
            game = Game(gameStatus=1)
            db.session.add(game)
            db.session.commit()
            user.isLeader = True
            commit_changes()
            # print(game)
            # print(user)
        except:
            print("error creating a new game from scratch")

    print(user)
    print(game)

    emit("pass_game", {"gameCode": game.gameCode, "username": name, "isLeader": user.isLeader})

    message = f"User {name} has joined the game"

    #emit("message_chat", {"message": message}, to=game.gameCode)

@socketio.on("game_join")
def game_join(data):

    username = data['username']
    gamecode = data['gameCode']

    user = User.query.filter_by(username=username).first()
    game = Game.query.filter_by(gameCode=gamecode).first()

    print(f"{username} has joined game {gamecode}")

    user.activeGame = game.id
    user.sessionInfo = request.sid
    game.playerCount = game.playerCount + 1

    commit_changes()

    print("before join")
    print(user.sessionInfo)
    print(user)
    print(game)
    join_room(gamecode)

    print("after join")
    print(user)
    print(game)

    message = f"{username} has joined the game!"
    emit("message_chat", {"message": message}, to=gamecode)


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")
    print(request.sid)

    # user = User.query.filter_by(sessionInfo=request.sid).first()
    #
    # # if user and user.activeGame:
    # #
    #     game = Game.query.filter_by(id=user.activeGame).first()
    #     print(user)
    #     print(game)
    #
    #     user.sessionInfo = None
    #     user.activeGame = None
    #     user.isLeader = False
    #
    #     if game.playerCount == 1:
    #         game.playerCount = game.playerCount - 1
    #         game.gameStatus = 2
    #
    #     db.session.commit()
    #
    #     print(user)
    #     print(game)
    #
    #     message = f"User {user.username} has joined the game"
    #
    #     emit("message_chat", {"message": message}, to=game.gameCode)
    # else:
    #     print("Trying to disconnect from no game")


# This will control the socket io end of game start
# sends hand
# sends locations (generates playerInfo records, generates weapon locations)
@socketio.on('start_game')
def start_game(data):
    game_id = data['gameCode']
    try:
        # Perform game start functions.
        # TODO: Add all necessary functions
        # emit('pop_locations', initialized_board)
        # print('emit initialized board!')
        # print(initialized_board)

        # initialize_board will perform game start functions
        initialize_board(game_id)
        
        # Acknowledge the client that the event was received and handled
        # return {'status': 'Game started', 'board': initialized_board} 
        return {'status': 'Game started'}
    except ValueError as e:
        emit('error', {'message': str(e)})
         # If there was an error, acknowledge that as well
        return {'status': 'error', 'message': str(e)}


@socketio.on('action_move')
def action_move(data):
    """
    Updates player location and emits that info to game status table.

    :param data: json with structure {username: username, location: location}
    :return none
    """
    # Get game information
    username = data["username"]
    location = data['new_loc']
    gid = User.getGid(username)
    gamecode = db.session.get(Game, gid).gameCode
    PlayerInfo.movePlayer(gamecode, location, username=username)
    emitState(gamecode)

    # Create message and emit message to summarize action
    message = f"{username} moved to {location}"
    emit("message_chat", {"message": message}, to=gamecode)
    #emit("message_chat", {"message": message}, to=gamecode)

@socketio.on('get_paths')
def get_paths(data):
    username = data['username']
    gamecode = Game.getGamecode_username(username)
    paths = Path.findConnected(gamecode, username)
    sid = request.sid

    emit("receive_paths", {"paths": paths}, to=sid)


@socketio.on('get_characters')
def get_characters(data):
    emit('receive_characters', {"characters": Character.getAllCharacters()}, to=request.sid)

@socketio.on('get_weapons')
def get_weapons(data):
    emit("receive_weapons", {"weapons": Weapon.getAllWeapons()}, to=request.sid)

@socketio.on('action_suggestion')
def action_suggestion(data):
    """
    Add user suggestion to guesses table and emit suggestion as message

    :param data: json with structure {username: username, character: character, weapon: weapon, room: room}
    :return none
    """

    try:
        # Get player and game IDs
        username = data['username']
        gamecode = Game.getGamecode_username(username)
        location = PlayerInfo.getPlayerLocation(gamecode, username)
        weapon = data['weapon']
        character = data['character']

        Guess.addGuess(gamecode, username, location, character, weapon)
        PlayerInfo.movePlayer(gamecode, location, character=character)
        WeaponLocation.moveWeapon(gamecode, weapon, location)
        dis = Hand.disprove(gamecode, character, weapon, location)
        message = f"{username} has suggested: {character}, {location}, {weapon}"
        emit("message_chat", {"message": message}, to=gamecode)
        #emit("message_chat", {"message": message})

        if dis:
            message = f"{username} was disproven by {dis}"
        else:
            message = f"{username} was not disproven"

        emit("message_chat", {"message": message}, to=gamecode)
        #emit("message_chat", {"message": message})

        emitState(gamecode)

    except Exception as e:
        # Log and emit the error
        db.session.rollback()
        emit("error_message", {"error": str(e)})

        # Print error
        print(f"Error in action_suggestion: {e}")


@socketio.on('action_accuse')
def action_accuse(data):
    """
    Add user accusation to guesses table and emit suggestion as message

    :param data: json with structure {username: username, character: character, weapon: weapon, room: room}
    :return none
    """

    # TODO: If we got suggestion/accusation specifier from the front-end in the json object we could consolidate this
    #   with the action_suggestion function
#    try:
    username = data['username']
    character = data['character']
    weapon = data['weapon']
    gamecode = Game.query.filter_by(id=User.getGid(username)).first().gameCode
    location = PlayerInfo.getPlayerLocation(gamecode, username)

    message = f"{username} has accused: {character}, {location}, {weapon}"
    emit("message_chat", {"message": message}, to=gamecode)
    #emit("message_chat", {"message": message})

    PlayerInfo.movePlayer(gamecode, location, character=character)
    WeaponLocation.moveWeapon(gamecode, weapon, location)
    Guess.addGuess(gamecode, username, location, character, weapon)
    correct = Solution.checkSol(gamecode, location, weapon, character)
    emitState(gamecode)

    if correct:
        message = f"{username} has guessed successfully!"
        emit("message_chat", {"message": message}, to=gamecode)
        #emit("message_chat", {"message": message})
        Winner.addWinner(username, gamecode)
        emit("game_over", {}, to=gamecode)
        #emit("game_over", {})
    else:
        PlayerOrder.setEliminated(gamecode, username)
        message = f"{username} has guessed incorrectly and has been eliminated!"
        emit("message_chat", {"message": message}, to=gamecode)
        emitTurnInfo(gamecode)

#    except Exception as e:
#        # Log and emit the error
#        db.session.rollback()
#        emit("error_message", {"error": str(e)}, to=gamecode)
#
#        # Print the error
#        print(f"Error in action_suggestion: {e}")


@socketio.on('action_turnEnd')
def action_turnEnd(data):
    """
    Invokes next turn function.

    :param data: json object with structure {gamecode: gamecode}
    :return: None 
    """
    print("hello")

    # Get game code and invoke next turn
    game_code = data["gamecode"]
    username = PlayerOrder.getCurrentUsername(game_code)

    message = f"{username}'s turn has started"
    emit("message_chat", {"message": message}, to=game_code)

    emitTurnInfo(game_code)
    

