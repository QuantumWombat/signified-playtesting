import csv
from pathlib import Path
import random
from typing import Dict, List
from typing import List
from signified.card import Card
from signified.constants import (
    CARD_COST,
    COMPANION_COST,
    INTEREST_RATE,
    REROLL_COST,
    SHOP_HEAL_AMOUNT,
    SHOP_HEAL_COST,
    ShopLevel,
)
from signified.entity import Companion, CompanionFactory, Enemy
from signified.utils import (
    closest_word,
    emoji_for_card_rarity,
    get_cleaned_input,
    print_combat_status,
    print_companion_roster,
    print_shop_state,
)


class TestingInstance:
    def __init__(
        self, available_companions: List[CompanionFactory], available_cards: List[Card]
    ) -> None:
        self.available_companions = available_companions
        self.available_cards = available_cards
        self.companion_roster: Dict[str, Companion] = {}
        self.player_gold = 0
        self.shop_level = ShopLevel.ONE

    def choose_starting_pokemon(self) -> None:
        option1 = random.sample(self.available_companions, 3)
        option2 = random.sample(self.available_companions, 3)
        print("Choose your starting companion team.")
        print("Option 1:", [c.name for c in option1])
        print("Option 2: ", [c.name for c in option2])
        print("Enter '1' for Option 1 or '2' for Option 2: ", end="")
        user_input = input()
        if user_input == "1":
            roster = [c.new_companion() for c in option1]
        elif user_input == "2":
            roster = [c.new_companion() for c in option2]
        else:
            raise ValueError(f"Unrecognized option '{user_input}'")
        self.companion_roster = {c.name: c for c in roster}

    def combat_reward(self, gold: int) -> None:
        print(f"Previous balance ${self.player_gold}")
        earned_interest = int(self.player_gold * INTEREST_RATE)
        print(
            f"You earned ${gold} combat reward and ${earned_interest} interest on your savings"
        )
        print(f"Total earnings: ${gold + earned_interest}")
        self.player_gold += gold + earned_interest
        print(f"Current balance ${self.player_gold}")

    def combat(self, enemies: List[Enemy]) -> None:
        if len(set([enemy.name for enemy in enemies])) < len(enemies):
            raise ValueError("names of enemies must be unique")

        enemy_tracker = {enemy.name: enemy for enemy in enemies}

        available_actions = ["damage", "exit", "status", "endturn"]
        print_combat_status(self.companion_roster, enemies)
        print("Starting combat.")
        print(f"Available actions: {available_actions}")
        print("Example: `damage Goon 4` deals 4 damage to the enemy called Goon")
        while True:
            print(">>>", end="")
            split = get_cleaned_input()
            action = split[0] if len(split) >= 1 else ""
            chosen_action = closest_word(action, available_actions)
            if chosen_action == "damage":
                try:
                    # We assume that the second index is the name of the entity
                    # and the third index is the amount of damage, e.g. damage Goon 1
                    name = split[1]
                    damage_count = int(split[2])
                except Exception as e:
                    print("proper usage :) `damage Goon 4`")
                    continue

                enemy_names = [enemy.name for enemy in enemies]
                companion_names = list(self.companion_roster.keys())
                selected_entity = closest_word(name, enemy_names + companion_names)
                print(f"Dealt {damage_count} damage to {selected_entity}")

                if selected_entity in enemy_names:
                    enemy_tracker[selected_entity].damage(damage_count)
                elif selected_entity in companion_names:
                    self.companion_roster[selected_entity].damage(damage_count)
            elif chosen_action == "exit":
                break
            elif chosen_action == "status":
                print_combat_status(self.companion_roster, enemies)
            elif chosen_action == "endturn":
                print("End of turn; scaling enemies")
                for _, enemy in enemy_tracker.items():
                    enemy.attack += enemy.scaling_factor
                print_combat_status(self.companion_roster, enemies)

    def shop(self) -> None:
        # Generate options for the shop first.
        companions = self._generate_companion_options()
        cards = self._generate_card_options()
        print_shop_state(self.player_gold, self.shop_level, companions, cards)
        available_actions = [
            "buy",
            "exit",
            "status",
            "upgrade",
            "reroll",
            "lookup",
            "heal",
        ]
        print("Welcome to the shop.")
        print(f"Available actions: {available_actions}")
        print(
            "Buy things using `buy` with the name of the card or companion, e.g. `buy Double Strike`"
        )
        print(
            "Use `lookup` to get information about a card or companion, e.g. `lookup Aborah`"
        )
        print(
            " ".join(
                [emoji_for_card_rarity(r) + r for r in ["Common", "Uncommon", "Rare"]]
            )
        )
        used_shop_heal = False
        while True:
            print(">>> ", end="")
            split = get_cleaned_input()
            action = split[0] if len(split) >= 1 else ""
            chosen_action = closest_word(action, available_actions)
            if chosen_action == "exit":
                break
            elif chosen_action == "buy":
                if len(split) < 2:
                    print("proper usage: `buy {card_name}`")
                    continue
                if len(companions) + len(cards) == 0:
                    print("shop is empty, please refresh")
                    continue

                choice = " ".join(split[1:])
                companion_names = [c.name for c in companions]
                card_names = [c.name for c in cards]
                selection = closest_word(choice, companion_names + card_names)
                if selection in card_names:
                    if self.player_gold - CARD_COST < 0:
                        print(
                            "you cannot afford to buy this card, current balance "
                            + f"${self.player_gold} and card cost ${CARD_COST}"
                        )
                        continue
                    self.player_gold -= CARD_COST
                    card_to_remove = [c for c in cards if c.name == selection][0]
                    cards.remove(card_to_remove)

                    print(f"You bought the card `{selection}`")
                    print(
                        f"This card belongs to the companion {card_to_remove.parent_companion}"
                    )
                    print(
                        "Get a copy of the card from your printed-out cards and add it to the deck of one of your companions."
                    )
                elif selection in companion_names:
                    if self.player_gold - COMPANION_COST < 0:
                        print(
                            "you cannot afford to buy this companion, current balance "
                            + f"${self.player_gold} and companion cost ${COMPANION_COST}"
                        )
                        continue
                    self.player_gold -= COMPANION_COST
                    companion_to_remove = [
                        c for c in companions if c.name == selection
                    ][0]
                    new_companion = companion_to_remove.new_companion()
                    self.companion_roster[new_companion.name] = new_companion
                    companions.remove(companion_to_remove)

                    print(f"You bought the companion `{selection}`")
                    print_companion_roster(self.companion_roster)

            elif chosen_action == "upgrade":
                if self.player_gold - self.shop_level.shop_constants.upgrade_cost < 0:
                    print(
                        "you cannot afford to upgrade the shop, current balance "
                        + f"${self.player_gold} and companion cost ${self.shop_level.shop_constants.upgrade_cost}"
                    )
                    continue
                self.player_gold -= self.shop_level.shop_constants.upgrade_cost
                self.shop_level = self.shop_level.succ()
                print(
                    f"You successfully upgraded the shop to shop level {self.shop_level.value}"
                )
                print(
                    "Your team size and mana are now different!",
                    self.shop_level.desc,
                )

            elif chosen_action == "reroll":
                if self.player_gold - REROLL_COST < 0:
                    print(
                        "you cannot afford to reroll, current balance "
                        + f"${self.player_gold} and reroll cost ${REROLL_COST}"
                    )
                    continue
                self.player_gold -= REROLL_COST

                companions = self._generate_companion_options()
                cards = self._generate_card_options()
                print("Successfully rerolled the shop")

                print_shop_state(self.player_gold, self.shop_level, companions, cards)

            elif chosen_action == "status":
                print_shop_state(self.player_gold, self.shop_level, companions, cards)
                print_companion_roster(self.companion_roster)

            elif chosen_action == "lookup":
                choice = " ".join(split[1:])
                companion_names = [c.name for c in companions]
                card_names = [c.name for c in cards]
                selection = closest_word(choice, companion_names + card_names)
                if selection in card_names:
                    card = [c for c in cards if c.name == selection][0]
                    print(card)
                elif selection in companion_names:
                    companion = [c for c in companions if c.name == selection][0]
                    print(companion)
            elif chosen_action == "heal":
                if used_shop_heal:
                    print("You can only use the heal in the shop once.")
                    continue
                if self.player_gold - SHOP_HEAL_COST < 0:
                    print(
                        "you cannot afford to heal, current balance "
                        + f"${self.player_gold} and heal cost ${SHOP_HEAL_COST}"
                    )
                    continue
                self.player_gold -= SHOP_HEAL_COST

                choice = " ".join(split[1:])
                companion_names = list(self.companion_roster.keys())
                selection = closest_word(choice, companion_names)

                cur_hp = self.companion_roster[selection].health
                updated_hp = min(
                    self.companion_roster[selection].max_health,
                    cur_hp + SHOP_HEAL_AMOUNT,
                )
                print(f"Healing companion {selection} for {updated_hp - cur_hp} HP")
                self.companion_roster[selection].health = updated_hp
                used_shop_heal = True

    def _generate_card_options(self) -> List[Card]:
        companion_roster_names = [
            c.companion_name for c in self.companion_roster.values()
        ]
        allowed_cards = [
            [card] * self.shop_level.shop_constants.card_shop_weights[card.rarity]
            for card in self.available_cards
            if card.parent_companion in set(companion_roster_names)
        ]
        allowed_cards = [card for card_dups in allowed_cards for card in card_dups]

        if len(allowed_cards) == 0:
            return []
        return random.sample(
            allowed_cards, self.shop_level.shop_constants.num_cards_to_show
        )

    def _generate_companion_options(self) -> List[CompanionFactory]:
        return random.sample(
            self.available_companions,
            self.shop_level.shop_constants.num_companions_to_show,
        )

    @staticmethod
    def init_from_csvs(
        companion_csv_path: Path, card_csv_path: Path
    ) -> "TestingInstance":
        available_companions = read_companion_csv(companion_csv_path)
        available_cards = read_card_csv(card_csv_path)
        return TestingInstance(available_companions, available_cards)


def read_companion_csv(path: Path) -> List[CompanionFactory]:
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return [CompanionFactory.from_csv_row(row) for row in reader]


def read_card_csv(path: Path) -> List[Card]:
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return [Card.from_csv_row(row) for row in reader]
