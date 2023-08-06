

from enum import Enum

class InstType(Enum):
    prompt = 0
    choice = 1
    question = 2
    action = 3
    set = 4
    get = 5
    setDefault = 6
    getDefault = 7
    input = 8
    output = 9
    name = 10
    block = 11
    loop = 12
    exit = 13
    finish = 14
    wait = 15
    exception = 16
    host = 17
    v = 18
    