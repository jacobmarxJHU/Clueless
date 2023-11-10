from app import db
from .models import (
    Users, GameStatus, ActivePlayers, ActiveGames, PlayerOrder, Characters, Locations, PlayerLocations, Rooms,
    Weapons, Paths, Solutions, Guesses, PlayerStatus, Card, Hand
)
import random
import json


# Utility function to commit changes to database as they're made
def commit_changes():
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


# Master initialize board function to pass initialized game state to front end
def initialize_board(game_id: int):
    character_assignments = assign_characters(game_id)
    starting_locations = get_starting_locations(game_id)

    board_setup = {
        "board_setup": {
            "CharacterAssignments": character_assignments,
            "StartingLocations": starting_locations,
        }
    }

    # Crete json object from nested dict to return to front end
    board_setup_json = json.dumps(board_setup)

    return board_setup_json


# Performs initial character assignment
def assign_characters(game_id: int):
    # Get active game
    active_game = ActiveGames.query.filter_by(id=game_id).first()

    if not active_game:
        raise ValueError("Active game not found.")

    # Get all active players and characters
    active_users = Users.query.filter_by(gameCode=active_game.gameCode).all()
    available_characters = Characters.query.all()

    # Random character assignment
    random.shuffle(available_characters)

    # Initialize user: character dictionary
    char_assignment = {}

    # Assign each user a character
    for user, character in zip(active_users, available_characters):
        user.characterId = character.id  # Set the characterId in the Users table
        db.session.add(user)  # Stage the changes for commit
        char_assignment[user.username] = character.character  # Build the response

    # Commit assignments
    commit_changes()

    # Return json for character assignment
    return {"Characters": char_assignment}


def get_starting_locations(game_id):
    pass
