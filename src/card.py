from dataclasses import dataclass
from enum import Enum


class Rarity(Enum):
    COMMON = 1
    UNCOMMON = 2
    RARE = 3


class Card(Enum):
    """Card is an enum representing all the static card types in Signified.

    The mapping from companion to card is represented on the companion level.
    """

    STRIKE = ("Strike", "deal damage", Rarity.COMMON)
    DEFEND = ("Defend", "block", Rarity.COMMON)

    # ARCHITECT cards
    SUMMON_RAT = (
        "Summon Rat",
        "summon a token that draws you a shiv each turn",
        Rarity.COMMON,
    )

    # CLOWN cards

    # ENTROPY cards
    BELLOWS = ("Bellows", "draw 3 and exhaust one of the cards", Rarity.COMMON)
    SELF_SHARPENING_BLADE = (
        "Self Sharpening Blade",
        "deal 5 damage. deal 5 more damage next time",
        Rarity.UNCOMMON,
    )

    # PYTHIA cards

    # WARRIOR cards
    BLOOD_SACRIFICE = (
        "Blood Sacrifice",
        "lose 3 HP, give a companion 2 strength",
        Rarity.COMMON,
    )
    DOUBLE_STRIKE = ("Double Strike", "deal 5 damage twice", Rarity.COMMON)
    VENGEFUL_SWEEP = ("Vengeful Sweep", "deal 8 damage to all enemies", Rarity.COMMON)
    TAKE_MY_ENERGY = ("Take my Energy", "lose 3 HP, gain 2 mana", Rarity.UNCOMMON)
    FINAL_FORM = (
        "Final Form",
        "go to 1 health. deal double dmg for rest of combat",
        Rarity.RARE,
    )

    def __new__(cls, value, description, rarity):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        obj.rarity = rarity
        return obj
