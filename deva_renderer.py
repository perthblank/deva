import curses
import deva_color as dcolor
from deva_sprite import Deva_Sprite
from deva_mesh import Deva_Mesh
from deva_const import ColorId, ChatTextType, ArrowAt, InventoryConst

import threading

class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Also, the decorated class cannot be
    inherited from. Other than that, there are no restrictions that apply
    to the decorated class.

    To get the singleton instance, use the `instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)

@Singleton
class Deva_Renderer:
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        
        if not curses.has_colors():
            print('Your terminal do not support curses colors, Deva refuse to run for now')
            exit(1)

        for color in dcolor.COLORS:
            curses.init_pair(color.id, color.front, color.back)

        self.width = 10
        self.height = 10

        # create an arrow >
        self._menuArr = Deva_Sprite(Deva_Mesh(['\n>\n']), (0, 0), 6, colorId = ColorId.YELLOW) 

        self._cameraPos = (0, 0)

        self.logList = []
        self.itemMap = {}
        self.meshMap = {}

        self._lock = threading.Lock()


    def __del__(self):
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def setMaps(self, **kargs):
        if 'itemMap' in kargs:
            self.itemMap = kargs['itemMap']
        if 'meshMap' in kargs:
            self.meshMap = kargs['meshMap']

    def dim(self, d):
        self.width = d[0]
        self.height = d[1]

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
        self.renderSprite(menu, False)
        if arrow:
            self._menuArr.x = menu.x - 2
            self._menuArr.y = menu.y + menu.opt
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
        self.renderMenu(inventory.categoryMenu, inventory.arrowAt == ArrowAt.LEV1)
        self.renderMenu(inventory.currentItemMenu, inventory.arrowAt == ArrowAt.LEV2)
        itemName = ''.join(inventory.currentItem.split('x')[:-1]).strip()
        if itemName in self.itemMap:
            meshName = self.itemMap[itemName]['meshName']
            sprite = Deva_Sprite(self.meshMap.get(meshName, ''), InventoryConst.FIG_POS, 5)
            self.renderSprite(sprite, False)


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
        self._lock.acquire()
        r = self._cameraPos[0]
        self._lock.release()
        return r

    @cameraX.setter
    def cameraX(self, x):
        self._lock.acquire()
        self._cameraPos = (x, self._cameraPos[1])
        self._lock.release()

    @property
    def cameraY(self):
        self._lock.acquire()
        r = self._cameraPos[1]
        self._lock.release()
        return r

    @cameraY.setter
    def cameraY(self, y):
        self._lock.acquire()
        self._cameraPos = (self._cameraPos[0], y)
        self._lock.release()
