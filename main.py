import curses
import time
import heapq
import threading

from dgsd_mesh import MeshMap
from dgsd_sprite import DGSD_Sprite
from dgsd_scene import DGSD_Scene
from dgsd_scene import SceneConfig0 #TODO
#from dgsd_menu import TextMenu


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

class ControlMode:
    normal = 1;
    menu = 2;

class DGSD_Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.sprites = []

        self.loadScene(SceneConfig0)

        self._mode = ControlMode.normal
        self.currentKey = ' '
        # self.exitMenu = DGSD_Sprite(dm.exitMenu, [0, 0])

        self._ok = True

    def loadScene(self, sceneConfig):
        self.clearScene()
        #self.currentScene = DGSD_Scene(sceneConfig)
        scene = DGSD_Scene(sceneConfig)

        self.role = DGSD_Sprite(MeshMap['role'], scene.rolePos, 1)
        self.addSprite(self.role, 5)

        for node in scene.item:
            self.addSprite(
                DGSD_Sprite(MeshMap[node['meshName']], node['pos']), node['zindex'])

    def addSprite(self, sprite, priority):
        heapq.heappush(self.sprites, (priority, sprite))

    def clearScene(self):
        self.sprites = []

    def handleControl(self, key):
        if key in Directions:
            self.role.x = self.role.x + Directions[key][0]
            self.role.y = self.role.y + Directions[key][1]
            self.role.touch()

    def handleUtil(self, key):
        if key == 'q':
            self.quit()

    def handleKeys(self):
        while self._ok:
            key = stdscr.getkey()
            self.currentKey = key
            if(self._mode == ControlMode.normal):
                self.handleControl(key)
                self.handleUtil(key)
            # else:
            #     self._activeMenu.handle(key)


    def quit(self):
        self._ok = False

        return
        # self._mode = ControlMode.menu
        # self.showExit()
        # self._activeMenu = self.exitMenu


    def showExit(self):
        pass


    def start(self):
        handleThread = threading.Thread(target=self.handleKeys)
        renderThread = threading.Thread(target=self.render)

        handleThread.start()
        renderThread.start()

        handleThread.join()
        renderThread.join()

    def renderSprites(self, lineNum):

        def renderLine(sprite):
            meshLineNum = lineNum - sprite.y
            if(meshLineNum >=0 and meshLineNum < sprite.height
                    and sprite.x >= 0 and sprite.x < self.width):
                meshLine = sprite.mesh[meshLineNum]
                stdscr.addstr(lineNum, sprite.x , meshLine, curses.color_pair(sprite.colorNum))

        if self._mode == ControlMode.normal:
            for spriteEntry in self.sprites:
                sprite = spriteEntry[1]
                renderLine(sprite)

        elif self._mode == ControlMode.menu:
            renderLine(self._activeMenu)
            pass
            

    def render(self):
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
            stdscr.refresh()

        stdscr.refresh()

if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)


    game = DGSD_Game(130, 40)

    try:
        #report_progress("file_{0}.txt".format(i), i+1)

        game.start()
        pass
    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()
