import nltk
import os
from typing import Dict, List
from signified.card import Card
from signified.constants import CARD_COST, COMPANION_COST, REROLL_COST

from signified.entity import Companion, CompanionFactory, Enemy
from signified.constants import ShopLevel


def closest_word(word: str, words: List[str]) -> str:
    edit_distances = [nltk.edit_distance(word, w) for w in words]
    for i, _ in enumerate(edit_distances):
        # Discount if we are using a unique common prefix.
        common_prefix = os.path.commonprefix([word.lower(), words[i].lower()])
        edit_distances[i] -= 4 * len(common_prefix)
    min_distance = min(edit_distances)
    chosen = words[edit_distances.index(min_distance)]
    return chosen


def get_cleaned_input() -> List[str]:
    raw = input()
    sep = [s.strip().lower() for s in raw.split(" ")]
    return [s for s in sep if len(s) > 0]


def print_combat_status(
    companion_roster: Dict[str, Companion], dudes: List[Enemy]
) -> None:
    print_enemies(dudes)
    print("-" * 10)
    print_companion_roster(companion_roster)
    print("-" * 10)


def print_companion_roster(companion_roster: Dict[str, Companion]):
    print("Your Companion Roster")
    for guy in companion_roster.values():
        print(f"{guy.name.ljust(15)} {guy.strength}⚔️ {guy.health}/{guy.max_health}💖")


def print_enemies(dudes: List[Enemy]) -> None:
    for dude in dudes:
        attack_pattern = dude.attack_pattern_tmpl.format(attack=dude.attack)
        print(
            f"{dude.name.ljust(15)} {dude.health}/{dude.max_health}💖 {attack_pattern}"
        )


def print_shop_state(
    player_gold: int,
    shop_level: ShopLevel,
    shown_companions: List[CompanionFactory],
    shown_cards: List[Card],
) -> None:
    companion_names = [c.name for c in shown_companions]
    card_names = [emoji_for_card_rarity(c.rarity) + c.name for c in shown_cards]
    print("-" * 10)
    print(f"Shop Level {shop_level.value}, {shop_level.desc}")
    print(f"Your current gold: ${player_gold}")
    print(f"Companions (${COMPANION_COST}): {' - '.join(companion_names)}")
    print(f"Cards (${CARD_COST}): {' - '.join(card_names)}")
    print(f"Upgrade the shop (${shop_level.shop_constants.upgrade_cost})")
    print(f"Reroll (${REROLL_COST})")
    print("-" * 10)


def emoji_for_card_rarity(rarity: str):
    if rarity == "Common":
        return "🥉"
    elif rarity == "Uncommon":
        return "🥈"
    elif rarity == "Rare":
        return "🥇"
    else:
        return ""
