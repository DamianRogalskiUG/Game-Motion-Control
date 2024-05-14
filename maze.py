import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BLOCK_SIZE = 40
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Maze layout
maze = [
    "#######################",
    "#                     #",
    "# ##### ##### ##### ###",
    "#     #     #     #   #",
    "# ### # ### # ### ### #",
    "#   #   # # #   # #   #",
    "### ##### # ### # ### #",
    "#       #   #   #     #",
    "### ### ### # ### # ###",
    "#   # #     # #     # #",
    "# ### # ##### # ### # #",
    "#     #       #     # #",
    "### # ### ### # ### # #",
    "#   # #   #   #   #   #",
    "# ### ### # ### # #####",
    "# #     # #     #     #",
    "# # ### # ######### ###",
    "# #   # #           # #",
    "# ### # ######### # # #",
    "#     #           #   #",
    "#######################"
]

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

def main():
    # Initialize
    clock = pygame.time.Clock()
    player = Player()

    # Dictionary to keep track of keys being held down
    keys_down = {pygame.K_w: False, pygame.K_a: False, pygame.K_s: False, pygame.K_d: False}

    while True:
        start_time = time.time()

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

        # Draw the maze
        screen.fill(BLACK)
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                if maze[y][x] == "#":
                    r = pygame.Rect((x * BLOCK_SIZE, y * BLOCK_SIZE), (BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, WHITE, r)

        # Draw the player
        player.draw(screen)

        pygame.display.update()
        clock.tick(4)  # Adjust the argument to change the speed (10 frames per second in this case)

        # Delay to slow down the movement
        elapsed_time = time.time() - start_time
        if elapsed_time < 0.1:
            time.sleep(0.1 - elapsed_time)

if __name__ == "__main__":
    main()
