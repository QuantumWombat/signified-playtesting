from enum import Enum
import random
from src.card import Card
from src.entity import Entity


class CompanionType(Enum):
    """Static enumeration of all the companion types in Signified."""

    ARCHITECT = (
        "Architect",
        "Start combat with 1 construct (deck full of shivs)",
        [Card.SUMMON_ARTIFACT, Card.IDEATE, Card.FINISHING_TOUCH, Card.MITOSIS],
        [Card.STRIKE] * 2 + [Card.DEFEND] * 2 + [Card.SUMMON_ARTIFACT],
    )
    CLOWN = (
        "Clown",
        "End of combat, gain 5 max HP",
        [],
        [],
    )
    ENTROPY = (
        "Entropy",
        "End of combat, remove one card PERMANENTLY",
        [
            Card.BELLOWS,
            Card.SELF_SHARPENING_BLADE,
            Card.SOOTY_ARMOR,
            Card.FIERY_ENCOURAGEMENT,
        ],
        [Card.STRIKE] * 2 + [Card.DEFEND] * 2 + [Card.BELLOWS],
    )
    PYTHIA = (
        "Pythia",
        "Retain 1 card",
        [Card.MENTAL_PRISM, Card.ADRENALINE, Card.FORCE_FIELD, Card.DISCHARGE],
        [Card.STRIKE] * 2 + [Card.DEFEND] * 2 + [Card.MENTAL_PRISM],
    )
    WARRIOR = (
        "Warrior",
        "When this companion dies, gain 1 strength PERMANENTLY",
        [
            Card.DOUBLE_STRIKE,
            Card.BLOOD_SACRIFICE,
            Card.VENGEFUL_SWEEP,
            Card.TAKE_MY_ENERGY,
            Card.FINAL_FORM,
        ],
        [Card.STRIKE] * 2 + [Card.DEFEND] * 2 + [Card.DOUBLE_STRIKE],
    )

    def __new__(cls, value, passive_desc, cards, starting_deck):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.passive_desc = passive_desc
        obj.cards = cards
        obj.starting_deck = starting_deck
        return obj

    def generate_name(self) -> str:
        prefix = random.choice(["Alpha", "Beta", "Gamma", "Delta", "Omega"])
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
