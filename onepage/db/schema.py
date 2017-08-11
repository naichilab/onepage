from orator import DatabaseManager
from orator import Schema

from onepage.db import dbconfig


USER_TABLE_NAME = 'Users'
NOVEL_TABLE_NAME = 'Novels'
CATEGORY_TABLE_NAME = 'Categories'

db = DatabaseManager(dbconfig.DATABASES)
schema = Schema(db)

if not schema.has_table(USER_TABLE_NAME):
    with schema.create(USER_TABLE_NAME) as table:
        table.increments('id')
        table.string('email')
        table.string('password_hash')
        table.string('pen_name')
        table.timestamps()

        table.unique('email')

if not schema.has_table(CATEGORY_TABLE_NAME):
    with schema.create(CATEGORY_TABLE_NAME) as table:
        table.increments('id')
        table.string('name')

if not schema.has_table(NOVEL_TABLE_NAME):
    with schema.create(NOVEL_TABLE_NAME) as table:
        table.increments('id')
        table.string('title')
        table.string('text')
        table.timestamps()
        table.big_integer('user_id')
        table.drop_foreign('Novels_user_id_foreign')
        table.foreign('user_id').references('id').on(USER_TABLE_NAME)
        table.big_integer('category_id')
        table.drop_foreign('Novels_category_id_foreign')
        table.foreign('category_id').references('id').on(CATEGORY_TABLE_NAME)
