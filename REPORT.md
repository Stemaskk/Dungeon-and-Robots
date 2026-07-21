# Dungeons and Robots: Human–Robot Interactive Game

## Abstract

This project presents an interactive _Dungeons & Dragons_-inspired game that combines computer vision, dynamic gesture recognition, large language model (LLM) narration, game logic, and human–robot interaction.

The game centers on two main roles:

- **Dungeon Master (DM):** Controls story progression, narration, and non-player characters. This role is assigned to Gretchen.
- **Player:** A human participant who interacts with the game world and its characters.

The player begins by entering a dungeon in a cave guarded by an evil robot named Gretchen and progresses through multiple stages of gameplay. The game starts with gesture-based interaction, which triggers narration, followed by a Rock–Paper–Scissors challenge using hand gesture recognition against Evil Gretchen. If successful, the player advances to a turn-based dice battle against Boss Gretchen.

Throughout the game, an LLM-generated voice and text provide story progression, commentary, and feedback, while background music enhances the immersive atmosphere. Robot movements are synchronized with game outcomes, allowing Gretchen to physically express approval or disapproval.

The purpose of this project is to demonstrate the integration of artificial intelligence, computer vision, and robotics to create an engaging interactive gaming experience.

---

# Introduction and Project Goals

Interactive entertainment systems increasingly combine artificial intelligence, computer vision, and robotics to create immersive user experiences. This project explores how these technologies can be integrated into an imagination-based game inspired by the tabletop role-playing game _Dungeons & Dragons_.

The game places the player in a dungeon where they must confront an evil robot guardian named Gretchen. Instead of using traditional input devices, the player interacts with the system through hand gestures. Gameplay consists of two major stages:

1. A Rock–Paper–Scissors challenge
2. A final dice-based boss battle

An AI narrator dynamically comments on the player's actions and game events, creating a more engaging and personalized experience.

## Project Goals

- Develop a gesture-controlled gaming interface using computer vision.
- Implement reliable hand gesture recognition for gameplay actions.
- Integrate an LLM-based narrator capable of generating contextual commentary.
- Develop game logic based on Dungeons & Dragons mechanics.
- Design a turn-based game system with multiple possible outcomes.
- Create semi-expressive robot behaviors that respond to game events.
- Demonstrate effective human–robot interaction within an entertainment application.

---

# Technologies Used

The project uses various technologies.

## Computer Vision

Computer vision is used to detect and interpret the player's hand gestures and dice colors through a webcam.

The game begins with a recognizable hand signal, and during the first stage, image frames are processed in real time to identify gestures corresponding to Rock, Paper, and Scissors. For the boss fight, computer vision is used to detect colored squares representing red, green, and blue.

## Dynamic Gesture Recognition

Gesture recognition algorithms classify hand poses and movements into predefined game commands. This allows players to participate in the Rock–Paper–Scissors challenge without using a keyboard or controller.

## Large Language Model (LLM)

An LLM is used as the game narrator. Based on the current game state and player actions, the model generates contextual dialogue, story progression, and reactions.

This creates a storytelling experience that changes with gameplay outcomes and is different in each round.

## Text-to-Speech (TTS)

The narrator's generated text is converted into speech and played through computer speakers. This provides an audio experience that allows players to receive feedback without reading text on the screen.

## Audio

Various types of music are played to immerse the player while adapting to the game context and helping create atmosphere.

## Robot Control and Human–Robot Interaction

The robot Gretchen acts as both the narrator and a physical game character.

Robot motion commands are triggered by game events. Examples include:

- Nodding to indicate victory
- Shaking its head to indicate defeat

These behaviors help bring Gretchen into the game as a physical presence rather than leaving it as only software.

## Game Logic

A custom game engine manages:

- Game states
- Player health
- Enemy health
- Turn order
- Dice rolls
- Victory conditions
- Progression through different stages

---

# Implementation

The game follows a sequential structure with several stages:

1. A person signals Gretchen to start the game.
2. Gretchen introduces the story through narrated dialogue, beginning with the player entering a dungeon.
3. A Rock–Paper–Scissors match between Evil Gretchen and the player determines whether the player may proceed.
4. If successful, the player enters the final boss battle.
5. If unsuccessful, the player dies and the game resets.
6. During the boss battle, the player and Gretchen take turns dealing damage.
7. The game ends when either side's health reaches zero.
8. Gretchen performs a victory or defeat sequence based on the outcome.

## Beginning Stage

The player begins the game by holding up an open palm to start the interaction.

## Rock–Paper–Scissors Stage

The first challenge uses computer vision to recognize the player's hand gesture.

The recognized gesture is compared against Gretchen's selected move according to standard Rock–Paper–Scissors rules.

### Possible Outcomes

- **Win:** Advance to the boss battle.
- **Lose:** Immediate game over.
- **Tie:** Repeat the round or continue according to the game rules.

