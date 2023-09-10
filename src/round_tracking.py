# Adam's attempt at a data collection system as another tool in the playtesting
# arsenal.
#
# Basic idea is to run multiple enemy-less rounds with a set of companions,
# then track the amount of damage the player deals / block they generate each turn.
#
# Eventually we can compile mean/median/st.dev stats for dmg/block on each turn
# with a given team, so that we can gauge consistency and relative 
# power level for each companion/group of companions.
#
# We will absolutely still need qualitative playtesting, but some more quantitative
# data should be useful as well.

# Architecture:
# This should totally be an RDS, but we're goin MVP for now. Leaving space
# for more information to be added/computed on each of these levels
# RoundTrackedEncounter:
#   - Companions: List<CompanionTypes>
#   - Rounds: List<Round>
# Round: 
#   - List<Turn>
# Turn:
#   - Damage: int
#   - Block: int
# This code is gonna be utter garbage to start with.

from dataclasses import dataclass, field
from enum import Enum
import os
import random
import pickle
from typing import Dict, List, Optional
from src import *
from src.companion import Companion, CompanionType

class Roundlol:
    def __init__(self, turns):
        self.turns = turns
        pass
        



class Turn:
    def __init__(self, damage: int, block: int):
        self.damage = damage
        self.block = block
    
    def __str__(self):
        # on a plane and forgot how to str format in python
        return "damage: " + damage + " block: " + block



class Round:
    def __init__(self, turns):
        self.turns = turns
        pass


class Testest:
    def __init__(self):
        test = 1


class TestedCompanionSet:
    def __init__(self, 
                 companions,
                 encounters):
        self.companions = companions
        self.encounters = encounters

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load(cls, filename):
        with open(filename, 'rb') as file:
            loaded_obj = pickle.load(file)
        if isinstance(loaded_obj, cls):
            return loaded_obj
        else:
            raise ValueError(f"Loaded object is not an instance of {cls.__name__}")


