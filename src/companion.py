from enum import Enum
import random
from src.card import Card
from src.entity import Entity

class CompanionType(Enum):
    """Static enumeration of all the companion types in Signified."""
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

    def generate_name(self) -> str:
        prefix = random.choice(["WideLloyd", "Jimothy", "Foo", "Wizard", "Marmot"])
        return prefix + self.value


class Companion(Entity):
    """Companion represents members of your team in Signified.

    Companions have a deck of cards associated with them.
    For the paper prototype, we can use physical cards.
    """

    def __init__(
        self,
        name: str,
        companion_type: CompanionType,
        starting_health: int = 20,
        starting_attack: int = 1,
    ):
        super().__init__(name, starting_health, starting_attack)
        self.companion_type = companion_type

    def __str__(self):
        return f"{self.name}: {self.attack}⚔️ {self.health}/{self.max_health}💖"
