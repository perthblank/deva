class KeyCode:
    ENTER = 10
    ESC = 27
    W = ord('w')
    S = ord('s')
    A = ord('a')
    D = ord('d')
    I = ord('i')


class MoveKey:
    UP      = KeyCode.W
    DOWN    = KeyCode.S
    LEFT    = KeyCode.A
    RIGHT   = KeyCode.D

Directions = {
    MoveKey.UP: [0, -1],
    MoveKey.DOWN: [0, 1],
    MoveKey.LEFT: [-1, 0],
    MoveKey.RIGHT: [1, 0],
}

class MeshType:
    STATIC = 1
    RANDOM = 2
    ANIMATE_ON_TOUCH = 3
    ANIMATE_AUTO = 4

class MenuConst:
    X = 3
    Y = 1

    TRIGGER_BY_ENTER = 1
    TRIGGER_BY_HOVER = 2

class RoleConst:
    COLLIDE_OFFSETS = [(1, 0), (0, 1), (2, 1), (1, 2)]

class SConst:
    BACK = 'Back'
    SAVE = 'Save'
    EXIT = 'Exit'

class ControlMode:
    MOVE = 1
    MENU = 2
    CHAT = 3
    INVENTORY = 4

class MapGridType:
    FREE    = '_'
    BLOCK   = 2

class TriggerType:
    CHANGE_SCENE = 1
    CHAT = 2
    ITEM = 3

class ColorId:
    YELLOW  = 1
    GREEN   = 2
    BLUE    = 3
    RED     = 4
    MAGENTA = 5
    CYAN    = 6

TRIGGER_CHAR = '#'

ROLE_ZINDEX = 5

class ChatTextType:
    STATEMENT   = 1
    BRANCH      = 2

class ChatBoxConst:
    X = 4

class ItemType:
    WEAPON      = 'Weapon'
    ARMOR       = 'Armor'
    MEDICINE    = 'Medicine'

class InventoryConst:
    MENU_POS = (5, 5)
    LIST_POS = (20, 5)

class ListOf:
    CHAT = 1
    MESH = 2

