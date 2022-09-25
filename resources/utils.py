from random import randint
from colorama import Style, Fore

def randomFromArray(arr):
    return arr[randint(0, len(arr))]

def logColor(color, text:str):
    print(color+text+Style.RESET_ALL)

def commandExecuteFailure(cmdname:str, reason:str, caller):
    logColor(Fore.RED, f"Failed to execute {cmdname} command ({reason}) [{str(caller)}]")

def commandExecuteSuccess(cmdname:str, details:str, caller):
    logColor(Fore.GREEN, f"{cmdname[0].upper()}{cmdname[1:]} command successfully completed ({details}) [{str(caller)}]")