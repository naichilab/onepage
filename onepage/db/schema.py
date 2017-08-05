from orator import DatabaseManager
from orator import Schema

from onepage.db import dbconfig


db = DatabaseManager(dbconfig.DATABASES)
schema = Schema(db)

with schema.create('Users') as table:
    table.increments('id')
    table.string('email')
    table.string('password_hash')
    table.string('pen_name')
    table.timestamps()

    table.unique('email')
