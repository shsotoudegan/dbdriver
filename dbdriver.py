import sqlite3

from pathlib import Path


class DBdriver():

    __DIR = Path(__file__).resolve()

    def __init__(self, name: str, dir=__DIR.parent):
        self.dbname = name
        self.dbpath = dir.__str__() + '/' + self.dbname + '.db'

    def __cncdec(func):
        def wrapper(*args, **kwargs):
            self = args[0]
            self.conection = sqlite3.connect(self.dbpath)
            self.cursor = self.conection.cursor()
            result = func(*args, **kwargs)
            self.conection.commit()
            self.conection.close()
            return result
        return wrapper

    @__cncdec
    def create_table(self, name: str, *columns):
        string = ''
        for column in columns:
            string = string + column + ' '
        self.cursor.execute(f"CREATE TABLE {name} ({string});")
