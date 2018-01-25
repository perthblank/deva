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

