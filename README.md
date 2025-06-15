# Space Invaders
![Screenshot 2025-06-15 at 20 41 42](https://github.com/user-attachments/assets/30f005b6-0029-4f6c-851a-1e0dd0b340f4)

A recreation of the classic Space Invaders arcade game using Python and Pygame.

## Game Features

- Player ship with movement and shooting mechanics
- Alien enemies that move in formation and shoot back
- Lives system with visual indicators
- Progressive difficulty with advancing levels
- Score system with higher points for tougher enemies

## Controls

- **LEFT/RIGHT arrows**: Move your ship
- **SPACEBAR**: Shoot (with cooldown to prevent spamming)
- **R**: Restart after game over
- **N**: Advance to next level after winning

## Game Mechanics

### Player
- 3 lives with temporary invulnerability after being hit
- Controlled shooting rate to balance difficulty
- Visual feedback when damaged

### Aliens
- Move in formation and descend when reaching screen edges
- Shooting frequency increases as fewer aliens remain
- Different rows worth different point values

### Difficulty Progression
- Each level increases alien speed
- Enemy shooting frequency increases over time
- Balanced to provide a challenging but fair experience

## Requirements
- Python 3.x
- Pygame library

## Installation

1. Clone this repository
2. Install Pygame: `pip install pygame`
3. Run the game: `python space_invaders.py`

## Future Improvements
- Add sound effects and music
- Implement high score tracking
- Add more enemy types and formations
- Include boss battles and power-ups
