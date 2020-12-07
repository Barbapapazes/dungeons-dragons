"""Main file"""

from window import Window
from screens.credits import Credits
from screens.menu import Menu
from screens.game import Game
from screens.load_game import LoadGame
from screens.shortcuts import Shortcuts
from screens.character_creation import CharacterCreation
from screens.options import Options
from config.screens import MENU, CREDITS, GAME, LOAD_GAME, SHORTCUTS, CHARACTER_CREATION, OPTIONS
from logger import logger

if __name__ == '__main__':
    logger.info("Create states")
    W = Window()
    STATES = {
        LOAD_GAME: LoadGame(),
        MENU: Menu(),
        GAME: Game(),
        CREDITS: Credits(),
        OPTIONS: Options(),
        SHORTCUTS: Shortcuts(),
        CHARACTER_CREATION: CharacterCreation(),
    }
    W.setup_states(STATES, MENU)
    W.main()
    W.quit()
