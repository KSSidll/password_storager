from sqlite3 import Connection


class DatabaseConnection(Connection):
    """
    Makeshift reference counter wrapper for database connections to make sure only 1 connection
    is open to each individual database file
    """

    def __init__(self, database_path: str):
        super().__init__(database_path)
        self.database_path = database_path
        self.__instances = 0
        self.closed = False

    def increment_reference_counter(self):
        self.__instances += 1

    def close(self):
        """
        Reduces the reference counter and closes the connection if it's 0 \n
        i.e. closes the connection if all 'instances' of class called this method
        """
        self.__instances -= 1
        if self.__instances == 0:
            super().close()
            self.closed = True

    def force_close(self):
        """
        Closes the connection
        """
        self.__instances = 0
        super().close()
        self.closed = True
