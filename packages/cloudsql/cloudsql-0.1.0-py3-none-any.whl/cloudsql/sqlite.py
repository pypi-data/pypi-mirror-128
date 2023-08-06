import sqlite3
from flask import g

# sqlite interfaces
def get_db(database):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database)
    return db

def get_tables(conn):
    tables = []
    for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall():
        tables.append(row[0])
    return tables