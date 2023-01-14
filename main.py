import string
import threading
import time

from db.password_database import PasswordsDatabase
from db.password_generator import PasswordGenerator
from encryptor import Encryptor


def wait_for_user_input():
    input("Continue...")


def try_to_remove_database_file(database, database_name):
    start_time = time.time()
    while True:
        if time.time() - start_time > 60:
            print(f"Encountered a problem during cleanup... Please remove "
                  + f"./{database.database_folder}/{database_name}.db"
                  + " manually")
            break
        try:
            database.delete_database(database_name)
            break
        except:
            pass


if __name__ == '__main__':
    database = PasswordsDatabase()
    _user_input = None

    while True:
        print("----------------------------")
        print(f"Currently using folder '{database.database_folder}' to search for databases")
        if database.current_connection is not None:
            print(f"Currently using database '{database.current_connection.database_path}'")
        print()
        print("0. Exit")
        print("1. Show available databases")
        print("2. Create new database")
        print("3. Delete database")
        print("4. Select database")
        print("5. Select database folder")
        print("6. Generate password")
        print("7. Encrypt database file")
        print("8. Decrypt database file")
        if database.current_connection is not None:
            print(f"9. Show database data")

        print()
        _user_input = input("Next command: ")

        print("----------------------------")

        match _user_input:
            # Exit
            case "0":
                break
            # Show available databases
            case "1":
                print('\n'.join(database.databases()))
                for encrypted in database.encrypted_databases():
                    print(encrypted + " (Encrypted)")
                wait_for_user_input()
            # Create new database
            case "2":
                database_name = input("Database name: ")
                if database_name not in database.databases():
                    database.create_database(database_name)
            # Delete database
            case "3":
                print("Available databases:")
                print('\n'.join(database.databases()))
                database_name = input("Database name: ")
                if database_name in database.databases():
                    database.delete_database(database_name)
            # Select database
            case "4":
                print("Available databases:")
                print('\n'.join(database.databases()))
                database_name = input("Database name: ")
                if database_name in database.databases():
                    database.set_connection(database_name=database_name)
            # Select database folder
            case "5":
                new_folder = input("Database folder name: ")
                if new_folder != "":
                    database.change_database_folder(new_folder)
            # Generate password
            case "6":
                letters = input(f"Include letters? [{string.ascii_letters}] Y/n: ")
                digits = input(f"Include digits? [{string.digits}] Y/n: ")
                special_characters = input(f"Include special characters? [{string.punctuation}] Y/n: ")
                pool = ""

                if letters == "N" or letters == "n":
                    letters = False
                else:
                    letters = True
                    pool += string.ascii_letters

                if digits == "N" or digits == "n":
                    digits = False
                else:
                    digits = True
                    pool += string.digits

                if special_characters == "N" or special_characters == "n":
                    special_characters = False
                else:
                    special_characters = True
                    pool += string.punctuation

                n = int(input("Password length: "))

                print(f"Max entropy = {PasswordGenerator.calculate_max_entropy(n, pool)}")

                min_entropy = float(input("Minimum entropy: "))

                passwd = PasswordGenerator.generate(n, letters, digits, special_characters, min_entropy)

                if passwd is None:
                    print("Couldn't generate a suitable password within 100 000 tries")
                else:
                    print(passwd)
                    print(f"Password entropy = {PasswordGenerator.calculate_entropy(passwd)}")
                wait_for_user_input()
            # Encrypt database file
            case "7":
                print("Available databases:")
                print('\n'.join(database.databases()))
                database_name = input("Database name: ")
                if database.current_connection is not None \
                        and database.current_connection.database_path == f"./{database.database_folder}/{database_name}.db":
                    database.current_connection.force_close()
                if database_name in database.databases():
                    passwd = input("Password: ")
                    Encryptor.encrypt_file(f"./{database.database_folder}/{database_name}.db",
                                           f"./{database.database_folder}/{database_name}.db.enc", passwd)
                    database.delete_database(database_name)
            # Decrypt database
            case "8":
                print("Available databases:")
                print('\n'.join(database.encrypted_databases()))
                database_name = input("Database name: ")
                if database_name in database.encrypted_databases():
                    passwd = input("Password: ")
                    try:
                        Encryptor.decrypt_file(f"./{database.database_folder}/{database_name}.db.enc",
                                               f"./{database.database_folder}/{database_name}.db", passwd)
                        database.delete_encrypted_database(database_name)
                    except ValueError:
                        print("Wrong password")
                        threading.Thread(target=try_to_remove_database_file, args=(database, database_name)).start()
                        wait_for_user_input()

            # Show database data file
            case "9":
                if database.current_connection is not None:
                    entries = database.select_all()
                    for itr in range(len(entries)):
                        print(f"{itr + 1} | username: {entries[itr].username} - password: {entries[itr].password}")

                    print()
                    print("1. Continue")
                    print("2. Add new")
                    print("3. Delete")
                    print("4. Modify")
                    print("5. Show details")

                    entries_user_input = input()

                    match entries_user_input:
                        # Continue
                        case "1":
                            continue
                        # Add new
                        case "2":
                            username = input("Username: ")
                            password = input("Password: ")
                            domain = input("Domain: ")
                            description = input("Description: ")

                            if username == "":
                                username = None
                            if password == "":
                                continue
                            if domain == "":
                                domain = None
                            if description == "":
                                description = None

                            database.insert(data=[(username, password, domain, description)])
                        # Delete
                        case "3":
                            entry_id = int(input("ID: ")) - 1
                            database.delete(entries[entry_id].rowid)
                        # Modify
                        case "4":
                            entry_id = int(input("ID: ")) - 1

                            change_username = input("Change username? N/y: ")
                            change_password = input("Change password? N/y: ")
                            change_domain = input("Change domain? N/y: ")
                            change_description = input("Change description? N/y: ")

                            if change_username == "y" or change_username == "Y":
                                username = input("Username: ")
                            else:
                                username = entries[entry_id].username

                            if change_password == "y" or change_password == "Y":
                                password = input("Password: ")
                            else:
                                password = entries[entry_id].password

                            if change_domain == "y" or change_domain == "Y":
                                domain = input("Domain: ")
                            else:
                                domain = entries[entry_id].domain

                            if change_description == "y" or change_description == "Y":
                                description = input("Description: ")
                            else:
                                description = entries[entry_id].description

                            if username == "":
                                username = None
                            if password == "":
                                continue
                            if domain == "":
                                domain = None
                            if description == "":
                                description = None

                            database.update(entries[entry_id].rowid, username, password, domain, description)
                        # Show details
                        case "5":
                            entry_id = int(input("ID: ")) - 1
                            print()
                            print(f"Rowid = {entries[entry_id].rowid}")
                            print(f"Username = {entries[entry_id].username}")
                            print(f"Password = {entries[entry_id].password}")
                            print(f"Domain = {entries[entry_id].domain}")
                            print(f"Description = {entries[entry_id].description}")
                            wait_for_user_input()
