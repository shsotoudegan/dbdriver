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

    @__conection_manager
    def insertMore(self, table, values):
        for value in values:
            self.insert(table, value)

    @__conection_manager
    def removeMore(self, table, rowids):
        for rowid in rowids:
            self.remove(table, rowid)

    @__conection_manager
    def get(self, table, rowid):
        self.cursor.execute(f"SELECT * FROM {table} WHERE rowid = {rowid}")
        return self.cursor.fetchall()

    @__conection_manager
    def getMore(self, table, rowids):
        values = []
        for rowid in rowids:
            values.append(self.get(table, rowid))
        return values

    @__conection_manager
    def getTable(self, table):
        self.cursor.execute(f"SELECT * FROM {table}")
        return self.cursor.fetchall()
