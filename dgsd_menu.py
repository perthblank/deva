from dgsd_sprite import DGSD_Sprite
from dgsd_mesh import DGSD_Mesh

class DGSD_MenuMap():
    def __init__(self, keyMap, keyOrder = None):
        if keyOrder is None:
            keyOrder = list(keyMap.keys())
        self._keys = keyOrder
        self._keyMap = keyMap

    @property
    def keys(self):
        return self._keys

    def call(self, key):
        self._keyMap[key]()


class DGSD_Menu(DGSD_Sprite):
    def __init__(self, menuMap, pos, colorId = 0):
        keys = menuMap.keys
        self.menuMap = menuMap
        mesh = '\n' + '\n'.join(keys) + '\n'
        super(DGSD_Menu, self).__init__(DGSD_Mesh(mesh), pos, colorId)
        self._keys = keys
        self._opt = 0

    def callCurrent(self):
        self.menuMap.call(self.currentKey())

    def currentKey(self):
        return self._keys[self.opt]

    def arrUp(self):
        self.opt = self.opt - 1

    def arrDown(self):
        self.opt = self.opt + 1

    @property
    def opt(self):
        return self._opt

    @opt.setter
    def opt(self, val):
        self._opt = max(0, min(val, self.height -1))

