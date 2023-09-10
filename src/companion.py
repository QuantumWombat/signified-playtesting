from enum import Enum
import random
from src.entity import Entity


class CompanionType(Enum):
    """Static enumeration of all the companion types in Signified."""

    ARCHITECT = (
        "Architect",
        "This companion starts with an orb. For each companion on your team, if they have at least "
        + "one orb, they get a shiv at the start of each turn.",
    )
    CLOWN = (
        "Clown",
        "Upon being attacked, exhaust the top card of this companion's deck and gain more"
        + "block if it's a status card and less block otherwise",
    )
    ENTROPY = (
        "Entropy",
        "End of combat, remove one card PERMANENTLY",
    )
    PYTHIA = (
        "Pythia",
        "At the start of each turn, draw an extra card from this companion.",
    )
    ABORAH = (
        "Aborah",
        "At the end of combat, permanently gain base strength. Starts with X base strength.",
    )

    def __new__(cls, value, passive_desc):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.passive_desc = passive_desc
        return obj

    def generate_name(self) -> str:
        prefix = random.choice(["A-", "B-", "C-", "D-", "E-"])
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
        starting_health: int = 10,
        starting_attack: int = 1,
    ):
        super().__init__(name, starting_health, starting_attack)
        self.companion_type = companion_type

    def __str__(self):
        return f"{self.name}: {self.attack}⚔️ {self.health}/{self.max_health}💖"
