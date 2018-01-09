from dgsd_sprite import DGSD_Sprite
from dgsd_mesh import DGSD_Mesh

class MenuMap():
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
    def __init__(self, keys, pos, colorId = 0):
        mesh = '\n' + '\n'.join(keys) + '\n'
        super(DGSD_Menu, self).__init__(DGSD_Mesh(mesh), pos, colorId)
        self._keys = keys

    def item(self, i):
        return self._keys[i]

