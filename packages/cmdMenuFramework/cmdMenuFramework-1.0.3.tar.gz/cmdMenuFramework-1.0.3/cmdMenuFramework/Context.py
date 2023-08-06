
from cmdMenuFramework.Path import Path

class Context:
    
    def __init__(self, file = 'yaml/index.yaml'):
        # path is the list of instructions leading to the one executing currently.
        self.path = Path()
        
        # Default menu vars
        self.file = file
        self.controllerFile = 'controllers/ControllerIndex.py'
        self.controllerClass = 'ControllerIndex'
        self.input = None
        self.output = None
        self.userChoice = None
        self.exit = False
        self.exception = None
        self.finish = False
        self.choicePrompt = '%#. %$' 
        self.inputPrompt = 'Your input > '
        self.indent = False
        self.availableChoices = []
        self.showTrace = True
        self.indentWithPipes = False
        
        # User menu vars: 
        self.vars = dict()
        
        
    
    
    
    