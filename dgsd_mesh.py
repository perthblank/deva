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
  `::.s   `s/--::   
 `s` y:    `s.  `+/ 
 ::  .+      /    
 o`   +           
 `                
"""
]

mountain = DGSD_Mesh(_mountain, MeshType.RANDOM)

exitDialog = [\
"""
------------------""" + """
|      Exit      |
|      Save      |
|      Back      |
------------------
"""]
exitMenu = DGSD_Mesh(exitDialog) 

MeshMap = {
        'mountain': mountain,
        'role': role
        }
