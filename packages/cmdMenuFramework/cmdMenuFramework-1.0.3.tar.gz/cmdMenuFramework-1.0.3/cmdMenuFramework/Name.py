from cmdMenuFramework.Instruction import Instruction
from cmdMenuFramework.InstType import InstType
from cmdMenuFramework.Printer import Printer

class Name(Instruction):
    
    def __init__(self,  context, name, content):
        super(Name, self).__init__(context, InstType.name, name, content)
        
    def execute(self):
        
        self.context.path.addInstruction(self)
        
        if type(self.content) == dict:
            if (len(self.content) != 1):
                Printer.printError ("Multiple embedded instructions: use a block instruction instead", self.context)
                self.context.path.goBack()
                return None
            for id in self.content:
                i = Instruction.letterToInstruction(id[:1], id, self.content[id], self.context)
                if i is None: 
                    self.context.path.goBack()
                    return None
                name = i.execute()
            
        else:   
            name = self.content
            
        self.context.path.goBack()
        return str(name)