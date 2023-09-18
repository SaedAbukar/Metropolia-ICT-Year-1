# Write a program that prompts the user for the airport's ICAO code.
# The program searches for and prints the name of the airport corresponding
# to the code and its location from the airport database used in the course.
# The ICAO code is stored in the ident column of the airport table.

import mysql.connector


def search_airport(ident):
    sql = "SELECT name, iso_country FROM airport WHERE ident = %s;"
    cursor = connection.cursor()
    cursor.execute(sql, (ident,))
    result = cursor.fetchall()
    if cursor.rowcount == 1:
        for row in result:
            print(f"The airport you searched for is {row[0]} and location is {row[1]}.")
    return


connection = mysql.connector.connect(
         host='127.0.0.1',
         port=3306,
         database='flight_game',
         user='root',
         password='12345678',
         autocommit=True
         )


airport = input('Enter the ICAO-code: ')
search_airport(airport)
