"""
This file contains functions that are called during gameplay.
"""

from .models import db, Game, User, PlayerInfo, PlayerOrder
from .utility import commit_changes


def next_turn(game_code: str):
    """
    Creates next game turn. Pulls the current turn number from PlayerOrder by querying by activeTurn boolean,
    increments that turn number, gets the next player from that incremented value, and then sets the activeTurn bool
    to true for that record.

    :params: None
    :return: None
    """

    try:
        # Get game ID and player count
        game = Game.query.filter_by(gameCode=game_code).first()
        game_id = game.id
        player_count = game.playerCount

        # Get current turn
        current_turn = PlayerOrder.query.filter_by(
            gameId=game_id,
            activeTurn=True
        ).first()

        # Set current turn value to false
        current_turn.activeTurn = False

        # Increment turn and reset if needed
        next_turn_value = 1 if current_turn.turn >= player_count else current_turn.turn + 1

        # Get record for next active turn
        next_active_turn = PlayerOrder.query.filter_by(
            gameId=game_id,
            turn=next_turn_value
        ).first()

        # Set next turn's active turn value to true
        next_active_turn.activeTurn = True

        commit_changes()

    except Exception as e:
        # Handle errors and rollback if necessary
        db.session.rollback()

        # Log error
        print("Error in next_turn function:", e)
        raise e


