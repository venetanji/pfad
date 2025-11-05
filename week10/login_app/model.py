from peewee import Model, CharField
from playhouse.sqlite_ext import SqliteExtDatabase

# Initialize the database
db = SqliteExtDatabase('users.db')

class User(Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db

# Create the table
db.connect()
db.create_tables([User])