import os
import sqlite3


class DatabaseConnection(sqlite3.Connection):
    def __init__(self, database_path):
        super().__init__(database_path)
        self.__instances = 0
        self.closed = False
    
    def increment_reference_counter(self):
        self.__instances += 1
        
    def close(self):
        """
        reduces the reference counter and closes the connection if it's 0 \n
        i.e. closes the connection if all 'instances' of class called this method
        """
        self.__instances -= 1
        if self.__instances == 0:
            super().close()
            self.closed = True

    def force_close(self):
        """
        closes the connection
        """
        self.__instances = 0
        super().close()
        self.closed = True


class Database:
    connections = {}

    @staticmethod
    def create_database(database_name):
        """
        Creates a new database file if it doesn't exist
        Passes any sqlite3.connect exceptions to caller
        :param database_name: string, Name of the database
        """
        if not os.path.exists("./db"):
            os.mkdir("./db")
        if not os.path.exists(f"./db/{database_name}.db"):
            connection = None
            try:
                connection = sqlite3.connect(f"./db/{database_name}.db")
            except:
                raise
            finally:
                if connection:
                    connection.close()

    @staticmethod
    def databases() -> list[str]:
        """
        returns assumed database connections
        :return: list, names of files that end with '.db' in ./db directory
        """
        return [x[:-3] for x in os.listdir("./db/") if x[-3:] == ".db"]

    @classmethod
    def connect(cls, database_name) -> DatabaseConnection:
        """
        Connects and returns the connection to specified database \n
        Ensures that there is always only 1 connection to each database
        :param database_name: string, name of the database
        :return: DatabaseConnection, Connection to the specified database
        """
        if (database_name not in cls.connections) or cls.connections[database_name].closed:
            cls.connections[database_name] = DatabaseConnection(f"./db/{database_name}.db")

        connection = cls.connections[database_name]
        connection.increment_reference_counter()

        return connection
