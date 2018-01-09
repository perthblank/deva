from dgsd_mesh import MeshType 
import random

class DGSD_Sprite:
    def __init__(self, mesh, pos, colorId = 0):
        if isinstance(mesh.mesh, list):
            self._mesh = [m.split('\n')[1:-1] for m in mesh.mesh]
            self._meshType = mesh.meshType
            if(self._meshType == MeshType.RANDOM):
                # randomly choose one
                self._mesh = [self._mesh[random.randrange(0, len(self._mesh))]]
            else:
                pass

        elif isinstance(mesh.mesh, str):
            self._mesh = [mesh.mesh.split('\n')[1:-1]]

        self.x = pos[0]
        self.y = pos[1]

        self._colorId = colorId

        self._height = len(self._mesh[0])

        self._meshAnimateNum = 0
        self._meshSize = len(self._mesh)

    def print(self):
        for line in self._mesh:
            print("\r" + line)

    def touch(self):
        if(self._meshType == MeshType.ANIMATE):
            index = (self._meshAnimateNum + 1) % self._meshSize
            self._meshAnimateNum = index

    @property
    def colorId(self):
        return self._colorId

    @property
    def mesh(self):
        return self._mesh[self._meshAnimateNum]

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

    
    def __lt__(self, other):
        # dont care the order
        return True


