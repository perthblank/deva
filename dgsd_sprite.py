from dgsd_mesh import MeshType 
import random

class DGSD_Sprite:
    def __init__(self, mesh, pos):
        self._mesh = [m.split('\n')[1:-1] for m in mesh.mesh]
        self._meshType = mesh.meshType

        # remove first and last (empty) lines
        self.x = pos[0]
        self.y = pos[1]

        self._height = len(self._mesh[0])

        self._meshAnimateNum = 0
        self._meshSize = len(self._mesh)

    def print(self):
        for line in self._mesh:
            print("\r" + line)

    @property
    def mesh(self):
        index = 0
        if(self._meshType == MeshType.animate):
            index = (self._meshAnimateNum + 1) % self._meshSize
            self._meshAnimateNum = index

        elif(self._meshType == MeshType.random):
            index = random.randrange(0, self._meshSize)

        return self._mesh[index]


    @property
    def height(self):
        return self._height

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



