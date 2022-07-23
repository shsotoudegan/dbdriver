import sqlite3

from pathlib import Path


class DBdriver():

    __DIR = Path(__file__).resolve()

    def __init__(self, name: str, dir=__DIR.parent):
        self.dbname = name
        self.dbpath = dir.__str__() + self.dbname + '.db'
        self.conection = sqlite3.connect(self.dbpath)
        self.cursor = self.conection.cursor()

    def create_table(self, name: str, *columns):
        string = ''
        for column in columns:
            string = string + column
        print(string)
        self.cursor.execute(f"CREATE TABLE {name} ({string});")
        self.conection.commit()
