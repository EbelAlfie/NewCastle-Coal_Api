import asyncio
from module.NewCastleModule import NewCastleModule

if __name__ == "__main__":
    module = NewCastleModule()
    asyncio.run(module.openWebSocket())