import sqlite3
from NBA import get_more_players




def create_database_table():
    conn = sqlite3.connect('combined_data.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS player (
        id INTEGER PRIMARY KEY,
        firstname TEXT,
        lastname TEXT,
        position TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER,
        points INTEGER,
        minutes TEXT,
        FOREIGN KEY (player_id) REFERENCES player (id)
    )
    ''')

    conn.commit()
    conn.close()





def insert_player_data(players_data):


    conn = sqlite3.connect('combined_data.db')
    cursor = conn.cursor()


    # for player in players_data:
    for i in range(len(players_data)):
        if i > 24:
            break
            
        # Insert player info
        player = players_data[i]
        cursor.execute('''
            INSERT OR IGNORE INTO player (
                id, firstname, lastname, position
            ) VALUES (?, ?, ?, ?)
        ''', (
            player["id"],
            player["firstname"],
            player["lastname"],
            player["position"]
        ))

        # Insert score info
        cursor.execute('''
            INSERT OR IGNORE INTO scores (
                player_id, points, minutes
            ) VALUES (?, ?, ?)
        ''', (
            player["id"],
            player["points"],
            player["minutes"]
        ))
        
    
        if cursor.rowcount >= 24: 
            break
        conn.commit()
        #conn.close()



def fetch_and_prepare_player_data():
    players_response = get_more_players(api = False)
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
            "position": player.get("pos") if player.get("pos") is not None else None,
            "points": points_value,
            "minutes": stat.get("min")
        }

        players_data.append(player_data)

    return players_data

    


def get_existing_player_count():
    conn = sqlite3.connect('combined_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM player')
    count = cursor.fetchone()[0]

    #conn.close()
    return count

def check_schema():
    conn = sqlite3.connect('combined_data.db')
    cursor = conn.cursor()

    print("\nPlayers Table Schema:")
    cursor.execute("PRAGMA table_info(player);")
    for column in cursor.fetchall():
        print(column)

    print("\nScores Table Schema:")
    cursor.execute("PRAGMA table_info(scores);")
    for column in cursor.fetchall():
        print(column)

    #conn.close()



def main():
    create_database_table()

    existing_count = get_existing_player_count()
    print(f"Current players in database: {existing_count}")

    players_data = fetch_and_prepare_player_data()
    print(f"Number of new players fetched: {len(players_data)}")

    insert_player_data(players_data)
    check_schema()


main()