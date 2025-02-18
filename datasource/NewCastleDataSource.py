import websockets
from string import Template

class NewCastleDataSource :
    ws: websockets.ClientConnection

    def __init__(self, symbols: list[str]) -> None:
        self.wsUrl = "wss://jerq-aggregator-prod.aws.barchart.com/socket.io/?EIO=3&transport=websocket"
        self.symbols = symbols
    
    async def openWebSocket(self, onWSMessage):
        async with websockets.connect(self.wsUrl) as websocket:
            self.ws = websocket
            while True :
                message = await websocket.recv()
                print(f"Raw: {message}")
                await onWSMessage(message)                
    
    async def sendRequest(self):
        if (self.ws == None): return 

        jsonStr = Template('42["subscribe/symbols",{"subscribeToPrices":true,"symbols":[${symbols}]}]')
        event = jsonStr.substitute(symbols= ', '.join(f"\"{symbol}\"" for symbol in self.symbols))
        await self.ws.send(event)
                

    
