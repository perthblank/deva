SceneConfig0 = {
    'rolePos': [20, 20],
    'item': [
        {
            'meshName': 'mountain',
            'pos': [30, 10],
            'zindex': 6
        },
        {
            'meshName': 'mountain',
            'pos': [40, 20],
            'zindex': 6
        },
    
    ]
}


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

