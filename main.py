"""Main file"""

from window import Window
from screens.credits import Credits
from screens.menu import Menu
from screens.game import Game
from config.screens import *

if __name__ == '__main__':
    STATES = {CREDITS: Credits(), MENU: Menu(), GAME: Game()}
    W = Window()
    W.setup_states(STATES, MENU)
    W.main()
    W.quit()
