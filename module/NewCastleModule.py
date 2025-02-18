from const.OperationType import OperationType
from module.data.MessageWrapper import MessageWrapper
from module.data.PacketModel import PacketModel
from module.decoder.PacketDecoder import PacketDecoder
from datasource.NewCastleDataSource import NewCastleDataSource

class NewCastleModule :
    def __init__(self) -> None:
        self.symbols = ["LQH25"]
        self.dataSource = NewCastleDataSource(self.symbols)
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
        await self.dataSource.openWebSocket(self.onWSMessage)                              
    
    async def onWSMessage(self, message) -> MessageWrapper:
        decodedMessage: PacketModel = self.decodeMessage(message)
        # print(f"Type: {decodedMessage.type.name}")
        # print(f"Message: {decodedMessage.data}\n")

        match decodedMessage.type:
            case OperationType.Open:
                return 
            case OperationType.Message:
                await self.onMessage(decodedMessage)
                return 
            case _:
               return 
    
    async def onMessage(self, message: PacketModel):
        decodedPacket = PacketDecoder().addDecoder(message.data)
        await self.dataSource.sendRequest() if (message.data == "0") else {}
        if (decodedPacket.data == None): return 
        PacketDecoder().onDecoded(decodedPacket.data)

    
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
        

    
