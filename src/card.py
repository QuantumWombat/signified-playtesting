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
    SUMMON_ARTIFACT = (
        "Summon Artifact",
        "summon a token that draws you a shiv each turn",
        Rarity.COMMON,
    )
    FINISHING_TOUCH = (
        "Finishing touch",
        "for each attack you played this turn, deal 3 damage",
        Rarity.COMMON,
    )
    IDEATE = (
        "Ideate",
        "draw a card for each artifact you control",
        Rarity.UNCOMMON,
    )
    MITOSIS = (
        "Mitosis",
        "destroy a token you control and summon 2 new ones",
        Rarity.UNCOMMON,
    )

    # CLOWN cards

    # ENTROPY cards
    BELLOWS = ("Bellows", "draw 3 and exhaust one of the cards", Rarity.COMMON)
    SOOTY_ARMOR = (
        "Sooty Armor",
        "give a companion 10 block, shuffle a status card into their deck",
        Rarity.COMMON,
    )
    FIERY_ENCOURAGEMENT = (
        "Fiery Encouragement",
        "give a companion X strength, shuffle in status card",
        Rarity.UNCOMMON,
    )
    SELF_SHARPENING_BLADE = (
        "Self Sharpening Blade",
        "deal 5 damage. deal 5 more damage next time",
        Rarity.UNCOMMON,
    )

    # PYTHIA cards
    DISCHARGE = (
        "Discharge",
        "for each card in your hand, deal 1 damage",
        Rarity.COMMON,
    )
    MENTAL_PRISM = (
        "Mental Prism",
        "draw 2 cards, gain 5 block",
        Rarity.COMMON,
    )
    FORCE_FIELD = (
        "Force field",
        "give a companion immune this turn",
        Rarity.UNCOMMON,
    )
    ADRENALINE = (
        "Adrenaline",
        "0 mana gain 1 energy draw 2 cards",
        Rarity.RARE,
    )

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
