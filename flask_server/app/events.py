from flask import request
from flask_socketio import emit, join_room
from .models import User, Game, db, PlayerInfo
from .initialize_board import initialize_board
import json
from .utility import commit_changes

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

    join_room(gameIn)

    emit("pass_game", {"gameCode": gameIn})

    message = f"User {name} has joined the game"

    emit("message_chat", {"message": message}, to=gameIn)


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

        if game.playerCount == 1:
            game.playerCount = game.playerCount - 1
            game.gameStatus = 2

        db.session.commit()

        print(user)
        print(game)

        message = f"User {user.username} has joined the game"

        emit("message_chat", {"message": message}, to=game.gameCode)
    else:
        print("Trying to diconnect from no game")


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
        emit('game_started', initialized_board)

    except ValueError as e:
        emit('error', {'message': str(e)})


# 
@socketio.on('action_move')
def action_move(data):
    # emits pop locations

    pass


@socketio.on('action_suggestion')
def action_suggestion(data):

    pass


@socketio.on('action_turnEnd')
def action_turnEnd(data):

    pass


@socketio.on('action_accuse')
def action_accuse(data):

    pass