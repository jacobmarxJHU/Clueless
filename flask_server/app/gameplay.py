"""
This file contains functions that are called during gameplay.
"""

import models
from .utility import commit_changes


def next_turn():
    """
    Creates next game turn. Pulls the current turn number from PlayerOrder by querying by activeTurn boolean,
    increments that turn number, gets the next player from that incremented value, and then sets the activeTurn bool
    to true for that record.

    :params: None
    :return: None
    """

    pass



