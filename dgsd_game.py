import time
import threading

from dgsd_renderer import DGSD_Renderer
from dgsd_mesh import DGSD_Mesh
from dgsd_sprite import DGSD_Sprite
from dgsd_scene import DGSD_Scene
from dgsd_menu import DGSD_Menu, DGSD_MenuMap
from dgsd_const import *

from config_mesh import MeshMap
from config_chat import ChatMap
from config_scene import SceneMap

from util import *

import dgsd_mesh as dm

class DGSD_Game:
    def __init__(self, width, height):
        self.viewWidth = width
        self.viewHeight = height

        self.renderer = DGSD_Renderer(width, height)

        self.printMsg = ''
        self.currentKey = ' '

        self._exitMenuMap = DGSD_MenuMap({
           SConst.BACK: self.resume,
           SConst.SAVE: self.save,
           SConst.EXIT: self.exit
        }, [SConst.BACK, SConst.SAVE, SConst.EXIT])

        self.loadScene(SceneMap['main'])
        self._mode = ControlMode.MOVE
        self._ok = True

    def start(self):
        handleThread = threading.Thread(target=self.handleKeys)
        renderThread = threading.Thread(target=self.render)
        animateThread = threading.Thread(target=self.animate)

        handleThread.start()
        renderThread.start()
        animateThread.start()
        handleThread.join()
        renderThread.join()
        animateThread.join()

    def animate(self):
        while self._ok:
            for s in self.sprites:
                s.animate()
            time.sleep(1)

    def loadScene(self, sceneConfig):
        self.clearScene()
        scene = DGSD_Scene(sceneConfig)
        self.grids = [MapGridType.FREE] * scene.width * scene.height
        self._activeScene = scene

        self.renderer.cameraPos = (max(0, scene.rolePos[0]-int(self.viewWidth/2)), max(0, scene.rolePos[1]-int(self.viewHeight/2)))

        self.role = DGSD_Sprite(MeshMap['role'], scene.rolePos, ROLE_ZINDEX)
        self.addSprite(self.role)

        for node in scene.meshNodes:
            sprite = DGSD_Sprite(MeshMap[node['meshName']], node['pos'], node['zindex'], node.get('colorId', 0), node.get('bold', False))
            self.addSprite(sprite, node['gridType'])
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
        return x * self._activeScene.height + y

    def isFreeGrid(self, x, y):
        return self.grids[self.getGridId(x, y)] == MapGridType.FREE

    def getTrigger(self, x, y):
        return self.triggers.get(self.getGridId(x, y), None)

    def addSprite(self, sprite, gridType = MapGridType.FREE):
        self.sprites.append(sprite)
        self.sprites = sorted(self.sprites, key = lambda a: a.zindex)

        for row in range(sprite.height):
            for col in range(sprite.width):
                x = col + sprite.x
                y = row + sprite.y
                if x < self._activeScene.width and y < self._activeScene.height:
                    gridId = self.getGridId((col + sprite.x), (row + sprite.y))
                    if(gridType != MapGridType.FREE):
                        self.grids[gridId] = gridType 

    def clearScene(self):
        self.sprites = []
        self.triggers = {}

    def log(self, s):
        self.renderer.log(str(s))

    def handleMove(self, keyCode):
        if keyCode in Directions:
            x, y = (self.role.x + Directions[keyCode][0], self.role.y + Directions[keyCode][1])
            if x > 0 and x < self._activeScene.width - self.role.width and y > 0 and y < self._activeScene.height - self.role.height:
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
                    cameraNewX = self.renderer.cameraX + Directions[keyCode][0]
                    if cameraNewX >=0 and cameraNewX + self.viewWidth < self._activeScene.width:
                        self.renderer.cameraX = cameraNewX

                    cameraNewY = self.renderer.cameraY + Directions[keyCode][1]
                    if cameraNewY >=0 and cameraNewY + self.viewHeight < self._activeScene.height:
                        self.renderer.cameraY = cameraNewY

                    # self.log(self.renderer.cameraPos)

                else:
                    for offset in RoleConst.COLLIDE_OFFSETS:
                        triggerObj = self.getTrigger(x + offset[0], y + offset[1])
                        if triggerObj:
                            if triggerObj['type'] == TriggerType.CHANGE_SCENE:
                                self.loadScene(SceneMap[triggerObj['item']])
                            elif triggerObj['type'] == TriggerType.CHAT:
                                self.showChat(ChatMap[triggerObj['item']])
                            break

            for s in self.sprites:
                s.touch()

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
            # self.log(list(self._activeChat.statusSet))
            if not hasNext:
                self._mode = ControlMode.MOVE

        elif keyCode == MyKeyCode.W:
            self._activeChat.arrUp()
        elif keyCode == MyKeyCode.S:
            self._activeChat.arrDown()

        # self.log(self._activeChat.opt)
            

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
                self.renderer.renderSprite(s)

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

            #self.renderer.addstr(self.viewHeight - 1, 20, self.printMsg)
            self.renderer.printLog()

            self.renderer.refresh()


if __name__ == "__main__":
    game = DGSD_Game(40, 30)
    try:
        game.start()
    finally:
        pass

