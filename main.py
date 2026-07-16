"""Entry point — wires up the orchestrator once the pieces below exist."""

from src.game_logic import Move
from src.orchestrator import Orchestrator
from src.narrator import Narrator


def get_player_move():
    """Stand-in for gesture.py — always plays rock for now."""
    return Move.ROCK


def get_dice_color():
    """Stand-in for dice_vision.py — always rolls red for now."""
    return "red"

def get_start_signal():
    return True


if __name__ == "__main__":
    narrator = Narrator()
    game = Orchestrator(get_start_signal, get_player_move, get_dice_color, narrator.narrate)
    game.run()
