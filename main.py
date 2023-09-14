from random_password import random_password, clipboard_copy
from database_config import *
from encrypting import *
from cryptography.fernet import Fernet
from pandas import DataFrame
import maskpass
from pathlib import Path
import sys
from time import sleep
from os import system

def leaving():
    for i in range(5):
        string = "leaving"
        print(string + "."*i, end="\r")
        sleep(0.5)
    print()

def menu():
    pass

def main():
    print("===================")
    print("Password Manager")
    print("===================")
    if not Path(".salt").exists():
        creating_db()
        print("As it is your first time\nPut the password/passphrase\nyou would like to use.")
        password = input("Enter password: ").strip()
        key = kdf(password= password)
        config_login(key= key)
        system("clear")
    else:
        print("Login:")
        password = maskpass.askpass()
        key = kdf(password= password)
        decrypting_db(key= key)
        if not check_login:
            print("Wrong password\n")
            leaving()
            system("clear")
            sys.exit()
        system("clear")

    menu()

    encrypting_db()
        


if __name__ == "__main__":
    main()