from module.const.Symbols import Symbols
from module.decoder import Decoder
from module.data.AttributeWrapper import AttributeWrapper
from array import array
from functools import reduce

class DataDecoder:
    curSymbol: str 
    attributes: array

    def __init__(self):
        self.absent = Symbols.ABSENT.value
        self.attributes = [
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

    def decode(self, data: str):
        reduced = self.decodeData(data) #reduce(self.decodePS, data.split(Symbols.DELIMITER.value))
        print(f"reduced {reduced}")
    
    def decodeData(self, data: str) :
        values = data.split(Symbols.DELIMITER.value)
        jsonData = {}
        for index, currentValue in enumerate(values):
            symbol = currentValue[0] #Char at 0
            if (symbol != Symbols.ABSENT.value):
                attribute = self.attributes[index] #, self.curSymbol
                
                if (symbol == Symbols.UNDEFINED.value):
                    self.curSymbol = None
                elif (symbol == Symbols.NULL.value) :
                    self.curSymbol = None
                else:
                    self.curSymbol = currentValue[1:]

                jsonData[attribute.name] = self.curSymbol
        
        print(jsonData)
        return jsonData
        