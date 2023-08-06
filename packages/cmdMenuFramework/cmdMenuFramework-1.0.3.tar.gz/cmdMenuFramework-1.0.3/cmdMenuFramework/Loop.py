from cmdMenuFramework.Instruction import Instruction
from cmdMenuFramework.InstType import InstType

class Loop(Instruction):
    
    def __init__(self, context, name, content):
        super(Loop, self).__init__(context, InstType.loop, name, content)
        
    def execute(self):
        
        self.context.path.addInstruction(self)

        while not self.context.finish==True:
            for id in self.content:
                
                if self.context.exit == True:
                    self.context.exit = False
                    self.context.finish = True
                    break
                
                i = Instruction.letterToInstruction(id[:1], id, self.content[id], self.context)
                
                if i is None: 
                    continue
                i.execute()
        
        self.context.finish = False
        self.context.path.goBack()
        return self.context.output