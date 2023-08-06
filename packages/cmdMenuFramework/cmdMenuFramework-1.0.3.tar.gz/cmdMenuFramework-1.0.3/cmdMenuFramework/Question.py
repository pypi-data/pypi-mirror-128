from cmdMenuFramework.Instruction import Instruction
from cmdMenuFramework.InstType import InstType
from cmdMenuFramework.Printer import Printer

class Question(Instruction):
    
    def __init__(self, context, name, content):
        super(Question, self).__init__(context, InstType.question, name, content)
        
    def execute(self):
        
        self.context.path.addInstruction(self)
        
        # set default parameters
        noExit = False
        ifError = None # contains the instruction
        ifExit = None
        
        if self.content is not None: # set custom parameters
            if type(self.content) != dict:
                Printer.printError("Question instruction expects either null or a dictionnary", self.context)
            
            # CHECK FOR THE DIFFERENT PARAMS IF THERE ARE
            for p in self.content:
                if p == 'noExit':
                    #test if we have a boolean
                    if type(self.content[p]) == bool:
                        noExit = self.content[p]
                        
                    #test if we have an embedded instruction 
                    elif type(self.content[p]) == dict:
                        # test if there is only one 
                        if (len(self.content[p])) != 1 :
                            Printer.printError ("Multiple embedded instructions: use a block instruction instead", self.context)
                            self.context.path.goBack()
                            return None
                        for id in self.content[p]: # create, execute, and check return value of embedded instruction
                            i = Instruction.letterToInstruction(id[:1], id, self.content[id], self.context)
                            if i is None: 
                                self.context.path.goBack()
                                return None
                            boolean = i.execute()
                            if type(boolean) != bool:
                                self.context.path.goBack()
                                Printer.printError("noExit parameter expects a boolean, got "+type(boolean)+" instead, from an embedded instruction", self.context)
                                return None
                            else: 
                                noExit = boolean
                    else: 
                        Printer.printError("noExit parameter expects a boolean, got "+type(self.content[p])+" instead", self.context)
                
                elif p == 'ifError': # ifError accepts only one instruction 
                    if self.content[p] is not None:
                        if type(self.content[p]) == dict:
                            if (len(self.content[p])) != 1 :
                                Printer.printError ("Multiple embedded instructions: use a block instruction instead", self.context)
                                self.context.path.goBack()
                                return None

                            for id in self.content[p]:
                                i = Instruction.letterToInstruction(id[:1], id, self.content[p][id], self.context)
                                if i is None: 
                                    self.context.path.goBack()
                                    return None
                                ifError = i
                        else : 
                            Printer.printError("ifError parameter expects an embedded instruction, got "+type(self.content[p])+" instead", self.context)
                
                elif p == 'ifExit': # onExit accepts only one instruction 
                    if self.content[p] is not None:
                        if type(self.content[p]) == dict:
                            if (len(self.content[p])) != 1 :
                                Printer.printError ("Multiple embedded instructions: use a block instruction instead", self.context)
                                self.context.path.goBack()
                                return None

                            for id in self.content[p]:
                                i = Instruction.letterToInstruction(id[:1], id, self.content[p][id], self.context)
                                if i is None: 
                                    self.context.path.goBack()
                                    return None
                                ifExit = i
                        else : 
                            Printer.printError("onExit parameter expects an embedded instruction, got "+type(self.content[p])+" instead", self.context)
                
                else: 
                    Printer.printError("Unrecognized parameter for a Question instruction: " + str(p), self.context)
                    
        # if the noExit == False: propose choice for exit
        if noExit==False:
            Printer.printExitChoice(self.context)
        
        # now ask for a choice
        choice = Printer.askForInput(self.context)
        self.context.userChoice = choice
        
        # interpret user response
        askForExit = False
        errorEncountered = None
        
        # if the choice is a number between 1 and however many choices there are
        maxId = len(self.context.availableChoices)+1
        if noExit==True: maxId -= 1 
        
        if choice.isnumeric() and (id:=int(choice))>0 and id<= maxId:
            # there is nothing to do if we ask to exit the choice, but in other case: 
            if id < len(self.context.availableChoices)+1:
                choosen = self.context.availableChoices[id-1]
                self.context.availableChoices = [] 
                choosen.executeContent()
                
            elif ifExit is not None:
                ifExit.execute()
                
        else:
            if ifError is not None:
                ifError.execute()
        
        self.context.availableChoices = []   
        self.context.path.goBack()
        return choice
        
    