from db import database

db = database.Database()
db.create_database("test")
db_test = db.connect("test")
print(db.databases())

