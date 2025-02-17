import websockets
from module.const.OperationType import OperationType
from module.data.MessageWrapper import MessageWrapper

class NewCastleModule :
    def __init__(self) -> None:
        self.wsUrl = "wss://jerq-aggregator-prod.aws.barchart.com/socket.io/?EIO=3&transport=websocket"
        self.symbols = ["LQH25"]
        self.operations= {
            0 : OperationType.Open,
            1 : OperationType.Close,
            2 : OperationType.Ping,
            3 : OperationType.Pong,
            4 : OperationType.Message,
            5 : OperationType.Error,
            6 : OperationType.Noop,
        }
    
    async def openWebSocket(self):
        async with websockets.connect(self.wsUrl) as websocket:
            while True :
                message = await websocket.recv()
                print(f"Received: {message}")
                self.onMessage(message)
    
    def onMessage(self, message):
        decodedMessage = self.decodePacket(message)
        print(decodedMessage.data)

    def decodePacket(self, packet: str, type = "") -> MessageWrapper: 
        if packet == "": return ""

        if packet[0] == "b" :
            return ""#self.decodeBase64Packet(packet[1:])

        operation = int(packet[0]) if packet[0].isnumeric() else ""
        return MessageWrapper(
            type= self.operations[operation],
            data= packet[1]
        ) if operation != "" or self.operations[operation] != None else MessageWrapper(
            type= OperationType.Error,
            data= "Error :("
        )

    # def decodeBase64Packet(data):
        

    
