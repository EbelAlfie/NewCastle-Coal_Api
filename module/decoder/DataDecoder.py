from module.const.Symbols import Symbols
from module.decoder import Decoder
from module.data.AttributeWrapper import AttributeWrapper
from array import array
from functools import reduce

class DataDecoder:
    curSymbol: str 
    attributes: array

    index: int

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
        self.index = 0 #ngakalin
        reduced = reduce(self.decodePS, data.split(Symbols.DELIMITER.value))
        print(f"reduced {reduced}")
    
    def decodePS(self, initial, current):
        symbol = current[0]
        if (symbol != Symbols.ABSENT.value):
            attribute = self.attributes[self.index] #, self.curSymbol
            
            if (symbol == Symbols.UNDEFINED.value):
                self.curSymbol = None
            elif (symbol == Symbols.NULL.value) :
                self.curSymbol = None
            else:
                self.curSymbol = current[1:]

            initial[attribute.name] = self.curSymbol

        self.index += 1

        return initial