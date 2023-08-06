from cmdMenuFramework.Menu import Menu

def startMenu(fileName : str):
    """
    Launches the menu that is described by the given yaml file, in the cmd prompt. 
    If the file is not found, throws an exception, and terminates.
    """
    menu = Menu(fileName)
    menu.start()