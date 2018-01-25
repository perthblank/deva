from dgsd_const import MeshType

class DGSD_Mesh:
    def __init__(self, mesh, meshType = MeshType.STATIC):
        self.mesh = mesh
        self.meshType = meshType

