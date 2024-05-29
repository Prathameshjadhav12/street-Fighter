import pygame
import sys
def title_screen():
    # Initialize Pygame
    pygame.init()

    # Set up the screen
    WIDTH, HEIGHT = 1900, 950
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Street Fighter")

    bg_image = pygame.image.load("Images/Bg.jpg").convert_alpha()

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    # Fonts


    def draw_bg():
        scaled_bg = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
        screen.blit(scaled_bg, (0, 0))

    def draw_text(text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        screen.blit(text_surface, text_rect)

    def main_game():
        # Placeholder for main game logic
        pass

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Start the game on spacebar press
                    running = False
        draw_bg()
        draw_text("Street Fighter", title_font, BLACK, WIDTH // 2, HEIGHT // 4)
        draw_text("Press Space to Start", button_font, RED, WIDTH // 2, HEIGHT * 3 // 4)
        pygame.display.flip()

    # Call the main game loop
    if __name__ == "__main__":
        main_game()
