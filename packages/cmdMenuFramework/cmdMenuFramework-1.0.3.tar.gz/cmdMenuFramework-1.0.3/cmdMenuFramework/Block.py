from cmdMenuFramework.Instruction import Instruction
from cmdMenuFramework.InstType import InstType

class Block(Instruction):
    
    def __init__(self, context, name, content):
        super(Block, self).__init__(context, InstType.block, name, content)
        
    def execute(self):
        
        self.context.path.addInstruction(self)

        for id in self.content:
            
            if self.context.exit == True:
                self.context.exit = False
                break
            
            i = Instruction.letterToInstruction(id[:1], id, self.content[id], self.context)
            
            if i is None: 
                continue
            i.execute()
        
        self.context.path.goBack()
        return self.context.output