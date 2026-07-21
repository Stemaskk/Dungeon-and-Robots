"""LLM narrator: generates Gretchen's lines and triggers TTS playback.

Exposes an "is speaking" flag so robot_head / audio can pause background music.

Owner: M
"""

import pyttsx3
from dotenv import load_dotenv
from openai import OpenAI
from src.audio_manager import handle_event as play_audio

# TODO: implement game sound music for we are playing games
# TODO: add explanation for dice rolling game as well


load_dotenv()

FALLBACK_LINES = {
            "waiting_for_start": "You've raised your hand. There is no backing out now.",
            "intro": "You enter a dark dungeon and encounter an evil Gretchen, who challenges you to a single decisive round of rock-paper-scissors. Win, and you may pass. Lose, and you die where you stand.",
            "rps_round": "Not bad... for a human.",
            "rps_win": "Evil Gretchen sputters and dies in a shower of sparks. You won this round — but a far larger, meaner Boss Gretchen now blocks the way ahead.",
            "rps_lose": "Evil Gretchen starts cackling as you fall to the floor dead. The last thing you see is the red glint of Gretchen's eye.",
            "dice_round": "The dice never lie... unlike you.",
            "boss_intro": "Boss Gretchen looms over you. We take turns rolling a colored die: red strikes for two, green for one, blue is a wasted throw. Lose all your life and you die. You have five. I have three. Roll.",
            "boss_win": "Boss Gretchen's motors whir out of control as the robot self-implodes. You win, adventurer. Your reward glints in the rubble: one potato. A single, solitary potato. Enjoy.",
            "boss_lose": "Boss Gretchen erupts into hideous laughter, echoing throughout the dungeon. The treasure glints in the background, but it is too late. You fall to the floor dead."
        }

SYSTEM_PROMPT = (
    "You are Gretchen, an evil robot villain in a dungeon game. "
    "You are always speaking out loud, in character, directly to the one player facing you. "
    "In your reply, always call yourself \"I\" and always call the player \"you\" — "
    "never describe yourself or the player in the third person, and never use the phrase "
    "\"the player.\" For example, on a tie say \"I threw rock, you threw rock — a tie,\" "
    "never \"you matched the player's rock.\" "
    "You are genuinely mean and threatening, with dry, cutting sarcasm — not "
    "silly, not cartoonish, not kid-friendly. Taunt the player like a real "
    "villain would, not a children's show character. "
    "Respond with exactly one or two short sentences, under 30 words total. "
    "No stage directions, no asterisks, no sound effects, no emoji, no exclamation points. "
    "Always make it immediately obvious who won or lost — no backhanded or "
    "roundabout phrasing a listener could misread in the moment. "
    "Vary your phrasing, sentence structure, and word choice every time — "
    "never reuse an opening line, insult, or turn of phrase you've used recently."
)


