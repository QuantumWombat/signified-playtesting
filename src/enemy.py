from src.entity import Entity


class Enemy(Entity):
    """Enemy represents a single enemy in Signified."""

    def __init__(self, name: str, starting_health: int = 20, starting_attack: int = 1):
        super().__init__(name, starting_health, starting_attack)

    def __str__(self):
        return f"😈 {self.name}: {self.health}/{self.max_health}💖"
