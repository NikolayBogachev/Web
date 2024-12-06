from tinydb import TinyDB


db = TinyDB("app/templates.json")


def get_db():
    return db


def get_all():
    db = get_db()
    return db.all()
