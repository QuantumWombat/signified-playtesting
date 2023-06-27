"""Module with entity information."""


class Entity:
    """Entity is the base class for all entity instances, friend or foe."""

    def __init__(self, name: str, starting_health: int = 20, starting_attack: int = 1):
        self.name = name
        self.max_health = starting_health
        self.health = starting_health
        self.attack = starting_attack

    def damage(self, amount: int):
        self.health -= amount
        print(self)
        if self.health <= 0:
            print(f"Entity {self.name} died")
