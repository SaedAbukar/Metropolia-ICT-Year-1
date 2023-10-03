import mysql.connector
import random
import story
from geopy import distance

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='footy',
    user='root',
    password='12345678',
    autocommit=True
)


def get_fields():
    sql = """SELECT * from wc_fields ORDER BY RAND();"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


# get all goals
def get_opponents():
    sql = "SELECT * FROM world;"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def create_game(start_points, p_range, cur_airport, p_name, a_fields):
    sql = "INSERT INTO game (points, player_range, location, screen_name) VALUES (%s, %s, %s, %s);"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (start_points, p_range, cur_airport, p_name))
    o_id = cursor.lastrowid

    # add goals / loot boxes
    opponents = get_opponents()
    opp_list = []
    for opp in opponents:
        for i in range(0, opp['probability'], 1):
            opp_list.append(opp['id'])

    # exclude starting airport
    opp_ports = a_fields[1:].copy()
    random.shuffle(opp_ports)

    for i, opp_id in enumerate(opp_list):
        sql = "INSERT INTO arenas (game, airport, goal) VALUES (%s, %s, %s);"
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (o_id, opp_ports[i]['ident'], opp_id))

    return o_id


# get airport info
def get_field_info(icao):
    sql = f'''SELECT iso_country, ident, name, latitude_deg, longitude_deg
                  FROM wc_fields
                  WHERE ident = %s'''
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    return result


def check_goal(g_id, cur_airport):
    sql = f'''SELECT arenas.id, goal, name, points 
    FROM arenas 
    JOIN world ON world.id = arenas.goal 
    WHERE game = %s 
    AND airport = %s'''
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (g_id, cur_airport))
    result = cursor.fetchone()
    if result is None:
        return False
    return result


def calculate_distance(current, target):
    start = get_field_info(current)
    end = get_field_info(target)
    return distance.distance((start['latitude_deg'], start['longitude_deg']),
                             (end['latitude_deg'], end['longitude_deg'])).km


# get airports in range
def fields_in_range(icao, a_fields, p_range):
    in_range = []
    for a_fields in a_fields:
        dist = calculate_distance(icao, a_fields['ident'])
        if dist <= p_range and not dist == 0:
            in_range.append(a_fields)
    return in_range


def update_location(icao, p_range, u_points, g_id):
    sql = f'''UPDATE game SET location = %s, player_range = %s, points = %s WHERE id = %s'''
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (icao, p_range, u_points, g_id))


CENTER = 0
LEFT = 1
RIGHT = 2


def dive():
    number = random.randint(1, 2)
    return number


# Implement your functions here.
def goal(kick_direction, dive_direction):
    if kick_direction == dive_direction:
        return False
    else:
        return True


def print_ball(ball):
    if ball == 1:
        print("-----------------")
        print("| O             |")
        print("|               |")
        print("|               |")

    if ball == 2:
        print("-----------------")
        print("|             O |")
        print("|               |")
        print("|               |")


def print_goalkeeper(goalkeeper):
    if goalkeeper == 1:
        print("-----------------")
        print("| _ o|          |")
        print("|    \          |")
        print("|     \\\        |")

    if goalkeeper == 2:
        print("-----------------")
        print("|          |o _ |")
        print("|          /    |")
        print("|        //     |")


def penalty_shootout(team):
    seed_number = 87
    random.seed(seed_number)

    print("-----------------")
    print("|     _ o _     |")
    print("|       |       |")
    print("|      / \      |")

    number_of_rounds = 5
    team1 = 'Suomi'
    team2 = team
    game_continues = True
    team1_score = 0
    team2_score = 0
    team1_turn = 0
    team2_turn = 0
    current_team = team2
    rounds = 0

    while game_continues:
        if abs(team1_score - team2_score) > (number_of_rounds - rounds) and team1_turn == team2_turn:
            game_continues = False
        else:
            if team1_turn == team2_turn:
                rounds += 1
                print(f'KIERROS {rounds}')
            print(f'{team1} on tehnyt {team1_score} maalia, {team2} on tehnyt {team2_score}.')
            if current_team == team1:
                current_team = team2
                print(f"Nyt on {current_team} joukkueen vuoro!")
                team2_turn += 1
            else:
                current_team = team1
                print(f"Nyt on {current_team} joukkueen vuoro")
                team1_turn += 1

            if current_team == team1:
                kick = int(input(f"Kumpaan suuntaan pelaaja vetää?? (1: vasemmalle/2: oikealle)\n"))
                while kick != 1 and kick != 2:
                    print(f'Syötä 1 tai 2')
                    kick = int(input(f"Kumpaan suuntaan pelaaja vetää? (1: vasemmalle/2: oikealle)\n"))
            else:
                kick = random.randint(1, 2)

            if current_team == team2:
                dive_direction = int(input(f"Minne maalivahti hyppää? (1: vasemmalle/2: oikealle)\n"))
                while dive_direction != 1 and dive_direction != 2:
                    print(f'Syötä 1 tai 2')
                    dive_direction = int(input(f"Minne maalivahti hyppää? (1: vasemmalle/2: oikealle)\n"))
            else:
                dive_direction = dive()

            if goal(kick, dive_direction):
                print(f'Veto: {kick} Torjunta: {dive_direction}')
                print(f"Ja veto menee...")
                print_ball(kick)
                print(f"Ja maalivahti menee...")
                print_goalkeeper(dive_direction)
                print(f'{current_team} sai maalin!')

                if current_team == team1:
                    team1_score += 1
                else:
                    team2_score += 1

            else:
                print(f'Veto: {kick} Torjunta: {dive_direction}')
                print(f"Ja veto menee...")
                print_ball(kick)
                print(f"Ja maalivahti menee...")
                print_goalkeeper(dive_direction)
                print(f'Ei maalia. Maalivahti torjui vedon!')

            if rounds >= number_of_rounds and team1_score == team2_score and team1_turn == team2_turn:
                print("Tasapeli! Siirrytään äkkikuolema -kierroksiin!")
                number_of_rounds += 1

    print(f'{team1} yritykset: {team1_turn}')
    print(f'{team2} yritykset: {team2_turn}')
    print(f"Peli päättyi! {team1} teki {team1_score} ja {team2} teki {team2_score}")
    if team1_score > team2_score:
        print(f"{team1} voitti!")
        return team1
    elif team2_score > team1_score:
        print(f"{team2} voitti!")
        return team2


# game stars


# game loop
def main():
    visited_fields = []

    lohkopelit = 3
    pudotuspelit = 1

    lohkopeli_voitot = 0
    pudotuspeli_voitot = 0

    storyDialog = input('Haluatko lukea pelin tarinan? (K/E): ')
    if storyDialog == 'K':
        for line in story.get_story():
            print(line)

    print('Tervetuloa Yhdysvaltojen, Meksikon ja Kanadan 2026 MM-kisoihin.')
    player = input('Syötä pelaaja nimesi: ')

    # check if the game is over
    game_over = False

    # check if the player has won
    win = False

    # starting money
    points = 0

    # starting range
    player_range = 5000

    played = 0

    # count the player score
    score = 0

    # all airports
    all_fields = get_fields()
    # starting point
    start_fields = all_fields[0]['ident']

    # current airport
    current_field = start_fields

    # game id
    game_id = create_game(points, player_range, start_fields, player, all_fields)

    while not game_over:
        print(f'Ottelut {played}/7. Voitot {score}/{played}. '
              f'Sinulla on jäljellä {7 - played} ottelua.')
        # get current airport info
        airport = get_field_info(current_field)
        print(f"Saavuit jalkapallokentälle: {airport['name']}.")
        print(f"Olet pelannut {played} ottelua ja voittanut {score}. "
              f"Sinulla on {points:.0f}pistettä ja {player_range:.0f}km etäisyyttä.")
        input('\033[32mPaina Enteriä selvittääksesi onko kentällä vastustaja...\033[0m')
        # if airport has an opponent the player plays them
        # check the goal type and add if wins
        for i in range(lohkopelit):
            goal = check_goal(game_id, current_field)
            if goal:
                print('Tällä kentällä on vastustaja. Valmistaudu!')
                winning_team = penalty_shootout(goal['name'])
                if winning_team == 'Suomi':
                    score += 1
                    played += 1
                    points += goal['points']
                    player_range += 500
                    print(f"Ottelun voittaja on {winning_team}!")
                else:
                    print(f'Peli päättyi. Hävisit ottelun. Onnea seuraavaan koitokseen!')
                    played += 1

            else:
                print(f'Tällä kentällä ei ole vastustajaa. Siirry seuraavalle kentälle')
        if lohkopeli_voitot >= 2:
            print(f'Onnittelut! Selvisit pudotuspelikierrokselle!')
            for i in range(pudotuspelit):
                goal = check_goal(game_id, current_field)
                if goal:
                    print('Tällä kentällä on vastustaja. Valmistaudu!')
                    winning_team = penalty_shootout(goal['name'])
                    if winning_team == 'Suomi':
                        score += 1
                        played += 1
                        points += goal['points']
                        player_range += 500
                        print(f"Ottelun voittaja on {winning_team}!")
                    else:
                        print(f'Peli päättyi. Hävisit ottelun. Onnea seuraavaan koitokseen!')
                        played += 1
                        game_over = True
        else:
            print(f'Valitettavasti et voittanut kahta peliä kolmesta lohkopeliotteluista.'
                  f'Sinun MM-kisa taivel päättyy tähän. Parempaa onnea seuraaviin kisoihin!')

        fields = fields_in_range(current_field, all_fields, player_range)
        print(f'Voit lentää näin monelle jalkapallokentälle {len(fields)}')
        print('Jalkapallo Stadionit:')
        for field in fields:
            f_distance = calculate_distance(current_field, field['ident'])
            print(f"ICAO: {field['ident']}, Name: {field['name']}, Distance: {f_distance:.0f}km")

        if played == 7:
            game_over = True

        try:
            dest = input('Syötä kohdekentän ICAO: ')
            while dest in visited_fields:
                print("Olet jo vieraillut tässä kentässä!")
                dest = input('Syötä uuden kohdekentän ICAO: ')

            else:
                selected_distance = calculate_distance(current_field, dest)
                update_location(dest, player_range, points, game_id)
                current_field = dest
                # Inside the loop where the player selects the destination field (after updating current_field):
                visited_fields.append(current_field)
        except ValueError:
            print(f'Virheellinen syöte. Syötä vaihtoehdoista haluamasi kohdekentän ICAO-koodi:')

    if score == 7:
        print(f'Olet maailman mestari!')
        print(f'Pelasit kaikki ottelut ja voitit jokaisen ottelun!')
        print(f'Pelasit {played} ottelua ja voitit {score} ottelua. Sait {points} verran pisteitä!')
    else:
        print(f'Taistelit hienosti, mutta et valitettavasti voittanut jokaista peliä.')
        print(f'Pelasit {played} ottelua ja voitit {score} ottelua. Sait {points} verran pisteitä!')
        print(f'Parempaa menestystä seuraavalle kerralle!')


main()
