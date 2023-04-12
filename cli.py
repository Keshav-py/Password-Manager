import json
from user import *
from crypto import *
from tables import *
from bcolors import bcolors


def input_command(key):
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
            input_command(key)
            break
        if option == '3':
            add_pass()
            input_command(key)
            break
        if option == '4':
            edit_row()
            input_command(key)
            break
        if option == '5':
            delete_row()
            input_command(key)
            break
        if option == '6':
            delete_account()
            user_active = False
            break
        elif option == ValueError:
            print(bcolors.FAIL + "Wrong Input" + bcolors.ENDC)
        else:
            print(bcolors.FAIL+"Wrong Input"+bcolors.ENDC)
    return user_active


if __name__ == "__main__":

    with open("credentials.json", "r") as creds:
        cred = json.load(creds)

    if cred["username"] == "":
        key = create_key(create_account()["MasterPassword"])
    else:
        key = create_key(login())
        decrypt_file(key)
    user_active = True

    try:
        while user_active:
            x = input_command(key)

            if not x:
                break

        exit()
    except KeyboardInterrupt:
        log_out(key)



