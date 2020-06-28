import sqlite3
from sqlite3 import Error


class Database:
    def __init__(self):
        try:
            self.connection = sqlite3.connect('db.sqlite3')
        except Error:
            print(Error)

    def execute_query(self, query, parameters=()):
        cursor = self.connection.cursor()
        result = cursor.execute(query, parameters)
        self.connection.commit()
        return result


databease = Database()
query = """INSERT INTO Metodologia VALUES (NULL,?,?,?,?),
                                     (NULL,?,?,?,?),
                                     (NULL,?,?,?,?);"""

databease.execute_query(query, ["AGIL", "AGIL", 'A', 'A',
                                "HIBRIDO", "HIBRIDO", 'H', 'A',
                                "TRADICIONAL", "TRADICIONAL", 'T', 'A'])
