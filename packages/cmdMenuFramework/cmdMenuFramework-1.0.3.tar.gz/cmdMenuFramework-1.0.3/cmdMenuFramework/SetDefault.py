from cmdMenuFramework.Instruction import Instruction
from cmdMenuFramework.InstType import InstType
from cmdMenuFramework.Printer import Printer

class SetDefault(Instruction):

        
    def __init__(self, context, name, content):
        super(SetDefault, self).__init__(context, InstType.setDefault, name, content)
        
    def execute(self):
        
        self.context.path.addInstruction(self)
        
        if type(self.content) != dict:
            Printer.printError ("SetDefault instruction expected a dictionnary, got "+str(type(self.content))+" instead", self.context)
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
                    s1 = 'when setting default variable "'+varName+'"'
                    Printer.printError ("Multiple embedded instructions "+s1+": use a block instruction instead", self.context)
                    continue
                for id in varContent:
                    i = Instruction.letterToInstruction(id[:1], id, varContent[id], self.context)
                    if i is None: 
                        break
                    output = i.execute()
                    
            # else
            else:
                output = varContent
            
            allDefNames = [
                'file' ,
                'controllerFile' ,
                'controllerClass',
                'input' ,
                'exit',
                'exception',
                'finish',
                'choicePrompt',
                'inputPrompt',
                'indent',
                'availableChoices',
                'indentWithPipes',
                'showTrace'
            ]
            
            if varName not in allDefNames:
                Printer.printError ('"'+varName+"\" is not a default menu variable! Oh no!  :'(", self.context)
                continue
            
            if varName == 'file':
                if (t := type(output)) == str:
                    self.context.file = output
                else:
                    Printer.printError ("'file' default variable expects a string, got "+str(t)+" instead", self.context)
                    continue
            
            if varName == 'controllerFile':
                if (t := type(output)) == str:
                    self.context.controllerFile = output
                else:
                    Printer.printError ("'controllerFile' default variable expects a string, got "+str(t)+" instead", self.context)
                    continue
            
            if varName == 'controllerClass':
                if (t := type(output)) == str:
                    self.context.controllerClass = output
                else:
                    Printer.printError ("'controllerClass' default variable expects a string, got "+str(t)+" instead", self.context)
                    continue
            
            if varName == 'input':
                if (t := type(output)) == str:
                    self.context.input = output
                else:
                    Printer.printError ("'input' default variable expects a string, got "+str(t)+" instead", self.context)
                    continue
            
            if varName == 'output':
                self.context.output = output
            
            if varName == 'userChoice':
                if (t := type(output)) == str:
                    self.context.userChoice = output
                else:
                    Printer.printError ("'userChoice' default variable expects a string, got "+str(t)+" instead", self.context)
                    continue
            
            if varName == 'exit':
                if (t := type(output)) == bool:
                    self.context.exit = output
                else:
                    Printer.printError ("'exit' default variable expects a boolean, got "+str(t)+" instead", self.context)
                    continue
            
            if varName == 'exception':
                if (t := type(output)) == str:
                    self.context.exception = output
                else:
                    Printer.printError ("'exception' default variable expects a string, got "+str(t)+" instead", self.context)
                    continue
            
            if varName == 'finish':
                if (t := type(output)) == bool:
                    self.context.finish = output
                else:
                    Printer.printError ("'finish' default variable expects a boolean, got "+str(t)+" instead", self.context)
                    continue
            
            if varName == 'choicePrompt':
                if (t := type(output)) == str:
                    self.context.choicePrompt = output
                else:
                    Printer.printError ("'choicePrompt' default variable expects a string, got "+str(t)+" instead", self.context)
                    continue
            
            if varName == 'inputPrompt':
                if (t := type(output)) == str:
                    self.context.inputPrompt = output
                else:
                    Printer.printError ("'inputPrompt' default variable expects a string, got "+str(t)+" instead", self.context)
                    continue
            
            if varName == 'indent':
                if (t := type(output)) == bool:
                    self.context.indent = output
                else:
                    Printer.printError ("'indent' default variable expects a boolean, got "+str(t)+" instead", self.context)
                    continue
            
            if varName == 'indentWithPipes':
                if (t := type(output)) == bool:
                    self.context.indentWithPipes = output
                else:
                    Printer.printError ("'indentWithPipes' default variable expects a boolean, got "+str(t)+" instead", self.context)
                    continue
            
            if varName == 'showTrace':
                if (t := type(output)) == bool:
                    self.context.showTrace = output
                else:
                    Printer.printError ("'showTrace' default variable expects a boolean, got "+str(t)+" instead", self.context)
                    continue
            
            
        self.context.path.goBack()
        