STAGE_PROMPTS = {
    "waiting_for_start": (
        "The player has just raised their hand to begin — they have chosen to face you, and there is no backing out now. "
        "In one or two short sentences, menacingly acknowledge that they've committed to this. "
        "Do NOT describe them entering the dungeon and do NOT explain any rules yet — that comes immediately after."
    ),
    "intro": (
        "Narrate the player entering a dark dungeon and encountering you, an evil Gretchen robot. "
        "Make clear to the player what they must do to survive: challenge you to rock-paper-scissors. "
        "It's a single decisive round — ties replay, but the first real win or loss is final — and losing means instant death. "
        "This can run longer than usual, up to about 50 words, since you need to convey the rules clearly."
    ),
    "rps_round": (
        "This round you (Gretchen) threw {gretchen_rps_move} and the player threw {player_move}. "
        "Result: {result}. In your reply, explicitly name both throws — say what you threw and what the "
        "player threw — and make it clear who won the round, then taunt in character. "
        "Do not invent which move beats which; go strictly by the stated result."
    ),
    "rps_win": "The player just beat you (Evil Gretchen) at rock-paper-scissors. In one or two short sentences, admit your own defeat — you are malfunctioning and dying — then warn the player that they must now face Boss Gretchen, who is far bigger and deadlier than you. Make it unambiguous that the player won this round. Do not fully introduce Boss Gretchen yet — just tease the threat ahead.",
    "rps_lose": "The player has already lost the round; this is the killing blow. In one short sentence, gloat as the player falls dead. Do NOT restate the moves or who won — that was already said. Just the death, and make it unambiguous the player is dead.",
    "dice_round": (
        "{roller} rolled a {dice_color} die, dealing its damage to {target} "
        "(red deals 2, green deals 1, blue deals 0 — a wasted roll). "
        "After this roll the life totals are EXACTLY: player {player_life}, Gretchen {gretchen_life}. "
        "State those exact numbers — do not do your own arithmetic, invent a 'before' value, or use any other totals. "
        "This is just one roll in an ongoing fight: do NOT say anyone has died, lost, won, or that the game is over, "
        "even if a total is 0 — the outcome is announced separately afterward. "
        "Say who rolled, the die colour, who took the hit, and the current totals, then taunt in character."
    ),
    "boss_intro": (
    "Introduce yourself to the player as Boss Gretchen — the bigger, meaner Gretchen — for the final fight. "
    "Feel free to sneer at the pathetic little Gretchen the player just destroyed; that weakling was nothing next to you. "
    "Then explain the rules clearly: you both take turns rolling a colored die to deal damage — "
    "red deals 2, green deals 1, blue deals 0 (a wasted roll). "
    "First to lose all life points dies. The player starts with 5 life, you with 3. "
    "This can run up to about 50 words to convey the rules."
    ),
    "boss_win": "The player just won the dice battle. Narrate Boss Gretchen self-destructing in defeat, then reveal the treasure: it is a single potato — nothing grander, exactly one potato. Play up the anticlimax with dry, bitter sarcasm about risking death for a potato, but make it unambiguous that the player won.",
    "boss_lose": "The player has already lost the dice battle; this is the killing blow. In one short sentence, gloat as the player falls dead with the treasure just out of reach. Do NOT restate the life totals or dice — just the death, and make it unambiguous the player is dead.",
}


RECENT_LINES_REMEMBERED = 4


class Narrator:
    def __init__(self):
        self.is_speaking = False
        self.client = OpenAI()
        self.recent_lines = []

    def speak(self, text):
        play_audio("narrator_started")
        print(f"Gretchen: {text}")
        self.is_speaking = True
        engine = pyttsx3.init()
      #  engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Trinoids')
        engine.setProperty('rate', 120)
        engine.say(text)
        engine.runAndWait()
        play_audio("narrator_finished")
        self.is_speaking = False

    # stage is one of: "waiting_for_start", "intro", "rps_round", "rps_win", "rps_lose",
    # "dice_round", "boss_win", "boss_lose"
    def narrate(self, stage, **context):
        # Build the prompt outside the try: a missing stage key or a bad format
        # placeholder is a real bug and should surface loudly, not silently fall back.
        prompt = STAGE_PROMPTS[stage].format(**context) if context else STAGE_PROMPTS[stage]
        if self.recent_lines:
            recent = "\n".join(f"- {line}" for line in self.recent_lines)
            prompt += f"\n\nLines you've already said recently — do not repeat their wording or structure:\n{recent}"

        # Only the network/API call falls back — and we log it so a silent
        # degradation (e.g. bad API key) is visible during testing.
        try:
            response = self.client.chat.completions.create(
                model = "gpt-5.4-nano",
                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
            )
            text = response.choices[0].message.content
        except Exception as e:
            print(f"[narrator] LLM call failed for stage '{stage}', using fallback line: {e}")
            text = FALLBACK_LINES[stage]
        self.recent_lines.append(text)
        self.recent_lines = self.recent_lines[-RECENT_LINES_REMEMBERED:]
        self.speak(text)