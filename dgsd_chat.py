from dgsd_const import ChatTextType, ChatBoxConst
from dgsd_menu import DGSD_Menu, DGSD_MenuMap

class DGSD_Chat:
    def __init__(self, chatlist):
        self.chatMap = {}
        for chat in chatlist:
            self.chatMap[chat['id']] = chat

        self.opt = None
        self._activeMenu = None
        self.statusSet = set()

        self.next()

    def jumpTo(self, id):
        def j():
            self.opt = id
        return j

    def valid(self):
        if not 'exclude_status' in self.currentTextItem:
            return True

        for status in self.currentTextItem['exclude_status']:
            if status in self.statusSet:
                return False

        return True

    def addStatusCode(self):
        if 'status_code' in self.currentTextItem:
            self.statusSet.add(self.currentTextItem['status_code'])


    def next(self):
        if self._activeMenu is None:
            if self.opt is None:
                self.opt = 0
            else:
                # add status code for current
                self.addStatusCode()

                if 'goto' in self.currentTextItem:
                    self.opt = self.currentTextItem['goto']
                else:
                    self.opt += 1

            while self.opt < len(self.chatMap) and not self.valid():
                self.opt += 1
            if self.opt < len(self.chatMap):
                textItem = self.chatMap[self.opt]

                if textItem['type'] == ChatTextType.BRANCH:
                    assert len(textItem['branch']) == len(textItem['branch_to'])
                    mmap = {}
                    for i in range(len(textItem['branch'])):
                        mmap[textItem['branch'][i]] = self.jumpTo(textItem['branch_to'][i])

                    self._activeMenu = DGSD_Menu(DGSD_MenuMap(mmap), (ChatBoxConst.X, 0))
                return True
            self.reset()
            return None
        else:
            self.addStatusCode()
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

    @property
    def activedStatus(self):
        return list(self.statusSet)

    def reset(self):
        self.opt = None
        self._activeMenu = None
        self.next()


chat0 = [
    {
        'id': 0,
        'type': ChatTextType.STATEMENT,
        'title': 'Welcome To DGSD. \nA Game and engine',
        'exclude_status': [22],
    },
    {
        'id': 1,
        'type': ChatTextType.STATEMENT,
        'title': 'You are the HERO, while \n I\'m an npc LOL',
        'exclude_status': [22],
    },
    {
        'id': 2,
        'type': ChatTextType.BRANCH,
        'title': 'Make a choice here',
        'branch': ['Anything', 'Bonus', 'Cat'],
        'branch_to': [3, 4, 5],
        'status_code': 22,
        'exclude_status': [22],
    },
    {
        'id': 3,
        'type': ChatTextType.STATEMENT,
        'title': 'Angthing you say?',
        'goto': 100,
        'status_code': 33,
        'exclude_status': [44, 55],
    },
    {
        'id': 4,
        'type': ChatTextType.STATEMENT,
        'title': '$100,000',
        'goto': 100,
        'status_code': 44,
        'exclude_status': [33, 55],
    },
    {
        'id': 5,
        'type': ChatTextType.STATEMENT,
        'title': 'MOW!',
        'goto': 100,
        'status_code': 55,
        'exclude_status': [44, 33],
    },
]

ChatMap = {
        'chat0': DGSD_Chat(chat0)
    }
