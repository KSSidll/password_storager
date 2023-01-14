import os
import sqlite3

from db.database_connection import DatabaseConnection


class Database:
    __connections = {}
    _password = None
    database_folder = "vault"
    current_connection: DatabaseConnection | None = None

    @classmethod
    def create_database(cls, database_name: str) -> bool:
        """
        Creates a new database file if it doesn't exist \n
        Passes any sqlite3.connect exceptions to caller
        :param database_name: string, Name of the database
        :return: bool, Whether database was created or not
        """
        if not os.path.exists(f"./{cls.database_folder}"):
            os.mkdir(f"./{cls.database_folder}")
        if not os.path.exists(f"./{cls.database_folder}/{database_name}.db"):
            connection = None
            try:
                connection = sqlite3.connect(f"./{cls.database_folder}/{database_name}.db")
            except:
                raise
            finally:
                if connection:
                    connection.close()
            return True
        else:
            return False

    @classmethod
    def databases(cls) -> list[str]:
        """
        Returns assumed database files
        :return: list, Names of files that end with '.db' in currently set database folder
        """
        return [x[:-3] for x in os.listdir(f"./{cls.database_folder}/") if x[-3:] == ".db"]

    @classmethod
    def encrypted_databases(cls) -> list[str]:
        """
        Returns assumed encrypted database files
        :return: list, Names of files that end with '.db.enc' in currently set database folder
        """
        return [x[:-7] for x in os.listdir(f"./{cls.database_folder}/") if x[-7:] == ".db.enc"]

    @classmethod
    def connect(cls, database_name: str) -> DatabaseConnection:
        """
        Connects and returns the connection to specified database \n
        Ensures that there is always only 1 connection to each database
        :param database_name: string, Name of the database
        :return: DatabaseConnection, Connection to the specified database
        """
        if (database_name not in cls.__connections) or cls.__connections[database_name].closed:
            cls.__connections[database_name] = DatabaseConnection(f"./{cls.database_folder}/{database_name}.db")

        connection = cls.__connections[database_name]
        connection.increment_reference_counter()

        return connection

    @classmethod
    def set_connection(cls, password: str | None, connection: DatabaseConnection = None, database_name: str = None)\
            -> None:
        """
        Sets current connection to the specified database \n
        If both arguments are passed, DatabaseConnection takes priority
        :param password: string, Password with which the data in the database was encrypted,
        use None only when closing connection
        :param connection: DatabaseConnection, connection obtained via method connect
        :param database_name: string, Name of the database
        """
        # close current connection
        if cls.current_connection is not None:
            cls.current_connection.close()
            cls.current_connection = None

        # set password for new connection
        cls._password = password

        # set new connection
        if connection is not None:
            cls.current_connection = connection
            return

        if database_name is not None:
            cls.current_connection = cls.connect(database_name)
            return

    @classmethod
    def delete_database(cls, database_name: str) -> None:
        """
        Deletes specified database if it exists
        :param database_name: string, Name of the database
        """
        file = f"./{cls.database_folder}/{database_name}.db"
        if os.path.exists(file):
            os.remove(file)

    @classmethod
    def delete_encrypted_database(cls, database_name: str) -> None:
        """
        Deletes specified database if it exists
        :param database_name: string, Name of the database
        """
        file = f"./{cls.database_folder}/{database_name}.db.enc"
        if os.path.exists(file):
            os.remove(file)

    @classmethod
    def change_database_folder(cls, database_folder: str) -> None:
        """
        Changes which folder to use as database storage
        :param database_folder: string, Name of the new folder
        """
        cls.database_folder = database_folder
