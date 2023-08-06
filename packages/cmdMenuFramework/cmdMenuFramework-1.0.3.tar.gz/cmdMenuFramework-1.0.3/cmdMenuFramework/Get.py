from cmdMenuFramework.Instruction import Instruction
from cmdMenuFramework.InstType import InstType
from cmdMenuFramework.Printer import Printer
class Get(Instruction):
    
    def __init__(self, context, name, content):
        super(Get, self).__init__(context, InstType.get, name, content)
        
    def execute(self):
        
        self.context.path.addInstruction(self)
        
        # find var name
        if self.content is None:
            self.context.path.goBack()
            return None
        
        if (type(self.content)) == dict:
            if (len(self.content) != 1):
                Printer.printError ("Multiple embedded instructions: use a block instruction instead", self.context)
                self.context.path.goBack()
                return None
            
            for id in self.content:
                i = Instruction.letterToInstruction(id[:1], id, self.content[id], self.context)
                if i is None: 
                    self.context.path.goBack()
                    return None
                varName = i.execute()
                if type(varName) != str:  
                    Printer.printError ("Get instruction expected a variable name (str), got "+ type(varName) +" from embedded instruction instead", self.context)
                    self.context.path.goBack() 
                    return None
                
        elif type(self.content) == str:   
            varName = self.content
        
        
        else: 
            Printer.printError ("Get instruction expected a variable name (str), got "+ type(self.content) +" instead", self.context)
            self.context.path.goBack() 
            return None
        
        
        # get var from context
        
        if varName == '*':
            self.context.path.goBack()
            return self.context.vars
        
        try :
            var = self.context.vars[varName]
        except KeyError :
            var = None
            
        self.context.path.goBack()
        return var