from cmdMenuFramework.Instruction import Instruction
from cmdMenuFramework.InstType import InstType
from cmdMenuFramework.Printer import Printer
from cmdMenuFramework.Menu import Menu
class Host(Instruction):
    
    def __init__(self, context, name, content):
        super(Host, self).__init__(context, InstType.host, name, content)
         
         
    def execute(self):
        self.context.path.addInstruction(self)
        
        fileName = None
        
        if self.content is not None: 
            if type(self.content) == str:
                fileName = self.content
            
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
                    fileName = i.execute()
                    if type(fileName) != str:  
                        Printer.printError ("Host instruction expected a string (yaml file), got "+ type(fileName) +" from embedded instruction instead", self.context)
                        self.context.path.goBack() 
                        return None
            
            else: 
                Printer.printError('Host instruction takes a string as parameter, was given '+type(self.content)+' instead.')
                self.context.path.goBack()
                return None
        else: 
            Printer.printError ("Host instruction recieved null as parameter.", self.context)
            self.context.path.goBack() 
            return None
            
        self.fileHosted = fileName
        embeddedMenu = Menu(fileName, self.context)
        output = embeddedMenu.start()
        
          
            
        self.context.path.goBack()
        return output