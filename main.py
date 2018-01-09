import curses
import time
import heapq
import threading

from dgsd_mesh import MeshMap, DGSD_Mesh
from dgsd_sprite import DGSD_Sprite
from dgsd_scene import DGSD_Scene
from dgsd_scene import SceneConfig0 #TODO

from dgsd_menu import DGSD_Menu, MenuMap

import dgsd_color as dcolor
import dgsd_mesh as dm

class MoveKey:
    UP = 'w'
    DOWN = 's'
    LEFT = 'a'
    RIGHT = 'd'

Directions = {
    MoveKey.UP: [0, -1],
    MoveKey.DOWN: [0, 1],
    MoveKey.LEFT: [-1, 0],
    MoveKey.RIGHT: [1, 0],
}

class MyKeyCode:
    ENTER = 10

class MenuConst:
    X = 3
    Y = 1
    X_ARR = 1

class SConst:
    BACK = 'Back'
    SAVE = 'Save'
    EXIT = 'Exit'

class ControlMode:
    GAME = 1;
    MENU = 2;

class DGSD_Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.sprites = []
        self._mode = ControlMode.GAME

        self.loadScene(SceneConfig0)

        self.currentKey = ' '
        self.printStr = ''

        self._exitMenuMap = MenuMap({
           SConst.BACK: self.resume,
           SConst.SAVE: self.save,
           SConst.EXIT: self.exit
        }, [SConst.BACK, SConst.SAVE, SConst.EXIT])

        self._ok = True

    def start(self):
        handleThread = threading.Thread(target=self.handleKeys)
        renderThread = threading.Thread(target=self.render)

        handleThread.start()
        renderThread.start()
        handleThread.join()
        renderThread.join()

    def loadScene(self, sceneConfig):
        self.clearScene()
        scene = DGSD_Scene(sceneConfig)

        self.role = DGSD_Sprite(MeshMap['role'], scene.rolePos)
        self.addSprite(self.role, 5)

        for node in scene.item:
            self.addSprite(
                DGSD_Sprite(MeshMap[node['meshName']], node['pos'], node.get('colorId', 0)), node['zindex'])

    def addSprite(self, sprite, priority):
        heapq.heappush(self.sprites, (priority, sprite))

    def clearScene(self):
        self.sprites = []

    def handleControl(self, keyCode):
        key = ''
        if(keyCode < 255):
            key = chr(keyCode)
        if key in Directions:
            x, y = (self.role.x + Directions[key][0], self.role.y + Directions[key][1])
            if x > 0 and x < self.width and y > 0 and y < self.height - self.role.height:
                self.role.pos = (x, y)
            self.role.touch()

    def handleUtil(self, keyCode):
        key = ''
        if(keyCode < 255):
            key = chr(keyCode)
        if key == 'q':
            self._mode = ControlMode.MENU
            self.showExitMenu()

    def handleMenu(self, keyCode):
        key = ''
        if(keyCode < 255):
            key = chr(keyCode)
        if key == 'w':
            self._menuOpt = max(0, self._menuOpt - 1)
            self._menuArr.y = 1 + self._menuOpt
        elif key == 's':
            self._menuOpt = min(self._activeMenu.height -1, self._menuOpt + 1)
            self._menuArr.y = 1 + self._menuOpt

        if keyCode == MyKeyCode.ENTER:
            menuKey = self._activeMenu.item(self._menuOpt)
            self._exitMenuMap.call(menuKey)


    def showExitMenu(self):
        self._activeMenu = DGSD_Menu(self._exitMenuMap.keys, (MenuConst.X, MenuConst.Y))
        self._menuArr = DGSD_Sprite(DGSD_Mesh(['\n>\n']), (MenuConst.X_ARR, MenuConst.Y), dcolor.YELLOW.id) 
        self._menuOpt = 0

    def handleKeys(self):
        while self._ok:
            keyCode = stdscr.getch()
            self.currentKey = str(keyCode)
            if(self._mode == ControlMode.GAME):
                self.handleControl(keyCode)
                self.handleUtil(keyCode)
            else:
                self.handleMenu(keyCode)
                

    def resume(self):
        self._mode = ControlMode.GAME

    def save(self):
        #TODO
        self._mode = ControlMode.GAME

    def exit(self):
        self._ok = False

    def showExit(self):
        pass

    def renderSprites(self, lineNum):

        def renderLine(sprite):
            meshLineNum = lineNum - sprite.y
            if(meshLineNum >=0 and meshLineNum < sprite.height
                    and sprite.x >= 0 and sprite.x < self.width):
                meshLine = sprite.mesh[meshLineNum]
                stdscr.addstr(lineNum, sprite.x , meshLine, curses.color_pair(sprite.colorId))

        for spriteEntry in self.sprites:
            sprite = spriteEntry[1]
            renderLine(sprite)

        if self._mode == ControlMode.MENU:
          renderLine(self._activeMenu)
          renderLine(self._menuArr)
          pass
            

    def render(self):
        time0 = time.clock()
        fps = 0
        lastFps = 0
        while self._ok:
            stdscr.erase()
            for lineNum in range(0, self.height):
                if(lineNum == 0 or lineNum == self.height -1):
                    board = self.currentKey + "-" * (self.width - 1)
                    stdscr.addstr(lineNum, 0, board)
                else:
                    self.renderSprites(lineNum)
                    stdscr.addstr(lineNum, 0, '|')
                    stdscr.addstr(lineNum, self.width-1, '|')

            fps += 1
            time1 = time.time()
            if(time1 - time0 > 1):
                lastFps = fps
                fps = 0
                time0 = time1

            stdscr.addstr(0, 20, 'fps:' + str(lastFps))
            stdscr.addstr(self.height - 1, 20, self.printStr)

            stdscr.refresh()

        stdscr.refresh()

if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    curses.start_color()

    for color in dcolor.COLORS:
        curses.init_pair(color.id, color.front, color.back)


    game = DGSD_Game(130, 40)

    try:
        #report_progress("file_{0}.txt".format(i), i+1)

        game.start()
        pass
    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()
