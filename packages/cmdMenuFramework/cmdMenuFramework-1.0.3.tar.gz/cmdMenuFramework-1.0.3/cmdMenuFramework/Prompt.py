from cmdMenuFramework.Instruction import Instruction
from cmdMenuFramework.InstType import InstType
from cmdMenuFramework.Printer import Printer

class Prompt(Instruction):
    
    def __init__(self, context, name, content):
        super(Prompt, self).__init__(context, InstType.prompt, name, content)
        
    def execute(self):
        """Runs the instruction. 
        
        If it contains a dictionnary, executes the first instruction from this dictionnary, and prints its return value.
        If it contains anything else, prints str(value)."""
        
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
                msg = i.execute()
            
        else:   
            msg = self.content
            
        Printer.print(str(msg), self.context)
        
        self.context.path.goBack()
        return msg
    
    
    
    