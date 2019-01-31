from deva_const import MeshType

class MeshUtil():
    @staticmethod
    def repeatBlock(pattern, width, height):
        return '\n'.join([pattern * width] * height)

    FlipPairs = [
        ('\\', '/')
    ]

    @staticmethod
    def flipChars(mesh):
        for pair in MeshUtil.FlipPairs:
            p1pos = []
            for i in range(0, len(mesh)):
                if mesh[i] == pair[1]:
                    p1pos.append(i)
            mesh = mesh.replace(pair[0], pair[1])
            for i in p1pos:
                mesh = mesh[:i] + pair[0] + mesh[i+1:]

        return mesh

    @staticmethod
    def flipMesh(mesh):
        return '\n'.join(
            MeshUtil.flipChars(row[::-1])
                for row in mesh.split('\n')
        )


# put the quotes in single lines
_role = [
"""
 o 
-+-
 ^ 
""",
"""
 o 
-+-
 " 
"""]

_npc = [
"""
 o 
+++
 ^ 
"""
]


#4x9
_rock_r = [
"""
|+/\    
:   `s\ 
s  ( `s.
|    )\.
"""
]

_rock_l = [
    MeshUtil.flipMesh(_rock_r[0])
]

_house = [
"""
   /---------\ 
  / -///:    `\ 
 /y+.  xxxx.//]\ 
+---------------+
|          +-+  |
|     yyy  +-+  |
|     yyy       |
--------###------
"""
]



_river = [
"""
                                                   ````..        
                              `````       :::-.````      ..`     
 /+/:--...``````````````````         ````-                       
           `:::::       ---...````````````     ````````````````` 
                                 `````````````                 `.
 ::.     ````````````````````                   ```````````      
  `--...`                                                  `:    
""",
"""
                                                   ````..        
                              `````       :::-.````      ..`     
 /+/:--...``````````````````         ````-                       
``````````            `:::::       ---...````````````     ```````
             `.                                 `````````````    
    ```````````       ::.     ````````````````````               
  `--...`                                                  `:    
""",
"""
                                                   ````..        
                              `````       :::-.````      ..`     
 /+/:--...``````````````````         ````-                       
````     `````````````````            `:::::       ---...````````
     `````````````                 `.                            
``                   ```````````       ::.     ``````````````````
  `--...`                                                  `:    
""",

]


_grass = [
    MeshUtil.repeatBlock('.', 90, 20)
]


_temple = [
"""
         /-          
       .+-+::-``     
   ``-/:`.d-``-::::::
-::--. `-+h-::-.`  /.
:/-.:++//.y...://:/- 
  `.o             +  
    y     -----:  s  
    s     y.```y  y  
    +-    m`   s  y  
    ::    y    s  s  
    :+::::+####+::/  
"""
]


_pickable = [
"""
x
""",
"""
o
"""
]

_sword = [
"""
  ^
 | |
 | |
 | |
=====
  |
""",
]

_swordFanri = [
"""
  ^
 |||
 |||
 |+|
=====
  |
""",
"""
  ^
 |+|
 |||
 |||
=====
  |
""",
"""
  ^
 |+|
 |||
 |||
=====
  |
""",
]

_dahuandan = [
"""

  oO
   o"
"""
]

_jinchuangyao = [
"""
  ^^^^^
  | J |
  [___]
"""
]

_hreb = [
"""
  lTI
 WOOOW
  lTI
   l
"""
]

_itemPlaceHolder = [
"""
+------------+
| No Picture |
+------------+
"""
]

_armor0 = [
"""
   ( )
=|--+--|=
  |-+-|
  |-+-|
  [-+-]
"""
]

_shoe0 = [
"""
 --
 {x}___
 |__|||)
"""
]


MeshList = [
    {
        'name': 'role',
        'mesh': _role,
        'type': MeshType.ANIMATE_ON_TOUCH,
    },
    {
        'name': 'rock_r',
        'mesh': _rock_r,
    },
    {
        'name': 'rock_l',
        'mesh': _rock_l,
    },
    {
        'name': 'npc',
        'mesh': _npc,
    },
    {
        'name': 'river',
        'mesh': _river,
        'type': MeshType.ANIMATE_AUTO,
    },
    {
        'name': 'grass',
        'mesh': _grass,
    },
    {
        'name': 'temple',
        'mesh': _temple,
    },
    {
        'name': 'house',
        'mesh': _house,
    },
    {
        'name': 'pickable',
        'mesh': _pickable,
        'type': MeshType.ANIMATE_AUTO,
    },
    {
        'name': 'sword',
        'mesh': _sword,
    },
    # TODO support inventory animation
    {
        'name': 'swordFanri',
        'mesh': _swordFanri,
        'type': MeshType.ANIMATE_AUTO,
    },
    {
        'name': 'placeHolder',
        'mesh': _itemPlaceHolder,
    },
    {
        'name': 'jinchuangyao',
        'mesh': _jinchuangyao,
    },
    {
        'name': 'dahuandan',
        'mesh': _dahuandan,
    },
    {
        'name': 'hreb',
        'mesh': _hreb,
    },
    {
        'name': 'shoe0',
        'mesh': _shoe0,
    },
    {
        'name': 'armor0',
        'mesh': _armor0,
    },
]

