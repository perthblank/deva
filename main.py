import time
import heapq
import threading

from dgsd_renderer import DGSD_Renderer
from dgsd_mesh import MeshMap, DGSD_Mesh
from dgsd_sprite import DGSD_Sprite
from dgsd_scene import DGSD_Scene
from dgsd_scene import SceneMap #TODO
from dgsd_menu import DGSD_Menu, DGSD_MenuMap
from dgsd_chat import ChatMap
from dgsd_const import *

import dgsd_mesh as dm


class DGSD_Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.renderer = DGSD_Renderer(width, height)

        self.printMsg = ''
        self.currentKey = ' '

        self._exitMenuMap = DGSD_MenuMap({
           SConst.BACK: self.resume,
           SConst.SAVE: self.save,
           SConst.EXIT: self.exit
        }, [SConst.BACK, SConst.SAVE, SConst.EXIT])

        self.loadScene(SceneMap['jiangnanMain'])
        self._mode = ControlMode.MOVE
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
                triggerObj = {'type': node['triggerType'], 'item': node['triggerItem']}
                triggerPos = []
                if node['triggerType'] == TriggerType.CHANGE_SCENE:
                    for row in range(sprite.height):
                        triggerPos += [(i + sprite.x, row + sprite.y) for i, c in enumerate(sprite.mesh[row]) if c == TRIGGER_CHAR]
                elif node['triggerType'] == TriggerType.CHAT:
                    for row in range(sprite.height):
                        triggerPos += [(i + sprite.x, row + sprite.y) for i, c in enumerate(sprite.mesh[row])]

                #self.printMsg += str(triggerPos)
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

    def log(self, s):
        self.renderer.log(str(s))

    def handleMove(self, keyCode):
        if keyCode in Directions:
            x, y = (self.role.x + Directions[keyCode][0], self.role.y + Directions[keyCode][1])
            if x > 0 and x < self.width - self.role.width and y > 0 and y < self.height - self.role.height:
                canStep = True
                for col in range(self.role.width):
                    for row in range(self.role.height):
                        if not self.isFreeGrid(col + x, row + y):
                            canStep = False
                            break
                    if not canStep:
                        break

                #self.log(str((x, y)))
                if canStep:
                    self.role.pos = (x, y)
                else:
                    for offset in RoleConst.COLLIDE_OFFSETS:
                        triggerObj = self.getTrigger(x + offset[0], y + offset[1])
                        if triggerObj:
                            if triggerObj['type'] == TriggerType.CHANGE_SCENE:
                                self.loadScene(SceneMap[triggerObj['item']])
                            elif triggerObj['type'] == TriggerType.CHAT:
                                self.showChat(ChatMap[triggerObj['item']])
                            break

            self.role.touch()
        if keyCode == ord('t'):
            self.test()

    def test(self):
        #self.printMsg = 'test'
        pass

    def showChat(self, chat):
        self._mode = ControlMode.CHAT
        self._activeChat = chat

    def handleUtil(self, keyCode):
        if keyCode == MyKeyCode.ESC:
            self._mode = ControlMode.MENU
            self.showExitMenu()

    def handleMenu(self, keyCode):

        if keyCode == MyKeyCode.W:
            self._activeMenu.arrUp()
        elif keyCode == MyKeyCode.S:
            self._activeMenu.arrDown()
        elif keyCode == MyKeyCode.ENTER:
            self._activeMenu.callCurrent()
        elif keyCode == MyKeyCode.ESC:
            self._mode = ControlMode.MOVE

    def handleChat(self, keyCode):
        # if keyCode == MyKeyCode.ESC:
        #     self._mode = ControlMode.MOVE


        if keyCode == MyKeyCode.ENTER:
            hasNext = self._activeChat.next()
            self.log(list(self._activeChat.statusSet))
            if not hasNext:
                self._mode = ControlMode.MOVE

        elif keyCode == MyKeyCode.W:
            self._activeChat.arrUp()
        elif keyCode == MyKeyCode.S:
            self._activeChat.arrDown()

        self.log(self._activeChat.opt)
            

    def showExitMenu(self):
        self._activeMenu = DGSD_Menu(self._exitMenuMap, (MenuConst.X, MenuConst.Y))

    def handleKeys(self):
        while self._ok:
            keyCode = self.renderer.getch()
            self.currentKey = str(keyCode)
            if self._mode == ControlMode.MOVE:
                self.handleMove(keyCode)
                self.handleUtil(keyCode)
            elif self._mode == ControlMode.CHAT:
                self.handleChat(keyCode)
            else:
                self.handleMenu(keyCode)
                
    def resume(self):
        self._mode = ControlMode.MOVE

    def save(self):
        #TODO
        self.log('save\n')
        self._mode = ControlMode.MOVE

    def exit(self):
        self._ok = False

    def render(self):
        time0 = time.clock()
        fps = 0
        lastFps = 0
        while self._ok:
            self.renderer.renderBorder()
            self.renderer.addstr(0, 0, self.currentKey)
            for s in self.sprites:
                sprite = s[1]
                self.renderer.renderSprite(sprite)

            mapDebug = False
            if mapDebug:
                for row in range(1, self.height -1):
                    for col in range(1, self.width -1):
                        self.renderer.addstr(row, col, str(self.map[self.getGridId(col, row)]))
                self.renderer.renderSprite(self.role)

            if self._mode == ControlMode.CHAT:
                self.renderer.renderChat(self._activeChat)
                pass

            if self._mode == ControlMode.MENU:
                self.renderer.renderMenu(self._activeMenu)

            fps += 1
            time1 = time.time()
            if(time1 - time0 > 1):
                lastFps = fps
                fps = 0
                time0 = time1

            self.renderer.addstr(0, 20, 'fps:' + str(lastFps))

            #self.renderer.addstr(self.height - 1, 20, self.printMsg)
            self.renderer.printLog()

            self.renderer.refresh()


if __name__ == "__main__":
    game = DGSD_Game(130, 40)
    try:
        game.start()
    finally:
        pass

