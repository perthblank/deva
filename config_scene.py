from deva_const import MapGridType, TriggerType, ColorId

main = {
    'rolePos': [20, 16],
    'dimension': [95, 35],
    'nodes': [
        {
            'meshName': 'npc',
            'pos': [25, 16],
            'zindex': 4,
            'colorId': ColorId.CYAN,
            'gridType': MapGridType.BLOCK,
            'triggerType': TriggerType.CHAT,
            'triggerItem': 'chat0',
            'bold': True,
        },
        {
            'meshName': 'rock',
            'pos': [27, 8],
            'zindex': 3,
            'colorId': ColorId.MAGENTA,
            'gridType': MapGridType.BLOCK,
            'bold': True,
        },
        {
            'meshName': 'rock',
            'pos': [52, 8],
            'zindex': 3,
            'colorId': ColorId.MAGENTA,
            'gridType': MapGridType.BLOCK,
            'bold': True,
        },
        {
            'meshName': 'house',
            'pos': [35, 6],
            'zindex': 4,
            'colorId': ColorId.YELLOW,
            'gridType': MapGridType.BLOCK,
            'triggerType': TriggerType.CHANGE_SCENE,
            'triggerItem': 'guilinMain',
            'bold': True,
        },
        {
            'meshName': 'grass',
            'pos': [5, 5],
            'zindex': 0,
            'colorId': ColorId.GREEN,
            'gridType': MapGridType.FREE,
        },
        {
            'meshName': 'river',
            'pos': [5, 26],
            'zindex': 3,
            'colorId': ColorId.BLUE,
            'gridType': MapGridType.FREE,
            'bold': True,
        },
        {
            'meshName': 'pickable',
            'pos': [65,7],
            'zindex': 5,
            'colorId': ColorId.YELLOW,
            'gridType': MapGridType.BLOCK,
            'triggerType': TriggerType.ITEM,
            'triggerItem': 'jinchuangyao',
        },
        {
            'meshName': 'pickable',
            'pos': [64,11],
            'zindex': 5,
            'colorId': ColorId.YELLOW,
            'gridType': MapGridType.BLOCK,
            'triggerType': TriggerType.ITEM,
            'triggerItem': 'herb',
        },
        {
            'meshName': 'pickable',
            'pos': [30,6],
            'zindex': 5,
            'colorId': ColorId.YELLOW,
            'gridType': MapGridType.BLOCK,
            'triggerType': TriggerType.ITEM,
            'triggerItem': 'sword',
        },
        {
            'meshName': 'pickable',
            'pos': [22,26],
            'zindex': 5,
            'colorId': ColorId.YELLOW,
            'gridType': MapGridType.BLOCK,
            'triggerType': TriggerType.ITEM,
            'triggerItem': 'fanri',
        },
        {
            'meshName': 'pickable',
            'pos': [19,27],
            'zindex': 5,
            'colorId': ColorId.YELLOW,
            'gridType': MapGridType.BLOCK,
            'triggerType': TriggerType.ITEM,
            'triggerItem': 'shoe',
        },
        {
            'meshName': 'pickable',
            'pos': [19,17],
            'zindex': 5,
            'colorId': ColorId.YELLOW,
            'gridType': MapGridType.BLOCK,
            'triggerType': TriggerType.ITEM,
            'triggerItem': 'armor',
        },
    ]
}

guilinMain = {
    'rolePos': [10, 20],
    'dimension': [80, 80],
    'nodes': [
        {
            'meshName': 'temple',
            'pos': [15, 6],
            'zindex': 4,
            'colorId': ColorId.RED,
            'gridType': MapGridType.BLOCK,
            'triggerType': TriggerType.CHANGE_SCENE,
            'triggerItem': 'main',
            'bold': True
        },
        {
            'meshName': 'grass',
            'pos': [5, 5],
            'zindex': 3,
            'colorId': ColorId.GREEN,
            'gridType': MapGridType.FREE,
        },
        {
            'meshName': 'grass',
            'pos': [5, 10],
            'zindex': 3,
            'colorId': ColorId.GREEN,
            'gridType': MapGridType.FREE,
        },
    ]
}

SceneMap = {
        'main': main,
        'guilinMain': guilinMain,
        }

