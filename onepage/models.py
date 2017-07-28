from orator import DatabaseManager, Model
from onepage.db import dbconfig


db = DatabaseManager(dbconfig.DATABASES)
Model.set_connection_resolver(db)


class User(Model):
    __table__ = 'Users'
    __fillable__ = ['pen_name']
    __guarded__ = ['email', 'password']
    __timestamps__ = False
