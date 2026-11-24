from uuid import uuid8
from time import time

class Project:
    def __init__(self, name: str):
        self.id = uuid8(int(time()))
        self.name = name
        pass
    pass
