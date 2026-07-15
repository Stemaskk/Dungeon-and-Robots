"""LLM narrator: generates Gretchen's lines and triggers TTS playback.

Exposes an "is speaking" flag so robot_head / audio can pause background music.

Owner: M
"""

import pyttsx3

class Narrator:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.is_speaking = False

    def speak(self, text):
        print(f"GretchenL {text}")
        self.is_speaking = True
        self.engine.say(text)
        self.engine.runAndWait()
        self.is_speaking = False

    # stage is one of: "intro", "rps_win", "rps_lose", "boss_win", "boss_lose"
    # canned lines for now - will swap to an OpenAI call later
    def narrate(self, stage):
        lines = {
            "intro":"",
            "rps_win": "",
            "rps_lose": "",
            "boss_win": "",
            "boss_lose":""
        }
        self.speak(lines[stage])