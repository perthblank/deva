class DGSD_Scene:
    def __init__(self, sceneConfig):
        self._rolePos = sceneConfig['rolePos']
        self._item = sceneConfig['item']

    @property
    def rolePos(self):
        return self._rolePos

    @property
    def item(self):
        return self._item


from dgsd_const import MapGridType, TriggerType, ColorId

jiangnanMain = {
    'rolePos': [20, 16],
    'item': [
        {
            'meshName': 'npc',
            'pos': [25, 16],
            'zindex': 4,
            'colorId': ColorId.YELLOW,
            'gridType': MapGridType.BLOCK,
            'triggerType': TriggerType.CHAT,
            'triggerItem': 'chat0',
        },
        {
            'meshName': 'mountain',
            'pos': [20, 10],
            'zindex': 4,
            'colorId': ColorId.GREEN,
            'gridType': MapGridType.BLOCK,
        },
        {
            'meshName': 'mountain',
            'pos': [60, 10],
            'zindex': 4,
            'colorId': ColorId.GREEN,
            'gridType': MapGridType.BLOCK,
        },
        {
            'meshName': 'house',
            'pos': [35, 6],
            'zindex': 4,
            'colorId': ColorId.YELLOW,
            'gridType': MapGridType.BLOCK,
            'triggerType': TriggerType.CHANGE_SCENE,
            'triggerItem': 'guilinMain',
        },
    
    ]
}

guilinMain = {
    'rolePos': [40, 20],
    'item': [
        {
            'meshName': 'house',
            'pos': [30, 30],
            'zindex': 4,
            'colorId': ColorId.YELLOW,
            'gridType': MapGridType.BLOCK
        },
        {
            'meshName': 'house',
            'pos': [60, 20],
            'zindex': 4,
            'colorId': ColorId.YELLOW,
            'gridType': MapGridType.BLOCK
        },
    
    ]
}

SceneMap = {
        'jiangnanMain': jiangnanMain,
        'guilinMain': guilinMain,
        }

