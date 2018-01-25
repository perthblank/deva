from dgsd_const import MeshType 
import random

class DGSD_Sprite:
    def __init__(self, mesh, pos, colorId = 0, bold = False):
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

        self._colorId = colorId

        self._height = len(self.meshList[0])
        self._width = len(self.meshList[0][0])

        self._bold = bold

        self.meshListAnimateNum = 0
        self.meshListSize = len(self.meshList)

    def print(self):
        for line in self.meshList:
            print("\r" + line)

    def touch(self):
        if(self.meshListType == MeshType.ANIMATE):
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

    def __lt__(self, other):
        # dont care the order
        return True


