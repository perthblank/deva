import curses
from dgsd_const import ColorId

class ColorPair:
    def __init__(self, id, front, back = curses.COLOR_BLACK):
        self._id = id
        self._front = front
        self._back = back

    @property
    def id(self):
        return self._id

    @property
    def front(self):
        return self._front

    @property
    def back(self):
        return self._back


YELLOW = ColorPair(ColorId.YELLOW, curses.COLOR_YELLOW)
GREEN = ColorPair(ColorId.GREEN, curses.COLOR_GREEN)
    
COLORS = [YELLOW, GREEN]
