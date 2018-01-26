from deva_const import MeshType

class Deva_Mesh:
    def __init__(self, mesh, meshType = MeshType.STATIC):
        self.mesh = mesh
        self.meshType = meshType

