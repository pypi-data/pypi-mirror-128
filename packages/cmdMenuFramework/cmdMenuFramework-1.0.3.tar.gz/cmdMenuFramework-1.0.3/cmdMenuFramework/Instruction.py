
from abc import ABC, abstractmethod
from cmdMenuFramework.Context import Context

class Instruction:
    
    
    
    def __init__(self, context:Context, type, name, content):
        self.type = type
        self.name = name # the key name for the instruction
        self.content = content # the contents of the instruction
        self.context = context
        
    @abstractmethod
    def execute(self): pass
    
    
    def __str__(self) :
        return str(self.type)+" [ "+self.name + ", " + str(self.content) + " ]"
    
    
    
    
    def letterToInstruction(letter, key, content, context):
        # keep those imports inside, otherwise, there is a circular import error
        from cmdMenuFramework.Prompt        import Prompt
        from cmdMenuFramework.Choice        import Choice
        from cmdMenuFramework.Name          import Name
        from cmdMenuFramework.Question      import Question
        from cmdMenuFramework.Action        import Action
        from cmdMenuFramework.Get           import Get
        from cmdMenuFramework.Set           import Set
        from cmdMenuFramework.SetDefault    import SetDefault
        from cmdMenuFramework.GetDefault    import GetDefault
        from cmdMenuFramework.Input         import Input
        from cmdMenuFramework.Host          import Host
        from cmdMenuFramework.Output        import Output
        from cmdMenuFramework.Exception     import Exception as X
        from cmdMenuFramework.Wait          import Wait
        from cmdMenuFramework.Value         import Value
        from cmdMenuFramework.Exit          import Exit
        from cmdMenuFramework.Finish        import Finish
        from cmdMenuFramework.Block         import Block
        from cmdMenuFramework.Loop          import Loop
        
        switcher = {
            'p': Prompt,
            'c': Choice,
            'n': Name, 
            'q': Question,
            'a': Action,
            's': Set,
            'g': Get,
            '-': SetDefault,
            '<': GetDefault,
            'i': Input, 
            'h': Host,
            'o': Output,
            'x': X,
            'w': Wait,
            'v': Value,
            'e': Exit, 
            'f': Finish,
            'b': Block,
            'l': Loop
        }
        # Get the constructor from switcher dictionary
        constructor = switcher.get(letter)
        
        if constructor is None:
            from Printer import Printer
            Printer.printError("Invalid instruction: "+letter, context)
            return None
        # Construct and return object
        return constructor(context, key, content)
    
    