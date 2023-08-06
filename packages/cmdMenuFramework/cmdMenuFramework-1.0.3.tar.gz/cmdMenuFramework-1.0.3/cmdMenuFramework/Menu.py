

from cmdMenuFramework.Printer import Printer
from cmdMenuFramework.Context import Context
from cmdMenuFramework.Instruction import Instruction
import yaml

class Menu:
    
    
    def __init__(self, file = 'yaml/index.yaml', context:Context = None):
        self.context = Context(file)
        if context is not None:
            self.context.vars = context.vars
            self.context.controllerFile = context.controllerFile
            self.context.controllerClass = context.controllerClass
            self.context.input = context.input
            self.context.exit = context.exit
            self.context.exception = context.exception
            self.context.finish = context.finish
            self.context.choicePrompt = context.choicePrompt
            self.context.inputPrompt = context.inputPrompt
            self.context.indent = context.indent
            self.context.showTrace = context.showTrace
            self.context.indentWithPipes = context.indentWithPipes
            self.context.availableChoices = context.availableChoices
            self.context.path = context.path
            
        
    
    def start(self):
        # loads then executes the base instructions, one by one.
        try: 
            with open(self.context.file) as f:
                self.instructionsAsDict = yaml.load(f, Loader=yaml.FullLoader)
                self.execute()
                return self.context.output
        except FileNotFoundError: 
            Printer.printError("File of menu to launch does not exist: "+str(self.context.file), self.context)
    
    
    def execute(self):
        for id in self.instructionsAsDict:
            
            if self.context.exit == True:
                self.context.exit = False
                break
                
            
            i = Instruction.letterToInstruction(id[:1], id, self.instructionsAsDict[id], self.context)
            
            if i is None: 
                continue
            i.execute()
    
    
    
    
    
    