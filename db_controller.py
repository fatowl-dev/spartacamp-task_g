import sqlite3


# データベースを操作するラッパー
# with文に対応
class DBController:
    def __init__(self, db_name: str):
        self.__db_name = db_name
        self.__connection = None
        self.__cursor = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def open(self):
        if self.__connection is not None:
            self.__connection.close()
        self.__connection = sqlite3.connect(self.__db_name)
        self.__cursor = self.__connection.cursor()
        return self

    def close(self):
        if self.__connection:
            self.__connection.close()
            self.__cursor = None
            self.__connection = None

    def execute(self, sql, params=()):
        self.__cursor.execute(sql, params)

    def fetchall(self):
        return self.__cursor.fetchall()

    def fetchone(self):
        return self.__cursor.fetchone()

    def commit(self):
        self.__connection.commit()

