"""Testbed is the main testbed for dogfooding GoFaceGames"""

from dataclasses import dataclass, field
from enum import Enum
import os
import random
import pickle
from typing import Dict, List, Optional
from src.card import Card, cards_for_companion

from src.enemy import Enemy
from src.companion import Companion, CompanionType
from src.constants import (
    CARD_COST,
    COMBAT_REWARD_GOLD,
    COMPANION_COST,
    NUM_STARTING_COMPANIONS,
    REROLL_COST,
)


class Testbed:
    """Testbed is the root data structure for a prototyping session.

    It holds state about the player's current roster, their economy, and
    the enemies to follow.
    """

    def __init__(
        self,
        seed: Optional[int] = None,
        enabled_companions: List[CompanionType] = list(CompanionType),
    ):
        if seed is not None:
            print(f"Using seed {seed}")
            random.seed(seed)
        # Generate a list of starter companions.
        self.enabled_companions = enabled_companions
        starting_companion_types = random.choices(
            enabled_companions, k=NUM_STARTING_COMPANIONS
        )
        self.companions: Dict[str, Companion] = {}
        for c in starting_companion_types:
            name = self._generate_unique_companion_name(c)
            self.companions[name] = Companion(name, c)
        self.shop = Shop()
        self.encounter_count = 1

    def _generate_unique_companion_name(self, c: CompanionType) -> str:
        i = 0
        while i < 5:
            name = c.generate_name()
            if name not in self.companions:
                return name
            i += 1
        raise ValueError(f"failed to generate unique name for companion {c.value}")

    def reroll_cards(self):
        if self.shop.gold < REROLL_COST:
            raise ValueError(f"cannot afford reroll cost of {REROLL_COST}")
        self.shop.gold -= REROLL_COST
        self.shop.generate_card_options(
            [c.companion_type for _, c in self.companions.items()]
        )

    def generate_shop_post_combat(self):
        print(f"Generating shop for Encounter #{self.encounter_count}")
        self.encounter_count += 1
        print(f"You earned ${COMBAT_REWARD_GOLD} gold for the combat")
        self.shop.gold += COMBAT_REWARD_GOLD
        self.shop.generate_card_options(
            [c.companion_type for _, c in self.companions.items()]
        )
        self.shop.generate_companion_options(self.enabled_companions)
        print(self)

    def buy_companion(self, companion: CompanionType) -> None:
        self.shop._buy_companion(companion)
        name = self._generate_unique_companion_name(companion)
        self.companions[name] = Companion(name, companion)

    def buy_card(self, card: Card) -> None:
        self.shop._buy_card(card)

    def __str__(self):
        """Pretty print global information about the state of the game."""
        disp = [
            self._roster_to_str(),
            str(self.shop),
        ]
        return "\n".join(disp)

    def _roster_to_str(self) -> str:
        disp = (
            "\n".join(["ROSTER"] + [str(v) for _, v in self.companions.items()]) + "\n"
        )
        return disp

    def print_roster(self) -> None:
        print(self._roster_to_str())

    def save_to_file(self, filepath: str = "out/testbed.pkl") -> None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w+b") as f:
            pickle.dump(self, f)

    @staticmethod
    def from_file(filepath: str = "out/testbed.pkl") -> "Testbed":
        with open(filepath, "rb") as f:
            return pickle.load(f)


class Encounter:
    def __init__(self, enemies: List[Enemy]):
        self.enemies = {e.name: e for e in enemies}
        self.turn_counter = 1

    def end_turn(self):
        print(f"End of turn {self.turn_counter}")
        for _, e in self.enemies.items():
            e.next_attack()
        self.turn_counter += 1
        print(self)

    def __str__(self):
        return "\n".join([str(e) for _, e in self.enemies.items()])


@dataclass(frozen=True)
class ShopConstants:
    """ShopConstants define the different constants in Signified."""

    num_cards_to_show: int
    num_companions_to_show: int
    upgrade_cost: int


class ShopLevel(Enum):
    """Shop level defines the different levels of the shop in Signified."""

    ONE = (
        1,
        "Energy: 3, Max Team Size: 3",
        ShopConstants(num_cards_to_show=3, num_companions_to_show=2, upgrade_cost=4),
    )
    TWO = (
        2,
        "Energy: 3, Max Team Size 4",
        ShopConstants(num_cards_to_show=4, num_companions_to_show=3, upgrade_cost=8),
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


@dataclass
class Shop:
    """Shop holds state about the current state of the economy.

    It holds the current level of the shop.
    Level up the shop to see better companions and better cards.
    """

    level: ShopLevel = ShopLevel.ONE
    card_options: List[Card] = field(default_factory=list)
    companion_options: List[CompanionType] = field(default_factory=list)
    gold: int = 0

    def upgrade(self) -> None:
        if self.gold < self.level.shop_constants.upgrade_cost:
            raise ValueError(
                f"cannot afford card cost of {self.level.shop_constants.upgrade_cost}, you have {self.gold}"
            )
        self.gold -= self.level.shop_constants.upgrade_cost
        self.level = self.level.succ()

    def generate_card_options(self, current_companions: List[CompanionType]) -> None:
        unique_companions = set(current_companions)
        card_opts = [
            card
            for companion in unique_companions
            for card in cards_for_companion(companion)
        ]
        # TODO: implement sampling without replacement
        # TODO: weight the cards with respect to their rarity.
        self.card_options = random.choices(
            card_opts,
            k=min(len(card_opts), self.level.shop_constants.num_cards_to_show),
        )

    def generate_companion_options(
        self, enabled_companions: List[CompanionType] = list(CompanionType)
    ) -> None:
        self.companion_options = random.choices(
            enabled_companions, k=self.level.shop_constants.num_companions_to_show
        )

    def _buy_card(self, card: Card) -> None:
        if card not in self.card_options:
            raise ValueError(f"card {card.value} not in options")
        if self.gold < CARD_COST:
            raise ValueError(
                f"cannot afford card cost of {CARD_COST}, you have {self.gold}"
            )
        self.card_options.remove(card)
        self.gold -= CARD_COST

    def _buy_companion(self, companion: CompanionType) -> None:
        if companion not in self.companion_options:
            raise ValueError(f"companion {companion.value} not in options")
        if self.gold < COMPANION_COST:
            raise ValueError(
                f"cannot afford companion cost of {COMPANION_COST}, you have {self.gold}"
            )
        self.companion_options.remove(companion)
        self.gold -= COMPANION_COST

    def __str__(self) -> str:
        disp = [
            f"Shop level: {self.level.value}: {self.level.desc}",
            f"Your current gold: {self.gold}",
            f"COMPANIONS ({COMPANION_COST} gold): "
            + ", ".join([c.value for c in self.companion_options]),
            f"CARDS ({CARD_COST} gold): \n"
            + "\n".join(
                [card.value + ": " + card.description for card in self.card_options]
            ),
            f"UPGRADE ({self.level.shop_constants.upgrade_cost} gold)",
            f"REROLL ({REROLL_COST} gold)",
        ]
        return "\n\n".join(disp)
