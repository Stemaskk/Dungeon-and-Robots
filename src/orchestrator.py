"""Game state machine: intro -> RPS -> boss fight -> game over / treasure.

Wires together gesture recognition, dice detection, narrator, and robot head.

Owner: M
"""

import time
from enum import Enum

from src.game_logic import resolve_rps, gretchen_rps_move, gretchen_dice, LifePoints


class GameState(Enum):
    WAITING_FOR_START = "waiting_for_start"
    INTRO = "intro"
    RPS = "rps"
    BOSS_FIGHT = "boss_fight"
    GAME_OVER = "game_over"
    TREASURE = "treasure"

class Orchestrator:
    def __init__(self, get_start_signal, get_player_move, get_dice_color, narrate, react, play_audio, start_state=GameState.WAITING_FOR_START):
        self.state = start_state
        self.get_start_signal = get_start_signal
        self.get_player_move = get_player_move
        self.get_dice_color = get_dice_color
        self.narrate = narrate
        self.react = react
        self.play_audio = play_audio
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
        # Wait for the player's start gesture (paper) FIRST ...
        while not self.get_start_signal():
            pass
        # ... then greet them over the music and move on.
        self.play_audio("game_started")
        self.narrate("waiting_for_start")
        self.state = GameState.INTRO


    def _handle_intro(self):
        self.narrate("intro")
        time.sleep(1) # player needs to reset 
        self.state = GameState.RPS


    def _handle_rps(self):
        while True:
            player_move = self.get_player_move()
            g_move = gretchen_rps_move()
            result = resolve_rps(player_move, g_move)
            print(f"Player: {player_move}, result: {result}")
            result_text = {
                "player": "the player won this round",
                "gretchen": "you (Gretchen) won this round",
                "tie": "this round was a tie",
            }[result]
            self.narrate("rps_round", player_move=player_move.value, gretchen_rps_move=g_move.value, result=result_text)
            if result != "tie":
                break
            print("Tie! You need to play again.")
        if result == "player":
            self.play_audio("rps_won")   # victory 
            self.react("won")            # head shake as Evil Gretchen dies
            self.narrate("rps_win")      # "I'm dying — but now face Boss Gretchen"
            self.state = GameState.BOSS_FIGHT
        else:
            self.play_audio("game_over")   # lose music
            self.react("lost")             
            self.narrate("rps_lose")       # final "you're dead"
            self.state = GameState.GAME_OVER


    def _handle_boss_fight(self):
        time.sleep(2)                    # brief pause after Evil Gretchen's death
        self.play_audio("boss_started")  # boss music 
        self.narrate("boss_intro")       # Boss Gretchen introduces itself over it
        current = "player"
        while self.life.winner() is None:
            if current == "player":
                dice_color = self.get_dice_color()
            else:
                dice_color = gretchen_dice()

            target = "gretchen" if current == "player" else "player"
            self.life.apply_dice_damage(target, dice_color)

            roller_text = "the player" if current == "player" else "you (Gretchen)"
            target_text = "the player" if target == "player" else "you (Gretchen)"
            self.narrate(
                "dice_round",
                roller=roller_text,
                target=target_text,
                dice_color=dice_color,
                player_life=self.life.player,
                gretchen_life=self.life.gretchen,
            )
            current = "gretchen" if current == "player" else "player"

        if (self.life.winner() == "player"):
            self.narrate("boss_win")
            self.play_audio("game_won")
            self.react("won")
            self.state = GameState.TREASURE
        else:
            self.play_audio("game_over")   # lose music
            self.react("lost")             # head moves
            self.narrate("boss_lose")      # final "you're dead"
            self.state = GameState.GAME_OVER
