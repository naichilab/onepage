from orator import DatabaseManager, Model
from orator.orm import scope

from onepage.db import dbconfig


db = DatabaseManager(dbconfig.DATABASES)
Model.set_connection_resolver(db)


class User(Model):
    __table__ = 'Users'
    __fillable__ = ['pen_name']
    __guarded__ = ['email', 'password_hash']
    __timestamps__ = False

    @scope
    def find_by_email(self, query, email):
        return query.where_email(email).get().first()
