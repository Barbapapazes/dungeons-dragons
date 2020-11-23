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
    key = bool(not mods & pg.KMOD_ALT and not keys[1] and not mods &
               pg.KMOD_CTRL and not keys[0] and event.key == keys[2])
    ctrl = bool(not mods & pg.KMOD_ALT and not keys[1] and mods & pg.KMOD_CTRL and keys[0] and event.key == keys[2])
    alt = bool(mods & pg.KMOD_ALT and keys[1] and not mods & pg.KMOD_CTRL and not keys[0] and event.key == keys[2])
    if bool(mods & pg.KMOD_ALT) and bool(mods & pg.KMOD_CTRL):
        return event.key == keys[2] and keys[0] and keys[1]
    else:
        return key or ctrl or alt
