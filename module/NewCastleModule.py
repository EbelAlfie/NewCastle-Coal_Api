from const.OperationType import OperationType
from module.data.MessageModel import MessageModel
from module.data.PacketModel import PacketModel
from module.decoder.PacketDecoder import PacketDecoder
from datasource.NewCastleDataSource import NewCastleDataSource
from const.ConnectionStatus import ConnectionStatus
from json import loads

#Decode the message from websocket into [MessageModel]
#Decode the message (If it is message) into [PacketModel]
#Decode the [PacketModel] into dictionary
class NewCastleModule :
    def __init__(self) -> None:
        self.symbols = ["LQH25"]
        self.dataSource = NewCastleDataSource(self.symbols)
        self.pingInterval = 0
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
    
    async def onWSMessage(self, message):
        decodedMessage: MessageModel = self.decodeMessage(message)
        
        match decodedMessage.type:
            case OperationType.Open:
                self.dataSource.onOpen()
                await self.onOpen(decodedMessage)
                return 
            case OperationType.Message:
                value = await self.onMessage(decodedMessage)
                print(value)
                return 
            case OperationType.Pong:
                print("Pong")
                self.dataSource.setPing(self.pingInterval)
                return 
            case _:
               return 
    
    async def onMessage(self, message: MessageModel):
        decodedPacket: PacketModel = PacketDecoder().addDecoder(message.data)
        await self.dataSource.sendRequest() if (message.data == "0") else {}
        if (decodedPacket.data == None): return 
        return PacketDecoder().onDecoded(decodedPacket.data)

    async def onOpen(self, message: MessageModel): 
        try:
            print(message.data)
            jsonData= loads(message.data)
            pingInterval = jsonData.get("pingInterval")
            if (pingInterval != None or pingInterval != ""):
                self.pingInterval = pingInterval
                self.dataSource.setPing(int(pingInterval))
        except ValueError:
            print("onOpen: Decode Json error")

    async def sendRequest(self, onMessage):
        self.messageCallback = onMessage
        if (self.dataSource.connectionStatus != ConnectionStatus.Connected): 
            await self.openWebSocket()

        await self.dataSource.sendRequest()

    def decodeMessage(self, packet: str, type = "") -> MessageModel: 
        if packet == "": return ""

        if packet[0] == "b" :
            return ""#self.decodeBase64Packet(packet[1:])
        
        operation = int(packet[0]) if packet[0].isnumeric() else ""
        return MessageModel(
            type= self.operations[operation],
            data= packet[1:]
        ) if operation != "" or self.operations[operation] != None else MessageModel(
            type= OperationType.Error,
            data= "Error :("
        )
        
    # def decodeBase64Packet(data):
        

    
