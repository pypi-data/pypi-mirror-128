from cmdMenuFramework.Instruction import Instruction
from cmdMenuFramework.InstType import InstType
from cmdMenuFramework.Printer import Printer
class Set(Instruction):

        
    def __init__(self, context, name, content):
        super(Set, self).__init__(context, InstType.set, name, content)
        
    def execute(self):
        
        self.context.path.addInstruction(self)
        
        if type(self.content) != dict:
            Printer.printError ("Set instruction expected a dictionnary, got "+str(type(self.content))+" instead", self.context)
            self.context.path.goBack()
            return None
        
        # look every value to set, and execute
        for varName in self.content:
            varContent = self.content[varName]
            # if content is none
            if varContent is None:
                self.context.vars[varName] = None
                
            # if content is dict: interpret it
            elif type(varContent) == dict:
                if (len(varContent) != 1):
                    s1 = 'when setting user variable "'+varName+'"'
                    Printer.printError ("Multiple embedded instructions "+s1+": use a block instruction instead", self.context)
                    continue
                for id in varContent:
                    i = Instruction.letterToInstruction(id[:1], id, varContent[id], self.context)
                    if i is None: 
                        break
                    output = i.execute()
                    self.context.vars[varName] = output
                    
            # else
            else:
                self.context.vars[varName] = varContent
            
        self.context.path.goBack()
        