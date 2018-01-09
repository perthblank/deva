import curses

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


YELLOW = ColorPair(1, curses.COLOR_YELLOW)
GREEN = ColorPair(2, curses.COLOR_GREEN)
    
COLORS = [YELLOW, GREEN]
