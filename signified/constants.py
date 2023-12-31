from dataclasses import dataclass
from enum import Enum
from typing import Dict


COMPANION_COST = 4
CARD_COST = 1
REROLL_COST = 1
INTEREST_RATE = 1 / 5


@dataclass(frozen=True)
class ShopConstants:
    """ShopConstants define the different constants in Signified."""

    num_cards_to_show: int
    num_companions_to_show: int
    upgrade_cost: int
    card_shop_weights: Dict[str, int]


class ShopLevel(Enum):
    """Shop level defines the different levels of the shop in Signified."""

    ONE = (
        1,
        "Energy: 3, Max Team Size: 3",
        ShopConstants(
            num_cards_to_show=4,
            num_companions_to_show=2,
            upgrade_cost=6,
            card_shop_weights={
                "Starting Deck": 0,
                "Common": 3,
                "Uncommon": 2,
                "Rare": 1,
            },
        ),
    )
    TWO = (
        2,
        "Energy: 3, Max Team Size 4",
        ShopConstants(
            num_cards_to_show=5,
            num_companions_to_show=2,
            upgrade_cost=12,
            card_shop_weights={
                "Starting Deck": 0,
                "Common": 1,
                "Uncommon": 1,
                "Rare": 1,
            },
        ),
    )
    THREE = (
        3,
        "Energy: 3, Max Team Size 5",
        ShopConstants(
            num_cards_to_show=5,
            num_companions_to_show=3,
            upgrade_cost=18,
            card_shop_weights={
                "Starting Deck": 0,
                "Common": 1,
                "Uncommon": 2,
                "Rare": 3,
            },
        ),
    )

    def __new__(cls, value, desc, shop_constants):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.desc = desc
        obj.shop_constants = shop_constants
        return obj

    def succ(self):
        v = self.value + 1
        return ShopLevel(v)

    def pred(self):
        v = self.value - 1
        if v <= 1:
            raise ValueError("Enumeration ended")
        return ShopLevel(v)
