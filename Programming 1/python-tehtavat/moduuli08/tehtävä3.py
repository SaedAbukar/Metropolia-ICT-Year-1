# Write a program that prompts the user for the ICAO codes of two airports.
# The program indicates the distance between the airports in kilometers.
# The calculation is based on the coordinates retrieved from the database.
# Calculate the distance using the geopy library:
import mysql.connector
from geopy.distance import geodesic


def search_airport(ident):
    sql = "SELECT latitude_deg, longitude_deg FROM airport WHERE ident = %s;"
    cursor = connection.cursor()
    cursor.execute(sql, (ident,))
    lat, long = result = cursor.fetchone()
    return lat, long

connection = mysql.connector.connect(
         host='127.0.0.1',
         port=3306,
         database='flight_game',
         user='root',
         password='12345678',
         autocommit=True
         )

airport1 = input('Enter the ICAO-code of the first airport: ')
airport2 = input('Enter the ICAO-code of the second airport: ')
distance = geodesic(search_airport(airport1), search_airport(airport2)).kilometers

print(f'The distance between the airports is {distance:.0f} kilometers.')
