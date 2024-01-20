from assets import pygame
from assets import icon
import singleplayer
import multiplayer
import main_menu
import threading
import sys
# Initialize pygame
pygame.init()
pygame.font.init()

# Set the dimensions of the chess board
width = 1000
height = 1000

pygame.display.set_icon(icon)

# Create a window to display the chess board
screen = pygame.display.set_mode((width, height))

# Set the title of the window
pygame.display.set_caption("Nathan Chess")

phase = 1

# Run the game loop
running = True
in_main_menu = True

multiplayer_session = True

while in_main_menu:
    in_main_menu, multiplayer_session = main_menu.tick(screen)

if multiplayer_session:
    try:
        t = threading.Thread(target=multiplayer.connect, args=[])
        t.daemon = True
        t.start()
    except (KeyboardInterrupt, SystemExit):
        sys.exit()

    while running:
        screen.fill((255, 255, 255))

        # scale while maintaining aspect ratio

        running = multiplayer.tick(screen)

        pygame.display.flip()


else:

    while running:
        screen.fill((255, 255, 255))

        # scale while maintaining aspect ratio

        running = singleplayer.tick(screen)

        pygame.display.flip()
