# A simple 2D-game using OpenGL

## How to play the game
Use the arrow keys to move your ship and aim at your target, use the space button to hit a ball. When you hit a ball for the first time, it splits up in two. When you hit a ball the second time, it explodes. Your main goal is to erase all the balls, before one of the balls hits you. Once you shoot all the balls, you get to the next level, with more balls that move faster. There are three levels in total, if you manage to get through all of them, you win the game. If you lose a level, you go back to the first level. 

## Functionality
* <kbd>←</kbd> to move the ship left
* <kbd>↑</kbd> to move the ship up
* <kbd>→</kbd> to move the ship right
* <kbd>↓</kbd> to move the ship down
* <kbd>Space</kbd> to shoot
* <kbd>cmd</kbd> <kbd>q</kbd> to quit

## Start the game
```
python -m pip install -r requirements.txt
python -m game
```