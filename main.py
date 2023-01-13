from db.password_database import PasswordsDatabase


database = PasswordsDatabase()
user_input = None
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
    if database.current_connection is not None:
        print(f"6. Show database data")

    print()
    user_input = input("Next command: ")

    print("----------------------------")

    match user_input:
        case "0":
            break
        case "1":
            print('\n'.join(database.databases()))
            input("Continue...")
        case "2":
            database_name = input("Database name: ")
            if database_name != "":
                database.create_database(database_name)
        case "3":
            database_name = input("Database name: ")
            if database_name != "":
                database.delete_database(input("Database name: "))
        case "4":
            database_name = input("Database name: ")
            if database_name != "":
                database.set_connection(database_name=database_name)
        case "5":
            new_folder = input("Database folder name: ")
            if new_folder != "":
                database.change_database_folder(new_folder)
        case "6":
            if database.current_connection is not None:
                entries = database.select_all()
                for itr in range(len(entries)):
                    print(f"{itr+1} | username: {entries[itr].username} - password: {entries[itr].password}")

                print()
                print("1. Continue")
                print("2. Add new")
                print("3. Delete")
                print("4. Modify")
                print("5. Show details")

                entries_user_input = input()

                match entries_user_input:
                    case "1":
                        continue
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
                    case "3":
                        entry_id = int(input("ID: ")) - 1
                        database.delete(entries[entry_id].rowid)
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
                    case "5":
                        entry_id = int(input("ID: ")) - 1
                        print()
                        print(f"Rowid = {entries[entry_id].rowid}")
                        print(f"Username = {entries[entry_id].username}")
                        print(f"Password = {entries[entry_id].password}")
                        print(f"Domain = {entries[entry_id].domain}")
                        print(f"Description = {entries[entry_id].description}")
                        input("Continue...")
