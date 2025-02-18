class PacketModel:
    type: int
    attachments: int
    nsp: str
    id: int
    data: any

    def __init__(self, type):
        self.type = type
        self.type = 0
        self.attachments= 0 
        self.nsp = ""
        self.id = 0
        self.data = None