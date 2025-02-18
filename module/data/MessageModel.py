from const.OperationType import OperationType

class MessageModel:
    type: OperationType
    data: str

    def __init__(self, type: OperationType, data: str):
        self.type = type
        self.data = data