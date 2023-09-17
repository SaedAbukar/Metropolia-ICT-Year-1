# Write a program that asks the user for the country code (for example FI)
# and prints the number of airports in that country by type. For example, for Finland,
# the result must be information that there are 65 small airports, 15 heliports, etc.
import mysql.connector


def search_airport(ident):
    sql = '''
    SELECT type, COUNT(*) FROM airport 
    WHERE iso_country = %s 
    GROUP BY type ORDER BY COUNT(*) DESC;
    '''
    # print(sql)
    cursor = connection.cursor()
    cursor.execute(sql, (ident,))
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            print(f"Type: {row[0]}\nCount: {row[1]}.")
    return


connection = mysql.connector.connect(
         host='127.0.0.1',
         port=3306,
         database='flight_game',
         user='root',
         password='12345678',
         autocommit=True
         )

countrycode = input('Enter country code(FI, US, GB etc): ')
search_airport(countrycode)





# SELECT airport.type, COUNT(*)
# FROM airport, country
# WHERE airport.iso_country = country.iso_country AND country.iso_country = 'FI'
# GROUP BY airport.type ORDER BY COUNT(*) DESC;