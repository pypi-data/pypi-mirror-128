
from cmdMenuFramework.instruction.InstType import InstType

class Path:
    
    def __init__(self):
        self.instructions = []
        
    
    def isAtRoot(self):
        return self.instructions == []
    
    def getInstruction( self, index ):
        return self.instructions[index]
            
    def getLastInstruction( self ):
        return self.instructions[-1]
    
    def goBack( self ):
        self.instructions.pop()
        
    def addInstruction( self, instruction ):
        self.instructions.append(instruction)
    
    def getChoicesMade( self ):
        choices = []
        for i in self.instructions:
            if i.type == InstType.choice:
                choices.append(i)
        # # if the last is a choice, it has not yet been choosen, its just declaring itself
        # if choices != []:
        #     if choices[-1].type == InstType.choice:
        #         choices = choices[:-1]
        return choices
    
    def getNbChoicesMade( self ):
        return len(self.getChoicesMade())
    
    
    def instructionsAsStackTrace(self):
        st = ""
        for i in self.instructions:
            st += 'at: '+i.name + "\n"
            if i.type == InstType.host:
                if hasattr(i, 'fileHosted'):
                    st+="In file: "+i.fileHosted+"\n"
        return st
    
    def __str__(self):
        list = 'Path object: [ '
        for item in self.instructions:
            list += str(item)+", \n"
        return  list + " ]"