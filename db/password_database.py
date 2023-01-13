from db.database import Database
from db.model.password_entry import PasswordEntry


class PasswordsDatabase(Database):
    """
    Wrapper for Database that operates on databases consisting of table `passwords` with
    (id, username, password NOT NULL, domain, description) schema
    """

    @classmethod
    def create_database(cls, database_name: str) -> bool:
        try:
            created = super().create_database(database_name)
        except:
            raise

        if not created:
            return False

        connection = cls.connect(database_name)
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE passwords(username, password NOT NULL, domain, description)")
        connection.commit()

        connection.close()

    @classmethod
    def insert(cls, columns: str = None, values: list[str] = None,
               data: list[tuple[str | None, str, str | None, str | None]] = None) -> None:
        """
        Inserts data into the passwords table \n
        Argument `data` is prioritized
        :param columns: str, Columns to which insert the values, requires values, format `str, str, str`
        :param values: list[str], Values which to insert into the columns, requires columns
        :param data: Data which to insert into the table, has to include all columns
        :except SyntaxError: The number of columns isn't equal to the number of values
        """
        cursor = cls.current_connection.cursor()

        if data is not None:
            cursor.executemany("INSERT INTO passwords VALUES (?, ?, ?, ?)", data)
            cls.current_connection.commit()
            return

        if (columns is not None) and (values is not None):
            if len(values) is not columns.count(","):
                raise SyntaxError("The number of columns isn't equal to the number of values")

            cursor.execute(f"INSERT INTO passwords ({columns}) VALUES ('{repr(',').join(values)}')")
            cls.current_connection.commit()
            return

    @classmethod
    def select_all(cls) -> list[PasswordEntry]:
        cursor = cls.current_connection.cursor()
        query_result = cursor.execute("SELECT rowid, username, password, domain, description FROM passwords")
        query_rows = query_result.fetchall()

        entries = [PasswordEntry(x[0], x[2], x[1], x[3], x[4]) for x in query_rows]

        return entries

    @classmethod
    def delete(cls, rowid) -> None:
        cursor = cls.current_connection.cursor()
        cursor.execute(f"DELETE FROM passwords WHERE rowid='{rowid}'")
        cls.current_connection.commit()

    @classmethod
    def update(cls, rowid, username, password, domain, description):
        cursor = cls.current_connection.cursor()
        cursor.execute(f"UPDATE passwords SET username='{username}', password='{password}', domain='{domain}', "
                       f"description='{description}' WHERE rowid={rowid}")
        cls.current_connection.commit()

