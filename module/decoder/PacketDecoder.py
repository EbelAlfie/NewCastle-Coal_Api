from module.const.PacketType import PacketType
from module.const.WhateverType import WhatEverType 
from module.const.Symbols import Symbols
from json import loads
from module.decoder.Decoder import Decoder
from functools import reduce
from module.decoder.DataDecoder import DataDecoder
from array import array

class PacketDecoder:
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
        decoded = self.Sb(data)
        print(decoded.data)
        print(type(decoded.data))

        if (decoded.data == None): return
        PacketDecoder().onDecoded(decoded.data)


    def Sb(self, data: str) -> Decoder:
        r = 0
        newDecoder = Decoder(type=int(data[0]))
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
                return DataDecoder().decode(data[1])
            case WhatEverType.QS.value :
                # DataDecoder().decode(data[1])
                return
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