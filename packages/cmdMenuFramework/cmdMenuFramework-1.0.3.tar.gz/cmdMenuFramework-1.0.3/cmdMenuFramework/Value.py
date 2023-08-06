from cmdMenuFramework.Instruction import Instruction
from cmdMenuFramework.InstType import InstType

class Value(Instruction):
    
    def __init__(self, context, name, content):
        super(Value, self).__init__(context, InstType.v, name, content)
        
    def execute(self):
        return self.content
    
    
    
    