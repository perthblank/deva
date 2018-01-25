from dgsd_const import ChatTextType, ChatBoxConst
from dgsd_menu import DGSD_Menu, DGSD_MenuMap

class DGSD_Chat:
    def __init__(self, chatlist):
        self.chatMap = {}
        for chat in chatlist:
            self.chatMap[chat['id']] = chat

        self.opt = 0
        self._activeMenu = None

    def jumpTo(self, id):
        def j():
            self.opt = id
        return j

    def next(self):
        if self._activeMenu is None:
            if 'goto' in self.currentTextItem:
                self.opt = self.currentTextItem['goto']
            else:
                self.opt += 1
            if self.opt < len(self.chatMap):
                textItem = self.chatMap[self.opt]
                mmap = {}
                if textItem['type'] == ChatTextType.BRANCH:
                    assert len(textItem['branch']) == len(textItem['branch_to'])
                    for i in range(len(textItem['branch'])):
                        mmap[textItem['branch'][i]] = self.jumpTo(textItem['branch_to'][i])

                    self._activeMenu = DGSD_Menu(DGSD_MenuMap(mmap), (ChatBoxConst.X, 0))
                return True
            self.reset()
            return None
        else:
            self._activeMenu.callCurrent()
            self._activeMenu = None
            return True

    def arrUp(self):
        if self._activeMenu:
            self._activeMenu.arrUp()

    def arrDown(self):
        if self._activeMenu:
            self._activeMenu.arrDown()

    @property
    def branchMenu(self):
        return self._activeMenu

    @property
    def currentTextItem(self):
        return self.chatMap[self.opt]

    def reset(self):
        self.opt = 0


chat0 = [
    {
        'id': 0,
        'type': ChatTextType.STATEMENT,
        'title': 'Welcome To DGSD. \nA Game and engine',
    },
    {
        'id': 1,
        'type': ChatTextType.STATEMENT,
        'title': 'You are the HERO, while \n I\'m an npc LOL',
    },
    {
        'id': 2,
        'type': ChatTextType.BRANCH,
        'title': 'Make a choice here',
        'branch': ['Anything', 'Bonus', 'Cat'],
        'branch_to': [3, 4, 5]
    },
    {
        'id': 3,
        'type': ChatTextType.STATEMENT,
        'title': 'Angthing you say?',
        'goto': 100,
    },
    {
        'id': 4,
        'type': ChatTextType.STATEMENT,
        'title': '$100,000',
        'goto': 100,
    },
    {
        'id': 5,
        'type': ChatTextType.STATEMENT,
        'title': 'MOW!',
        'goto': 100,
    },
]

ChatMap = {
        'chat0': DGSD_Chat(chat0)
    }
