class MeshType:
    STATIC = 1
    RANDOM = 2
    ANIMATE = 3

class DGSD_Mesh:
    def __init__(self, mesh, meshType = MeshType.STATIC):
        self.mesh = mesh
        self.meshType = meshType

# put the quotes in single lines
_role = [\
"""
 o 
-+-
 ^ 
""",\
"""
 o 
-+-
 " 
"""]


role = DGSD_Mesh(_role, MeshType.ANIMATE)

_npc = [\
"""
 o 
+++
 ^
"""
]

npc = DGSD_Mesh(_npc)

#4x9
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
""",\
"""
-+//+         
s   `s/--
:    `s. 
+      / 
"""
]

mountain = DGSD_Mesh(_mountain, MeshType.RANDOM)

_house = [\
"""
        `-///:   
    -///:    `+/ 
 oy+.  xxxx.///o+
o- :++------   -+
d///::h        -+
y     y   |    -+
y     y   |    -+
--------###------
"""
]

house = DGSD_Mesh(_house, MeshType.STATIC)

MeshMap = {
        'mountain': mountain,
        'role': role,
        'house': house,
        'npc': npc,
        }
