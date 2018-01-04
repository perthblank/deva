import curses
import time
import heapq
import threading

import dgsd_mesh as dm
from dgsd_sprite import DGSD_Sprite


class MoveKey:
    up = 'w'
    down = 's'
    left = 'a'
    right = 'd'

Directions = {
    MoveKey.up: [0, -1],
    MoveKey.down: [0, 1],
    MoveKey.left: [-1, 0],
    MoveKey.right: [1, 0],
}

#Scene0

class DGSD_Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.sprites = []

        self.role = DGSD_Sprite(dm.role, [20, 20])
        self.addSprite(self.role, 5)
        self.addSprite(DGSD_Sprite(dm.mountain, [30,10]), 6)

        self._ok = True

    def addSprite(self, sprite, priority):
        heapq.heappush(self.sprites, (priority, sprite))

    def handleControl(self, key):
        if key in Directions:
            self.role.x = self.role.x + Directions[key][0]
            self.role.y = self.role.y + Directions[key][1]

    def handleUtil(self, key):
        if key == 'q':
            self.quit()

    def handleKeys(self):
        while self._ok:
            key = stdscr.getkey()
            self.handleControl(key)
            self.handleUtil(key)

    def quit(self):
        self._ok = False

    def start(self):
        handleThread = threading.Thread(target=self.handleKeys)
        renderThread = threading.Thread(target=self.render)

        handleThread.start()
        renderThread.start()

        handleThread.join()
        renderThread.join()

    def renderSprites(self, lineNum, line):
        line = list(line)
        for spriteEntry in self.sprites:
            sprite = spriteEntry[1]
            meshLineNum = lineNum - sprite.y
            if(meshLineNum >=0 and meshLineNum < sprite.height
                    and sprite.x >= 0 and sprite.x < self.width):
                meshLine = sprite.mesh[meshLineNum]
                for i in range(len(meshLine)):
                    line[sprite.x + i] = meshLine[i]

        return ''.join(line)

    def render(self):
        while self._ok:
            for lineNum in range(0, self.height):
                line = ' ' * self.width
                if(lineNum == 0 or lineNum == self.height -1):
                    board = "-" * self.width
                    stdscr.addstr(lineNum, 0, board)
                else:
                    line = self.renderSprites(lineNum, line)
                    line = '|' + line[1:]
                    line = line[0:-1] + '|'
                    stdscr.addstr(lineNum, 0, line)
            stdscr.refresh()


if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()


    game = DGSD_Game(130, 40)

    try:
        #report_progress("file_{0}.txt".format(i), i+1)

        game.start()
        pass
    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()
