from dataclasses import dataclass
import random
import string
from typing import Any, Dict


@dataclass
class Entity:
    name: str
    max_health: int
    health: int

    def damage(self, amount: int):
        self.health -= amount
        if self.health <= 0:
            print(f"Entity {self.name} died")


@dataclass
class Enemy(Entity):
    attack: int
    attack_pattern_tmpl: str
    # Optional scaling factor for the Enemy that gives linearly increasing attack.
    scaling_factor: int = 0


@dataclass
class Companion(Entity):
    strength: int
    companion_name: str


@dataclass
class CompanionFactory:
    name: str
    passive_ability: str

    starting_health: int
    starting_strength: int

    @staticmethod
    def from_csv_row(row: Dict[str, Any]) -> "CompanionFactory":
        return CompanionFactory(
            row["name"], row["PassiveAbility"], int(row["Health"]), int(row["Strength"])
        )

    def new_companion(self) -> Companion:
        prefix = "".join(random.choices(string.ascii_lowercase, k=2)) + "-"
        return Companion(
            prefix + self.name,
            self.starting_health,
            self.starting_health,
            self.starting_strength,
            self.name,
        )
