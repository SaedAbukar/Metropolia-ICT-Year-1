import json
import random
from flask import Flask
from database import Database
from flask_cors import CORS
from geopy import distance

db = Database()
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# @app.route('/continents')
# def continents():
#     sql = f'''SELECT DISTINCT continent
#               FROM country'''
#     cursor = db.get_conn().cursor(dictionary=True)
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     return json.dumps(result)
# #
# #
# @app.route('/countries/<continent>')
# def countries_by_continent(continent):
#     sql = f'''SELECT iso_country, name
#               FROM country
#               WHERE continent = %s'''
#     cursor = db.get_conn().cursor(dictionary=True)
#     cursor.execute(sql, (continent,))
#     result = cursor.fetchall()
#     return json.dumps(result)
#
#
# @app.route('/airports/<country>')
# def airports_by_country(country):
#     sql = f'''SELECT ident, name, latitude_deg, longitude_deg
#               FROM wc_fields
#               WHERE iso_country = %s'''
#     cursor = db.get_conn().cursor(dictionary=True)
#     cursor.execute(sql, (country,))
#     result = cursor.fetchall()
#     return json.dumps(result)
#
#
# @app.route('/airport/<icao>')
# def airport(icao):
#     sql = f'''SELECT name, latitude_deg, longitude_deg
#               FROM airport
#               WHERE ident=%s'''
#     cursor = db.get_conn().cursor(dictionary=True)
#     cursor.execute(sql, (icao,))
#     result = cursor.fetchone()
#     return json.dumps(result)



@app.route('/get_fields')
def get_fields():
    sql = """SELECT * from wc_fields ORDER BY RAND();"""
    cursor = db.get_conn().cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return json.dumps(result)


@app.route('/get_opponents')
def get_opponents():
    sql = "SELECT * FROM world;"
    cursor = db.get_conn().cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return json.dumps(result)


# @app.route('/create_game/<start_points>/<p_range>/<cur_airport>/<p_name>/<a_fields>')
# def create_game(start_points, p_range, cur_airport, p_name):
#     sql = "INSERT INTO game (points, player_range, location, screen_name) VALUES (%s, %s, %s, %s);"
#     cursor = db.get_conn().cursor(dictionary=True)
#     cursor.execute(sql, (start_points, p_range, cur_airport, p_name))
#     o_id = cursor.lastrowid
#
#
#     # Lisää vastustajat
#     opponents = get_opponents()
#     opp_list = []
#     for opp in opponents:
#         for i in range(0, opp['probability'], 1):
#             opp_list.append(opp['id'])
#
#     # älä lisää vastustajaa aloituskentälle
#     opp_ports = a_fields[1:].copy()
#     random.shuffle(opp_ports)
#
#     for i, opp_id in enumerate(opp_list):
#         sql = "INSERT INTO arenas (game, airport, goal) VALUES (%s, %s, %s);"
#         cursor = db.get_conn().cursor(dictionary=True)
#         cursor.execute(sql, (o_id, opp_ports[i]['ident'], opp_id))
#
#     return json.dumps(o_id)

@app.route('/fields/<icao>')
def airport(icao):
    sql = f'''SELECT name, latitude_deg, longitude_deg
              FROM wc_fields
              WHERE ident=%s'''
    cursor = db.get_conn().cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    return json.dumps(result)


@app.route('/get_field_info/<icao>')
# kentän info
def get_field_info(icao):
    sql = f'''SELECT iso_country, ident, name, latitude_deg, longitude_deg
                  FROM wc_fields
                  WHERE ident = %s'''
    cursor = db.get_conn().cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    return json.dumps(result)


@app.route('/check_goal/<g_id>/<cur_airport>')
# tarkista onko kentällä vastustaja
def check_goal(g_id, cur_airport):
    sql = f'''SELECT arenas.id, goal, name, points
    FROM arenas
    JOIN world ON world.id = arenas.goal
    WHERE game = %s
    AND airport = %s'''
    cursor = db.get_conn().cursor(dictionary=True)
    cursor.execute(sql, (g_id, cur_airport))
    result = cursor.fetchone()
    if result is None:
        return False
    return json.dumps(result)
#
#
# # laske etäisyys
# def calculate_distance(current, target):
#     start = get_field_info(current)
#     end = get_field_info(target)
#     return distance.distance((start['latitude_deg'], start['longitude_deg']),
#                              (end['latitude_deg'], end['longitude_deg'])).km
# #
# #
# # # get airports in range
# @app.route('/fields_in_range/<icao>/<a_fields>/<p_range>')
# def fields_in_range(icao, a_fields, p_range):
#     in_range = []
#     for a_fields in a_fields:
#         dist = calculate_distance(icao, a_fields['ident'])
#         if dist <= p_range and not dist == 0:
#             in_range.append(a_fields)
#     return json.dumps(in_range)
#
#
# päivitä pelaajan uusi sijainti
@app.route('/update_location/<icao>/<p_range>/<u_points>/<g_id>')
def update_location(icao, p_range, u_points, g_id):
    sql = f'''UPDATE game SET location = %s, player_range = %s, points = %s WHERE id = %s'''
    cursor = db.get_conn().cursor(dictionary=True)
    cursor.execute(sql, (icao, p_range, u_points, g_id))
    result = cursor.fetchone()
    return json.dumps(result)
#
#
if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
#
# inputs and prints are moved to web page
