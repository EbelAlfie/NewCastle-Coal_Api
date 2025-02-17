import asyncio
from module.NewCastleModule import NewCastleModule

if __name__ == "__main__":
    module = NewCastleModule()
    asyncio.get_event_loop().run_until_complete(module.openWebSocket())