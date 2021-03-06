from deva_sprite import Deva_Sprite
from deva_mesh import Deva_Mesh
from deva_const import KeyCode, MenuConst, ColorId
from deva_renderer import Deva_Renderer as DR

class Deva_MenuMap():
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


class Deva_Menu(Deva_Sprite):
    def __init__(self, menuMap, pos, **kw):
        keys = menuMap.keys
        self.menuMap = menuMap
        mesh = '\n' + '\n'.join(keys) + '\n'
        colorId = kw.get('colorId', 0)
        bold = kw.get('bold', False)

        super(Deva_Menu, self).__init__(Deva_Mesh(mesh), pos, 6, colorId = colorId, bold = bold)

        self._keys = keys
        self._mode = kw.get('mode', MenuConst.TRIGGER_BY_ENTER)

        self.opt = 0

    def handleKey(self, keyCode):
        if keyCode == KeyCode.W:
            self.arrUp()
        elif keyCode == KeyCode.S:
            self.arrDown()
        elif keyCode == KeyCode.ENTER:
            self.callCurrent()

    def callCurrent(self):
        self.menuMap.call(self.currentKey)

    def arrUp(self):
        self.opt = self.opt - 1

    def arrDown(self):
        self.opt = self.opt + 1

    @property
    def currentKey(self):
        return self._keys[self.opt]

    @property
    def opt(self):
        return self._opt

    @opt.setter
    def opt(self, val):
        self._opt = max(0, min(val, self.height -1))
        if self._mode == MenuConst.TRIGGER_BY_HOVER:
            self.callCurrent()

