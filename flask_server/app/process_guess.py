"""
Contains functions for processing guesses, disproving suggestions, and accusations.
"""
from app import db
from .models import (
    Game, PlayerOrder, WeaponLocation, Path, Hand, PlayerInfo, Solution, Weapon, Character, Location, Guess, Solution,
    Card
)
import random
import json
from .utility import commit_changes
from .extensions import socketio


def disprove_suggestion(gamecode: str):
    """
    Automated disprove function. Iterates over each player in game, checks hand contents to find a match with some
    element in the player's suggestion. If found, the disproving card is shown to that user. If not found, play
    returns to the user, allowing them to end their turn or make an accusation.
    """

    #  Get game, player list, guessing player, and guess
    game = Game.query.filter_by(gameCode=gamecode).first()
    player_list = PlayerOrder.query.filter_by(gameId=game.id).all()
    active_player = PlayerOrder.query.filter_by(gameId=game.id, activeTurn=True).first()

    # TODO: Guesses has no most recent guess option, so for now we have to grab the guess with the highest int ID
    player_guesses = Guess.query.filter_by(playerId=active_player.id).all()

    # Naive solution to get most recent guess for the player
    active_guess = None
    highest_id = -1
    for guess in player_guesses:
        if guess.id > highest_id:
            highest_id = guess.id
            active_guess = guess

    # Check solution first to speed things up a bit if they guessed correctly
    game_solution = Solution.query.filter_by(gameId=game.id).first()
    if active_guess.characterId == game_solution.characterCard \
            and active_guess.locationId == game_solution.locationCard \
            and active_guess.weaponId == game_solution.weaponCard:

        message = f"{active_player.username}'s suggestion could not be disproven."
        socketio.emit("suggestion_result", message, to=gamecode)
        return

    # TODO: Possible last resort disprove where we just find the card that disproves from collection of all cards
    # # Get collection of cards from player hands
    # active_cards = []
    # for player in player_list:
    #     hand_cards = Hand.query.filter_by(playerInfo=player.id).all()
    #     for card in hand_cards:
    #         active_cards.append(card.id)


    # Get current turn number
    current_turn = active_player.turn

    # Create list with guess details
    guess_details = [active_guess.weaponId, active_guess.locationId, active_guess.characterId]

    # Just a variable to prevent an infinite loop
    loop_count = 0

    # Naive loop to disprove player suggestion
    while True:
        # Stop infinite loops
        loop_count += 1
        if loop_count >= len(player_list):
            print("There was an error during the disprove suggestion loop.")
            break

        # Attempt to disprove with next player
        current_turn += 1
        if current_turn > len(player_list):
            current_turn = 0

        # Slow but probably faster than another database query
        disprove_player = None
        for player in player_list:
            if player.turn == current_turn:
                disprove_player = player

        # Get disproving player hand
        hand_cards = Hand.query.filter_by(playerInfo=disprove_player.id).all()
        for hand in hand_cards:
            if hand.cardId in guess_details:
                # Get username and card name for message
                disprove_username = PlayerInfo.query.filter_by(id=disprove_player.playerId).first()
                disprove_card = Card.query.filter_by(id=hand.cardId).first()

                # TODO: I think I'm using this right
                disprove_card_name = disprove_card.getItem()

                # Emit disproving details
                message = f"{disprove_username} has disproven your suggestion with their {disprove_card_name} card."
                socketio.emit("suggestion_result", message, to=active_player.username)
                return




