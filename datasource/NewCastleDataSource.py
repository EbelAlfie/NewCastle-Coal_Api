import websockets
import asyncio
from string import Template
from const.ConnectionStatus import ConnectionStatus

class NewCastleDataSource :
    ws: websockets.ClientConnection

    def __init__(self, symbols: list[str]) -> None:
        self.wsUrl = "wss://jerq-aggregator-prod.aws.barchart.com/socket.io/?EIO=3&transport=websocket"
        self.symbols = symbols
        self.pingTimer = None
        self.connectionStatus: ConnectionStatus = ConnectionStatus.Disconnected
    
    async def openWebSocket(self, onWSMessage):
        async def connectWebsocket():
            async with websockets.connect(self.wsUrl) as websocket:
                self.ws = websocket
                while True :
                    message = await websocket.recv()
                    print(f"Raw: {message}")
                    await onWSMessage(message)                

        try: 
            await connectWebsocket()
        except websockets.exceptions.ConnectionClosedError as err:
            self.connectionStatus = ConnectionStatus.Disconnected
            print("Error, reconnecting")
            await asyncio.sleep(1)
            self.connectionStatus = ConnectionStatus.Connecting
            await connectWebsocket()
    
    async def sendRequest(self):
        if (self.ws == None): return 

        jsonStr = Template('42["subscribe/symbols",{"subscribeToPrices":true,"symbols":[${symbols}]}]')
        event = jsonStr.substitute(symbols= ', '.join(f"\"{symbol}\"" for symbol in self.symbols))
        await self.ws.send(event)

    def setPing(self, interval: int):
        print("Ping")
        self.clearPing()
        self.pingTimer = asyncio.get_event_loop().create_task(self.pingTask(interval)) 

    async def pingTask(self, interval):
        await asyncio.sleep(interval / 1000.)
        await self.sendPing()

    def clearPing(self):
        if (self.pingTimer != None) :
            self.pingTimer.cancel()
        self.pingTimer = None

    async def sendPing(self):
        await self.ws.send("2")

    def onOpen(self):
        self.connectionStatus = ConnectionStatus.Connected       

    
