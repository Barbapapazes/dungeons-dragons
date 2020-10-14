from window import Window
from screens.credits import Credits
from screens.menu import Menu

if __name__ == '__main__':
    states = {'credits': Credits(), 'menu': Menu()}
    w = Window()
    w.setup_states(states, 'credits')
    w.main()
    w.quit()
