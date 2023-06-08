"""Module with entity information."""

from typing import List

from src.card import Card, Rarity

class Entity:
    def __init__(self, name: str, starting_health: int = 20, starting_attack: int = 1):
        self.name = name
        self.max_health = starting_health
        self.health = starting_health
        self.attack = starting_attack

    def damage(self, amount: int):
        self.health -= amount
        if self.health <= 0:
            print(f"Entity {self.name} died")


class Enemy(Entity):
    """Enemy represents a single enemy in Signified."""

    def __init__(self, name: str, starting_health: int = 20, starting_attack: int = 1):
        super().__init__(name, starting_health, starting_attack)

    def __str__(self):
        return f"😈 {self.name}: {self.health}/{self.max_health}💖"


# The following enumerate the list of companions in Signified.
ARCHITECT_COMPANION = "Architect"
ENTROPY_COMPANION = "Entropy"

# Each card in the game is associated with a single companion.
# Strikes and defends are the only cards shared across, but they
# do not appear here since they should not show up in shops.
COMPANION_TO_CARDS = {
    ARCHITECT_COMPANION: [
        Card("Summon Rat", Rarity.COMMON)
    ],
    ENTROPY_COMPANION: [
        Card("Bellows", Rarity.COMMON)
    ],
}
    

class Companion(Entity):
    """Companion represents members of your team in Signified.
    
    Companions have a deck of cards associated with them.
    For the paper prototype, we can use physical cards.
    """

    def __init__(
        self, 
        name: str, 
        starting_health: int = 20, 
        starting_attack: int = 1,
        starting_cards: List[str] = [],
    ):
        super().__init__(name, starting_health, starting_attack)
        self.starting_cards = starting_cards

    def __str__(self):
        return f"{self.name}: {self.attack}⚔️ {self.health}/{self.max_health}💖"
