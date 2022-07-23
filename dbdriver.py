import sqlite3

from pathlib import Path


class DBdriver():

    __DIR = Path(__file__).resolve()

    def __init__(self, name: str, dir=__DIR.parent):
        self.dbname = name
        self.dbpath = dir.__str__() + '/' + self.dbname + '.db'
        self.__var_filler()

    def __conection_manager(func):
        def wrapper(*args, **kwargs):
            self = args[0]
            self.conection = sqlite3.connect(self.dbpath)
            self.cursor = self.conection.cursor()
            result = func(*args, **kwargs)
            self.conection.commit()
            self.conection.close()
            return result
        return wrapper

    @__conection_manager
    def __var_filler(self):
        self.cursor.execute(
            'SELECT name from sqlite_master where type= "table"')
        self.tables = self.cursor.fetchall()

    @__conection_manager
    def create_table(self, name: str, *columns):
        self.tables.append(name)
        string = ''
        for column in columns:
            string = string + column + ', '
        string = string[:-2]
        print(string)
        self.cursor.execute(f"CREATE TABLE {name} ({string});")

    @__conection_manager
    def insert(self, table: str, values: tuple):
        string = ''
        for value in values:
            if type(value) == str:
                string = string + "'" + value + "', "
            else:
                string = string + value.__str__() + ", "
        string = string[:-2]
        print(string)
        self.cursor.execute(f"INSERT INTO {table} VALUES ({string});")

    @__conection_manager
    def remove(self, table, rowid: int):
        self.cursor.execute(f"DELETE from {table} WHERE rowid = {rowid};")
