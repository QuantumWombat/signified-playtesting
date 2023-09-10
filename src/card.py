from enum import Enum
from typing import List
from src.companion import CompanionType


class Rarity(Enum):
    COMMON = 1
    UNCOMMON = 2
    RARE = 3


class Card(Enum):
    """Card is an enum representing all the static card types in Signified.

    The mapping from companion to card is represented on the companion level.
    """

    # ARCHITECT cards
    PROTECT_FOR_EACH_ORB = (
        "Protect for each orb",
        CompanionType.ARCHITECT,
        "target companion gets X block for each orb they have",
        Rarity.COMMON,
    )
    STRENGTH_FOR_ALL_WITH_ORB = (
        "Strength for all with an orb",
        CompanionType.ARCHITECT,
        "each companion with at least one orb gets X strength",
        Rarity.COMMON,
    )
    SUMMON_ORB = (
        "Summon orb",
        CompanionType.ARCHITECT,
        "summon an orb on a companion",
        Rarity.COMMON,
    )

    # CLOWN cards
    FIRE_EATING = (
        "Fire eating",
        CompanionType.CLOWN,
        "Shuffle N status cards into this deck that say: "
        + "When exhausted, deal X damage to a random enemy",
        Rarity.COMMON,
    )
    POWER_THROUGH = (
        "Power through",
        CompanionType.CLOWN,
        "Give a companion X block and shuffle 2 wound status cards into their deck",
        Rarity.COMMON,
    )
    REPRIEVE = (
        "Reprieve",
        CompanionType.CLOWN,
        "Gain X block. When exhausted, this companion heals Y HP",
        Rarity.COMMON,
    )

    # ENTROPY cards
    BELLOWS = (
        "Bellows",
        CompanionType.ENTROPY,
        "draw X and exhaust Y of the cards",
        Rarity.COMMON,
    )
    SOOTY_ARMOR = (
        "Sooty Armor",
        CompanionType.ENTROPY,
        "give a companion X block and exhaust the top card of their deck",
        Rarity.COMMON,
    )
    SELF_SHARPENING_BLADE = (
        "Self Sharpening Blade",
        CompanionType.ENTROPY,
        "deal X damage. deal Y more damage next time",
        Rarity.COMMON,
    )

    # PYTHIA cards
    DISCHARGE = (
        "Discharge",
        CompanionType.PYTHIA,
        "for each X cards in your hand, deal Y damage",
        Rarity.COMMON,
    )
    BACKFLIP = (
        "Backflip",
        CompanionType.PYTHIA,
        "draw 2 cards, gain X block",
        Rarity.COMMON,
    )
    SIMPLE_SCRY = (
        "Simple scry",
        CompanionType.PYTHIA,
        "Scry 2",
        Rarity.COMMON,
    )

    # ABORAH cards
    HIT_THE_GYM = (
        "Hit the Gym",
        CompanionType.ABORAH,
        "2 mana, gain X strength",
        Rarity.COMMON,
    )
    DOUBLE_STRIKE = (
        "Double Strike",
        CompanionType.ABORAH,
        "lose 1 strength, deal X damage twice",
        Rarity.COMMON,
    )
    BIG_STRIKE = (
        "Big strike",
        CompanionType.ABORAH,
        "lose 1 strength, deal X damage",
        Rarity.COMMON,
    )

    def __new__(cls, value, companion, description, rarity):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.companion = companion
        obj.description = description
        obj.rarity = rarity
        return obj


def cards_for_companion(companion_type: CompanionType) -> List[Card]:
    return [card for card in list(Card) if card.companion == companion_type]
