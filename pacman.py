import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man Style Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Cell size for the grid
CELL_SIZE = 40
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# Define the maze layout
# 0 = empty space, 1 = wall, 2 = dot, 3 = power pellet
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1],
    [1, 3, 1, 0, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 0, 1, 3, 1],
    [1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 2, 1, 1, 0, 0, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 2, 1, 1, 0, 0, 0, 0, 1, 1, 2, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 2, 1, 1, 0, 0, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 2, 1, 1, 0, 0, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 2, 1, 1, 0, 0, 0, 0, 1, 1, 2, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1],
    [1, 3, 2, 2, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 2, 2, 3, 1],
    [1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE - 10, CELL_SIZE - 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (CELL_SIZE // 2 - 5, CELL_SIZE // 2 - 5), CELL_SIZE // 2 - 5)
        self.rect = self.image.get_rect()
        self.rect.x = 10 * CELL_SIZE + 5
        self.rect.y = 15 * CELL_SIZE + 5
        self.speed = 4
        self.direction = None
        self.next_direction = None
        self.grid_pos = [15, 10]
        self.target_pos = [15 * CELL_SIZE + 5, 10 * CELL_SIZE + 5]
        self.moving = False
        self.power_mode = False
        self.power_timer = 0

    def can_move(self, direction):
        x, y = self.grid_pos
        if direction == "UP":
            return y > 0 and maze[y-1][x] != 1
        elif direction == "DOWN":
            return y < GRID_HEIGHT - 1 and maze[y+1][x] != 1
        elif direction == "LEFT":
            return x > 0 and maze[y][x-1] != 1
        elif direction == "RIGHT":
            return x < GRID_WIDTH - 1 and maze[y][x+1] != 1
        return False

    def update(self):
        # Check if we've reached the target position
        if self.rect.x == self.target_pos[0] and self.rect.y == self.target_pos[1]:
            self.moving = False
            
            # Try to change direction if requested
            if self.next_direction and self.can_move(self.next_direction):
                self.direction = self.next_direction
                self.next_direction = None
                self.moving = True
                
                # Update grid position based on direction
                if self.direction == "UP":
                    self.grid_pos[1] -= 1
                elif self.direction == "DOWN":
                    self.grid_pos[1] += 1
                elif self.direction == "LEFT":
                    self.grid_pos[0] -= 1
                elif self.direction == "RIGHT":
                    self.grid_pos[0] += 1
                
                # Set new target position
                self.target_pos = [self.grid_pos[0] * CELL_SIZE + 5, self.grid_pos[1] * CELL_SIZE + 5]
            
            # Continue in same direction if possible
            elif self.direction and self.can_move(self.direction):
                self.moving = True
                
                # Update grid position based on direction
                if self.direction == "UP":
                    self.grid_pos[1] -= 1
                elif self.direction == "DOWN":
                    self.grid_pos[1] += 1
                elif self.direction == "LEFT":
                    self.grid_pos[0] -= 1
                elif self.direction == "RIGHT":
                    self.grid_pos[0] += 1
                
                # Set new target position
                self.target_pos = [self.grid_pos[0] * CELL_SIZE + 5, self.grid_pos[1] * CELL_SIZE + 5]
        
        # Move towards target position
        if self.moving:
            if self.rect.x < self.target_pos[0]:
                self.rect.x += min(self.speed, self.target_pos[0] - self.rect.x)
            elif self.rect.x > self.target_pos[0]:
                self.rect.x -= min(self.speed, self.rect.x - self.target_pos[0])
            
            if self.rect.y < self.target_pos[1]:
                self.rect.y += min(self.speed, self.target_pos[1] - self.rect.y)
            elif self.rect.y > self.target_pos[1]:
                self.rect.y -= min(self.speed, self.rect.y - self.target_pos[1])
        
        # Handle power mode timer
        if self.power_mode:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.power_mode = False
                for ghost in ghosts:
                    ghost.frightened = False

# Ghost class
class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.normal_image = pygame.Surface((CELL_SIZE - 10, CELL_SIZE - 10), pygame.SRCALPHA)
        pygame.draw.circle(self.normal_image, color, (CELL_SIZE // 2 - 5, CELL_SIZE // 2 - 5), CELL_SIZE // 2 - 5)
        
        self.frightened_image = pygame.Surface((CELL_SIZE - 10, CELL_SIZE - 10), pygame.SRCALPHA)
        pygame.draw.circle(self.frightened_image, BLUE, (CELL_SIZE // 2 - 5, CELL_SIZE // 2 - 5), CELL_SIZE // 2 - 5)
        
        self.image = self.normal_image
        self.rect = self.image.get_rect()
        self.rect.x = x * CELL_SIZE + 5
        self.rect.y = y * CELL_SIZE + 5
        self.speed = 3
        self.grid_pos = [x, y]
        self.target_pos = [x * CELL_SIZE + 5, y * CELL_SIZE + 5]
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.frightened = False
        
    def can_move(self, direction):
        x, y = self.grid_pos
        if direction == "UP":
            return y > 0 and maze[y-1][x] != 1
        elif direction == "DOWN":
            return y < GRID_HEIGHT - 1 and maze[y+1][x] != 1
        elif direction == "LEFT":
            return x > 0 and maze[y][x-1] != 1
        elif direction == "RIGHT":
            return x < GRID_WIDTH - 1 and maze[y][x+1] != 1
        return False
        
    def update(self):
        # Update image based on frightened state
        self.image = self.frightened_image if self.frightened else self.normal_image
        
        # Check if we've reached the target position
        if self.rect.x == self.target_pos[0] and self.rect.y == self.target_pos[1]:
            # Choose a new direction
            possible_directions = []
            for direction in ["UP", "DOWN", "LEFT", "RIGHT"]:
                if direction != self.get_opposite_direction() and self.can_move(direction):
                    possible_directions.append(direction)
            
            if possible_directions:
                self.direction = random.choice(possible_directions)
            else:
                # If no other direction is possible, allow reversing
                if self.can_move(self.get_opposite_direction()):
                    self.direction = self.get_opposite_direction()
            
            # Update grid position based on direction
            if self.direction == "UP" and self.can_move("UP"):
                self.grid_pos[1] -= 1
            elif self.direction == "DOWN" and self.can_move("DOWN"):
                self.grid_pos[1] += 1
            elif self.direction == "LEFT" and self.can_move("LEFT"):
                self.grid_pos[0] -= 1
            elif self.direction == "RIGHT" and self.can_move("RIGHT"):
                self.grid_pos[0] += 1
            
            # Set new target position
            self.target_pos = [self.grid_pos[0] * CELL_SIZE + 5, self.grid_pos[1] * CELL_SIZE + 5]
        
        # Move towards target position
        if self.rect.x < self.target_pos[0]:
            self.rect.x += min(self.speed, self.target_pos[0] - self.rect.x)
        elif self.rect.x > self.target_pos[0]:
            self.rect.x -= min(self.speed, self.rect.x - self.target_pos[0])
        
        if self.rect.y < self.target_pos[1]:
            self.rect.y += min(self.speed, self.target_pos[1] - self.rect.y)
        elif self.rect.y > self.target_pos[1]:
            self.rect.y -= min(self.speed, self.rect.y - self.target_pos[1])
    
    def get_opposite_direction(self):
        if self.direction == "UP":
            return "DOWN"
        elif self.direction == "DOWN":
            return "UP"
        elif self.direction == "LEFT":
            return "RIGHT"
        elif self.direction == "RIGHT":
            return "LEFT"
        return None

# Dot class
class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (4, 4), 3)
        self.rect = self.image.get_rect()
        self.rect.centerx = x * CELL_SIZE + CELL_SIZE // 2
        self.rect.centery = y * CELL_SIZE + CELL_SIZE // 2

# Power Pellet class
class PowerPellet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (8, 8), 7)
        self.rect = self.image.get_rect()
        self.rect.centerx = x * CELL_SIZE + CELL_SIZE // 2
        self.rect.centery = y * CELL_SIZE + CELL_SIZE // 2
        self.animation_timer = 0

    def update(self):
        # Make power pellets blink
        self.animation_timer += 1
        if self.animation_timer > 30:
            self.animation_timer = 0
            self.image.set_alpha(255 if self.image.get_alpha() == 100 else 100)

# Create sprite groups
all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
dots = pygame.sprite.Group()
power_pellets = pygame.sprite.Group()
ghosts = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create maze elements
for y in range(len(maze)):
    for x in range(len(maze[y])):
        if maze[y][x] == 1:  # Wall
            wall = pygame.sprite.Sprite()
            wall.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
            wall.image.fill(BLUE)
            wall.rect = wall.image.get_rect()
            wall.rect.x = x * CELL_SIZE
            wall.rect.y = y * CELL_SIZE
            walls.add(wall)
            all_sprites.add(wall)
        elif maze[y][x] == 2:  # Dot
            dot = Dot(x, y)
            dots.add(dot)
            all_sprites.add(dot)
        elif maze[y][x] == 3:  # Power Pellet
            pellet = PowerPellet(x, y)
            power_pellets.add(pellet)
            all_sprites.add(pellet)

# Create ghosts
ghost_positions = [(9, 8, RED), (10, 8, PINK), (9, 9, CYAN), (10, 9, ORANGE)]
for x, y, color in ghost_positions:
    ghost = Ghost(x, y, color)
    ghosts.add(ghost)
    all_sprites.add(ghost)

# Game variables
score = 0
lives = 3
font = pygame.font.SysFont(None, 36)
game_over = False

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    # Keep the game running at the right speed
    clock.tick(60)
    
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.next_direction = "UP"
            elif event.key == pygame.K_DOWN:
                player.next_direction = "DOWN"
            elif event.key == pygame.K_LEFT:
                player.next_direction = "LEFT"
            elif event.key == pygame.K_RIGHT:
                player.next_direction = "RIGHT"
            elif event.key == pygame.K_r and game_over:
                # Reset game
                game_over = False
                score = 0
                lives = 3
                
                # Reset player
                player.rect.x = 10 * CELL_SIZE + 5
                player.rect.y = 15 * CELL_SIZE + 5
                player.grid_pos = [10, 15]
                player.target_pos = [10 * CELL_SIZE + 5, 15 * CELL_SIZE + 5]
                player.direction = None
                player.next_direction = None
                player.moving = False
                player.power_mode = False
                
                # Reset ghosts
                for i, (x, y, color) in enumerate(ghost_positions):
                    ghost = list(ghosts)[i]
                    ghost.rect.x = x * CELL_SIZE + 5
                    ghost.rect.y = y * CELL_SIZE + 5
                    ghost.grid_pos = [x, y]
                    ghost.target_pos = [x * CELL_SIZE + 5, y * CELL_SIZE + 5]
                    ghost.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
                    ghost.frightened = False
                
                # Reset dots and power pellets
                dots.empty()
                power_pellets.empty()
                
                for y in range(len(maze)):
                    for x in range(len(maze[y])):
                        if maze[y][x] == 2:  # Dot
                            dot = Dot(x, y)
                            dots.add(dot)
                            all_sprites.add(dot)
                        elif maze[y][x] == 3:  # Power Pellet
                            pellet = PowerPellet(x, y)
                            power_pellets.add(pellet)
                            all_sprites.add(pellet)
    
    if not game_over:
        # Update
        player.update()
        ghosts.update()
        power_pellets.update()
        
        # Check for dot collisions
        dot_collisions = pygame.sprite.spritecollide(player, dots, True)
        for dot in dot_collisions:
            score += 10
        
        # Check for power pellet collisions
        pellet_collisions = pygame.sprite.spritecollide(player, power_pellets, True)
        for pellet in pellet_collisions:
            score += 50
            player.power_mode = True
            player.power_timer = 300  # 5 seconds at 60 FPS
            for ghost in ghosts:
                ghost.frightened = True
        
        # Check for ghost collisions
        ghost_collisions = pygame.sprite.spritecollide(player, ghosts, False)
        for ghost in ghost_collisions:
            if player.power_mode and ghost.frightened:
                # Reset ghost position
                x, y, _ = ghost_positions[list(ghosts).index(ghost)]
                ghost.rect.x = x * CELL_SIZE + 5
                ghost.rect.y = y * CELL_SIZE + 5
                ghost.grid_pos = [x, y]
                ghost.target_pos = [x * CELL_SIZE + 5, y * CELL_SIZE + 5]
                score += 200
            else:
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    # Reset player position
                    player.rect.x = 10 * CELL_SIZE + 5
                    player.rect.y = 15 * CELL_SIZE + 5
                    player.grid_pos = [10, 15]
                    player.target_pos = [10 * CELL_SIZE + 5, 15 * CELL_SIZE + 5]
                    player.direction = None
                    player.next_direction = None
                    player.moving = False
                    
                    # Reset ghost positions
                    for i, (x, y, color) in enumerate(ghost_positions):
                        ghost = list(ghosts)[i]
                        ghost.rect.x = x * CELL_SIZE + 5
                        ghost.rect.y = y * CELL_SIZE + 5
                        ghost.grid_pos = [x, y]
                        ghost.target_pos = [x * CELL_SIZE + 5, y * CELL_SIZE + 5]
        
        # Check if all dots and pellets are collected
        if len(dots) == 0 and len(power_pellets) == 0:
            game_over = True
    
    # Draw
    screen.fill(BLACK)
    
    # Draw sprites
    walls.draw(screen)
    dots.draw(screen)
    power_pellets.draw(screen)
    ghosts.draw(screen)
    screen.blit(player.image, player.rect)
    
    # Draw score and lives
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))
    
    # Draw game over message
    if game_over:
        if len(dots) == 0 and len(power_pellets) == 0:
            game_over_text = font.render("YOU WIN! - Press R to Restart", True, WHITE)
        else:
            game_over_text = font.render("GAME OVER - Press R to Restart", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2))
    
    # Flip the display
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()
