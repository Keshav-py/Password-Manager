import hashlib
import json
import re
import getpass
from bcolors import bcolors
from crypto import *
import csv
from cli import *

def password_strength(password):
    # calculating the length
    length_error = len(password) < 8
    # searching for digits
    digit_error = re.search(r"\d", password) is None
    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None
    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None
    # searching for symbols
    symbol_error = re.search(r"[@!#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None
    # overall result
    password_ok = not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)
    return {
        'password_ok': password_ok,
        'length_error': length_error,
        'digit_error': digit_error,
        'uppercase_error': uppercase_error,
        'lowercase_error': lowercase_error,
        'symbol_error': symbol_error,
    }


def create_account():
    username = input("Enter username for new account (case insensitive): ").lower().strip()
    while True:

        MasterPassword = getpass.getpass("Enter strong Master Password: ")

        if password_strength(MasterPassword)['password_ok']:
            print(bcolors.OKGREEN + bcolors.BOLD + "Strong Password!" + bcolors.ENDC)

            confirm_pass = getpass.getpass("Confirm Master Password: ")

            if MasterPassword == confirm_pass:
                break
            else:
                print(bcolors.FAIL + "passwords didn't match!" + bcolors.ENDC)

        if password_strength(MasterPassword)['length_error'] == True or password_strength(MasterPassword)[
            'digit_error'] == True or password_strength(MasterPassword)['uppercase_error'] or \
                password_strength(MasterPassword)['lowercase_error'] or password_strength(MasterPassword)[
            'symbol_error']:

            print(bcolors.WARNING + """
A password is considered strong if:
    8 characters length or more
    1 digit or more
    1 symbol or more
    1 uppercase letter or more
    1 lowercase letter or more
                        """ + bcolors.ENDC)

    hashed_username = hashlib.sha256(username.encode()).hexdigest()
    hashed_password = hashlib.sha256(MasterPassword.encode()).hexdigest()
    cred_update = {
        "username": hashed_username,
        "password": hashed_password
    }

    with open("credentials.json", "w") as creds:
        json.dump(cred_update, creds, indent=4)

    print(bcolors.OKGREEN + bcolors.BOLD + "CONGRATULATIONS! Account created!" + bcolors.ENDC)

    return {
        "username": username,
        "MasterPassword": MasterPassword
    }


def login():
    global MasterPass
    print("Please Login", end='\n')
    user_match = False
    pass_match = False
    logged_in = False

    while not logged_in:
        username = input("Enter username: ").lower().strip()
        MasterPass = getpass.getpass("Enter your Master Password: ")

        hashed_username = hashlib.sha256(username.encode()).hexdigest()
        hashed_password = hashlib.sha256(MasterPass.encode()).hexdigest()

        with open("credentials.json", "r") as creds:
            cred = json.load(creds)

        if cred['username'] == hashed_username:
            user_match = True

        if cred['password'] == hashed_password:
            pass_match = True

        if user_match and pass_match:
            logged_in = True

            print(bcolors.OKGREEN + bcolors.BOLD + "LOGIN SUCCESSFUL" + bcolors.ENDC)

        else:
            print(bcolors.FAIL + "username/password didn't match" + bcolors.ENDC)

    return MasterPass


def log_out(key):
    encrypt_file(key)
    print(bcolors.OKGREEN + bcolors.BOLD + "LOGOUT SUCCESSFUL" + bcolors.ENDC)


def delete_account():
    while True:
        confirmation = input(bcolors.WARNING + bcolors.BOLD + "Are you sure you want to delete your account? (y/n): " + bcolors.ENDC).lower().strip()
        if confirmation == 'y':

            cred_update = {
                "username": '',
                "password": ''
            }

            with open("credentials.json", "w") as creds:
                json.dump(cred_update, creds, indent=4)

            with open('passes.csv', 'r') as readcsv:
                length = list(csv.reader(readcsv))
                del length[1:]

            with open('passes.csv', 'w') as writecsv:
                writer = csv.writer(writecsv)

                for row in length:
                    writer.writerow(row)

            print(bcolors.BOLD + bcolors.OKBLUE + "\nAccount deleted successfully!" + bcolors.ENDC)

            exit()

        elif confirmation == 'n':
            input_command(key=key, password=password)


        else:
            print(bcolors.FAIL+"Wrong Input"+bcolors.ENDC)

def change_pass(password):

    while True:
        confirmation = input(bcolors.WARNING + bcolors.BOLD + "Are you sure you want to change your Master Password? (y/n): " + bcolors.ENDC).lower().strip()
        print(confirmation)
        if confirmation == 'y':
            while True:

                MasterPassword = getpass.getpass("Enter strong Master Password: ")

                if password_strength(MasterPassword)['password_ok']:
                    print(bcolors.OKGREEN + bcolors.BOLD + "Strong Password!" + bcolors.ENDC)

                    confirm_pass = getpass.getpass("Confirm Master Password: ")

                    if MasterPassword == confirm_pass:
                        break
                    else:
                        print(bcolors.FAIL + "passwords didn't match!" + bcolors.ENDC)

                if password_strength(MasterPassword)['length_error'] == True or password_strength(MasterPassword)[
                    'digit_error'] == True or password_strength(MasterPassword)['uppercase_error'] or \
                        password_strength(MasterPassword)['lowercase_error'] or password_strength(MasterPassword)[
                    'symbol_error']:

                    print(bcolors.WARNING + """
            A password is considered strong if:
                8 characters length or more
                1 digit or more
                1 symbol or more
                1 uppercase letter or more
                1 lowercase letter or more
                                    """ + bcolors.ENDC)

            if MasterPassword == password:
                print("The new password is same as your current!")
                change_pass(password)
                break
            hashed_password = hashlib.sha256(MasterPassword.encode()).hexdigest()

            with open("credentials.json", "r") as credj:
                username = json.load(credj)

            cred_update = {
                "username": username['username'],
                "password": hashed_password
            }

            with open("credentials.json", "w") as credsj:
                json.dump(cred_update, credsj, indent=4)

            new_key = create_key(MasterPassword)
            encrypt_file(new_key)
            print(bcolors.OKGREEN+"Password has been changed!"+bcolors.ENDC)
            print(bcolors.BOLD+"\nPlease restart the program and login again."+bcolors.ENDC)

            exit()

        if confirmation == 'n':
            break

        else:
            print(bcolors.FAIL+"Wrong Input"+bcolors.ENDC)