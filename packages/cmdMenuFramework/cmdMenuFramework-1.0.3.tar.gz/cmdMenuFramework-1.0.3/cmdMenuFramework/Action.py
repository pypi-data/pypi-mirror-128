from cmdMenuFramework.Instruction import Instruction
from cmdMenuFramework.InstType import InstType
from cmdMenuFramework.Printer import Printer
import importlib
import importlib.util

class Action(Instruction):
    
    def __init__(self, context, name, content):
        super(Action, self).__init__(context, InstType.action, name, content)
           
    def execute(self):
        self.context.path.addInstruction(self)
        
        if (typ := type(self.content)) == dict:
            if (len(self.content) != 1):
                Printer.printError ("Multiple embedded instructions: use a block instruction instead", self.context)
                self.context.path.goBack()
                return None
            
            for id in self.content:
                i = Instruction.letterToInstruction(id[:1], id, self.content[id], self.context)
                if i is None: 
                    self.context.path.goBack()
                    return None
                actionName = i.execute()
                if type(actionName) != str:  
                    Printer.printError ("Action instruction expected a method name (str), got "+ type(actionName) +" from embedded instruction instead", self.context)
                    self.context.path.goBack() 
                    return None
                
        elif typ == str:   
            actionName = self.content
            
        else: 
            Printer.printError ("Action instruction expected a method name (str), got "+str(typ)+" instead", self.context)
            self.context.path.goBack() 
            return None
        
        
        # execute action from controller
        try:
            
            spec = importlib.util.spec_from_file_location("controllingModule", self.context.controllerFile)
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)  
            
            if self.context.controllerClass is None:
                klass = foo
            else: 
                klass = foo.__dict__[self.context.controllerClass]
            method =  klass.__dict__[actionName]
            
            output = method(self.context)
            self.context.path.goBack()
            return output
            
        except FileNotFoundError as e:
            Printer.printError('There is no file named: '+self.context.controllerFile, self.context)
            self.context.path.goBack()
            return None    
        except KeyError:
            Printer.printError('There is either: \n    -no class named: '+self.context.controllerClass+' in the file: '+self.context.controllerFile
                +'\n    -or no method named: '+actionName+' in this class.', self.context)
            self.context.path.goBack()
            return None
            
        
        