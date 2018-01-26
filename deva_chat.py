from deva_const import ChatTextType, ChatBoxConst
from deva_menu import Deva_Menu, Deva_MenuMap

class Deva_Chat:
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

                    self._activeMenu = Deva_Menu(Deva_MenuMap(mmap), (ChatBoxConst.X, 0))
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

