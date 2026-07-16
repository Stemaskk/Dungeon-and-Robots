"""Core game rules: RPS resolution, dice damage table, life points, win/lose checks.

Owner: M
"""

from enum import Enum
import random

class Move(Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"

# What each move beats
BEATS = {
    Move.ROCK: Move.SCISSORS,
    Move.PAPER: Move.ROCK,
    Move.SCISSORS: Move.PAPER
}

# Returns "player", "gretchen", or "tie"
def resolve_rps(player_move, gretchen_move):
    if player_move == gretchen_move:
        return "tie"
    return "player" if BEATS[player_move] == gretchen_move else "gretchen"


# Returns a random move
def gretchen_move():
    return random.choice(list(Move))

# Dice colour -> damage dealth
DICE_DAMAGE = {
    "red": 2,
    "green": 1,
    "blue": 0
}

STARTING_LIFE = 5

class LifePoints:
    def __init__(self):
        self.player = STARTING_LIFE
        self.gretchen = 3

    def apply_dice_damage(self, target, color):
        damage = DICE_DAMAGE[color]
        if target == "player":
            self.player = max(0, self.player-damage)
        else:
            self.gretchen = max(0, self.gretchen - damage)
    
    def winner(self):
        if self.gretchen <= 0:
            return "player"
        if self.player <= 0:
            return "gretchen"
        return None
