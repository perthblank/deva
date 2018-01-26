from deva_const import ChatTextType
from deva_chat import Deva_Chat

chat0 = [
    {
        'id': 0,
        'type': ChatTextType.STATEMENT,
        'title': 'Welcome To Deva. \nA Game and engine',
        'exclude_status': [22],
    },
    {
        'id': 1,
        'type': ChatTextType.STATEMENT,
        'title': 'You are the HERO, while \nI\'m an npc\nLOL',
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
        'chat0': Deva_Chat(chat0)
    }

