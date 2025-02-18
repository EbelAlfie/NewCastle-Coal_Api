from const.Symbols import Symbols
from module.data.AttributeWrapper import AttributeWrapper
from array import array
from json import dumps

class DataDecoder:
    curSymbol: str 
    attributes: array

    def __init__(self, attributes):
        self.absent = Symbols.ABSENT.value
        self.attributes = attributes

    def decode(self, data: str):
        reduced = self.decodeData(data)
        print(f"{dumps(reduced)}")
    
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
        
        return jsonData
        