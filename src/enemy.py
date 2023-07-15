from enum import Enum
from typing import List
from src.entity import Entity

NUM_ATTACKS = 20


class EnemyType(Enum):
    """Static enumeration of all the companion types in Signified."""

    THIEF = (
        "Thief",
        "Basic enemy that attacks the same amount each turn.",
        [10] * NUM_ATTACKS,
        30,
    )
    CRINGELORD = (
        "Cringelord",
        "The cringelord scales, dealing increasing damage each turn.",
        [1 * i + 10 for i in range(NUM_ATTACKS)],
        40,
    )
    GOBLIN = (
        "Goblin",
        "Basic enemy that attacks the same amount each turn but weaker",
        [5] * NUM_ATTACKS,
        20,
    )

    def __new__(
        cls,
        value,
        description: str,
        attack_pattern: List[int],
        starting_health: int,
    ):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        obj.attack_pattern = attack_pattern
        obj.starting_health = starting_health
        return obj


class Enemy(Entity):
    """Enemy represents a single enemy in Signified."""

    def __init__(self, name: str, enemy_type: EnemyType):
        super().__init__(name, enemy_type.starting_health, 0)
        self.enemy_type = enemy_type
        self.attack_counter = 0

    def __str__(self):
        return (
            f"😈 {self.name}, {self.enemy_type.value}: {self.health}/{self.max_health}💖. "
            f"Attacking for {self.enemy_type.attack_pattern[self.attack_counter]}"
        )

    def next_attack(self) -> None:
        self.attack_counter += 1

    def prev_attack(self) -> None:
        self.attack_counter -= 1
