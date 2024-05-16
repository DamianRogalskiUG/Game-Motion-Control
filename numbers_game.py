import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Number Clicker Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font
font = pygame.font.Font(None, 100)


def generate_number():
    """Generate a random number between 1 and 4."""
    return random.randint(1, 4)


def display_number(number):
    """Display the given number at the center of the screen."""
    text_surface = font.render(str(number), True, BLACK)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_surface, text_rect)


def main():
    """Main function to run the game."""
    clock = pygame.time.Clock()
    running = True
    current_number = generate_number()
    correct_key_pressed = False
    correct_key_time = 0

    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and not correct_key_pressed:
                if event.unicode.isdigit():
                    pressed_number = int(event.unicode)
                    if pressed_number == current_number:
                        print("Correct!")
                        correct_key_pressed = True
                        correct_key_time = pygame.time.get_ticks()
                    else:
                        print("Wrong!")

        # Handle correct key press
        if correct_key_pressed:
            correct_surface = font.render("Correct!", True, BLACK)
            screen.blit(correct_surface, (SCREEN_WIDTH // 2 - correct_surface.get_width() // 2,
                                           SCREEN_HEIGHT // 2 - correct_surface.get_height() - 50))
            if pygame.time.get_ticks() - correct_key_time >= 2000:
                current_number = generate_number()
                correct_key_pressed = False

        # Display current number



        display_number(current_number)
        pygame.display.flip()

        clock.tick(30)

if __name__ == "__main__":
    main()
