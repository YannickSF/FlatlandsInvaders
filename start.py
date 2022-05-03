
import pygame
from src.system import Game


TITLE = "Flatland's Invaders"
DISPLAY_X = 1000
DISPLAY_Y = 900
STEP = 20

if __name__ == '__main__':

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((DISPLAY_X, DISPLAY_Y))
    pygame.display.set_caption(TITLE)

    game = Game(screen)
    game.screen.blit(game.background, (0, 0))

    game.run()
