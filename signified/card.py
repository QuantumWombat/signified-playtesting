from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Card:
    name: str
    parent_companion: str
    card_text: str
    mana: int

    @staticmethod
    def from_csv_row(row: Dict[str, Any]) -> "Card":
        mana_cost = 1 if row["Mana"] == "" else int(row["Mana"])
        owner = row["Owner"].split(" ")[0]
        return Card(row["name"], owner, row["CardText"], mana_cost)
