from random_password import random_password, clipboard_copy
from database_config import *
from encrypting import *
import maskpass
from pathlib import Path
import sys
from time import sleep
from os import system

def leaving():
    for i in range(5):
        string = "leaving"
        print(string + "."*i, end="\r")
        sleep(0.3)
    print()

def menu(key: bytes):
    again = 'y'

    while (again == 'y'):
        system("clear")
        print("""
        Operations:
        (1) Generate random password
        (2) Add a password to the database
        (3) Remove a password from the database
        (4) See the passwords in the database
        (5) Exit
        """)
        option = int(input("-> "))
        try:
            match option:
                case 1:
                    print()
                    length = int(input("Length of the password: "))
                    passwd = random_password(length= length)
                    print(passwd)
                    clipboard_copy(passwd= passwd)
                
                case 2:
                    print()
                    print("If no password is passed the system will abort the operation.")
                    username = input("Username: ").strip()
                    application = input("Application: ").strip()
                    email = input("Email: ").strip()
                    password = input("Password: ").strip()

                    if password == "":
                        print("No password passed, operation aborted")
                        raise ValueError
                    
                    adding_db(username= username, application= application, email= email, password= password)
                    print("New data added.")
                    sleep(2)
                
                case 3:
                    print()
                    print("If one of the two fields is left blank the operation will be aborted.")
                    username = input("Username: ").strip()
                    application = input("Application: ").strip()

                    if (username == "" or application == ""):
                        print("One field was left blank, operation aborted")
                        raise ValueError
                    deleting_db(username= username, application= application)
                    print("Data deleted")
                    sleep(2)
                
                case 4:
                    print()
                    showing_db()
                    answer = input("Would you like to copy a password? (y/n)\n-> ").strip().lower()
                    if answer == "y":
                        id = input("Id: ").strip()
                        username = input("Username: ").strip()
                        if (id == "" or username == ""):
                            print("Empty field, operation aborted.")
                            raise ValueError
                        copying_passwd_db(id= id, username= username)
                        sleep(2)
                    else:
                        sleep(2)
                
                case 5:
                    encrypting_db(key= key)
                    leaving()
                    sys.exit()

                case _:
                    raise ValueError
        except:
            pass
        
        again = input("Continue? (y/n) ").strip().lower()

def main():
    print("===================")
    print("Password Manager")
    print("===================")
    if (not Path(".salt").exists()) and (not Path(".database.db").exists()):
        creating_db()
        print("As it is your first time\nPut the password/passphrase\nyou would like to use.")
        print("Because it is your first time\nthe password won't be hide")
        password = input("Enter password: ").strip()
        password = password.encode()
        key = kdf(password= password)
        config_login(key= key)
    else:
        print("Login:")
        password = maskpass.askpass().strip()
        password = password.encode("utf-8")
        key = kdf(password= password)
        decrypting_db(key= key)
        if not check_login:
            print("Wrong password\n")
            leaving()
            system("clear")
            encrypting_db(key= key)
            sys.exit()

    menu(key= key)

    system("clear")
    encrypting_db(key= key)

