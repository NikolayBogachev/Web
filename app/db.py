import os
from tinydb import TinyDB

# Используем абсолютный путь относительно текущего каталога приложения
db_path = os.path.join(os.path.dirname(__file__), "templates.json")
db = TinyDB(db_path)


def get_db():
    return db


def get_all():
    db = get_db()
    return db.all()
