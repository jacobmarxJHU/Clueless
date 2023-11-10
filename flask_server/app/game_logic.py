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
    # TODO: Add all necessary functions to initialize board.
    character_assignments = assign_characters(game_id)
    starting_locations = get_starting_locations(game_id)
    weapons_locations = get_weapon_locations(game_id)

    board_setup = {
        "board_setup": {
            "CharacterAssignments": character_assignments,
            "StartingLocations": starting_locations,
            "WeaponsLocations": weapons_locations,

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

    # Return dict for character assignment
    return {"Characters": char_assignment}


# Gets and returns starting locations for each player in the game
def get_starting_locations(game_id):
    pass


# Generates weapon starting locations
def get_weapon_locations(game_id):
    # Get active game
    active_game = ActiveGames.query.filter_by(id=game_id).first()

    if not active_game:
        raise ValueError("Active game not found.")

    # Get all rooms. Assumes that rooms are being pulled from locations table.
    rooms = Locations.query.filter_by(isRoom=True).all()

    # Get all weapons
    weapons = Weapons.query.all()

    # Initialize weapon: room dictionary
    weapon_assignment = {}

    # TODO: Randomize assignment?
    # Assign each weapon to a room
    for weapon, room in zip(weapons, rooms):

        # TODO: How are we actually storing weapon location relationships in the database? A GameWeaponsLocations table?
        weapon.roomID = room.id
        db.session.add(weapon)
        weapon_assignment[weapon.name] = room.name

    commit_changes()

    return {"Weapons": weapon_assignment}

