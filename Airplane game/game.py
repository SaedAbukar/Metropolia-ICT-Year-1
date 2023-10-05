# Start of the game. Welcome the player

import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='kalifornian_goldrush',
    user='root',
    password='12345678',
    autocommit=True
)

# Functions
def get_airports():
    sql = """
SELECT ident, NAME, latitude_deg, longitude_deg
FROM airport
WHERE ident IN('KJFK', 'KPIT', 'KCMH', 'KCVG', 'KMEM', 'KMCI', 'KTUL', 'KDEN', 'LHS', 'KONT', 'KLAX') 
ORDER BY longitude_deg DESC
;"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

# get all python questions
def get_python_questions():
    sql = "SELECT * FROM python_questions;"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


# get all gold_questions
def get_gold_questions():
    sql = "SELECT * FROM gold_questions;"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

# create new python game
def create_python_game(start_money, p_lives, cur_airport, p_name, p_range, r_answers, w_answers, attempts, a_ports):
    sql = """
INSERT INTO game (money, lives, location, screen_name, player_range, right_answers, wrong_answers, attempts)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (start_money, p_lives, cur_airport, p_name, p_range, r_answers, w_answers, attempts))
    g_id = cursor.lastrowid
    # add python questions
    python_questions = get_python_questions()
    py_questions_list = []
    for python_question in python_questions:
        for i in range(0, python_question['id'], 1):
            py_questions_list.append(python_question['id'])


    python_q_ports = a_ports.copy()
    for i, python_question_id in enumerate(py_questions_list):
        sql = """
INSERT INTO ports (game, airport, question, answer, wrong_answer, wrong_answer2, wrong_answer3)
VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (g_id, python_q_ports[i]['ident'], python_question_id, python_question_id,
                             python_question_id, python_question_id, python_question_id))

    return g_id


# game starts
airports = get_airports()
# print(get_python_questions())
create_python_game(100, 3, 'KJFK', 'Lebron James', 350, 0, 0, 0, airports)









# Explain the rules of the game

# First airport. First three questions

# Second airport based on the answers

# if 3/3 move max distance.
# if 2/3 move max distance times 2/3.
# if 1/3 move max distance times 1/3.
# if 0/3 use money, or health to try again.
