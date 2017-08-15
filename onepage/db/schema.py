from orator import DatabaseManager
from orator import Schema

from onepage.db import dbconfig


USER_TABLE_NAME = 'Users'
NOVEL_TABLE_NAME = 'Novels'
TAG_TABLE_NAME = 'Tags'
TAG_NOVEL_TABLE_NAME = 'Novels_Tags'

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

if not schema.has_table(TAG_TABLE_NAME):
    with schema.create(TAG_TABLE_NAME) as table:
        table.increments('id')
        table.string('name')

if not schema.has_table(NOVEL_TABLE_NAME):
    with schema.create(NOVEL_TABLE_NAME) as table:
        table.increments('id')
        table.string('title')
        table.string('text')
        table.timestamps()

        table.integer('user_id').unsigned()
        table.foreign('user_id').references('id').on(USER_TABLE_NAME)

if not schema.has_table(TAG_NOVEL_TABLE_NAME):
    with schema.create(TAG_NOVEL_TABLE_NAME) as table:
        table.increments('id')

        table.integer('tag_id').unsigned()
        table.foreign('tag_id').references('id').on(TAG_TABLE_NAME)
        table.integer('novel_id').unsigned()
        table.foreign('novel_id').references('id').on(NOVEL_TABLE_NAME)
