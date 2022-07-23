import sqlite3
from pathlib import Path


class DBdriver():
    DIR = Path(__file__).resolve()

    def __init__(self, dir: str, name: str):
        self.dbpath = dir
        self.dbname = name
