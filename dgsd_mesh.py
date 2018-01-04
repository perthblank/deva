# put the quotes in single lines

class MeshType:
    static = 1
    random = 2
    animate = 3

class DGSD_Mesh:
    def __init__(self, mesh, meshType):
        self.mesh = mesh
        self.meshType = meshType


_role = [\
"""
 o
-+-
 ^
""",\
"""
 o
-+-
 |
"""]


role = DGSD_Mesh(_role, MeshType.animate)

_mountain = [\
"""
    .-.  
`/-+` `/ 
/  :    /
.  `    .
""",\
"""
 -.-      
 / `:     
|   ::--` 
     `  - 
"""
]

mountain = DGSD_Mesh(_mountain, MeshType.static)
