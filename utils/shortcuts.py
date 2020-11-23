import pygame as pg


def key_for(keys, event):
    """Check if keys are pressed

        Args:
            keys (List) : [ctrl, alt, key]
            event (Event)

    Returns:
        Boolean
        """
    mods = pg.key.get_mods()
    if (not keys[0] and not keys[1]) and event.key == keys[2]:
        print("save a game 0")

    if keys[0] and mods & pg.KMOD_CTRL and event.key == keys[2]:
        print("save a game 1 ")

    if keys[1] and mods & pg.KMOD_ALT and event.key == keys[2]:
        print("save a game 2")
    if (keys[0] and mods & pg.KMOD_CTRL) and (keys[1] and mods & pg.KMOD_ALT) and event.key == keys[2]:
        print("save a game 3")

    print(keys, event)
    return 0
