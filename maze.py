import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BLOCK_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player class
class Player:
    def __init__(self):
        self.x = 1
        self.y = 1

    def move(self, dx, dy):
        if maze[self.y + dy][self.x + dx] != "#":
            self.x += dx
            self.y += dy

    def draw(self, surface):
        r = pygame.Rect((self.x * BLOCK_SIZE, self.y * BLOCK_SIZE), (BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(surface, GREEN, r)

# Whistle class
class Whistle:
    def __init__(self):
        self.x = random.randint(1, GRID_WIDTH - 2)
        self.y = random.randint(1, GRID_HEIGHT - 2)
        self.color = BLUE

    def draw(self, surface):
        r = pygame.Rect((self.x * BLOCK_SIZE, self.y * BLOCK_SIZE), (BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(surface, self.color, r)

# Finish line class
class FinishLine:
    def __init__(self):
        self.x = GRID_WIDTH - 2
        self.y = GRID_HEIGHT - 2
        self.color = RED

    def draw(self, surface):
        r = pygame.Rect((self.x * BLOCK_SIZE, self.y * BLOCK_SIZE), (BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(surface, self.color, r)

def generate_random_map():
    maze = [["#" for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    def recursive_backtracking(x, y):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + 2 * dx, y + 2 * dy
            if 1 <= nx < GRID_WIDTH - 1 and 1 <= ny < GRID_HEIGHT - 1 and maze[ny][nx] == "#":
                maze[y + dy][x + dx] = " "
                maze[ny][nx] = " "
                recursive_backtracking(nx, ny)

    recursive_backtracking(1, 1)
    return maze


def main():
    # Generate random map
    global maze
    maze = generate_random_map()

    # Initialize
    clock = pygame.time.Clock()
    player = Player()
    whistle = Whistle()
    finish_line = FinishLine()

    # Dictionary to keep track of keys being held down
    keys_down = {pygame.K_w: False, pygame.K_a: False, pygame.K_s: False, pygame.K_d: False}

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in keys_down:
                    keys_down[event.key] = True
            elif event.type == pygame.KEYUP:
                if event.key in keys_down:
                    keys_down[event.key] = False

        # Move the player based on keys being held down
        dx, dy = 0, 0
        if keys_down[pygame.K_w]:
            dy = -1
        elif keys_down[pygame.K_s]:
            dy = 1
        if keys_down[pygame.K_a]:
            dx = -1
        elif keys_down[pygame.K_d]:
            dx = 1
        player.move(dx, dy)

        # Check if player collects the whistle
        if player.x == whistle.x and player.y == whistle.y:
            whistle.x = random.randint(1, GRID_WIDTH - 2)
            whistle.y = random.randint(1, GRID_HEIGHT - 2)

        # Draw the maze
        screen.fill(BLACK)
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                if maze[y][x] == "#":
                    r = pygame.Rect((x * BLOCK_SIZE, y * BLOCK_SIZE), (BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, WHITE, r)

        # Draw the finish line
        finish_line.draw(screen)

        # Draw the whistle
        whistle.draw(screen)

        # Draw the player
        player.draw(screen)

        pygame.display.update()
        clock.tick(10)

if __name__ == "__main__":
    main()
