from cmdMenuFramework.Instruction import Instruction
from cmdMenuFramework.InstType import InstType
from cmdMenuFramework.Printer import Printer

class Input(Instruction):
    
    def __init__(self, context, name, content):
        super(Input, self).__init__(context, InstType.input, name, content)
         
    def execute(self):
        self.context.path.addInstruction(self)
        
        customPrompt = None
        
        if self.content is not None: 
            if type(self.content) == str:
                customPrompt = self.content
            
            elif type(self.content) == dict:
                if (len(self.content) != 1):
                    Printer.printError ("Multiple embedded instructions: use a block instruction instead", self.context)
                    self.context.path.goBack()
                    return None
            
                for id in self.content:
                    i = Instruction.letterToInstruction(id[:1], id, self.content[id], self.context)
                    if i is None: 
                        self.context.path.goBack()
                        return None
                    customPrompt = i.execute()
                    if type(customPrompt) != str:  
                        Printer.printError ("Input instruction expected a string, got "+ type(customPrompt) +" from embedded instruction instead", self.context)
                        self.context.path.goBack() 
                        return None
            
            else: 
                Printer.printError('Input instruction takes null or a string as parameter, was given '+type(self.content)+' instead.')
                self.context.path.goBack()
                return None
            
                
        
        output = Printer.askForInput(self.context, customPrompt)
        self.context.input = output  
            
        self.context.path.goBack()
        return output