"""Game state machine: intro -> RPS -> boss fight -> game over / treasure.

Wires together gesture recognition, dice detection, narrator, and robot head.

Owner: M
"""

from enum import Enum

from src.game_logic import resolve_rps, gretchen_move, LifePoints


class GameState(Enum):
    WAITING_FOR_START = "waiting_for_start"
    INTRO = "intro"
    RPS = "rps"
    BOSS_FIGHT = "boss_fight"
    GAME_OVER = "game_over"
    TREASURE = "treasure"

class Orchestrator:
    def __init__(self, get_start_signal, get_player_move, get_dice_color, narrate, react, start_state=GameState.WAITING_FOR_START):
        self.state = start_state
        self.get_start_signal = get_start_signal
        self.get_player_move = get_player_move
        self.get_dice_color = get_dice_color
        self.narrate = narrate
        self.react = react
        self.life = LifePoints()


    # State machine
    def run(self):
        while self.state not in (GameState.GAME_OVER, GameState.TREASURE):
            if self.state == GameState.WAITING_FOR_START:
                self._handle_waiting_for_start()
            elif self.state == GameState.INTRO:
                self._handle_intro()
            elif self.state == GameState.RPS:
                self._handle_rps()
            elif self.state == GameState.BOSS_FIGHT:
                self._handle_boss_fight()
        print(f"Game ended: {self.state}")

    def _handle_waiting_for_start(self):
        self.narrate("waiting_for_start")
        while True:
            if self.get_start_signal():
                self.state = GameState.INTRO
                break


    def _handle_intro(self):
        self.narrate("intro")
        self.state = GameState.RPS


    def _handle_rps(self):
        while True:
            player_move = self.get_player_move()
            g_move = gretchen_move()
            result = resolve_rps(player_move, g_move)
            print(f"Player: {player_move}, result: {result}")
            result_text = {
                "player": "the player won this round",
                "gretchen": "you (Gretchen) won this round",
                "tie": "this round was a tie",
            }[result]
            self.narrate("rps_round", player_move=player_move.value, gretchen_move=g_move.value, result=result_text)
            if result != "tie":
                break
            print("Tie! You need to play again.")
        if result == "player":
            self.narrate("rps_win")
            self.react("won")
            self.state = GameState.BOSS_FIGHT
        else:
            self.narrate("rps_lose")
            self.react("lost")
            self.state = GameState.GAME_OVER


    def _handle_boss_fight(self):
        current = "gretchen"
        while self.life.winner() is None:
            dice_color = self.get_dice_color()
            self.life.apply_dice_damage(current, dice_color)
            roller_text = "the player" if current == "player" else "you (Gretchen)"
            self.narrate(
                "dice_round",
                roller=roller_text,
                dice_color=dice_color,
                player_life=self.life.player,
                gretchen_life=self.life.gretchen,
            )
            current = "player" if current != "player" else "gretchen"
        if (self.life.winner() == "player"):
            self.narrate("boss_win")
            self.react("won")
            self.state = GameState.TREASURE
        else:
            self.narrate("boss_lose")
            self.react("lost")
            self.state = GameState.GAME_OVER
