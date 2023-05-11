import json
from user import *
from crypto import *
from tables import *
from bcolors import bcolors


def input_command(key,password):
    global user_active
    command_menu()
    while True:
        option = input("Enter command input number: ").strip()
        if option == '1':
            log_out(key)
            user_active = False
            break
        if option == '2':
            display_table()
            input_command(key=key,password=password)
            break
        if option == '3':
            add_pass()
            input_command(key=key,password=password)
            break
        if option == '4':
            edit_row()
            input_command(key=key,password=password)
            break
        if option == '5':
            change_pass(password)
            input_command(key=key,password=password)
        if option == '6':
            delete_row()
            input_command(key=key,password=password)
            break
        if option == '7':
            delete_account()
            break
        elif option == ValueError:
            print(bcolors.FAIL + "Wrong Input" + bcolors.ENDC)
        else:
            print(bcolors.FAIL+"Wrong Input"+bcolors.ENDC)
    return user_active


if __name__ == "__main__":

    try:
        with open("credentials.json", "r") as creds:
            cred = json.load(creds)

        if cred["username"] == "":
            password = create_account()["MasterPassword"]
            key = create_key(password)
        else:
            password = login()
            key = create_key(password)
            decrypt_file(key)

        while True:
            x = input_command(key=key,password=password)

            if not x:
                break

        exit()
    except KeyboardInterrupt:
        log_out(key)



