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
    'rolePos': [20, 20],
    'item': [
        {
            'meshName': 'mountain',
            'pos': [30, 10],
            'zindex': 4,
            'colorId': ColorId.GREEN,
            'gridType': MapGridType.BLOCK,
        },
        {
            'meshName': 'mountain',
            'pos': [40, 20],
            'zindex': 4,
            'colorId': ColorId.GREEN,
            'gridType': MapGridType.BLOCK,
        },
        {
            'meshName': 'house',
            'pos': [80, 10],
            'zindex': 4,
            'colorId': ColorId.YELLOW,
            'gridType': MapGridType.TRIGGER,
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

