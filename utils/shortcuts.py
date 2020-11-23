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
    return ((not keys[0] and not keys[1]) and event.key == keys[2]) or(keys[0] and mods & pg.KMOD_CTRL and event.key == keys[2]) or (keys[1] and mods & pg.KMOD_ALT and event.key == keys[2]) or ((keys[0] and mods & pg.KMOD_CTRL) and (keys[1] and mods & pg.KMOD_ALT) and event.key == keys[2])
