from deva_const import MeshType 
import random

class Deva_Sprite:
    def __init__(self, mesh, pos, zindex, **kw):
        if isinstance(mesh.mesh, list):
            self.meshList = [m.split('\n')[1:-1] for m in mesh.mesh]
            self.meshListType = mesh.meshType
            if(self.meshListType == MeshType.RANDOM):
                # randomly choose one
                self.meshList = [self.meshList[random.randrange(0, len(self.meshList))]]
            else:
                pass

        elif isinstance(mesh.mesh, str):
            self.meshList = [mesh.mesh.split('\n')[1:-1]]

        self.x = pos[0]
        self.y = pos[1]

        self._colorId = kw.get('colorId', 0)
        self._bold = kw.get('bold', 0)

        self._height = len(self.meshList[0])
        self._width = len(self.meshList[0][0])

        self._zindex = zindex

        self.meshListAnimateNum = 0
        self.meshListSize = len(self.meshList)

    def print(self):
        for line in self.meshList:
            print("\r" + line)

    def touch(self):
        if self.meshListType == MeshType.ANIMATE_ON_TOUCH:
            index = (self.meshListAnimateNum + 1) % self.meshListSize
            self.meshListAnimateNum = index

    def animate(self):
        if self.meshListType == MeshType.ANIMATE_AUTO:
            index = (self.meshListAnimateNum + 1) % self.meshListSize
            self.meshListAnimateNum = index

    @property
    def colorId(self):
        return self._colorId

    @property
    def mesh(self):
        return self.meshList[self.meshListAnimateNum]

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def pos(self):
        return [self.x, self.y] 

    @pos.setter
    def pos(self, val):
        self.x = val[0]
        self.y = val[1] 

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = max(0, val)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, val):
        self._y = max(0, val)

    @property
    def bold(self):
        return self._bold

    @property
    def zindex(self):
        return self._zindex

    def __lt__(self, other):
        # dont care the order
        return True


