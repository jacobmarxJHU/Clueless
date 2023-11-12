from flask import request
from flask_socketio import emit, join_room
from .models import User, Game, db, PlayerInfo
from .initialize_board import initialize_board
import json

from .extensions import socketio

@socketio.on("connect")
def handle_connect():
    print("Client Connected")


@socketio.on("user_join")
def handle_user_join(data):

    data = json.loads(data)
    name = data['username']
    gameIn = data['gameCode']

    print("User joined")
    print(f"attempted join with username: {name}, gameCode: {gameIn}")

    try:
        print('attempt now')
        user = User.query.filter_by(username=name).first()
        user.sessionInfo = request.sid
        user.playerStatus = 1
        db.session.commit()
        print(user)
    except:
        raise("Error locating the user")


    if gameIn:
        # game code provided, check if new game or existing
        game = Game.query.filter_by(gameCode=gameIn).first()

        if game:
            print(" exists")
            # exists check if in lobby or inactive
            if game.playerCount >= 6:
                print("trying to join a full lobby")
                return
            elif game.status == 2:
                # 2 -> inactive
                print("inactive")
                game.status = 1
                user.isLeader = True
                user.activeGame = game.id
                db.session.commit()
                print(game)

            elif game.status == 1:
                # 1 -> lobby
                print("lobby")
                db.session.commit()
                print(game)

            else:
                # how to raise error?
                print("trying to join in progress game")
        else:
            # create a new game with that code
            game = Game(gameCode=gameIn, gameStatus=1)
            db.session.add(Game)
            db.session.commit()
            user.isLeader = True
            db.session.commit()

    else:
        print("no game code provided: create a new one")
        try:
            game = Game(gameStatus=1)
            db.session.add(game)
            db.session.commit()
            user.isLeader = True
            db.session.commit()
            print(game)
            print(user)
        except:
            print("error creating a new game from scratch")

    user.activeGame = game.id
    game.playerCount = game.playerCount + 1
    db.session.commit()
    print('before join game')

    print(game)
    print(user)

    join_room(gameIn)

    emit("pass_game", {"gameCode": gameIn})
    emit("join_room", {"username": name}, to=gameIn)


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")
    print(request.sid)
    user = User.query.filter_by(sessionInfo=request.sid).first()
    game = Game.query.filter_by(id=user.activeGame).first()

    print(user)
    print(game)

    user.sessionInfo = None
    user.activeGame = None
    game.decrementCount()
    db.session.commit()

    print(user)
    print(game)

    emit("leave_room", {"username": user.username}, to=game.gameCode)


# This will control the socket io end of game start
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

