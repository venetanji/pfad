from peewee import Model, CharField, BooleanField
from playhouse.sqlite_ext import SqliteExtDatabase

# Initialize the database
db = SqliteExtDatabase('users.db')

class User(Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    is_active = BooleanField(default=True)
    is_admin = BooleanField(default=False)

    class Meta:
        database = db

# Create the table
db.connect()
db.create_tables([User])