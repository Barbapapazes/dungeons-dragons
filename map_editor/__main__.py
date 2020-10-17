"""Main for the map editor"""

# pylint: disable=no-member

from window import Window

if __name__ == '__main__':
    # create the window object
    w = Window()
    w.show_start_screen()
    while True:
        w.new()
        w.run()
        w.show_go_screen()
