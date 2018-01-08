from dgsd_color import DGSD_Colors as dcolor



class MeshType:
    static = 1
    random = 2
    animate = 3

class DGSD_Mesh:
    def __init__(self, mesh, meshType):
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

mountain = DGSD_Mesh(_mountain, MeshType.random)

_exitDialog = [\
"""
------------------""" + """
|      Exit      |
|      Save      |
|      Back      |
------------------
"""]
exitMenu = DGSD_Mesh(_exitDialog, MeshType.static) 

MeshMap = {
        'mountain': mountain,
        'role': role
        }
