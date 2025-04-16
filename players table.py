import sqlite3
from NBA import get_more_players



def create_database_table():
    conn = sqlite3.connect('nba_data.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY,
        firstname TEXT,
        lastname TEXT,
        height REAL,
        weight REAL,
        points INTEGER,
        minutes TEXT
    )
    ''')

    conn.commit()
    conn.close()





def insert_player_data(players_data):
    conn = sqlite3.connect('nba_data.db')
    cursor = conn.cursor()

    for player in players_data:
        cursor.execute('''
            INSERT OR IGNORE INTO players (
                id, firstname, lastname, height, weight, points, minutes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            player["id"],
            player["firstname"],
            player["lastname"],
            player["height"],
            player["weight"],
            player["points"],
            player["minutes"],
        ))


    conn.commit()
    conn.close()


    
def fetch_and_prepare_player_data():
    players_response = get_more_players()
    players_list = players_response.get("response", [])

    players_data = []

    for stat in players_list:
        player = stat.get("player")
        if not player:
            continue

        points = stat.get("points")
        points_value = int(points) if points is not None else 0


        player_data = {
            "id": player.get("id"),
            "firstname": player.get("firstname"),
            "lastname": player.get("lastname"),
            "height": float(player["height"]["meters"]) if player.get("height") and player["height"].get("meters") else None,
            "weight": float(player["weight"]["kilograms"]) if player.get("weight") and player["weight"].get("kilograms") else None,
            "points": points_value,
            "minutes": stat.get("min")
            
        }

        players_data.append(player_data)

    return players_data


def get_existing_player_count():
    conn = sqlite3.connect('nba_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM players')
    count = cursor.fetchone()[0]

    conn.close()
    return count

def check_schema():
    conn = sqlite3.connect('nba_data.db')
    cursor = conn.cursor()
    
    #players table 
    cursor.execute("PRAGMA table_info(players);")
    columns = cursor.fetchall()

    for column in columns:
        print(column)





def main():
    create_database_table()

    existing_count = get_existing_player_count()
    print(f"Current players in database: {existing_count}")

    players_data = fetch_and_prepare_player_data()
    print(f"Number of new players fetched: {len(players_data)}")

    insert_player_data(players_data)
    check_schema()
    
    
main()

# def create_database_table():
#     conn = sqlite3.connect('nba_data.db')
#     cursor = conn.cursor()

#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS players (
#         id INTEGER PRIMARY KEY,
#         firstname TEXT,
#         lastname TEXT,
#         height REAL,
#         weight REAL,
#         position TEXT,
#         minutes TEXT
#     )
#     ''')

#     conn.commit()
#     conn.close()


# def insert_player_data(players_data):
#     conn = sqlite3.connect('nba_data.db')
#     cursor = conn.cursor()

#     for player in players_data:
#         cursor.execute('''
#             INSERT OR IGNORE INTO players (
#                 id, firstname, lastname, height, weight, position, minutes
#             )
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#         ''', (
#             player["id"],
#             player["firstname"],
#             player["lastname"],
#             player["height"],
#             player["weight"],
#             player["position"],
#             player["minutes"]
#         ))

#     conn.commit()
#     conn.close()


# def fetch_and_prepare_player_data():
#     players_response = get_more_players()
#     players_list = players_response.get("response", [])

#     players_data = []

#     for stat in players_list:
#         player = stat.get("player")
#         if not player:
#             continue

#         player_data = {
#             "id": player.get("id"),
#             "firstname": player.get("firstname"),
#             "lastname": player.get("lastname"),
#             "height": float(player["height"]["meters"]) if player.get("height") and player["height"].get("meters") else None,
#             "weight": float(player["weight"]["kilograms"]) if player.get("weight") and player["weight"].get("kilograms") else None,
#             "position": stat.get("pos"),
#             "minutes": stat.get("min")
#         }

#         players_data.append(player_data)

#     return players_data


# def get_existing_player_count():
#     conn = sqlite3.connect('nba_data.db')
#     cursor = conn.cursor()

#     cursor.execute('SELECT COUNT(*) FROM players')
#     count = cursor.fetchone()[0]

#     conn.close()
#     return count


# def check_schema():
#     conn = sqlite3.connect('nba_data.db')
#     cursor = conn.cursor()

#     cursor.execute("PRAGMA table_info(players);")
#     columns = cursor.fetchall()

#     for column in columns:
#         print(column)

#     conn.close()


# def main():
#     create_database_table()

#     existing_count = get_existing_player_count()
#     print(f"Current players in database: {existing_count}")

#     players_data = fetch_and_prepare_player_data()
#     print(f"Number of new players fetched: {len(players_data)}")

#     insert_player_data(players_data)
#     check_schema()


# if __name__ == "__main__":
#     main()
    
    