## Boss Battle System

The boss battle is implemented as a turn-based combat system.

Each participant starts with a predefined amount of health points. During each turn, a colored die is rolled. Each color corresponds to a specific damage value.

### Dice Outcomes

| Dice Color | Damage            |
| ---------- | ----------------- |
| Red        | High Damage (-2)  |
| Green      | Low Damage (-1)   |
| Blue       | Critical Miss (0) |

For Gretchen, a random number generator determines the damage dealt to the player each round, ranging from 0 to 2 damage.

The damage is deducted from the opponent's health, and the battle continues until one participant's health reaches zero.

## Narration System

The narration system continuously receives information about the current game state, including:

- Stage progression
- Dice outcomes
- Health values
- Victory or defeat events
- Player actions

The LLM generates contextual responses that are converted into speech using a text-to-speech system. This allows the narrator to react dynamically rather than relying only on scripted dialogue.

## Robot Behavior Control

Robot actions are linked directly to game outcomes.

Examples include:

- Shaking its head in defeat when the player wins
- Celebrating when the player is defeated

These behaviors are triggered through the game controller and executed by the robot in real time.

---

# Discussion: Challenges

## Maryam Al-Farooq

I primarily worked on the game logic, the LLM prompts and TTS, and tying all the components together. Overall, I found the most difficult part of this was prompt engineering the LLM. This is because initially I didn't provide it with enough information (e.g. life points, whose move it is, past history). This led to the LLM hallucinating moves and trying to do its own calculations, and I thought there was a problem with the game logic itself rather than a hallucination. This took some time to figure out, but I solved it by adding a lot more detail to the prompts. Another challenge stemmed from the relatively short project timeline and small scope of the project, meaning we didn't agree on an interface before starting to code. This caused some type mismatches, particularly with `Move` and `gesture.py`. We fixed this by casting - not the best solution but it works.

### A

### T

I worked on the Audio Manager and the robot head movements.

For the audio, I implemented the background music, sound effects for winning and losing, and a simple event-based system to control playback. I also added volume fading so the background music is reduced while the LLM narrator is speaking and restored afterwards.

For the robot, I created the head animations used during the game. Gretchen shakes its head when the player wins and nods when the player loses. The movement speed, angle, and number of repetitions can all be adjusted easily.

The biggest challenge was making the robot's movements look natural. After some testing, I found that moving the head back to the center between left and right movements made the animation much smoother. Another challenge was keeping the code modular so the audio and robot behavior could be triggered independently from the main game logic.

### Lilla Megyeri 

My main coding work focused on dice color detection and the game logic. I faced several challenges while developing this part of the project. One of the first issues was detecting the color red. After some research, I learned that red falls into two separate ranges in the color space, so I needed to create two different masks and combine them. Another challenge was getting Gretchen to recognize when an object was actually a square. I was able to detect quadrilaterals with roughly equal sides, but not always true squares, which sometimes caused random background objects to be detected instead. I also had trouble with the color ranges being too broad. Since red is such a common color, I initially used a wide range to account for different lighting conditions, but that caused the system to detect too many unrelated objects. I solved this by narrowing the range and testing different shades of red until I found a more reliable setting.After that came the turn-based game logic. That part was relatively simple, but I still had to determine how to convert each detected color into a numerical value for damage.

The most challenging and interesting part, however, was gameplay timing. At first, once Gretchen started running, the game would end almost immediately because it kept detecting colors and applying damage too quickly. I needed to slow the process down, so I added a sleep function. However, that still did not fully solve the problem because the system could continue detecting random background objects instead of the actual dice. I was also concerned that during gameplay I might not have enough time to show the correct dice color, or that the delay between rolls would become too long. To address this, I briefly considered using an input function where I would press Enter each time I wanted the system to detect a color. While this worked, it made the camera less visible and the game feel less automatic. After getting some advice, I created a stability count instead. This required the system to detect the same color consistently for a certain number of frames before confirming it as a valid detection. This helped reduce background noise and ensured the dice color was clearly visible before it was accepted. It also allowed me to keep the camera view active so I could verify that I was showing the correct color.

---

# Conclusion

This project demonstrates how computer vision, artificial intelligence, and robotics can be combined to create a fun and interactive gaming experience.

By using gesture-based controls, dynamic storytelling, and expressive robot behavior, the system offers a more engaging form of human–robot interaction than a traditional game interface.

The project also highlights the potential of combining multiple AI technologies in entertainment and educational settings.

With further development, the game could be expanded with:

- Additional stages
- More advanced robot animations
- A larger set of gestures
- Difficulty adjustments based on player performance

Overall, the project successfully created an immersive dungeon adventure where players can interact naturally with an intelligent robotic opponent through vision-based controls and AI-driven storytelling.
