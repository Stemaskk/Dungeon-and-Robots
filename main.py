"""Entry point — wires up the orchestrator once the pieces below exist."""

import sys

from src.game_logic import Move
from src.orchestrator import GameState, Orchestrator
from src.narrator import Narrator
from src.dice_vision import get_dice_color as detect_dice_color
from src.gesture import Gesture
from gretchen.camera import Camera

cam = Camera(0)
cam.start()

def get_player_move():
    """Stand-in for gesture.py — always plays rock for now."""
    gesture = Gesture()
    return gesture.rps()

def get_start_signal():
    return True


if __name__ == "__main__":
    narrator = Narrator()
    start_state = GameState.BOSS_FIGHT if "--boss-fight" in sys.argv else GameState.WAITING_FOR_START
    game = Orchestrator(
        get_start_signal,
        get_player_move,
        lambda: detect_dice_color(cam),
        narrator.narrate,
        start_state=start_state,
    )
    game.run()

