from pathlib import Path
import time

#Importing pygame to handle music in a game setting 
import pygame

#Creating Path to sounds folder
SOUNDS_FOLDER = Path(__file__).parent / "sounds"

#Global 
is_narrator_speaking = False

#Building function to initialize audio system
def initialize_audio():
    pygame.mixer.init()

#Building function to play music
def play_music(filename, loop=False, volume=1.0):
    music_path = SOUNDS_FOLDER / filename

    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(volume)

    if loop: 
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.play()

    print(f"Playing: {music_path.name} at volume {volume}")



#Building functions to handle music

def stop_music():
    pygame.mixer.music.stop()

def pause_music():
    pygame.mixer.music.pause()

def resume_music():
    pygame.mixer.music.unpause()

def set_volume(volume):
    pygame.mixer.music.set_volume(volume)

def fade_volume(target_volume, duration=1):
    current_volume = pygame.mixer.music.get_volume()
    steps = 20
    volume_change = (target_volume - current_volume) / steps

    for _ in range(steps):
        current_volume = current_volume + volume_change
        pygame.mixer.music.set_volume(current_volume)
        time.sleep(duration / steps)


# Building function to connect audio manager to main system. 
# Allows main system to handle music based on events e.g. "narrator speaking"

def handle_event(event):
    global is_narrator_speaking

    if event == "game_started":
        play_music("Dungeon of Agony.mp3", loop=True, volume=0.7)

    elif event == "narrator_started":
        is_narrator_speaking = True
        fade_volume(0.2,duration=2)

    elif event == "narrator_finished":
        is_narrator_speaking = False
        fade_volume(0.7,duration=2)
    
    elif event == "game_won":
        stop_music()
        play_music("Victory.mp3")
    
    elif event == "game_over":
        stop_music()
        play_music("game_over_bad_chest.wav")


    

initialize_audio()


handle_event("game_started")

time.sleep(5)

handle_event("narrator_started")

time.sleep(4)

handle_event("narrator_finished")

time.sleep(5)

handle_event("game_won")

input("Press Enter to end the test...")





