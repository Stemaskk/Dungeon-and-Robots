# Dungeons and Robots

The player enters a dungeon guarded by the evil robot Gretchen. The game starts with a hand gesture, after which Gretchen narrates the story through the computer speakers along with background music. Throughout the game, the narrator (using a LLM) comments on each stage and the player's actions.

The player first challenges Gretchen in a Rock–Paper–Scissors game using hand gesture recognition. Winning unlocks the final boss battle, while losing results in an immediate game over.

In the boss fight, the player and Gretchen take turns rolling colored dice to deal damage until one side loses all life points. Each color of the dice represents certain damage points. Defeating Gretchen reveals the treasure if the player wins, otherwise, the game ends.

The project utilizes computer vision, dynamic gesture recognition, game logic, and human/robot interaction.

## Layout

```
main.py                    entry point — wires the pieces together and runs the game
requirements.txt           Python dependencies
src/
  orchestrator.py          game state machine
  game_logic.py            RPS resolution, dice damage, life points
  narrator.py              LLM narration (OpenAI) + TTS playback
  gesture.py               hand gesture recognition (start signal + RPS)
  dice_vision.py           colored dice detection via camera
  robot_head.py            Gretchen's pan/tilt reactions
  audio_manager.py         speaker playback + music/TTS switching
  gesture_model/
    gesture_recognizer.task   MediaPipe gesture model
  audio/sounds/            background music and sound effects (.mp3)
tests/                     test suite
```

## Requirements

**Hardware** — this game drives a physical [Gretchen](https://teaching.csap.snu.ac.kr/) robot:

- A Gretchen robot connected over USB serial. The port is currently hardcoded in `main.py` as `/dev/tty.usbserial-FT94EP38` — update this to match your machine (`ls /dev/tty.usbserial-*` on macOS).
- The robot's onboard camera (used for both gesture and dice detection).
- Speakers for narration and music.

**Software**

- Python 3.14 (the version this project is developed against).
- macOS: install SDL2 first — `pygame` has no prebuilt wheel for recent Python versions and needs it to compile from source:

  ```
  brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
  ```

- Access to the SNU teaching GitLab, since `requirements.txt` pulls the `gretchen` robot library directly from it:

  ```
  git+https://teaching.csap.snu.ac.kr/.../gretchen.git
  ```

  Make sure your git credentials for `teaching.csap.snu.ac.kr` are set up before installing, or the `pip install` will fail on that line.

## Setup

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The narrator needs an OpenAI API key (it uses the `gpt-5.4-nano` model plus `pyttsx3` for text-to-speech). Set it before running:

```
export OPENAI_API_KEY=...
```

or put it in a `.env` file in the project root — `.env` is gitignored:

```
OPENAI_API_KEY=...
```

## Running the game

With the robot plugged in and the virtual environment active:

```
python main.py
```

The game waits for the start hand gesture, then runs through Rock–Paper–Scissors and (on a win) the boss fight.

To skip straight to the boss fight while developing, use:

```
python main.py --boss-fight
```

## Tests

```
pytest
```
