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

    def renderSprite(self, sprite):
        for row in range(sprite.height):
            meshRow = sprite.mesh[row]
            self.stdscr.addstr(sprite.y + row, sprite.x, meshRow, curses.color_pair(sprite.colorId))

    def renderMenu(self, menu):
        self._menuArr.x = menu.x - 2
        self._menuArr.y = menu.y + menu.opt
        self.renderSprite(self._menuArr)
        self.renderSprite(menu)

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

