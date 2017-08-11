from orator import DatabaseManager
from orator import Model
from orator.orm import has_many
from orator.orm import belongs_to

from onepage.db import dbconfig
from onepage.db import schema

Model.set_connection_resolver(DatabaseManager(dbconfig.DATABASES))


class User(Model):
    __table__ = schema.USER_TABLE_NAME
    __fillable__ = ['pen_name']
    __guarded__ = ['email', 'password_hash']
    __timestamps__ = False

    @classmethod
    def find_by_email(cls, email):
        return cls.query().where_email(email).get().first()

    @has_many
    def novels(self):
        return Novel


class Category(Model):
    __table__ = schema.CATEGORY_TABLE_NAME
    __fillable__ = ['name']

    @has_many
    def novels(self):
        return Novel


class Novel(Model):
    __table__ = schema.NOVEL_TABLE_NAME
    __fillable__ = ['title', 'text', 'user_id', 'category_id']

    @belongs_to
    def user(self):
        return User

    @belongs_to
    def category(self):
        return Category
