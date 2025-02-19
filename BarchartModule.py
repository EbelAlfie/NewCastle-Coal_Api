import asyncio
from module.NewCastleModule import NewCastleModule

class BarChartModule:

    def __init__(self):
        self.module = NewCastleModule()

    async def establishWsConnection(self):
        print("Establishing websocket connection to barchart")
        await self.module.openWebSocket()

    async def requestData(self, onMessage):
        await self.module.sendRequest(onMessage)