import curses
import time
import heapq
import threading

from dgsd_mesh import MeshMap, DGSD_Mesh
from dgsd_sprite import DGSD_Sprite
from dgsd_scene import DGSD_Scene
from dgsd_scene import SceneMap #TODO

from dgsd_menu import DGSD_Menu, MenuMap

import dgsd_color as dcolor
import dgsd_mesh as dm

from dgsd_const import *

class DGSD_Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.printMsg = ''
        self.currentKey = ' '

        self._exitMenuMap = MenuMap({
           SConst.BACK: self.resume,
           SConst.SAVE: self.save,
           SConst.EXIT: self.exit
        }, [SConst.BACK, SConst.SAVE, SConst.EXIT])

        self.loadScene(SceneMap['jiangnanMain'])
        self._mode = ControlMode.GAME
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
            sprite = DGSD_Sprite(MeshMap[node['meshName']], node['pos'], node.get('colorId', 0))
            self.addSprite(sprite, node['zindex'], node['gridType'])
            if 'triggerType' in node and 'triggerItem' in node:
                triggerPos = []
                for row in range(sprite.height):
                    triggerPos += [(i + sprite.x, row + sprite.y) for i, c in enumerate(sprite.mesh[row]) if c == TRIGGER_CHAR]
                triggerObj = {'type': node['triggerType'], 'item': node['triggerItem']}
                #self.printMsg = str(triggerPos)
                for t in triggerPos:
                    self.triggers[self.getGridId(t[0], t[1])] = triggerObj



    def getGridId(self, x, y):
        return x * self.height + y

    def isFreeGrid(self, x, y):
        return self.map[self.getGridId(x, y)] == MapGridType.FREE

    def getTrigger(self, x, y):
        return self.triggers.get(self.getGridId(x, y), None)

    def addSprite(self, sprite, priority, gridType = MapGridType.FREE):
        heapq.heappush(self.sprites, (priority, sprite))
        for row in range(sprite.height):
            for col in range(sprite.width):
                gridId = self.getGridId((col + sprite.x), (row + sprite.y))
                self.map[gridId] = gridType 

    def clearScene(self):
        self.sprites = []
        self.triggers = {}
        self.map = [MapGridType.FREE] * self.width * self.height

    def handleControl(self, keyCode):
        key = ''
        if(keyCode < 255):
            key = chr(keyCode)
        if key in Directions:
            x, y = (self.role.x + Directions[key][0], self.role.y + Directions[key][1])
            if x > 0 and x < self.width - self.role.width and y > 0 and y < self.height - self.role.height:
                canStep = True
                for col in range(self.role.width):
                    for row in range(self.role.height):
                        if not self.isFreeGrid(col + x, row + y):
                            canStep = False
                            break
                    if not canStep:
                        break

                if canStep:
                    self.role.pos = (x, y)
                else:
                    triggerObj = self.getTrigger(x + RoleConst.HEAD_X, y + RoleConst.HEAD_Y)
                    if triggerObj:
                        if triggerObj['type'] == TriggerType.CHANGE_SCENE:
                            #self.save()
                            self.loadScene(SceneMap[triggerObj['item']])

            self.role.touch()

    def handleUtil(self, keyCode):
        key = ''
        if(keyCode < 255):
            key = chr(keyCode)
        if keyCode == MyKeyCode.ESC:
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
        # create an arrow >
        self._menuArr = DGSD_Sprite(DGSD_Mesh(['\n>\n']), (MenuConst.X_ARR, MenuConst.Y), ColorId.YELLOW) 
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

    def renderLine(self, lineNum):
        # deprecated for now

        def renderSpriteOnLine(sprite):
            meshLineNum = lineNum - sprite.y
            if(meshLineNum >=0 and meshLineNum < sprite.height
                    and sprite.x >= 0 and sprite.x < self.width):
                meshLine = sprite.mesh[meshLineNum]
                stdscr.addstr(lineNum, sprite.x , meshLine, curses.color_pair(sprite.colorId))

        for spriteEntry in self.sprites:
            sprite = spriteEntry[1]
            renderSpriteOnLine(sprite)

        if self._mode == ControlMode.MENU:
          renderSpriteOnLine(self._activeMenu)
          renderSpriteOnLine(self._menuArr)


    def renderSprite(self, sprite):
        for row in range(sprite.height):
            meshRow = sprite.mesh[row]
            stdscr.addstr(sprite.y + row, sprite.x, meshRow, curses.color_pair(sprite.colorId))

            

    def render(self):
        time0 = time.clock()
        fps = 0
        lastFps = 0
        lineFlush = ' ' * self.width
        while self._ok:
            stdscr.erase()
            for lineNum in range(0, self.height):
                # draw broad
                if(lineNum == 0 or lineNum == self.height -1):
                    board = "-" * self.width
                    stdscr.addstr(lineNum, 0, board)
                    stdscr.addstr(lineNum, 0, self.currentKey)
                else:
                    #self.renderLine(lineNum)
                    stdscr.addstr(lineNum, 0, lineFlush)
                    stdscr.addstr(lineNum, 0, '|')
                    stdscr.addstr(lineNum, self.width-1, '|')

            for s in self.sprites:
                sprite = s[1]
                self.renderSprite(sprite)

            mapDebug = False
            if mapDebug:
                for row in range(1, self.height -1):
                    for col in range(1, self.width -1):
                        stdscr.addstr(row, col, str(self.map[self.getGridId(col, row)]))
                self.renderSprite(self.role)

            if self._mode == ControlMode.MENU:
                self.renderSprite(self._activeMenu)
                self.renderSprite(self._menuArr)

            fps += 1
            time1 = time.time()
            if(time1 - time0 > 1):
                lastFps = fps
                fps = 0
                time0 = time1

            stdscr.addstr(0, 20, 'fps:' + str(lastFps))
            stdscr.addstr(self.height - 1, 20, self.printMsg)

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
