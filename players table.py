import sqlite3
from NBA import get_players 




def create_database_table():
    conn = sqlite3.connect('nba_data.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY,
        firstname TEXT,
        lastname TEXT,
        height INTEGER,
        weight INTEGER
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
                id, firstname, lastname, height, weight
            )
            VALUES (?, ?, ?, ?, ?)
        ''', (
            players_data[i]["id"],
            players_data[i]["firstname"],
            players_data[i]["lastname"],
            players_data[i]["height"],
            players_data[i]["weight"]
        ))

    conn.commit()
    conn.close()


    
def fetch_and_prepare_player_data():
    players_response = get_players()
    players_list = players_response.get("response", [])

    players_data = {}
    
    for i, player in enumerate(players_list, start=1):  
        if i > 25:
            break

        player_id = player.get("id")
        if not player_id:
            continue

        players_data[i] = {
            "id": player_id,
            "firstname": player.get("firstname"),
            "lastname": player.get("lastname"),
            "height": float(player["height"]["meters"]) if player.get("height") and player["height"].get("meters") else None,
            "weight": float(player["weight"]["kilograms"]) if player.get("weight") and player["weight"].get("kilograms") else None
        }


    return players_data



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

    players_data = fetch_and_prepare_player_data()
    print(f"Number of players fetched: {len(players_data)}")

    insert_player_data(players_data)
    check_schema()
    
main()