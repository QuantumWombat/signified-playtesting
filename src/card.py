from dataclasses import dataclass
from enum import Enum

class Rarity(Enum):
    COMMON = 1
    UNCOMMON = 2
    RARE = 3

@dataclass(frozen=True, repr=False)
class Card():
    name: str
    rarity: Rarity

    def __str__(self) -> str:
        return f"🃏 {self.name}"

    def __repr__(self):
        return self.__str__()
