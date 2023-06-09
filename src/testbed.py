"""Testbed is the main testbed for dogfooding GoFaceGames"""

from dataclasses import dataclass
from typing import Dict, List

from src.entity import COMPANION_TO_CARDS, Companion, CompanionType, Enemy

class Testbed():
    """Testbed is the root data structure for a prototyping session.
    
    It holds state about the player's current roster, their economy, and
    the enemies to follow.
    """
    def __init__(self):
        self.companions: List[Companion] = []
        self.shop = Shop()

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

    def generate_card_options(current_companions: List[CompanionType]) -> List[str]:
        card_mapping = COMPANION_TO_CARDS
        all_cards = []
