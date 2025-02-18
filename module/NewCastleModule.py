import websockets
from module.const.OperationType import OperationType
from module.const.PacketType import PacketType
from module.data.MessageWrapper import MessageWrapper
from string import Template
from module.decoder.PacketDecoder import PacketDecoder
from module.decoder.Decoder import Decoder

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
                print(f"Raw: {message}")

                packet = await self.onMessage(message, websocket)                
                        
    
    async def onMessage(self, message, websocket: websockets.ClientConnection) -> MessageWrapper:
        decodedMessage = self.decodeMessage(message)
        print(f"Type: {decodedMessage.type.name}")
        print(f"Message: {decodedMessage.data}\n")

        match decodedMessage.type:
            case OperationType.Open:
                return decodedMessage
            case OperationType.Message:
                PacketDecoder().addDecoder(decodedMessage.data)
                await self.onConnected(websocket) if (decodedMessage.data == "0") else {}
                return decodedMessage
            case _:
               return decodedMessage
        return decodedMessage
    
    async def onConnected(self, websocket: websockets.ClientConnection):
        jsonStr = Template('42["subscribe/symbols",{"subscribeToPrices":true,"symbols":[${symbols}]}]')
        event = jsonStr.substitute(symbols= ', '.join(f"\"{symbol}\"" for symbol in self.symbols))
        await websocket.send(event)

    def decodeMessage(self, packet: str, type = "") -> MessageWrapper: 
        if packet == "": return ""

        if packet[0] == "b" :
            return ""#self.decodeBase64Packet(packet[1:])

        operation = int(packet[0]) if packet[0].isnumeric() else ""
        return MessageWrapper(
            type= self.operations[operation],
            data= packet[1:]
        ) if operation != "" or self.operations[operation] != None else MessageWrapper(
            type= OperationType.Error,
            data= "Error :("
        )
        

    # def decodeBase64Packet(data):
        

    
