import pygame
import random

# Initialize Pygame
pygame.init()

# Set screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hover Object Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Object parameters
BASE_OBJECT_SIZE = 50
MIN_OBJECT_SIZE = 20

# Function to spawn a random object on the screen
def spawn_object(score):
    # Adjust size based on score
    object_size = max(BASE_OBJECT_SIZE - score // 10 * 5, MIN_OBJECT_SIZE)
    x = random.randint(0, SCREEN_WIDTH - object_size)
    y = random.randint(0, SCREEN_HEIGHT - object_size)
    return pygame.Rect(x, y, object_size, object_size)

# Main game loop
def main():
    clock = pygame.time.Clock()
    running = True
    score = 0
    time_limit = 300  # Initial time
    time_remaining = time_limit
    object_rect = None
    time_added_on_hover = 100

    # Set up font
    font = pygame.font.Font(None, 36)

    # Game over font
    game_over_font = pygame.font.Font(None, 72)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(WHITE)

        # Draw the score
        score_text = font.render("Score: " + str(score), True, RED)
        screen.blit(score_text, (10, 10))

        # Draw the time remaining
        time_text = font.render("Time: " + str(max(round(time_remaining / 100, 1), 0)), True, RED)
        screen.blit(time_text, (10, 50))

        if time_remaining > 0 and object_rect is None:
            # Spawn the object if it's not already spawned
            object_rect = spawn_object(score)

        if object_rect:
            # Draw the object
            pygame.draw.rect(screen, RED, object_rect)

            # Check for hover
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if object_rect.collidepoint(mouse_x, mouse_y):
                score += 1
                time_remaining += time_added_on_hover  # Increase time on hover
                object_rect = None  # Reset object

        # Decrease time remaining
        time_remaining -= clock.get_rawtime()  # Use get_rawtime to ensure consistent timing

        # Increase difficulty over time
        if time_limit > 500:
            time_limit -= 500  # Decrease time limit by 5 milliseconds per frame

        # Check if time runs out
        if time_remaining <= 0:
            # Display game over message
            game_over_text = game_over_font.render("Game Over", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
            score_text = font.render("Score: " + str(score), True, RED)
            screen.blit(score_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50))

            # Draw retry option
            retry_text = font.render("Gesture to Restart", True, RED)
            screen.blit(retry_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100))

            # Check for retry input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                score = 0
                time_remaining = 300  # Reset time remaining to initial value

        # Update the display
        pygame.display.flip()

        clock.tick(60)  # Keep a consistent frame rate

    pygame.quit()

if __name__ == "__main__":
    main()
