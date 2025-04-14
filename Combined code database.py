import sqlite3


def create_database_table():
    conn = sqlite3.connect('nba_data.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE players (
        id INTEGER PRIMARY KEY,
        firstname TEXT,
        lastname TEXT,
        team TEXT,
        pos TEXT,
        height INTEGER,
        weight INTEGER,
        min INTEGER,
        points INTEGER,
        assists INTEGER
    )
    ''')

    conn.commit()
    conn.close()


def insert_player_data(players_data):
    conn = sqlite3.connect('nba_data.db')
    cursor = conn.cursor()

    for i in players_data:
        cursor.execute('''
            INSERT OR IGNORE INTO players (
                id, firstname, lastname, team, pos, height, weight, min, points, assists
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            players_data[i]["id"],
            players_data[i]["firstname"],
            players_data[i]["lastname"],
            players_data[i]["team"],
            players_data[i]["pos"],
            players_data[i]["height"],
            players_data[i]["weight"],
            players_data[i]["min"],
            players_data[i]["points"],
            players_data[i]["assists"]
        ))

    conn.commit()
    conn.close()


def fetch_player_stats():
    conn = sqlite3.connect('nba_data.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT 
        p.firstname, p.lastname, p.height, p.weight, p.team, p.pos, p.min, p.assists
    FROM players p
    ''')

    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.close()


def check_schema():
    conn = sqlite3.connect('nba_data.db')
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(players);")
    columns = cursor.fetchall()

    print("Table schema:")
    for column in columns:
        print(column)

    conn.close()


def main():
    players_data = {}
    for i in range(1, 101):
        players_data[i] = {
            "id": i,
            "firstname": f"Player{i}",
            "lastname": f"Lastname{i}",
            "team": f"Team{i % 10}",
            "pos": ["PG", "SG", "SF", "PF", "C"][i % 5],
            "height": 180 + (i % 20),
            "weight": 75 + (i % 25),
            "min": 20 + (i % 10),
            "points": 10 + (i % 15),
            "assists": i % 10
        }

    print(f"Number of players fetched: {len(players_data)}")

    create_database_table()
    insert_player_data(players_data)
    check_schema()
    fetch_player_stats()


main()