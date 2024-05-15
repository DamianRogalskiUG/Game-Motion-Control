import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000
BLOCK_SIZE = 40
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

# Define multiple maps
maps = [
    [
        "#######################",
        "#                     #",
        "# ##### ##### ##### ###",
        "#    .#     #     #   #",
        "# ### # ### # ### ### #",
        "#   #   # # #   # #   #",
        "### ##### # ### # ### #",
        "#    .  #   #   #    .#",
        "### ### ### # ### # ###",
        "#   # #    .# #     # #",
        "# ### # ##### # ### # #",
        "#     #       #     # #",
        "### # ### ### # ### # #",
        "#   # #   #   #   #   #",
        "# ### ### # ### # #####",
        "# #     # #     #     #",
        "# # ### # ######### ###",
        "# #   # #           # #",
        "# ### # ######### # # #",
        "#F    #           #   #",
        "#######################"
    ],
    [
        "#######################",
        "#                     #",
        "#  .### #   #   #     #",
        "# #   # # ### # ### ###",
        "# # # # #     # #     #",
        "# # # # ##### # ##### #",
        "# # # #     # #     # #",
        "# # # ##### # ##### # #",
        "# # #     # # #     # #",
        "# # ##### # # # ##### #",
        "# #       # # #       #",
        "# ######### # #########",
        "#           #         #",
        "### ##### ### ##### ###",
        "#     #         #     #",
        "# ### ##### ### ##### #",
        "# #   #     #       # #",
        "# # # ##### ##### # # #",
        "#   #             #   #",
        "##### ########### #####",
        "#######################"
    ],
    [
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
        "#F    #           #   #",
        "#######################"
    ]
]

# Player class
class Player:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.points = 0

    def move(self, dx, dy):
        if maps[current_map][self.y + dy][self.x + dx] != "#":
            self.x += dx
            self.y += dy
            if maps[current_map][self.y][self.x] == "F":  # Check if player reaches finish line
                print("Congratulations! You reached the finish line!")
                pygame.quit()
                sys.exit()
            elif maps[current_map][self.y][self.x] == ".":  # Check if player collects a point
                self.points += 1
                maps[current_map][self.y] = maps[current_map][self.y][:self.x] + " " + maps[current_map][self.y][self.x+1:]

    def draw(self, surface):
        r = pygame.Rect((self.x * BLOCK_SIZE, self.y * BLOCK_SIZE), (BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(surface, GREEN, r)

# Draw points on the screen
def draw_points(surface):
    for y in range(len(maps[current_map])):
        for x in range(len(maps[current_map][y])):
            if maps[current_map][y][x] == ".":
                point = pygame.Rect((x * BLOCK_SIZE + BLOCK_SIZE // 3, y * BLOCK_SIZE + BLOCK_SIZE // 3),
                                    (BLOCK_SIZE // 3, BLOCK_SIZE // 3))
                pygame.draw.rect(surface, BLUE, point)

def display_notification(surface, text):
    font = pygame.font.Font(None, 36)
    notification = font.render(text, True, WHITE)
    surface.blit(notification, ((SCREEN_WIDTH - notification.get_width()) // 2, 50))

def display_menu(surface):
    font = pygame.font.Font(None, 72)
    text1 = font.render("Select Map:", True, WHITE)
    text2 = font.render("Press 1, 2, or 3", True, WHITE)
    surface.blit(text1, ((SCREEN_WIDTH - text1.get_width()) // 2, 300))
    surface.blit(text2, ((SCREEN_WIDTH - text2.get_width()) // 2, 400))

def main():
    global current_map
    current_map = 0  # Start with the first map
    menu_displayed = True

    # Initialize
    clock = pygame.time.Clock()
    player = Player()
    notification_timer = 0
    notification_text = ""

    # Dictionary to keep track of keys being held down
    keys_down = {pygame.K_w: False, pygame.K_a: False, pygame.K_s: False, pygame.K_d: False}

    while True:
        start_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if menu_displayed:
                    if event.key == pygame.K_1:
                        current_map = 0
                        menu_displayed = False
                    elif event.key == pygame.K_2:
                        current_map = 1
                        menu_displayed = False
                    elif event.key == pygame.K_3:
                        current_map = 2
                        menu_displayed = False
                else:
                    if event.key in keys_down:
                        keys_down[event.key] = True
            elif event.type == pygame.KEYUP:
                if event.key in keys_down:
                    keys_down[event.key] = False

        if menu_displayed:
            display_menu(screen)
            pygame.display.update()
            continue

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
        for y in range(len(maps[current_map])):
            for x in range(len(maps[current_map][y])):
                if maps[current_map][y][x] == "#":
                    r = pygame.Rect((x * BLOCK_SIZE, y * BLOCK_SIZE), (BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, WHITE, r)
                elif maps[current_map][y][x] == "F":  # Draw finish line
                    r = pygame.Rect((x * BLOCK_SIZE, y * BLOCK_SIZE), (BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, RED, r)

        # Draw points
        draw_points(screen)

        # Draw the player
        player.draw(screen)

        # Display points counter
        font = pygame.font.Font(None, 36)
        text = font.render(f"Points: {player.points}", True, WHITE)
        screen.blit(text, (10, 10))

        # Display notification if there is one
        if time.time() - notification_timer < 1:
            display_notification(screen, notification_text)

        pygame.display.update()
        clock.tick(4)  # Adjust the argument to change the speed (10 frames per second in this case)

        # Delay to slow down the movement
        elapsed_time = time.time() - start_time
        if elapsed_time < 0.1:
            time.sleep(0.1 - elapsed_time)

if __name__ == "__main__":
    main()