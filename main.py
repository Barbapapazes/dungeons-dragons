"""Main file"""

from window import Window
from screens.credits import Credits
from screens.menu import Menu
from screens.game import Game
from screens.load_game import LoadGame
from config.screens import MENU, CREDITS, GAME, LOAD_GAME
from logger import logger

if __name__ == '__main__':
    logger.info("Create states")
    STATES = {
        LOAD_GAME: LoadGame(),
        MENU: Menu(),
        GAME: Game(),
        CREDITS: Credits(),
    }
    W = Window()
    W.setup_states(STATES, LOAD_GAME)
    W.main()
    W.quit()
