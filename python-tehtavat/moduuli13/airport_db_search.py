import mysql.connector

def connectDB():

    connection = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        database='world_cup',
        user='root',
        password='12345678',
        autocommit=True
        )

    return connection


def airport_search(icao):
    connection = connectDB()
    sql = """
    SELECT name, municipality
    FROM airport
    WHERE ident = %s;"""
    cursor = connection.cursor()
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    # print(result)
    if cursor.rowcount > 0:
        return result
    else:
        return "not found", "not found"
