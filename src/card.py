from dataclasses import dataclass
from enum import Enum

class Rarity(Enum):
    COMMON = 1
    UNCOMMON = 2
    RARE = 3

@dataclass(frozen=True)
class Card():
    name: str
    rarity: Rarity

    def __str__(self) -> str:
        return f"🃏 {self.name}"
