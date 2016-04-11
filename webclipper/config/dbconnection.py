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
    result = None
    connection = sqlite3.connect(locations.database)
    cursor = connection.execute(query)
    try:
        result = cursor.lastrowid
    except Exception:
        pass
    connection.commit()
    cursor.close()
    connection.close()
    return result
