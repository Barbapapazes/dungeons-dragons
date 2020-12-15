"""Main file"""

from config.screens import (CHARACTER_CREATION, CHOOSE_MAP, CREDITS, GAME,
                            INTRODUCTION, LOAD_GAME, MENU, NEW_GAME,
                            ONLINE_GAME, OPTIONS, SHORTCUTS)
from logger import logger
from screens.character_creation import CharacterCreation
from screens.choose_map import ChooseMap
from screens.credits import Credits
from screens.game import Game
from screens.introduction import Introduction
from screens.load_game import LoadGame
from screens.menu import Menu
from screens.new_game import NewGame
from screens.online_game import OnlineGame
from screens.options import Options
from screens.shortcuts import Shortcuts
from window import Window
from config.screens import MENU, CREDITS, GAME, LOAD_GAME, SHORTCUTS, CHARACTER_CREATION, OPTIONS, NEW_GAME
from screens.options_music import Options_music
from config.screens import MENU, CREDITS, GAME, LOAD_GAME, SHORTCUTS, CHARACTER_CREATION, OPTIONS, NEW_GAME,OPTIONS_MUSIC
from logger import logger

if __name__ == '__main__':
    logger.info("Create states")
    W = Window()
    STATES = {
        LOAD_GAME: LoadGame(),
        MENU: Menu(),
        GAME: Game(),
        ONLINE_GAME: OnlineGame(),
        CREDITS: Credits(),
        OPTIONS: Options(),
        SHORTCUTS: Shortcuts(),
        CHARACTER_CREATION: CharacterCreation(),
        NEW_GAME: NewGame(),
        INTRODUCTION: Introduction(),
        CHOOSE_MAP: ChooseMap()
        INTRODUCTION: Introduction()
        OPTIONS_MUSIC:Options_music(),
    }
    W.setup_states(STATES, MENU)
    W.main()
    W.quit()
