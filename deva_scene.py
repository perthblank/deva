class Deva_Scene:
    def __init__(self, sceneConfig):
        self._rolePos = sceneConfig['rolePos']
        self._item = sceneConfig['nodes']
        self._dimension = sceneConfig['dimension']

    @property
    def rolePos(self):
        return self._rolePos

    @property
    def meshNodes(self):
        return self._item

    @property
    def width(self):
        return self._dimension[0]

    @property
    def height(self):
        return self._dimension[1]

