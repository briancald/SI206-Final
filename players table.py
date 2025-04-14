import sqlite3
from NBA import get_players, get_statistics

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



def fetch_and_prepare_player_data():
    # players_response = get_players()
    # players_list = players_response.get("response", [])

    # players_data = {}

    # for i, player in enumerate(players_list, start=1):
    #     player_id = player.get("id")
    #     if not player_id:
    #         continue

    #     stats_response = get_statistics(player_id)
    #     stats_list = stats_response.get("response", [])

    #     if stats_list:
    #         stats = stats_list[0]  # Use first game's stats
    #         min_played = int(stats.get("min", 0)) if stats.get("min") else 0
    #         points = int(stats.get("points", 0)) if stats.get("points") else 0
    #         assists = int(stats.get("assists", 0)) if stats.get("assists") else 0
    #     else:
    #         min_played = 0
    #         points = 0
    #         assists = 0

    #     players_data[i] = {
    #         "id": player_id,
    #         "firstname": player.get("firstname"),
    #         "lastname": player.get("lastname"),
    #         "team": player["team"]["name"] if player.get("team") else None,
    #         "pos": player.get("pos"),
    #         "height": float(player["height"]["meters"]) if player.get("height") and player["height"].get("meters") else None,
    #         "weight": float(player["weight"]["kilograms"]) if player.get("weight") and player["weight"].get("kilograms") else None,
    #         "min": min_played,
    #         "points": points,
    #         "assists": assists
    #     }
        players_response = get_players()
        players_list = players_response.get("response", [])

        players_data = {}

        for i, player in enumerate(players_list, start=1):
            player_id = player.get("id")
            if not player_id:
                continue

            stats_response = get_statistics(player_id)
            stats_list = stats_response.get("response", [])

            if stats_list:
                stats = stats_list[0]  # Use first game's stats
                
                # Fix for handling 'min' as a time string 'MM:SS'
                min_played_str = stats.get("min", "0:00")
                try:
                    if min_played_str != "0:00":
                        minutes, seconds = min_played_str.split(":")
                        min_played = int(minutes)  # Convert minutes to integer
                    else:
                        min_played = 0  # In case 'min' is '0:00' or missing
                except ValueError:
                    min_played = 0  # Default to 0 if there's an error in parsing
                
                # Convert other stats (points, assists) safely
                points = int(stats.get("points", 0)) if stats.get("points") else 0
                assists = int(stats.get("assists", 0)) if stats.get("assists") else 0
            else:
                min_played = 0
                points = 0
                assists = 0

            players_data[i] = {
                "id": player_id,
                "firstname": player.get("firstname"),
                "lastname": player.get("lastname"),
                "team": player["team"]["name"] if player.get("team") else None,
                "pos": player.get("pos"),
                "height": float(player["height"]["meters"]) if player.get("height") and player["height"].get("meters") else None,
                "weight": float(player["weight"]["kilograms"]) if player.get("weight") and player["weight"].get("kilograms") else None,
                "min": min_played,
                "points": points,
                "assists": assists
            }

        return players_data

        



def check_schema():
    conn = sqlite3.connect('nba_data.db')
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(players);")
    columns = cursor.fetchall()

    print("Table schema:")
    for column in columns:
        print(column)

    conn.close()



# def main():
    # players_data = {}
    # for i in range(1, 101):
    #     players_data[i] = {
    #         "id": i,
    #         "firstname": f"Player{i}",
    #         "lastname": f"Lastname{i}",
    #         "team": f"Team{i % 10}",
    #         "pos": ["PG", "SG", "SF", "PF", "C"][i % 5],
    #         "height": 180 + (i % 20),
    #         "weight": 75 + (i % 25),
    #         "min": 20 + (i % 10),
    #         "points": 10 + (i % 15),
    #         "assists": i % 10
    #     }



    # create_database_table()
    # insert_player_data(players_data)
    # check_schema()
        # create_database_table()

        # players_data = fetch_and_prepare_player_data()
        # print(f"Number of players fetched: {len(players_data)}")

        # insert_player_data(players_data)
        # check_schema()
        
def main():
    create_database_table()

    players_data = fetch_and_prepare_player_data()
    print(f"Number of players fetched: {len(players_data)}")

    insert_player_data(players_data)
    check_schema()

main()