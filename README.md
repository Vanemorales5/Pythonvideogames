# Pythonvideogames
HAMSTER HEROS- Comp61 extra credit
# Hamster Heroes

## Setup
1. Make sure you have Python 3.x installed
2. Install Pygame: `pip install pygame`
3. Download the code and assets from this repository
4. Run the game: `python hamster_heroes.py`

## Game Overview

### Game Title: Hamster Heroes

### Game Summary
Hamster Heroes is an arcade-style game where you control a brave hamster defending its home from a barrage of falling seeds. Armed with carrots to throw, your mission is to prevent the seeds from reaching the bottom of the screen while collecting sunflowers for bonus points. As time progresses, the game gets more challenging with faster-falling seeds and more obstacles. Can you protect your hamster's home and become a true Hamster Hero?

### Core Gameplay Loop
Move your hamster left and right at the bottom of the screen while throwing carrots at falling seeds. Score points by hitting seeds with carrots and collecting sunflowers. Avoid letting seeds reach the bottom or hit your hamster. The game's difficulty increases over time, creating an engaging challenge that requires quick reflexes and strategy.

## Gameplay Mechanics

### Controls
- **Left Arrow Key**: Move hamster left
- **Right Arrow Key**: Move hamster right
- **Space Bar**: Throw carrot
- **Escape Key**: Return to main menu
- **Mouse**: Navigate menus

### Core Mechanics
- **Throwing Carrots**: Launch carrots upward to hit falling seeds
- **Dodging Seeds**: Move left and right to avoid being hit by seeds
- **Collecting Sunflowers**: Grab sunflowers for bonus points
- **Increasing Difficulty**: Seeds fall faster as levels progress

### Level Progression
The game automatically advances to higher levels every 30 seconds of gameplay. With each new level, seeds fall faster, increasing the challenge. Your current level is displayed on the screen during gameplay.

### Win/Loss Conditions
- **Win**: Reach 1000 points
- **Lose**: A seed reaches the bottom of the screen or hits your hamster

## Story and Narrative
You play as a heroic hamster who has been tasked with defending your underground home from a barrage of seeds falling from above. If too many seeds pile up, your home will be buried and your family will be unable to access their food stores. Armed with an endless supply of carrots, you must knock away the falling seeds while collecting magical sunflowers that grant you special powers (points).

## Features
- Animated hamster character
- Multiple enemies (seeds) with varying speeds
- Projectile system (carrots)
- Collectible power-ups (sunflowers)
- Scoring system
- Level progression
- Sound effects and background music
- Complete menu system with splash screen
- Instructions screen
- Game over and win conditions

## Game Assets
The game is designed to work with the following assets (which you'll need to provide):
- hamster.png (and hamster_frame1.png through hamster_frame4.png for animation)
- seed.png
- carrot.png
- sunflower.png
- background.jpg

Note: The game includes fallback graphics using simple shapes if the image files are not found.
