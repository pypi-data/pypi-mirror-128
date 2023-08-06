from cmdMenuFramework.Instruction import Instruction
from cmdMenuFramework.InstType import InstType
from cmdMenuFramework.Printer import Printer

class Choice(Instruction):
    
    def __init__(self, context, name, content):
        super(Choice, self).__init__(context, InstType.choice, name, content)
        
    def execute(self):
        """Runs the instruction. 
        
        Stores the choice in the context as available, and displays it.
        Does not return anything."""
        
        self.context.path.addInstruction(self)
        
        #get name of the choice
        self.choiceName = None
        for id in self.content:
            letter1 = id[:1]
            if letter1 == 'n':
                nameInstruction = Instruction.letterToInstruction(id[:1], id, self.content[id], self.context)
                self.choiceName = nameInstruction.execute()
                break
        
        if self.choiceName is None:
            Printer.printError("This choice does not have a name instruction", self.context)
        
        #add to list of choices
        self.context.availableChoices.append(self)
        
        # print choice
        Printer.printChoice(self, self.context)
        
        self.context.path.goBack()
        
        
        
    def executeContent(self):
        self.context.path.addInstruction(self)
        
        if len(self.content)>2:
            Printer.printError ("Group the instructions inside a choice into a block instruction if there are multiple (except for the name instruction)", self.context)

        
        for id in self.content:
            letter1 = id[:1]
            if letter1 != 'n':
                instruction = Instruction.letterToInstruction(id[:1], id, self.content[id], self.context)
                output = instruction.execute()
                self.context.path.goBack()
                return output
            
        self.context.path.goBack()
        return None
        
        