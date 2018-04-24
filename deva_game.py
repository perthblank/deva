import time
import threading

from deva_renderer import Deva_Renderer
from deva_mesh import Deva_Mesh
from deva_sprite import Deva_Sprite
from deva_scene import Deva_Scene
from deva_menu import Deva_Menu, Deva_MenuMap
from deva_inventory import Deva_Inventory
from deva_chat import Deva_Chat
from deva_const import *

from util import *

import deva_mesh as dm

class Deva_Game:
    def __init__(self, **configs):
        self.viewWidth  = configs['dim'][0]
        self.viewHeight = configs['dim'][1]
        self.meshMap  = self.convertConfigMap(configs['meshList'], ListOf.MESH)
        self.sceneMap = self.convertConfigMap(configs['sceneList'])
        self.chatMap  = self.convertConfigMap(configs['chatList'], ListOf.CHAT)
        self.itemMap  = self.convertConfigMap(configs['itemList'])

        self.renderer = Deva_Renderer.instance()
        self.renderer.setMaps(itemMap = self.itemMap, meshMap = self.meshMap)
        self.renderer.dim(configs['dim'])

        self.printMsg = ''
        self.currentKey = ' '

        self._exitMenuMap = Deva_MenuMap({
           SConst.BACK: self.resume,
           SConst.SAVE: self.save,
           SConst.EXIT: self.exit
        }, [SConst.BACK, SConst.SAVE, SConst.EXIT])

        self.loadScene(self.sceneMap['main'])
        self._keyModeHandler = {
            ControlMode.MOVE: self.handleMove,
            ControlMode.MENU: self.handleMenu,
            ControlMode.CHAT: self.handleChat,
            ControlMode.INVENTORY: self.handleInventory,
        }

        self._activePicked = None

        self._roleInventory = Deva_Inventory()

        self.mode = ControlMode.MOVE
        self._ok = True

        for i in configs['itemList']:
            self._roleInventory.add(i)

        self._roleInventory.loadItemMenu()

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
        scene = Deva_Scene(sceneConfig)
        self.grids = [MapGridType.FREE] * scene.width * scene.height
        self._activeScene = scene

        self.renderer.cameraPos = (max(0, scene.rolePos[0]-int(self.viewWidth/2)), max(0, scene.rolePos[1]-int(self.viewHeight/2)))

        self.role = Deva_Sprite(self.meshMap['role'], scene.rolePos, ROLE_ZINDEX)
        self.addSprite(self.role)

        for node in scene.meshNodes:
            sprite = Deva_Sprite(self.meshMap[node['meshName']], node['pos'], node['zindex'], colorId = node.get('colorId', 0), bold = node.get('bold', False))
            self.addSprite(sprite, node['gridType'])
            if 'triggerType' in node and 'triggerItem' in node:
                triggerObj = {'type': node['triggerType'], 'item': node['triggerItem'], 'spriteId': id(sprite)}
                triggerPos = []
                if node['triggerType'] == TriggerType.CHANGE_SCENE:
                    for row in range(sprite.height):
                        triggerPos += [(i + sprite.x, row + sprite.y) for i, c in enumerate(sprite.mesh[row]) if c == TRIGGER_CHAR]
                elif node['triggerType'] == TriggerType.CHAT or node['triggerType'] == TriggerType.ITEM:
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

    def removeSprite(self, spriteId):
        newSprites = []
        for s in self.sprites:
            if id(s) != spriteId:
                newSprites.append(s)
        self.sprites = newSprites

    def clearScene(self):
        self.sprites = []
        self.triggers = {}

    def log(self, s):
        self.renderer.log(str(s))

    def handleMove(self, keyCode):
        if keyCode in Directions:
            x, y = (self.role.x + Directions[keyCode][0], self.role.y + Directions[keyCode][1])
            self._activePicked = None
            
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
                    if cameraNewX >=0 and cameraNewX + self.viewWidth <= self._activeScene.width:
                        self.renderer.cameraX = cameraNewX

                    cameraNewY = self.renderer.cameraY + Directions[keyCode][1]
                    if cameraNewY >=0 and cameraNewY + self.viewHeight <= self._activeScene.height:
                        self.renderer.cameraY = cameraNewY

                    # self.log(self.renderer.cameraPos)

                else:
                    for offset in RoleConst.COLLIDE_OFFSETS:
                        triggerObj = self.getTrigger(x + offset[0], y + offset[1])
                        if triggerObj:
                            if triggerObj['type'] == TriggerType.CHANGE_SCENE:
                                self.loadScene(self.sceneMap[triggerObj['item']])
                            elif triggerObj['type'] == TriggerType.CHAT:
                                self.activeChat(self.chatMap[triggerObj['item']])
                            elif triggerObj['type'] == TriggerType.ITEM:
                                self.pickItem(selfitemMap[triggerObj['item']], triggerObj['spriteId'])
                                self.grids[self.getGridId(x + offset[0], y + offset[1])] = MapGridType.FREE
                            break

            for s in self.sprites:
                s.touch()

        elif keyCode == KeyCode.ESC or keyCode == KeyCode.Q:
            self.mode = ControlMode.MENU
            self.activeExitMenu(self._exitMenuMap)

        elif keyCode == KeyCode.I:
            self.mode = ControlMode.INVENTORY
            #self.showInventory()

        if keyCode == ord('t'):
            self.test()

    def test(self):
        # self.log(' '.join([str(id(s)) for s in self.sprites]))
        pass

    def activeChat(self, chat):
        self.mode = ControlMode.CHAT
        self._activeChat = chat

    def activeExitMenu(self, menuMap):
        self._activeMenu = Deva_Menu(menuMap, (MenuConst.X, MenuConst.Y))

    def showInventory(self):
        pass

    def handleMenu(self, keyCode):
        if keyCode == KeyCode.ESC:
            self.mode = ControlMode.MOVE
        else:
            self._activeMenu.handleKey(keyCode)

    def handleChat(self, keyCode):
        if keyCode == KeyCode.ENTER:
            hasNext = self._activeChat.next()
            if not hasNext:
                self.mode = ControlMode.MOVE
        else:
            self._activeChat.handleKey(keyCode)

    def handleInventory(self, keyCode):
        if keyCode == KeyCode.ESC:
            self.mode = ControlMode.MOVE
        else:
            self._roleInventory.handleKey(keyCode)

        # self.log(self._roleInventory.currentItems())

    def handleKeys(self):
        while self._ok:
            keyCode = self.renderer.getch()
            #self.currentKey = str(keyCode)

            self._keyModeHandler[self.mode](keyCode)

    def pickItem(self, item, spriteId):
        #self.log(item)

        self._activePicked = item
        self._roleInventory.add(item)
        self.removeSprite(spriteId)
                
    def resume(self):
        self.mode = ControlMode.MOVE

    def save(self):
        #TODO
        self.log('save\n')
        self.mode = ControlMode.MOVE

    def exit(self):
        self._ok = False

    def render(self):
        time0 = time.clock()
        fps = 0
        lastFps = 0
        while self._ok:
            self.renderer.renderBorder()
            # self.renderer.addstr(0, 0, self.currentKey)
            if self.mode == ControlMode.INVENTORY:
                self.renderer.renderInventory(self._roleInventory)

            else:
                for s in self.sprites:
                    self.renderer.renderSprite(s)

                if self.mode == ControlMode.CHAT:
                    self.renderer.renderChat(self._activeChat)

                if self.mode == ControlMode.MENU:
                    self.renderer.renderMenu(self._activeMenu)

                if self._activePicked is not None:
                    self.renderer.renderPicked(self.role, self._activePicked)

            fps += 1
            time1 = time.time()
            if(time1 - time0 > 1):
                lastFps = fps
                fps = 0
                time0 = time1

            self.renderer.addstr(0, 20, 'fps:' + str(lastFps))

            self.renderer.printLog()
            self.renderer.refresh()

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, m):
        self._mode = m

    def convertConfigMap(self, configList, listOf = None):
        mmap = {}
        if listOf == ListOf.CHAT:
            for x in configList:
                mmap[x['name']] = Deva_Chat(x['content'])
        elif listOf == ListOf.MESH:
            for x in configList:
                mmap[x['name']] = Deva_Mesh(x['mesh'], x.get('type', MeshType.STATIC))
        else:
            for x in configList:
                mmap[x['name']] = x

        return mmap


from config_mesh import MeshList
from config_chat import ChatList
from config_scene import SceneList
from config_item import ItemList

if __name__ == "__main__":
    game = Deva_Game(
      dim = (80,30), 
      meshList = MeshList, 
      chatList = ChatList, 
      sceneList = SceneList, 
      itemList = ItemList
    )
    try:
        game.start()
    except:
        print('Error')
    finally:
        pass

