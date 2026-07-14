"""Game state machine: intro -> RPS -> boss fight -> game over / treasure.

Wires together gesture recognition, dice detection, narrator, and robot head.

Owner: M
"""

from enum import Enum

from src.game_logic import resolve_rps, gretchen_move, LifePoints


class GameState(Enum):
    INTRO = "intro"
    RPS = "rps"
    BOSS_FIGHT = "boss_fight"
    GAME_OVER = "game_over"
    TREASURE = "treasure"

# TODO: get_player_move and get_dice_color are mocked for now - need to change 
# TODO: change all the print statement to the LLM stuff
class Orchestrator:
    def __init__(self, get_player_move, get_dice_color):
        self.state = GameState.INTRO
        self.get_player_move = get_player_move
        self.get_dice_color = get_dice_color
        self.life = LifePoints()


    # State machine
    def run(self):
        while self.state not in (GameState.GAME_OVER, GameState.TREASURE):
            if self.state == GameState.INTRO:
                self._handle_intro()
            elif self.state == GameState.RPS:
                self._handle_rps()
            elif self.state == GameState.BOSS_FIGHT:
                self._handle_boss_fight()
        print(f"Game ended: {self.state}")


    def _handle_intro(self):
        print("You walk into a dungeon and encounter an evil Gretchen...")
        self.state = GameState.RPS


    def _handle_rps(self):
        while True:
            player_move = self.get_player_move()
            result = resolve_rps(player_move, gretchen_move())
            print(f"Player: {player_move}, result: {result}")
            if result != "tie":
                break
            print("Tie! You need to play again.")
        if result == "player":
            self.state = GameState.BOSS_FIGHT
        else:
            self.state = GameState.GAME_OVER


    def _handle_boss_fight(self):
        current = "gretchen"
        while self.life.winner() is None:
            dice_color = self.get_dice_color()
            self.life.apply_dice_damage(current, dice_color)
            current = "player" if current != "player" else "gretchen"
        if (self.life.winner() == "player"):
            print("You win!")
            self.state = GameState.TREASURE
        else:
            self.state = GameState.GAME_OVER
