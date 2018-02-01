import curses
import deva_color as dcolor
from deva_sprite import Deva_Sprite
from deva_mesh import Deva_Mesh
from deva_const import ColorId, ChatTextType

class Deva_Renderer:
    def __init__(self, width, height):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        
        if not curses.has_colors():
            print('Your terminal do not support curses colors, Deva refuse to run for now')
            exit(1)

        for color in dcolor.COLORS:
            curses.init_pair(color.id, color.front, color.back)

        self.width = width
        self.height = height

        # create an arrow >
        self._menuArr = Deva_Sprite(Deva_Mesh(['\n>\n']), (0, 0), 6, colorId = ColorId.YELLOW) 

        self._cameraPos = (0, 0)

        self.logList = []

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

    def renderMenu(self, menu, arrow = True):
        self._menuArr.x = menu.x - 2
        self._menuArr.y = menu.y + menu.opt
        self.renderSprite(menu, False)
        
        if arrow:
            self.renderSprite(self._menuArr, False)

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

    def renderPicked(self, role, picked):
        pickedName = picked['name']
        self.stdscr.addstr(max(role.y - 1 - self.cameraY, 0), max(role.x - self.cameraX - int(len(pickedName)/2), 0), pickedName)

    def renderInventory(self, inventory):
        self.renderMenu(inventory.categoryMenu)
        self.renderMenu(inventory.currentItemMenu, False)

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

