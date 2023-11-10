from flask import request
from flask_socketio import emit, join_room
from .utility import generate_room_code
from .models import Users, ActiveGames, db
from .game_logic import initialize_board
import json

from .extensions import socketio

@socketio.on("connect")
def handle_connect():
    print("Client Connected")


@socketio.on("user_join")
def handle_user_join(data):
    # Prints information about user join event
    print("User Join")
    data = json.loads(data)
    name = data['username']
    game = data['gameCode']


    print(f"Username: {name}")
    print(f"User-Specified Game ID: {game}")

    activeGames = ActiveGames.query.all()
    activeGameCodes = []
    for ag in activeGames:
        activeGameCodes.append(ag.gameCode)
    
    print("Active Game IDs: " + ', '.join(activeGameCodes))

    if not game:
        game = generate_room_code(4, activeGameCodes)
    
    print("Current Game ID: " + game)

    if game not in activeGameCodes:
        # game does not exist so create it, set status equal to lobby
        new_game = ActiveGames(gameCode=game, gameStatus=1, playerCount=1)
        db.session.add(new_game)
        db.session.commit()

    else:
        # set game status to active
        curr_game = ActiveGames.query.filter_by(gameCode=game).first()
        playerCount = curr_game.playerCount
        curr_game.playerCount = playerCount + 1
        if curr_game.gameStatus == 2 or curr_game.gameStatus is None:
            curr_game.gameStatus = 1
        
        db.session.commit()
    
    join_room(game)

    print(f"Session ID: {request.sid}")
    print()
    # update user information
    user = Users.query.filter_by(username=data['username']).first()
    user.sessionInfo = request.sid
    user.gameCode = game
    username = user.username
    db.session.commit()

    emit("pass_game", {"gameCode": game})
    emit("join_room", {"username": username}, to=game)


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")
    user = Users.query.filter_by(sessionInfo=request.sid).first()
    username = user.username
    gameCode = user.gameCode
    curr_game = ActiveGames.query.filter_by(gameCode=gameCode).first()

    if curr_game.playerCount <= 1:
        curr_game.playerCount = 0
        curr_game.gameStatus = 2
    else:
        curr_game.playerCount = curr_game.playerCount - 1

    user.sessionInfo = None
    user.gameCode = None
    db.session.commit()
    emit("leave_room", {"username": username}, to=gameCode)

# This will control the socket io end of game start
@socketio.on('start_game')
def start_game(data):
    game_id = data['game_id']
    try:
        # Perform game start functions.
        # TODO: Add all necessary functions
        initialized_board = initialize_board(game_id)
        emit('game_started', initialized_board)

    except ValueError as e:
        emit('error', {'message': str(e)})
