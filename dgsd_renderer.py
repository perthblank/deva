import curses
import dgsd_color as dcolor
from dgsd_sprite import DGSD_Sprite
from dgsd_mesh import DGSD_Mesh
from dgsd_const import ColorId, ChatTextType

class DGSD_Renderer:
    def __init__(self, width, height):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        for color in dcolor.COLORS:
            curses.init_pair(color.id, color.front, color.back)

        self.width = width
        self.height = height

        # create an arrow >
        self._menuArr = DGSD_Sprite(DGSD_Mesh(['\n>\n']), (0, 0), ColorId.YELLOW) 

        self.logList = []

        self._cameraPos = (0, 0)

    def __del__(self):
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def renderBorder(self):
        self.stdscr.erase()
        lineFlush = ' ' * self.width
        for lineNum in range(0, self.height):
            if(lineNum == 0 or lineNum == self.height -1):
                border = "-" * self.width
                self.stdscr.addstr(lineNum, 0, border)
            else:
                self.stdscr.addstr(lineNum, 0, lineFlush)
                self.stdscr.addstr(lineNum, 0, '|')
                self.stdscr.addstr(lineNum, self.width-1, '|')

    def renderSprite(self, sprite, viewport = True):
        for indRow in range(sprite.height):
            meshRow = sprite.mesh[indRow]
            attr = curses.color_pair(sprite.colorId)
            if sprite.bold:
                attr |= curses.A_BOLD
            for indCol in range(len(meshRow)):
                y = sprite.y + indRow - (self.cameraY if viewport else 0)
                x = sprite.x + indCol - (self.cameraX if viewport else 0)
                if(y>=1 and y < self.height - 1 and x >=1 and x < self.width - 1):
                    self.stdscr.addstr(y, x, meshRow[indCol], attr)

    def renderMenu(self, menu):
        self._menuArr.x = menu.x - 2
        self._menuArr.y = menu.y + menu.opt
        self.renderSprite(self._menuArr, False)
        self.renderSprite(menu, False)

    def renderChat(self, chat):
        textItem = chat.currentTextItem
        titles = textItem['title'].split('\n')
        if textItem['type'] == ChatTextType.STATEMENT:
            for i in range(len(titles)):
                self.stdscr.addstr(self.height - 2 - len(titles) + i, 2, titles[i])
        elif textItem['type'] == ChatTextType.BRANCH:
            menu = chat.branchMenu
            menu.y = self.height - 2 - menu.height
            self.renderMenu(menu)
            for i in range(len(titles)):
                self.stdscr.addstr(self.height - 2 - len(titles) + i - menu.height, 2, titles[i])

    def refresh(self):
        self.stdscr.refresh()

    def addstr(self, row, col, s):
        # debug use only
        self.stdscr.addstr(row, col, s)

    def getch(self):
        return self.stdscr.getch()

    def log(self, s):
        self.logList.append(s)
        self.logList = self.logList[-15:]

    def printLog(self):
        for i in range(len(self.logList)):
            self.stdscr.addstr(self.height + 1 + i, 0, self.logList[i])

    @property
    def cameraPos(self):
        return self._cameraPos

    @cameraPos.setter
    def cameraPos(self, pos):
        self._cameraPos = pos

    @property
    def cameraX(self):
        return self._cameraPos[0]

    @cameraX.setter
    def cameraX(self, x):
        self._cameraPos = (x, self._cameraPos[1])

    @property
    def cameraY(self):
        return self._cameraPos[1]

    @cameraY.setter
    def cameraY(self, y):
        self._cameraPos = (self._cameraPos[0], y)

