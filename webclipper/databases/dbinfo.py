import os
import sqlite3

__package_dir = os.path.abspath(os.path.dirname(__file__))
location = os.path.join(__package_dir, 'database.db')


def select(query: str()):
    connection = sqlite3.connect(location)
    cursor = connection.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


def modify(query: str()):
    connection = sqlite3.connect(location)
    connection.execute(query)
    connection.commit()
    connection.close()
