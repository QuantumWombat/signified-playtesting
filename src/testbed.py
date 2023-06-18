"""Testbed is the main testbed for dogfooding GoFaceGames"""

from dataclasses import dataclass
import random
from typing import Dict, List
from src.card import Card

from src.entity import Companion, CompanionType, Enemy
from src.constants import NUM_CARDS_TO_SHOW

class Testbed():
    """Testbed is the root data structure for a prototyping session.

    It holds state about the player's current roster, their economy, and
    the enemies to follow.
    """
    def __init__(self):
        # Generate a list of starter companions.
        starting_companions = [Companion(c) for c in random.choices(list(CompanionType), k=3)]
        self.companions: List[Companion] = starting_companions
        self.shop = Shop()
        self.gold = 0

    def __str__(self):
        """Pretty print global information about the state of the game."""
        return ""

class Encounter():

    def __init__(self):
        self.enemies: Dict[str, Enemy] = {}

    def add_enemy(self, enemy: Enemy):
        self.enemies[enemy.name] = enemy

    def __str__(self):
        return "\n".join([str(e) for _, e in self.enemies.items()])

@dataclass
class Shop():
    """Shop holds state about the current state of the economy.

    It holds the current level of the shop.
    Level up the shop to see better companions and better cards.
    """
    level: int = 1

    def generate_card_options(self, current_companions: List[CompanionType]) -> List[Card]:
        unique_companions = set(current_companions)
        card_opts = [card for companion in unique_companions for card in companion.cards]
        # TODO: implement sampling without replacement
        # TODO: weight the cards with respect to their rarity.
        return random.choices(card_opts, k=min(len(card_opts), NUM_CARDS_TO_SHOW))
