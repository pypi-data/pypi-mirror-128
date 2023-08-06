from cmdMenuFramework.Instruction import Instruction
from cmdMenuFramework.InstType import InstType
from cmdMenuFramework.Printer import Printer

class Exception(Instruction):
    
    def __init__(self, context, name, content):
        super(Exception, self).__init__(context, InstType.exception, name, content)
         
    
    def execute(self):
        self.context.path.addInstruction(self)
        
        msg = None
        
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
                    msg = i.execute()
                    if type(self.content) != str:
                        Printer.printError('Exception instruction expects a string (the message to display), got '+type(self.content)+' from embedded instruction instead.')
                        self.context.path.goBack()
                        return None
            
            elif type(self.content) == str:
                msg = self.content
            
            else: 
                self.context.path.goBack()
                Printer.printError('Exception instruction expects a string (the message to display), got '+type(self.content)+' instead.')
                return None
        
        else: 
            # return the last exception
            self.context.path.goBack()
            return self.context.exception    
            
        Printer.printError(msg, self.context)
        self.context.path.goBack()
        return msg