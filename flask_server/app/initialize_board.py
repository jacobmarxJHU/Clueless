from app import db
from .models import (
    Game, User, Character, Location, Weapon, WeaponLocation, StartLocation, Card, Hand, PlayerInfo, Solution
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
    active_game = Game.query.filter_by(game_code=game_code).first()

    if not active_game:
        raise ValueError("Active game not found.")

    # Generate game solution and player hands
    generate_solution(active_game)
    generate_hands(active_game)

    # Generate states for board initialization
    character_assignments = assign_characters(active_game)
    starting_locations = get_starting_locations()
    weapons_locations = get_weapon_locations(active_game)
    player_hands = retrieve_hands(active_game)

    board_setup = {
        "board_setup": {
            "CharacterAssignments": character_assignments,
            "StartingLocations": starting_locations,
            "WeaponsLocations": weapons_locations,
            "StartingHands": player_hands,
        }
    }

    # Crete json object from nested dict to return to front end
    board_setup_json = json.dumps(board_setup)

    return board_setup_json


# Performs initial character assignment
def assign_characters(active_game: Game):
    # Get all active players and characters
    active_players = PlayerInfo.query.filter_by(gameId=active_game.id).all()
    available_characters = Character.query.all()

    # Random character assignment
    random.shuffle(available_characters)

    # Initialize user: character dictionary
    char_assignment = {}

    # Assign each player a character
    for player, character in zip(active_players, available_characters):
        player.characterId = character.id  # Set the characterId in the PlayerInfo table
        db.session.add(player)  # Stage the changes for commit
        char_assignment[player.playerId] = character.name  # Build the response

    # TODO: Is it more efficient to commit all changes back in the calling function or to commit incrementally for
    #   better error handling?
    # Commit assignments
    commit_changes()

    # Return dict for character assignment
    # TODO: This dictionary has a structure of playerID: character name. If different key needed, change for loop
    #   key assignment
    return {"Characters": char_assignment}


# Gets and returns starting locations for each player in the game
def get_starting_locations():
    # Get all starting locations from database and return character-location pairs
    # Join character and location names from respective tables
    starting_locations = StartLocation.query.join(
        Character, StartLocation.characterId == Character.id
    ).join(
        Location, StartLocation.locationId == Location.id
    ).add_columns(
        Character.name, Location.name
    ).all()

    # Create character-location dictionary
    start_locations = {}
    for start_location in starting_locations:
        character_name = start_location.Character.character
        location_name = start_location.Location.locationName
        start_locations[character_name] = location_name

    return {"start_locations": start_locations}


# Generates weapon starting locations
def get_weapon_locations(active_game: Game):
    # Get all rooms
    rooms = Location.query.filter_by(isRoom=True).all()

    # Get all weapons
    weapons = Weapon.query.all()
    random.shuffle(weapons)

    # Initialize weapon: room dictionary
    weapon_assignment = {}

    # Assign each weapon to a room
    for weapon, room in zip(weapons, rooms):
        # Create entry in WeaponLocations table
        new_weapon_location = WeaponLocation(weaponId=weapon.id, roomId=room.id, gameId=active_game.id)
        db.session.add(new_weapon_location)

        # Assign pair to dictionary
        weapon_assignment[weapon.name] = room.name

    commit_changes()

    return {"Weapons": weapon_assignment}


# Generates game solution
def generate_solution(active_game: Game):
    # Fetch each type of card separately
    location_cards = Card.query.filter(Card.locationId.isnot(None)).all()
    character_cards = Card.query.filter(Card.characterId.isnot(None)).all()
    weapon_cards = Card.query.filter(Card.weaponId.isnot(None)).all()

    # Randomly select one card from each type for the solution
    solution = {
        "location": random.choice(location_cards),
        "character": random.choice(character_cards),
        "weapon": random.choice(weapon_cards),
    }

    # Create record for game solution
    new_solution = Solution(
        location_id=solution["location"].id,
        character_id=solution["character"].id,
        weapon_id=solution["weapon"].id,
        game_id=solution["game"].id
    )

    # Add the new object to the session and commit
    db.session.add(new_solution)
    commit_changes()


# Generate player hands
def generate_hands(active_game: Game):
    # Get players in the current game
    players_in_game = PlayerInfo.query.filter_by(gameId=active_game.id).all()

    # Get current game solution
    game_solution = Solution.query.filter_by(gameId=active_game.id).first()

    # Fetch all cards excluding the solution
    solution_card_ids = [game_solution.locationId, game_solution.characterId, game_solution.weaponId]
    all_cards = Card.query.filter(Card.id.not_in(solution_card_ids)).all()

    # Shuffle the cards
    random.shuffle(all_cards)

    # Deal cards to players in a round-robin fashion and add hand record to database
    for i, card in enumerate(all_cards):
        player = players_in_game[i % len(players_in_game)]
        new_hand_entry = Hand(gameId=active_game.id, playerId=player.id, cardId=card.id)
        db.session.add(new_hand_entry)

    # Commit the session to save all new Hand records
    commit_changes()


# Retrieves and returns player hands as dictionary for board initialization
def retrieve_hands(active_game):
    # Initialize player hands dictionary
    players_hands = {}

    # Get all players in the game
    players = PlayerInfo.query.filter_by(gameId=active_game.id).all()

    for player in players:
        # Get the hand for each player
        player_hand_records = Hand.query.filter_by(gameId=active_game.id, playerId=player.id).all()

        # Fetch card details for each card in the hand
        player_hand = []
        for hand_record in player_hand_records:
            card = Card.query.get(hand_record.cardId)
            card_detail = {
                "cardId": card.id,
                "cardType": "location" if card.locationId else "character" if card.characterId else "weapon",
                "cardName": get_card_name(card)
            }

            player_hand.append(card_detail)

        # TODO: Assumes we want to return the player ID as the key. Can change this if needed.
        # Add the player's hand to the dictionary
        players_hands[player.id] = player_hand

    # Return dictionary of player hands
    return {"Hands": players_hands}


# Utility function to return the name of a card given a Card record
def get_card_name(card):
    if card.locationId:
        location = Location.query.get(card.locationId)
        return location.name if location else None

    elif card.characterId:
        character = Character.query.get(card.characterId)
        return character.name if character else None

    elif card.weaponId:
        weapon = Weapon.query.get(card.weaponId)
        return weapon.name if weapon else None

    return None  # Return None if no card type matches
