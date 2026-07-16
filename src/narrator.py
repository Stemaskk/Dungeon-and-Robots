"""LLM narrator: generates Gretchen's lines and triggers TTS playback.

Exposes an "is speaking" flag so robot_head / audio can pause background music.

Owner: M
"""

import pyttsx3
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

FALLBACK_LINES = {
            "waiting_for_start": "Do you wish to enter the dungeon?",
            "intro": "You enter a dark dungeon and encounter an evil Gretchen.",
            "rps_round": "Not bad... for a human.",
            "rps_win": "Evil Gretchen shakes rapidly and explodes. You step over the 3D-printed debris and creep into the corridor beyond, where a much larger, meaner-looking Gretchen awaits, next to a colorful dice.",
            "rps_lose": "Evil Gretchen starts cackling as you fall to the floor dead. The last thing you see is the red glint of Gretchen's eye.",
            "dice_round": "The dice never lie... unlike you.",
            "boss_win": "Boss Gretchen's motors whir uncontrollably as the robot starts to self-implode. Congratulations, adventurer. The treasure is yours...",
            "boss_lose": "Boss Gretchen erupts into hideous laughter, echoing throughout the dungeon. The treasure glints in the background, but it is too late. You fall to the floor dead."
        }

SYSTEM_PROMPT = (
    "You are Gretchen, an evil robot villain in a dungeon game. "
    "You are genuinely mean and threatening, with dry, cutting sarcasm — not "
    "silly, not cartoonish, not kid-friendly. Taunt the player like a real "
    "villain would, not a children's show character. "
    "Respond with exactly one or two short sentences, under 30 words total. "
    "No stage directions, no asterisks, no sound effects, no emoji, no exclamation points. "
    "Always make it immediately obvious who won or lost — no backhanded or "
    "roundabout phrasing a listener could misread in the moment."
)


STAGE_PROMPTS = {
    "intro": "Narrate the player entering a dark dungeon and encountering you, an evil Gretchen robot.",
    "rps_round": "The player just threw {player_move}, you (Gretchen) threw {gretchen_move}, and the result was: {result}. React in character to this specific round.",
    "rps_win": "Narrate Evil Gretchen exploding after losing rock-paper-scissors, and introduce a bigger, meaner Boss Gretchen waiting ahead.",
    "rps_lose": "Narrate Evil Gretchen gloating as the player is defeated.",
    "dice_round": "{roller} just rolled a {dice_color} die. Player life is now {player_life}, Gretchen life is now {gretchen_life}. React in character to this specific roll.",
    "boss_win": "Narrate Boss Gretchen self-destructing after losing the dice battle, and reveal the treasure.",
    "boss_lose": "Narrate Boss Gretchen gloating as the player is defeated, treasure just out of reach.",
}


class Narrator:
    def __init__(self):
        self.is_speaking = False
        self.client = OpenAI()

    def speak(self, text):
        print(f"Gretchen: {text}")
        self.is_speaking = True
        engine = pyttsx3.init()
        engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Trinoids')
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()
        self.is_speaking = False

    # stage is one of: "waiting_for_start", "intro", "rps_round", "rps_win", "rps_lose",
    # "dice_round", "boss_win", "boss_lose"
    def narrate(self, stage, **context):
        try:
            prompt = STAGE_PROMPTS[stage].format(**context) if context else STAGE_PROMPTS[stage]
            response = self.client.chat.completions.create(
                model = "gpt-5.4-nano",
                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
            )
            text = response.choices[0].message.content
        except Exception:
            text = FALLBACK_LINES[stage]
        self.speak(text)