"""Testbed is the main testbed for dogfooding GoFaceGames"""

from typing import Dict

from src.entity import Companion, Enemy

class Testbed():

    def __init__(self):
        self.companions: Dict[str, Companion] = {}


class Encounter():

    def __init__(self):
        self.enemies: Dict[str, Enemy] = {}

    def add_enemy(self, enemy: Enemy):
        self.enemies[enemy.name] = enemy

    def __str__(self):
        return "\n".join([str(e) for _, e in self.enemies.items()])
