"""Main file"""

from screens.choose_map import ChooseMap
from window import Window
from screens.online_game import OnlineGame
from screens.credits import Credits
from screens.menu import Menu
from screens.game import Game
from screens.load_game import LoadGame
from screens.shortcuts import Shortcuts
from screens.character_creation import CharacterCreation
from screens.options import Options
from screens.new_game import NewGame
from screens.introduction import Introduction
from config.screens import CHOOSE_MAP, INTRODUCTION, MENU, CREDITS, GAME, LOAD_GAME, SHORTCUTS, CHARACTER_CREATION, OPTIONS, NEW_GAME
from logger import logger

if __name__ == '__main__':
    logger.info("Create states")
    W = Window()
    STATES = {
        LOAD_GAME: LoadGame(),
        MENU: Menu(),
        GAME: Game(),
        "online_game": OnlineGame(),
        CREDITS: Credits(),
        OPTIONS: Options(),
        SHORTCUTS: Shortcuts(),
        CHARACTER_CREATION: CharacterCreation(),
        NEW_GAME: NewGame(),
        INTRODUCTION: Introduction(),
        CHOOSE_MAP: ChooseMap()
    }
    W.setup_states(STATES, MENU)
    W.main()
    W.quit()
