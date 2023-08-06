from cmdMenuFramework.Instruction import Instruction
from cmdMenuFramework.InstType import InstType
from cmdMenuFramework.Printer import Printer
class GetDefault(Instruction):
    
    def __init__(self, context, name, content):
        super(GetDefault, self).__init__(context, InstType.getDefault, name, content)
        
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
                    Printer.printError ("GetDefault instruction expected a variable name (str), got "+ type(varName) +" from embedded instruction instead", self.context)
                    self.context.path.goBack() 
                    return None
                
        elif type(self.content) == str:   
            varName = self.content
        
        
        else: 
            Printer.printError ("GetDefault instruction expected a variable name (str), got "+ type(self.content) +" instead", self.context)
            self.context.path.goBack() 
            return None
        
        
        # get var from context
        if varName is None:
            self.context.path.goBack() 
            return None
        
        allDefDic = {
                'file' : self.context.file,
                'controllerFile' : self.context.controllerFile,
                'controllerClass' : self.context.controllerClass,
                'input' : self.context.input,
                'output': self.context.output,
                'exit' : self.context.exit,
                'exception' : self.context.exception,
                'finish' : self.context.finish,
                'choicePrompt' : self.context.choicePrompt,
                'inputPrompt' : self.context.inputPrompt,
                'indent' : self.context.indent,
                'userChoice': self.context.userChoice,
                'availableChoices' : self.context.availableChoices,
                'path': self.context.path,
                'showTrace': self.context.showTrace,
                'indentWithPipes': self.context.indentWithPipes
            }
        
        if varName == '*':
            self.context.path.goBack()
            return allDefDic
        
        try :
            var = allDefDic[varName]
        except KeyError :
            Printer.printError ('"'+varName+"\" is not a default menu variable! Oh no!  :'(", self.context)
            self.context.path.goBack()
            return None
            
        self.context.path.goBack()
        return var
    
   