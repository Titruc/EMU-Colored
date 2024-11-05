import time, os

class color():
    RED = "\x1b[1;31m"
    BLACK = "\x1b[1;30m"
    GREEN = "\x1b[1;32m"
    YELLOW = "\x1b[1;33m"
    BLUE = "\x1b[1;34m"
    MAGENTA = "\x1b[1;35m"
    CYAN = "\x1b[1;36m"
    WHITE = "\x1b[1;37m",
    BRIGHT_RED = "\x1b[1;91m"
    BRIGHT_BLACK = "\x1b[1;90m"
    BRIGHT_GREEN = "\x1b[1;92m"
    BRIGHT_YELLOW = "\x1b[1;93m"
    BRIGHT_BLUE = "\x1b[1;94m"
    BRIGHT_MAGENTA = "\x1b[1;95m"
    BRIGHT_CYAN = "\x1b[1;96m"
    BRIGHT_WHITE = "\x1b[1;97m"
    GRAY = "\x1b[90m"
    DEFAULT = "\x1b[1;38m"
    BOLD = "\033[1m"
    RESET = "\x1b[1;39m"
    
    
    index = {"RED" : RED, "BLACK" : BLACK, "GREEN" : GREEN, "YELLOW" : YELLOW, "BLUE" : BLUE, "MAGENTA" : MAGENTA, "CYAN" : CYAN, "WHITE" : WHITE, "LIGHT_RED" : BRIGHT_RED, "BRIGHT_BLACK" : BRIGHT_BLACK, "BRIGHT_GREEN" : BRIGHT_GREEN, "BRIGHT_YELLOW" : BRIGHT_YELLOW, "BRIGHT_BLUE" : BRIGHT_BLUE, "BRIGHT_MAGENTA" : BRIGHT_MAGENTA, "BRIGHT_CYAN" : BRIGHT_CYAN, "BRIGHT_WHITE" : BRIGHT_WHITE, "GRAY" : GRAY, "BOLD" : BOLD,"DEFAULT" : DEFAULT, "RESET" : RESET}

def MKprint(printStr : str, instrName : str = "default", colorID : "color" = "DEFAULT") -> None:
    print(coloredStr("[" + getHourStr() + " - "+ instrName + "] ", colorID)  + printStr)
    
def getHourStr() -> str:
    return time.strftime("%H:%M:%S")

def coloredStr(string : str, colorID : "color") -> str:
    return color.index[colorID] + string + color.index["RESET"]

def colored(r, g, b, text) -> str:
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def printColored(text : str, colorID : str) -> None:
    print(coloredStr(text, colorID))

def printColoredWithoutNewLine(text : str, colorID : str) -> None:
    print(coloredStr(text,colorID), end='')

def printError(text):
    print(coloredStr(text, "RED"))
    
os.system('')

