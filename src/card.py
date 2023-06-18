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
    STRIKE = ("Strike", Rarity.COMMON)
    DEFEND = ("Defend", Rarity.COMMON)

    # ARCHITECT cards
    SUMMON_RAT = ("Summon Rat", Rarity.COMMON)

    # ENTROPY cards
    BELLOWS = ("Bellows", Rarity.COMMON)

    def __new__(cls, value, rarity):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.rarity = rarity
        return obj
