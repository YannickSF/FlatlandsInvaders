
import pygame
from src.system import Game, GAME_VARIABLES

if __name__ == '__main__':

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((GAME_VARIABLES.DISPLAY_X, GAME_VARIABLES.DISPLAY_Y))
    pygame.display.set_caption(GAME_VARIABLES.TITLE)

    game = Game(screen)
    game.screen.blit(game.background, (0, 0))

    game.run()
