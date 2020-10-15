"""Main file"""

from window import Window
from screens.credits import Credits
from screens.menu import Menu
from screens.game import Game

if __name__ == '__main__':
    STATES = {'credits': Credits(), 'menu': Menu(), 'game': Game()}
    W = Window()
    W.setup_states(STATES, 'credits')
    W.main()
    W.quit()
