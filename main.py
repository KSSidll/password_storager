from db.password_database import PasswordsDatabase

db = PasswordsDatabase()
db.create_database("test")
db.set_connection(database_name="test")
print(db.databases())

