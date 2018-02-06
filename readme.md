# Deva (天众)
Enjoy an RPG, in terminal.

> A *deva* (देव Sanskrit and Pāli, Mongolian tenger (тэнгэр)) in Buddhism is one of many different types of non-human beings who share the godlike characteristics of being more powerful, longer-lived, and, in general, much happier than humans, although the same level of veneration is not paid to them as to buddhas. 


### What is Deva
- A terminal RPG
- A terminal RPG maker by writing config files

Text-image rendered by `curses` in python.

### Get started
Simply run
```
python3 deva_game.py
```
for demo

Keys: move: `w`, `a`, `s`, `d`, inventory: `i`,  select: `Enter`, cancel/back: `Esc`

### Make a game
This project provides the following RPG factors to config:
- mesh
- scene (viewport)
- chat
- inventory

next
- attribute
- battle system
- task system

#### Mesh
Refer `config_mesh.py`

A mesh is a character layout. Any node in the scene is a mesh. There're three types of mesh supported:
- `MeshType.STATIC`: a static mesh (eg. `house`)
- `MeshType.ANIMATE_ON_TOUCH`: an animating mesh, the mesh will play next frame when player touch move key (eg. `role`)
- `MeshType.ANIMATE_AUTO`: an auto animating mesh, the mesh will play next frame each 1 sec (eg. `river`)
- `MeshType.RANDOM`: the game will randomly load one frame from the given mesh list when starts (eg, `rock`)

Example:
```python
# put the quotes in single lines
_role = [
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

# renderer will loop the two frames in cycle
role = Deva_Mesh(_role, MeshType.ANIMATE_ON_TOUCH)


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

# a static mesh, and the `#` on the edge will be recognized as trigger point
# if this mesh is configed as trigger `CHANGE_SCENE` in scene config
temple = Deva_Mesh(_temple)
```

#### Scene
Refer `config_scene.py`

A scene is defined as the starting place of role and all other mesh nodes.
```
scene = {
  'name': scene name
  'rolePos': [x, y],
  'dimension': [width, height],
  'nodes': [...mesh_nodes]
}
```
`dimension` tells the width and height of the scene. If the dimension is larger than viewport, then the camera  will render a part of the scene, like a normal RPG. Otherwise, the whole scene will be rendered.

Each mesh node has following attribute:
- `meshName`: defined name in MeshMap in mesh config
- `pos`: mesh position
- `zindex`: higher value ones will cover lower ones
- `colorId`(*optinal*): constant from `ColorId.YELLOW, ColorId.GREEN, ColorId.BLUE, ColorId.RED, ColorId.MAGENTA, ColorId.CYAN`
- `gridType`: constant from `MapGridType.BLOCK, MapGridType.FREE`, where `BLOCK` means the role can not step on the mesh
- `triggerType`(*optinal*): constant from `TriggerType.CHAT, TriggerType.CHANGE_SCENE, TriggerType.ITEM`, where `CHAT` will trigger a chat when collide with the mesh (npc), and `CHANGE_SCENE` will load another scene when the role collides with the `TRIGGER_CHAR`(#) on the mesh, and `ITEM` can be picked up (need inventory to complete). The attribute come along with `triggerItem`
- `triggerItem`(*optinal*): chat or scene name defined in config
- `bold`(*optinal*): show the mesh characters in bold font

#### Chat
Refer `config_chat.py`

A chat is defined as a list of chat nodes. Each chat node has  following attribute:
- `id`: index of the node
- `title`: text of current chat box
- `type`: constant from `ChatTextType.STATEMENT, ChatTextType.BRANCH`, where `branch` means current chat box contains a choice question, come with the attribute `branch`, `branch_to`
- `branch`: a list of choices
- `branch_to`: a list index of the corresponding choice should jump to. Should have equal length with `branch`
- `status_code`(*optional*): a status that current chat node will trigger
- `exclude_status`: status that if triggered by previous chat nodes, this node will not be shown anymore
- `prereq_status`: status that needed to be triggered to show this node


#### Viewport
A smaller viewport will render a part of the scene, and the camera will follow the role
```
100-----------------fps:556-------------
|......................................|
|...........x....        `-///:   .....|
|................    -///:    `+/ .....|
|........-+//+ .. oy+.  xxxx.///o+    .|
|........s   `s/-o- :++------   -+`/-+`|
|........:    `s.d///::h        -+/  : |
|........+      /y     y   |    -+.  ` |
|................y     y   |    -+.....|
|................--------###------.....|
|......................................|
|                                      |
|       o                              |
|      +++                             |
|       ^                              |
|                    o                 |
|                   -+-                |
|                    "                 |
|                                      |
|                                      |
|                                      |
|                                      |
|                                     `|
|                `````       :::-.```` |
|``````````````         ````-          |
|````````````            `:::::       -|
|````                 `.               |
|       ```````````       ::.     `````|
|                                      |
----------------------------------------
```
When the viewport is larger or equal than the scene dimension, the whole scene will be displayed

#### Inventory
Refer `config_item.py` to configure item set

#### FAQ
1. Get error like `_curses.error: addwstr() returned ERR`

Make sure the size of the terminal window is larger than viewport in game (default is 80 chars * 30 lines).

### Acknowledgement
![TianLong](img/tianlongbabu.jpg)

