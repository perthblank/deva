from deva_const import ItemType, InventoryConst, KeyCode, MenuConst, ColorId, ArrowAt
from deva_menu import Deva_Menu, Deva_MenuMap

class Deva_Inventory:
    def __init__(self):
        #self._size = 100

        typeList = [ItemType.WEAPON, ItemType.MEDICINE, ItemType.ARMOR] 
        self._typeMap = {}
        menuMap = {}

        for t in typeList:
            self._typeMap[t] = {}
            menuMap[t] = self.showItems(t)

        self._categoryMenu = Deva_Menu(Deva_MenuMap(menuMap, typeList), InventoryConst.MENU_POS, mode = MenuConst.TRIGGER_BY_HOVER, colorId = ColorId.YELLOW)

        self.arrowAt = ArrowAt.LEV1

        self.loadItemMenu()

    def loadItemMenu(self):
        menuMap = {}
        for item, num in self.currentItems.items():
            showLine = item + max(15-len(item), 0) * ' ' + 'x' + str(num)
            menuMap[showLine] = lambda : 0
        self._currentItemMenu = Deva_Menu(Deva_MenuMap(menuMap), InventoryConst.LIST_POS, mode = MenuConst.TRIGGER_BY_ENTER)

    def showItems(self, t):
        def j():
            self.opt = t
        return j

    def add(self, item):
        t = item['type']
        n = item['name']
        self._typeMap[t][n] = self._typeMap[t].get(n, 0) + 1

    def handleKey(self, keyCode):
        if self.arrowAt == ArrowAt.LEV1:
            if keyCode == KeyCode.W:
                self._categoryMenu.arrUp()
            elif keyCode == KeyCode.S:
                self._categoryMenu.arrDown()
            elif keyCode == KeyCode.D:
                self.arrowAt = ArrowAt.LEV2
            self.loadItemMenu()
            #TODO cache item menu
        else:
            if keyCode == KeyCode.W:
                self._currentItemMenu.arrUp()
            elif keyCode == KeyCode.S:
                self._currentItemMenu.arrDown()
            elif keyCode == KeyCode.A:
                self.arrowAt = ArrowAt.LEV1

    @property
    def categoryMenu(self):
        return self._categoryMenu

    @property
    def currentItemMenu(self):
       return self._currentItemMenu

    @property
    def currentItems(self):
        return self._typeMap[self._categoryMenu.currentKey]

    @property
    def currentItem(self):
        return self._currentItemMenu.currentKey

    def test(self):
        return self._categoryMenu.currentKey

