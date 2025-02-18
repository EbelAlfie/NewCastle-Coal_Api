from const.PacketType import PacketType
from const.WhateverType import WhatEverType 
from const.Symbols import Symbols
from json import loads
from module.data.PacketModel import PacketModel
from functools import reduce
from module.decoder.DataDecoder import DataDecoder
from array import array
from module.data.AttributeWrapper import AttributeWrapper

class PacketDecoder:
    attributesPS = [ #attribute p/s
        AttributeWrapper(name="symbol", type="string"),
        AttributeWrapper(name="sequence", type="int32"),
        AttributeWrapper(name="name", type="string"),
        AttributeWrapper(name="exchange", type="string"),
        AttributeWrapper(name="unitCode", type="string"),
        AttributeWrapper(name="pointValue", type="float"),
        AttributeWrapper(name="tickIncrement", type="int8"),
        AttributeWrapper(name="root", type="string"),
        AttributeWrapper(name="month", type="string"),
        AttributeWrapper(name="year", type="int8"),
    ]

    attributesQS = [
        AttributeWrapper(name="symbol", type="string"),
        AttributeWrapper(name="sequence", type="int32"),
        AttributeWrapper(name="flag", type="string"),
        AttributeWrapper(name="mode", type="string"),
        AttributeWrapper(name="day", type="string"),
        AttributeWrapper(name="dayNum", type="uint8"),
        AttributeWrapper(name="session", type="string"),
        AttributeWrapper(name="sessionT", type="boolean"),
        AttributeWrapper(name="sessionDateDisplay", type="string"),
        AttributeWrapper(name="bidPrice", type="double"),
        AttributeWrapper(name="bidSize", type="uint32"),
        AttributeWrapper(name="askPrice", type="double"),
        AttributeWrapper(name="askSize", type="uint32"),
        AttributeWrapper(name="lastPrice", type="double"),
        AttributeWrapper(name="lastPriceT", type="double"),
        AttributeWrapper(name="tradePrice", type="double"),
        AttributeWrapper(name="tradeSize", type="uint32"),
        AttributeWrapper(name="tradeTime", type="date"),
        AttributeWrapper(name="tradeTimeActual", type="uint48"),
        AttributeWrapper(name="tradeTimeDisplay", type="string"),
        AttributeWrapper(name="tradeDateDisplay", type="string"),
        AttributeWrapper(name="numberOfTrades", type="uint32"),
        AttributeWrapper(name="settlementPrice", type="double"),
        AttributeWrapper(name="openPrice", type="double"),
        AttributeWrapper(name="highPrice", type="date"),
        AttributeWrapper(name="lowPrice", type="double"),
        AttributeWrapper(name="volume", type="uint32"),
        AttributeWrapper(name="volumePrevious", type="uint32"),
        AttributeWrapper(name="openInterest", type="uint32"),
        AttributeWrapper(name="time", type="date"),
        AttributeWrapper(name="timeActual", type="uint48"),
        AttributeWrapper(name="timeDisplay", type="string"),
        AttributeWrapper(name="timeDateDisplay", type="string"),
        AttributeWrapper(name="previousPrice", type="double"),
        AttributeWrapper(name="previousPricePreview", type="double"),
        AttributeWrapper(name="previousPreviousPrice", type="double"),

        AttributeWrapper(name="previousSettlementPrice", type="double"),
        AttributeWrapper(name="previousOpenPrice", type="double"),
        AttributeWrapper(name="previousHighPrice", type="double"),
        AttributeWrapper(name="previousLowPrice", type="double"),
        AttributeWrapper(name="previousTime", type="date"),
        AttributeWrapper(name="previousTimeDateDisplay", type="string"),
        AttributeWrapper(name="online", type="boolean"),
    ]
    types = [
        "CONNECT", 
        "DISCONNECT", 
        "EVENT", 
        "ACK", 
        "ERROR", 
        "BINARY_EVENT", 
        "BINARY_ACK"
    ]

    def addDecoder(self, data: str):
        decoded = self.decodePacket(data)
        return decoded

    def decodePacket(self, data: str) -> PacketModel:
        r = 0
        newDecoder = PacketModel(type=int(data[0]))
        if (self.types[newDecoder.type] == None): 
            print("Unknown packet type")
        if (PacketType.BINARY_EVENT == newDecoder.type or PacketType.BINARY_ACK == newDecoder.type):
            r += 1
            while r < len(data) and data[r] != "-":
                r += 1

            n = r + 1
            o = data[n:r]
            if (not o.isnumeric()) or r >= len(data) or data[r] != "-":
                raise ValueError("Illegal attachments")
            
            print("attachments")
            newDecoder.attachments = int(o)
        if (len(data) > r + 1 and data[r + 1] == '/'):
            r += 1
            while r < len(data):
                i = data[r]
                if i == "," or r == len(data):
                    break
                r += 1
            print("nsp")
            newDecoder.nsp = data[n:r]
        else :
            newDecoder.nsp = '/'
        
        p = data[r + 1] if (len(data) > r + 1) else ""
        if (p != "" and p.isnumeric()):
            r += 1
            while r < len(data):
                i = data[r]
                if i is None or not i.isdigit():
                    r -= 1
                    break
                if r == len(data) - 1:
                    break
                r += 1

            print("ID")
            newDecoder.id = int(data[n:r + 1])
        
        r += 1
        if (len(data) > r and data[r] != ''): 
            try:
                jsonData = loads(data[r:])
                print(f"HERE")
                newDecoder.data = jsonData
            except:
                print("Yahhh")
        
        return newDecoder

    def onDecoded(self, data: list) -> dict[str, str]:
        match (data[0]):
            case WhatEverType.PS.value :
                return DataDecoder(self.attributesPS).decode(data[1])
            case WhatEverType.QS.value :
                return DataDecoder(self.attributesQS).decode(data[1])
            case WhatEverType.QD.value :
                return
            case WhatEverType.BS.value :
                return
            case WhatEverType.ES.value :
                return
            case WhatEverType.T.value :
                return
            case WhatEverType.R.value :
                return