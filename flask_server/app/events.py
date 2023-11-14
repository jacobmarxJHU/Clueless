from flask import request
from flask_socketio import emit, join_room
from .models import User, Game, db, PlayerInfo, WeaponLocation, Location, Weapon, Guess, Solution, Hand
from .board_manipulation import initialize_board, emitTurnInfo
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
            print(game)
            print(user)
        except:
            print("error creating a new game from scratch")

    user.activeGame = game.id
    game.playerCount = game.playerCount + 1
    commit_changes()
    print('before join game')

    print(game)
    print(user)

    join_room(game.gameCode)

    emit("pass_game", {"gameCode": game.gameCode, "username": name, "isLeader": user.isLeader})

    message = f"User {name} has joined the game"

    emit("message_chat", {"message": message}, to=game.gameCode)


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")
    print(request.sid)

    user = User.query.filter_by(sessionInfo=request.sid).first()

    if user and user.activeGame:

        game = Game.query.filter_by(id=user.activeGame).first()
        print(user)
        print(game)

        user.sessionInfo = None
        user.activeGame = None
        user.isLeader = False

        if game.playerCount == 1:
            game.playerCount = game.playerCount - 1
            game.gameStatus = 2

        db.session.commit()

        print(user)
        print(game)

        message = f"User {user.username} has joined the game"

        emit("message_chat", {"message": message}, to=game.gameCode)
    else:
        print("Trying to disconnect from no game")


# This will control the socket io end of game start
# sends hand
# sends locations (generates playerInfo records, generates weapon locations)
@socketio.on('start_game')
def start_game(data):
    game_id = data['gameCode']
    try:
        # Perform game start functions.
        # TODO: Add all necessary functions
        initialized_board = initialize_board(game_id)
        print('emit!')
        emit('game_started', initialized_board)
        
        # Acknowledge the client that the event was received and handled
        return {'status': 'Game started', 'board': initialized_board}
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
    game_id = User.query.filter_by(username=data["username"]).first().activeGame
    game = Game.query.filter_by(id=game_id).first()

    # Get location ID to add to PlayerInfo
    location_id = Location.query.filter_by(locationName=data["location"]).first().id

    # Get player info record
    player_info = PlayerInfo.query.filter_by(username=data["username"]).first()

    # Update and commit player info with new location
    player_info.locationId = location_id
    commit_changes()

    # Create message and emit message to summarize action
    message = f"{data['username']} moved to {data['location']}"
    emit("message_chat", {"message": message}, to=game.gameCode)


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

        if dis is None:
            message = f"{username} was disproven by {dis}"
        else:
            message = f"{username} was not disproven"

        emit("message_chat", {"message": message}, to=gamecode)

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
    try:
        # Get player and game IDs
        user = User.query.filter_by(username=data["username"]).first()
        if not user:
            raise ValueError("User not found")

        player_id = user.id
        game_id = user.activeGame

        # Get game info for message
        game = Game.query.filter_by(id=game_id).first()

        Guess.addGuess(game.gameCode, data["username"], data['room'], data['character'], data['weapon'])

        # Create message and emit message to summarize action
        message = f"{data['username']} has accused: {data['character']}, {data['room']}, {data['weapon']}"
        emit("message_chat", {"message": message}, to=game.gameCode)



    except Exception as e:
        # Log and emit the error
        db.session.rollback()
        emit("error_message", {"error": str(e)})

        # Print the error
        print(f"Error in action_suggestion: {e}")


@socketio.on('action_turnEnd')
def action_turnEnd(data):
    """
    Invokes next turn function.

    :param data: json object with structure {gamecode: gamecode}
    :return: None
    """

    # Get game code and invoke next turn
    game_code = data["gamecode"]
    emitTurnInfo(game_code)
    

