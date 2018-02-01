from deva_const import ItemType, InventoryConst, KeyCode
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

        self._menu = Deva_Menu(Deva_MenuMap(menuMap, typeList), InventoryConst.MENU_POS)

    def showItems(self, t):
        def j():
            self.opt = t
        return j

    def add(self, item):
        n = item['name']
        t = item['type']
        self._typeMap[t][n] = self._typeMap[t].get(n, 0) + 1

    @property
    def menu(self):
        return self._menu

