import sqlite3

from webclipper.config import locations


def select(query: str()):
    connection = sqlite3.connect(locations.database)
    cursor = connection.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


def modify(query: str()):
    connection = sqlite3.connect(locations.database)
    connection.execute(query)
    connection.commit()
    connection.close()
