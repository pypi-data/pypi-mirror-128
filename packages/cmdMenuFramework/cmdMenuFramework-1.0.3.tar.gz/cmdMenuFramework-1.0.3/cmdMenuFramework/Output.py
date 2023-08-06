from cmdMenuFramework.Instruction import Instruction
from cmdMenuFramework.InstType import InstType
from cmdMenuFramework.Printer import Printer

class Output(Instruction):
    
    def __init__(self, context, name, content):
        super(Output, self).__init__(context, InstType.output, name, content)
         
    
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
            
        self.context.output = output
        self.context.path.goBack()
        return output