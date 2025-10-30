
import sys
from colorama import Fore
from tqdm import tqdm


def print(message,end,file,):
    tqdm.write(message,file,end)

def print_red(message:str,end="\n",file=sys.stdout):
    print(f"{Fore.RED}{message}{Fore.RESET}",end=end,file=file)

def print_yellow(message:str,end="\n",file=sys.stdout):
    print(f"{Fore.YELLOW}{message}{Fore.RESET}",end=end,file=file)

def print_green(message:str,end="\n",file=sys.stdout):
    print(f"{Fore.GREEN}{message}{Fore.RESET}",end=end,file=file)


def print_red_ansi(message:str,end="\n",file=sys.stdout):
    print(f"\033[91m{message}\033[00m",end=end,file=file)

def print_yellow_ansi(message:str,end="\n",file=sys.stdout):
    print(f"\033[93m{message}\033[00m",end=end,file=file)

def print_green_ansi(message:str,end="\n",file=sys.stdout):
    print(f"\033[92m{message}\033[00m",end=end,file=file)

if __name__ =="__main__":
    print_yellow("hello")