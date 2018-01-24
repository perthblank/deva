class MoveKey:
    UP = 'w'
    DOWN = 's'
    LEFT = 'a'
    RIGHT = 'd'

Directions = {
    MoveKey.UP: [0, -1],
    MoveKey.DOWN: [0, 1],
    MoveKey.LEFT: [-1, 0],
    MoveKey.RIGHT: [1, 0],
}

class MyKeyCode:
    ENTER = 10
    ESC = 27

class MenuConst:
    X = 3
    Y = 1
    X_ARR = 1

class RoleConst:
    HEAD_X = 1
    HEAD_Y = 0

class SConst:
    BACK = 'Back'
    SAVE = 'Save'
    EXIT = 'Exit'

class ControlMode:
    GAME = 1
    MENU = 2

class MapGridType:
    FREE = '_'
    BLOCK = 2

class TriggerType:
    CHANGE_SCENE = 1
    CHAT = 2

class ColorId:
    YELLOW = 1
    GREEN = 2


TRIGGER_CHAR = '#'
