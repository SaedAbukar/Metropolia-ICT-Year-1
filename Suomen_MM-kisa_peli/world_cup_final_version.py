import mysql.connector
import random
import story
from penalties import penalty_shootout
from colorama import Fore, Style
from geopy import distance

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='footy',
    user='root',
    password='12345678',
    autocommit=True
)


# Pelin funktiot
def get_fields():
    sql = """SELECT * from wc_fields ORDER BY RAND();"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


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

    # Lisää vastustajat
    opponents = get_opponents()
    opp_list = []
    for opp in opponents:
        for i in range(0, opp['probability'], 1):
            opp_list.append(opp['id'])

    # älä lisää vastustajaa aloituskentälle
    opp_ports = a_fields[1:].copy()
    random.shuffle(opp_ports)

    for i, opp_id in enumerate(opp_list):
        sql = "INSERT INTO arenas (game, airport, goal) VALUES (%s, %s, %s);"
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (o_id, opp_ports[i]['ident'], opp_id))

    return o_id


# kentän info
def get_field_info(icao):
    sql = f'''SELECT iso_country, ident, name, latitude_deg, longitude_deg
                  FROM wc_fields
                  WHERE ident = %s'''
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    return result


# tarkista onko kentällä vastustaja
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


# laske etäisyys
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


# päivitä pelaajan uusi sijainti
def update_location(icao, p_range, u_points, g_id):
    sql = f'''UPDATE game SET location = %s, player_range = %s, points = %s WHERE id = %s'''
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (icao, p_range, u_points, g_id))


# Peli alkaa
# Peli looppi
def main():
    print(story.colored_text)
    visited_fields = []
    lohkopeli_voitot = 0
    storyDialog = input('Haluatko lukea pelin tarinan? (K/E): ').lower()
    if storyDialog == 'k':
        story.get_story()

    rulesDialog = input('Haluatko lukea pelin säännöt? (K/E): ').lower()
    if rulesDialog == 'k':
        story.get_rules()

    # Tervetuloa teksti
    usa = story.yhdysvallat
    meksiko = story.meksiko
    kanada = story.kanada
    print(f'Tervetuloa {usa} {story.statue_of_liberty_emoji}, {meksiko} {story.cactus_emoji} ja {kanada} {story.maple_emoji} 2026 MM-kisoihin.')
    player = input('Syötä pelaaja nimesi: ')

    # Tarkista pelin tilanne
    game_over = False

    # Aloitus raha
    points = 0

    # Aloitus etäisyys
    player_range = 5000

    # Pelaajan tilastot
    played = 0
    yritykset = 0
    co2_consumed = 0
    score = 0

    # Tallenna kaikki kentät muuttujaan
    all_fields = get_fields()

    # Aloitus kenttä muuttujaan
    start_fields = all_fields[0]['ident']

    # Tämän hetkinen kenttä muuttujaan
    current_field = start_fields

    # Pelin id
    game_id = create_game(points, player_range, start_fields, player, all_fields)

    # Alkulohko looppi
    while not game_over:
        print(f'Ottelut: {played}/7, Voitot: {score}/{played}, Matkustuskerrat: {yritykset}, CO2 päästöt: {co2_consumed}.'
              f' Sinulla on jäljellä {7 - played} ottelua.')
        # tämän hetkisen kentän info
        airport = get_field_info(current_field)
        print(f"Saavuit jalkapallokentälle: {airport['name']} {story.landing_airplane_emoji}.")
        input(Fore.BLUE + 'Paina Enteriä selvittääksesi onko kentällä vastustaja...' + Fore.RESET)
        # Jos kentällä on vastustaja pelaaja pelaa ottelun
        # Tarkista vastustaja ja lisää ehdot voitolle
        goal = check_goal(game_id, current_field)
        if goal:
            print(f'Tällä kentällä on vastustaja. {story.check_mark_emoji} Valmistaudu!')
            print(f"Tämän ottelun vastustaja on {goal['name']}...")
            winning_team = penalty_shootout(goal['name'])
            yritykset += 1
            co2_consumed += 200
            if winning_team == 'Suomi':
                score += 1
                played += 1
                points += goal['points']
                player_range += 500
                lohkopeli_voitot += 1
                print(f"Ottelun voittaja on {winning_team}!")
            else:
                print(f'Peli päättyi. Hävisit ottelun. Onnea seuraavaan koitokseen!')
                played += 1

        else:
            print(f'Tällä kentällä ei ole vastustajaa. {story.x_emoji} Siirry seuraavalle kentälle. {story.next_emoji}')
            yritykset += 1
            co2_consumed += 200

        # Tarkista selvisikö pelaaja pudotuspelivaiheeseen
        if played >= 3 and lohkopeli_voitot >= 2:
            print(f'Onnittelut! Selvisit pudotuspelikierrokselle! {story.smiley_emoji}')
            fields = fields_in_range(current_field, all_fields, player_range)
            print(f'Voit lentää näin monelle jalkapallokentälle: {len(fields) - len(visited_fields)}.{story.takeoff_airplane_emoji}. Värjätyille kentille et voi lentää!')
            print(f'Jalkapallokentät{story.stadium_emoji}:')
            for field in fields:
                if field['ident'] in visited_fields:
                    f_distance = calculate_distance(current_field, field['ident'])
                    # Print visited fields in red
                    print(
                        f"{Fore.GREEN}ICAO: {field['ident']}, Name: {field['name']}, Distance: {f_distance:.0f}km (Vierailtu!){Fore.RESET}")
                else:
                    f_distance = calculate_distance(current_field, field['ident'])
                    print(f"ICAO: {field['ident']}, Name: {field['name']}, Distance: {f_distance:.0f}km")

            while True:
                try:
                    dest = input('Syötä kohdekentän ICAO: ').upper()
                    if dest in visited_fields:
                        print("Olet jo vieraillut tässä kentässä!")
                    elif dest in [field['ident'] for field in fields]:
                        selected_distance = calculate_distance(current_field, dest)
                        update_location(dest, player_range, points, game_id)
                        current_field = dest
                        visited_fields.append(current_field)
                        break  # Poistutaan silmukasta, kun käyttäjän syöte on kelvollinen
                    else:
                        print(f"Virheellinen syöte. {story.x_emoji} Syötä kohdekenttä listalta.")
                except ValueError:
                    print(f"Virheellinen syöte. {story.x_emoji} Syötä kohdekentän ICAO-koodi.")

            # Pudotuspeli looppi
            i = 0
            pudotuspeli_voitot = 0
            pudotuspeli_häviöt = 0
            while pudotuspeli_voitot < 4 and pudotuspeli_häviöt < 1:
                if played >= 7 and pudotuspeli_voitot >= 4 or pudotuspeli_häviöt > 0:
                    game_over = True
                vaiheet = ['16-parhaan joukko', '8-parhaan joukko', 'Semi-finaali', 'Finaali']
                print(f'Ottelut: {played}/7, Voitot: {score}/{played}, Matkustuskerrat: {yritykset}, CO2 päästöt {co2_consumed}.'
                      f' Sinulla on jäljellä {7 - played} ottelua.')
                print(f'Pudotuspelivaihe: {vaiheet[i]}.')
                input(Fore.BLUE + 'Paina Enteriä selvittääksesi onko kentällä vastustaja...' + Fore.RESET)
                goal = check_goal(game_id, current_field)
                if goal:
                    print(f'Tällä kentällä on vastustaja. {story.check_mark_emoji} Valmistaudu!')
                    print(f"Tämän ottelun vastustaja on {goal['name']}...")
                    winning_team = penalty_shootout(goal['name'])
                    yritykset += 1
                    co2_consumed += 200
                    if winning_team == 'Suomi':
                        score += 1
                        played += 1
                        pudotuspeli_voitot += 1
                        points += goal['points']
                        player_range += 500
                        i += 1
                        print(f"Ottelun voittaja on {winning_team}!")
                        if played >= 7 and pudotuspeli_voitot >= 4 or pudotuspeli_häviöt > 0:
                            game_over = True
                        else:
                            fields = fields_in_range(current_field, all_fields, player_range)
                            print(f'Voit lentää näin monelle jalkapallokentälle: {len(fields) - len(visited_fields)} {story.takeoff_airplane_emoji}. Värjätyille kentille et voi lentää!')
                            print(f'Jalkapallokentät {story.stadium_emoji}:')
                            for field in fields:
                                if field['ident'] in visited_fields:
                                    f_distance = calculate_distance(current_field, field['ident'])
                                    # Tulosta vieraillut kentät vihreällä
                                    print(
                                        f"{Fore.GREEN}ICAO: {field['ident']}, Name: {field['name']}, Distance: {f_distance:.0f}km (Vierailtu!){Fore.RESET}")
                                else:
                                    f_distance = calculate_distance(current_field, field['ident'])
                                    print(
                                        f"ICAO: {field['ident']}, Name: {field['name']}, Distance: {f_distance:.0f}km")

                            while True:
                                try:
                                    dest = input('Syötä kohdekentän ICAO: ').upper()
                                    if dest in visited_fields:
                                        print(Fore.RED + f"Olet jo vieraillut tässä kentässä!{story.x_emoji}" + Fore.RESET)
                                    elif dest in [field['ident'] for field in fields]:
                                        selected_distance = calculate_distance(current_field, dest)
                                        update_location(dest, player_range, points, game_id)
                                        current_field = dest
                                        visited_fields.append(current_field)
                                        break  # Poistutaan silmukasta, kun käyttäjän syöte on kelvollinen
                                    else:
                                        print(f"Virheellinen syöte.{story.x_emoji} Syötä kohdekenttä listalta.")
                                except ValueError:
                                    print(f"Virheellinen syöte.{story.x_emoji} Syötä kohdekentän ICAO-koodi.")
                    else:
                        print(f'Voi ei! Hävisit rangaistuspotkukilpailun!{story.sad_emoji}'
                              f' Tällä kertaa matkasi loppui pudotuspelivaiheeseen: {vaiheet[i]}.')
                        pudotuspeli_häviöt += 1
                        played += 1
                        game_over = True
                else:
                    print(f'Tällä kentällä ei ole vastustajaa. {story.x_emoji} Siirry seuraavalle kentälle. {story.next_emoji}')
                    yritykset += 1
                    co2_consumed += 200
                    fields = fields_in_range(current_field, all_fields, player_range)
                    print(f'Voit lentää näin monelle jalkapallokentälle: {len(fields) - len(visited_fields)} {story.takeoff_airplane_emoji}. Värjätyille kentille et voi lentää!')
                    print(f'Jalkapallokentät {story.stadium_emoji}:')
                    for field in fields:
                        if field['ident'] in visited_fields:
                            f_distance = calculate_distance(current_field, field['ident'])
                            print(
                                f"{Fore.GREEN}ICAO: {field['ident']}, Name: {field['name']}, Distance: {f_distance:.0f}km (Vierailtu!){Fore.RESET}")
                        else:
                            f_distance = calculate_distance(current_field, field['ident'])
                            print(f"ICAO: {field['ident']}, Name: {field['name']}, Distance: {f_distance:.0f}km")

                    while True:
                        try:
                            dest = input('Syötä kohdekentän ICAO: ').upper()
                            if dest in visited_fields:
                                print(Fore.RED + "Olet jo vieraillut tässä kentässä!" + Fore.RESET)
                            elif dest in [field['ident'] for field in fields]:
                                selected_distance = calculate_distance(current_field, dest)
                                update_location(dest, player_range, points, game_id)
                                current_field = dest
                                visited_fields.append(current_field)
                                break  # Poistutaan silmukasta, kun käyttäjän syöte on kelvollinen
                            else:
                                print(f"Virheellinen syöte. {story.x_emoji} Syötä kohdekenttä listalta.")
                        except ValueError:
                            print(f"Virheellinen syöte. {story.x_emoji} Syötä kohdekentän ICAO-koodi.")
        # Jos jää lohkovaiheeseen
        if played >= 3 and lohkopeli_voitot < 2:
            print(f'Valitettavasti et voittanut kahta peliä kolmesta lohkopeliotteluista.'
                  f'Sinun MM-kisa taivel päättyy tähän...')
            game_over = True
        # Jos pelaa kaikki pelit
        if played == 7:
            game_over = True
        # Lohkopelivaiheen kentälle siirtyminen
        if played < 3:
            fields = fields_in_range(current_field, all_fields, player_range)
            print(f'Voit lentää näin monelle jalkapallokentälle: {len(fields) - len(visited_fields)} {story.takeoff_airplane_emoji}. Värjätyille kentille et voi lentää!')
            print(f'Jalkapallokentät {story.stadium_emoji}:')
            for field in fields:
                if field['ident'] in visited_fields:
                    f_distance = calculate_distance(current_field, field['ident'])
                    print(
                        f"{Fore.GREEN}ICAO: {field['ident']}, Name: {field['name']}, Distance: {f_distance:.0f}km (Vierailtu!){Fore.RESET}")
                else:
                    f_distance = calculate_distance(current_field, field['ident'])
                    print(f"ICAO: {field['ident']}, Name: {field['name']}, Distance: {f_distance:.0f}km")

            while True:
                try:
                    dest = input('Syötä kohdekentän ICAO: ').upper()
                    if dest in visited_fields:
                        print(Fore.RED + f"Olet jo vieraillut tässä kentässä! {story.x_emoji}" + Fore.RESET)
                    elif dest in [field['ident'] for field in fields]:
                        selected_distance = calculate_distance(current_field, dest)
                        update_location(dest, player_range, points, game_id)
                        current_field = dest
                        visited_fields.append(current_field)
                        break  # Poistutaan silmukasta, kun käyttäjän syöte on kelvollinen
                    else:
                        print(f"Virheellinen syöte. {story.x_emoji} Syötä kohdekenttä listalta.")
                except ValueError:
                    print(f"Virheellinen syöte. {story.x_emoji} Syötä kohdekentän ICAO-koodi.")
    # Tarkista voittaako kaikki pelit
    if score == 7:
        print(Fore.LIGHTYELLOW_EX + f'Se oli siinä! POIKA TULI KOTIIN!!!{story.trophy}{story.trophy}{story.trophy}' + Fore.RESET)
        print(Fore.LIGHTYELLOW_EX + f'Pelasit turnauksen kunniakkaasti loppuun ja voitit jokaisen ottelun!{story.fanfare_emoji}' + Fore.RESET)
        print(Fore.LIGHTYELLOW_EX + f'SUOMI ON MAAILMANMESTARI!{story.number1_emoji}' + Fore.RESET)
        print(f'Tilastot {story.diagram_emoji}')
        print(f'Ottelut: {story.football_emoji} | Voitot: {story.number1_emoji} | Matkustuskerrat: {story.airplane_emoji} | CO2 päästöt: {story.co2_emoji}')
        print('-' * 30)
        print(f'{played:<11} | {score:<10} | {yritykset:<19} | {co2_consumed:<8}')
        print(f'Loistava suoritus {story.smiley_emoji}')
    else:
        print(f'Taistelit hienosti, mutta et valitettavasti voittanut jokaista peliä.{story.sad_emoji}')
        print(f'Tilastot {story.diagram_emoji}')
        print(f'Ottelut: {story.football_emoji} | Voitot: {story.number1_emoji} | Matkustuskerrat: {story.airplane_emoji} | CO2 päästöt: {story.co2_emoji}')
        print('-' * 30)
        print(f'{played:<11} | {score:<10} | {yritykset:<19} | {co2_consumed:<8}')
        print(f'Parempaa menestystä seuraavalle kerralle!')


if __name__ == "__main__":
    main()
