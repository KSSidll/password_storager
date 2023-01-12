import os
import sqlite3

from db.database_connection import DatabaseConnection


class Database:
    __database_folder = "vault"
    __connections = {}

    @classmethod
    def create_database(cls, database_name) -> None:
        """
        Creates a new database file if it doesn't exist \n
        Passes any sqlite3.connect exceptions to caller
        :param database_name: string, Name of the database
        """
        if not os.path.exists(f"./{cls.__database_folder}"):
            os.mkdir(f"./{cls.__database_folder}")
        if not os.path.exists(f"./{cls.__database_folder}/{database_name}.db"):
            connection = None
            try:
                connection = sqlite3.connect(f"./{cls.__database_folder}/{database_name}.db")
            except:
                raise
            finally:
                if connection:
                    connection.close()

    @classmethod
    def databases(cls) -> list[str]:
        """
        Returns assumed database connections
        :return: list, Names of files that end with '.db' in currently set database folder
        """
        return [x[:-3] for x in os.listdir(f"./{cls.__database_folder}/") if x[-3:] == ".db"]

    @classmethod
    def connect(cls, database_name) -> DatabaseConnection:
        """
        Connects and returns the connection to specified database \n
        Ensures that there is always only 1 connection to each database
        :param database_name: string, Name of the database
        :return: DatabaseConnection, Connection to the specified database
        """
        if (database_name not in cls.__connections) or cls.__connections[database_name].closed:
            cls.__connections[database_name] = DatabaseConnection(f"./{cls.__database_folder}/{database_name}.db")

        connection = cls.__connections[database_name]
        connection.increment_reference_counter()

        return connection

    @classmethod
    def delete(cls, database_name) -> None:
        """
        Deletes specified database if it exists
        :param database_name: string, Name of the database
        """
        file = f"./{cls.__database_folder}/{database_name}.db"
        if os.path.exists(file):
            os.remove(file)

    @classmethod
    def change_database_folder(cls, database_folder) -> None:
        """
        Changes which folder to use as database storage
        :param database_folder: string, Name of the new folder
        """
        cls.__database_folder = database_folder
