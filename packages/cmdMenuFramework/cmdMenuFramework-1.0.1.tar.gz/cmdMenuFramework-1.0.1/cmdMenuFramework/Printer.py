

from cmd_menu_framework.Context import Context

from colorama import Fore, Style, Back



class Printer: 
    """The class responsible for prints."""
    
    def prepareIndent(context, forChoice = False):
        # prepare the indent
        # print ('#### '+str(context.path.getNbChoicesMade()))
        prefix = ""
        if context.indent == True:
            
            r = context.path.getNbChoicesMade()
            if forChoice==True: r = r-1
            
            for i in range(r):
                if context.indentWithPipes: prefix+='|'
                prefix+="    "
            
        return prefix
    
    def replaceWithVars(msg:str, context: Context):
        
        try:
            i1 = msg.index("%$")
            i2 = msg.index("$%")+2
            varName = msg[i1+2:i2-2]
            varValue = context.vars[varName]
            msg = msg[:i1] + str(varValue) + msg[i2:]
            return Printer.replaceWithVars(msg, context)
        except ValueError:
            pass

        try:
            i1 = msg.index("%=")
            i2 = msg.index("=%")+2
            varName = msg[i1+2:i2-2]
            varValue = context.__dict__[varName]
            msg = msg[:i1] + str(varValue) + msg[i2:]
            return Printer.replaceWithVars(msg, context)
        except ValueError:
            pass
        except KeyError: 
            Printer.printError(varName+ ' is not a default menu variable!', context)
        
        return msg
    
    def print(message:str, context:Context, forChoice = False):
        """Prints a simple message."""
        
        message = Printer.replaceWithVars(message, context)
        
        print (Printer.prepareIndent(context, forChoice) + str(message))
        
        
    def printError(message:str, context:Context):
        """Prints an error message in red, followed by the instructions in the file that led to it."""
        
        message = Printer.replaceWithVars(message, context)
        
        fullMsg = ""
        fullMsg += Fore.RED + Style.BRIGHT + message+"\n"
        fullMsg += "In file: "+context.file
        if context.showTrace:
            fullMsg+= "\n"+str(context.path.instructionsAsStackTrace())
        fullMsg += Style.RESET_ALL + Fore.RESET
        
        print (fullMsg)
        
        context.exception = fullMsg
        
    def printChoice(choiceInstr, context:Context):
    #     print(context.path)
        id = len(context.availableChoices)
        msg = context.choicePrompt
        msg = msg.replace('%$', str(choiceInstr.choiceName))
        msg = msg.replace('%#', str(id))
        
        Printer.print(msg, context, True)
    
    def printExitChoice(context: Context):
        id = len(context.availableChoices)+1
        name = 'Exit'
        msg = context.choicePrompt
        msg = msg.replace('%$', str(name))
        msg = msg.replace('%#', str(id))
        Printer.print(msg, context, False)
        
    def askForInput(context: Context, prompt:str = None):
        if prompt is None: 
            prompt = context.inputPrompt
        prompt = Printer.replaceWithVars(prompt, context)
        
        return input(Printer.prepareIndent(context)+prompt)