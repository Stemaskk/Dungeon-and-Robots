"""Entry point — wires up the orchestrator once the pieces below exist."""

import sys

from src.orchestrator import GameState, Orchestrator
from src.narrator import Narrator
from src.dice_vision import get_dice_color as detect_dice_color
from src.robot_head import react 
from src.audio_manager import initialize_audio, handle_event as play_audio
from src.gesture import Gesture
from gretchen.robot import Robot

robot = Robot('/dev/tty.usbserial-FT94EP38', 0)
cam = robot.camera
robot.start()

initialize_audio()


gesture = Gesture()

def get_start_signal():
    return True

if __name__ == "__main__":
    narrator = Narrator()
    start_state = GameState.BOSS_FIGHT if "--boss-fight" in sys.argv else GameState.WAITING_FOR_START
    game = Orchestrator(
        get_start_signal,
        lambda: gesture.rps(cam),
        lambda: detect_dice_color(cam),
        narrator.narrate,
        lambda outcome: react(robot, outcome),
        play_audio,
        start_state=start_state,
    )
    robot.move(0,0)
    game.run()

