from cmdMenuFramework.Instruction import Instruction
from cmdMenuFramework.InstType import InstType
from cmdMenuFramework.Printer import Printer         
import time
class Wait(Instruction):
    
    def __init__(self, context, name, content):
        super(Wait, self).__init__(context, InstType.wait, name, content)
        
    def execute(self):
        """Runs the instruction. 
        
        If it contains a dictionnary, executes the first instruction from this dictionnary, and prints its return value.
        If it contains anything else, prints str(value)."""
        
        self.context.path.addInstruction(self)
        
        c = None
        
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
                    c = i.execute()
                    if type(c)!=str and type(c)!=int:
                        Printer.printError ("Wait instruction expected either a string or an integer, got "+str(type(c))+" from embedded instruction instead.", self.context)
                        self.context.path.goBack()
                        return None
                    
            elif type(self.content)==str or type(self.content)==int:
                c = self.content
            else: 
                Printer.printError ("Wait instruction expected either a string or an integer, got "+type(self.content)+" instead.", self.context)
                self.context.path.goBack()
                return None
                
                
        if type(c)==str:
            while True:
                if c == "":
                    msg = "Press enter to continue"
                else: 
                    msg = 'Write "'+c+'" to continue'
                written = Printer.askForInput(self.context, msg+" > ")
                if written == c:
                    break;
        
        elif type(c)==int:
            time.sleep(c)
    
        
        self.context.path.goBack()
    
    
    
    