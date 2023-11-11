from app import db
from .models import (
    Users, GameStatus, ActivePlayers, Games, PlayerOrder, Characters, Locations, PlayerLocations,
    Weapons, Paths, Solutions, Guesses, PlayerStatus, Card, Hand, WeaponLocations
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
def initialize_board(game_code: str):
    # Get active game
    active_game = Games.query.filter_by(game_code=game_code).first()

    if not active_game:
        raise ValueError("Active game not found.")

    # TODO: Add all necessary functions to initialize board.
    character_assignments = assign_characters(active_game)
    starting_locations = get_starting_locations(active_game)
    weapons_locations = get_weapon_locations(active_game)

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
def assign_characters(active_game: Games):
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

    # TODO: Is it more efficient to commit all changes back in the calling function or to commit incrementally for
    #   better error handling?
    # Commit assignments
    commit_changes()

    # Return dict for character assignment
    return {"Characters": char_assignment}


# Gets and returns starting locations for each player in the game
def get_starting_locations(active_game: Games):
    pass


# Generates weapon starting locations
def get_weapon_locations(active_game: Games):
    # Get all rooms
    rooms = Locations.query.filter_by(isRoom=True).all()

    # Get all weapons
    weapons = Weapons.query.all()
    random.shuffle(weapons)

    # Initialize weapon: room dictionary
    weapon_assignment = {}

    # Assign each weapon to a room
    for weapon, room in zip(weapons, rooms):
        # Create entry in WeaponLocations table
        new_weapon_location = WeaponLocations(weaponId=weapon.id, roomId=room.id, gameId=active_game.id)
        db.session.add(new_weapon_location)

        # Assign pair to dictionary
        weapon_assignment[weapon.name] = room.name

    commit_changes()

    return {"Weapons": weapon_assignment}

