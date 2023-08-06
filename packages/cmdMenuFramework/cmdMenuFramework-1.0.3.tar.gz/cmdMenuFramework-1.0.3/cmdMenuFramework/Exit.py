from cmdMenuFramework.Instruction import Instruction
from cmdMenuFramework.InstType import InstType
from cmdMenuFramework.Printer import Printer

class Exit(Instruction):
    
    def __init__(self, context, name, content):
        super(Exit, self).__init__(context, InstType.exit, name, content)
         
    
    def execute(self):
        self.context.path.addInstruction(self)
        
        output = None
        
        if self.content is not None: 
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
                    output = i.execute()
            
            else: 
                output = self.content
            
        if type(output) != bool:
            Printer.printError ("Exit instruction expects a boolean, got "+str(type(output))+' instead', self.context)
            self.context.path.goBack()
            return None
        
        self.context.exit = output
        self.context.path.goBack()
        return output