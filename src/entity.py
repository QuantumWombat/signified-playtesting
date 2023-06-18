"""Module with entity information."""

from enum import Enum
from typing import List

from src.card import Card

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
class CompanionType(Enum):
    ARCHITECT = (
        "Architect",
        [Card.SUMMON_RAT],
        [Card.STRIKE] * 2 + [Card.DEFEND] * 2 + [Card.SUMMON_RAT],
    )
    ENTROPY = (
        "Entropy",
        [Card.BELLOWS],
        [Card.STRIKE] * 2 + [Card.DEFEND] * 2 + [Card.BELLOWS],
    )

    def __new__(cls, value, cards, starting_deck):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.cards = cards
        obj.starting_deck = starting_deck
        return obj


class Companion(Entity):
    """Companion represents members of your team in Signified.

    Companions have a deck of cards associated with them.
    For the paper prototype, we can use physical cards.
    """

    def __init__(
        self,
        companion_type: CompanionType,
        starting_health: int = 20,
        starting_attack: int = 1,
    ):
        super().__init__(companion_type.value, starting_health, starting_attack)
        self.starting_cards = companion_type.starting_deck

    def __str__(self):
        return f"{self.name}: {self.attack}⚔️ {self.health}/{self.max_health}💖"
