import csv
from prettytable import PrettyTable
from bcolors import bcolors


def add_pass():
    input_password = False
    print(bcolors.OKBLUE+"\nADD PASSWORD\n"+bcolors.ENDC)

    with open('passes.csv', 'r') as readcsv:
        length = list(csv.reader(readcsv))
        readcsv.close()

    with open('passes.csv', 'a') as csvfile:
        fieldnames = ['ROW NO.', 'APP', 'LOGIN', 'PASSWORD', 'COMMENTS']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # writer.writeheader()
        login = input("Enter user (username/phone number/email): ").strip()
        app = input("Enter Name of app/resource: ").strip().lower()

        while not input_password:
            password = input("Enter password: ").strip()

            if password == "":
                print(bcolors.FAIL + "Invalid Pass" + bcolors.ENDC)
            else:
                input_password = True

        comments = input("Enter Comment: ").strip()
        writer.writerow(
            {'ROW NO.': len(length), 'APP': app, 'LOGIN': login, 'PASSWORD': password, 'COMMENTS': comments})
    print(bcolors.BOLD+bcolors.OKBLUE+"Entry Successful!"+bcolors.ENDC)
    display_table()


def display_table():
    with open('passes.csv', newline='') as csvfile:
        csv_data = list(csv.reader(csvfile))
        mytable = PrettyTable(['ROW NO.', 'APP', 'LOGIN', 'PASSWORD', 'COMMENTS'])

        if not csv_data[1:]:
            print(bcolors.FAIL + "You have stored nothing" + bcolors.ENDC)
            add_pass()
        else:
            for i, e in enumerate(csv_data):
                if i == 0:
                    pass
                else:
                    mytable.add_row(e)
            print(mytable)


def edit_row():
    display_table()

    input_password = False

    with open('passes.csv', 'r') as readcsv:
        length = list(csv.reader(readcsv))

    while True:
        row_no = int(input("Which row do you want to edit?: "))
        if 1 <= row_no <= len(length):
            break

    new_row = [row_no]

    app = input("Enter Name of app/resource: ").strip().lower()
    new_row.insert(1, app)

    login = input("Enter user (username/phone number/email): ").strip()
    new_row.insert(2, login)

    while not input_password:
        password = input("Enter password: ").strip()

        if password == "":
            print(bcolors.FAIL + "Invalid Pass" + bcolors.ENDC)
        else:
            input_password = True
            new_row.insert(3, password)

    comments = input("Enter Comment: ").strip()
    new_row.insert(4, comments)

    length.pop(row_no)
    length.insert(row_no,new_row)
    readcsv.close()

    with open('passes.csv', 'w') as writecsv:
        write = csv.writer(writecsv)
        for row in length:
            write.writerow(row)
    print(bcolors.BOLD+bcolors.OKBLUE+"\nRow edited successfully!"+bcolors.ENDC)

    display_table()


def delete_row():
    while True:

        confirmation = input(bcolors.WARNING+bcolors.BOLD+"Are you sure you want to delete an entry? (y/n): "+bcolors.ENDC).lower().strip()
        if confirmation == 'y':

            with open('passes.csv', 'r') as readcsv:
                length = list(csv.reader(readcsv))

            while True:
                display_table()
                row_no = int(input("Which row do you want to delete?: "))
                if 1 <= row_no <= len(length):
                    break

            for i, lists in enumerate(length):
                if i == 0:
                    continue
                length[i][0] = str(int(lists[0]) )

            del length[row_no]
            readcsv.close()

            with open('passes.csv', 'w') as writecsv:
                write = csv.writer(writecsv)
                for row in length:
                    write.writerow(row)

            print(bcolors.BOLD + bcolors.OKBLUE + "\nRow deleted successfully!" + bcolors.ENDC)
            break

        elif confirmation == 'n':
            break

        else:
            print(bcolors.FAIL+"Wrong Input"+bcolors.ENDC)


def command_menu():
    commands = PrettyTable([bcolors.WARNING+bcolors.BOLD+"INPUT"+bcolors.ENDC, bcolors.WARNING+bcolors.BOLD+"COMMAND"+bcolors.ENDC])

    # Add rows
    commands.add_row([bcolors.OKCYAN+'1'+bcolors.ENDC, bcolors.pink+'LOG OUT'+bcolors.ENDC])
    commands.add_row([bcolors.OKCYAN+'2'+bcolors.ENDC, bcolors.green+'VIEW PASSWORDS'+bcolors.ENDC])
    commands.add_row([bcolors.OKCYAN+'3'+bcolors.ENDC, bcolors.blue+'MAKE ENTRY'+bcolors.ENDC])
    commands.add_row([bcolors.OKCYAN+'4'+bcolors.ENDC, 'EDIT ENTRY'])
    commands.add_row([bcolors.OKCYAN+'5'+bcolors.ENDC, bcolors.WARNING+'CHANGE MASTER PASSWORD'+bcolors.ENDC])
    commands.add_row([bcolors.OKCYAN+'6'+bcolors.ENDC, bcolors.red+'DELETE ENTRY'+bcolors.ENDC])
    commands.add_row([bcolors.OKCYAN+'7'+bcolors.ENDC, bcolors.red+bcolors.BOLD+'DELETE ACCOUNT'+bcolors.ENDC])

    print(commands)