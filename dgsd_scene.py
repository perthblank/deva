import dgsd_color as dcolor

SceneConfig0 = {
    'rolePos': [20, 20],
    'item': [
        {
            'meshName': 'mountain',
            'pos': [30, 10],
            'zindex': 4,
            'colorId': dcolor.GREEN.id,
        },
        {
            'meshName': 'mountain',
            'pos': [40, 20],
            'zindex': 4,
            'colorId': dcolor.GREEN.id,
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

