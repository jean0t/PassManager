import string
import secrets as sc
from random import shuffle
from argparse import ArgumentParser
import pyperclip
import os

def random_password(length: int) -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation

    password = ''.join(sc.choice(alphabet) for i in range(length)) #create a first password and the variable 'password'
    while ((string.digits in password) and (string.punctuation in password) and (string.ascii_letters in password)): #guarantees that all the symbols will be used
        password = ''.join(sc.choice(alphabet) for i in range(length)) 

    return password


if __name__ == "__main__":
    try:
        #cli argument
        parser = ArgumentParser(prog="Password generator")
        parser.add_argument("-l", "--length", type=int, default=12, action="store", help="Length of the password")
        args = parser.parse_args()

        passwd = random_password(args.length) #generating the password
        print(f"Password: {passwd}")
        if pyperclip.is_available():
            pyperclip.copy(passwd)
            print("Copied to clipboard.")
        else:
            os.system(f"echo '{passwd}' | xclip -selection c")
            print("Copied to clipboard.")
    except:
        print("An unexpected error has occurred.")