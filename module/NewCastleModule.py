import websockets

class NewCastleModule :
    def __init__(self) -> None:
        self.wsUrl = "wss://jerq-aggregator-prod.aws.barchart.com/socket.io/?EIO=3&transport=websocket"
    
    async def openWebSocket(self):
        async with websockets.connect(self.wsUrl) as websocket:
            message = await websocket.recv()
            print(f"Received: {message}")
    
