import sqlite3


def create_database_table():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('nba_data.db')
    cursor = conn.cursor()
    
    
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
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

def insert_player_data(players_data):
    conn = sqlite3.connect('nba_data.db')
    cursor = conn.cursor()

    # Generate 100 rows of sample data
        # Generate 100 rows of sample data matching the table columns
    # players_data = {
    #     "id": 374,
    #     "firstname": "Dwayne",
    #     "lastname": "Wade",
    #     "team":  "Miami Heat",
    #     "pos" : "SF",
    #     "height" : 193,
    #     "weight" : 104,
    #     "min" : 21,
    #     "points" : 14,
    #     "assists" : 1
    # }
    # Insert 25 rows at a time
    # for i in range(0, len(players_data), 25):
        #batch = players_data[i:i + 25]
    print(players_data)
    i = 1
    while i < len(players_data) - 1:
        print(i)
        cursor.execute('''
            INSERT OR IGNORE INTO players (
                id, firstname, lastname, team, pos, height, weight, min, points, assists
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (players_data[i]["id"],players_data[i]["firstname"], players_data[i]["lastname"], players_data[i]["team"], players_data[i]["pos"], players_data[i]["height"], players_data[i]["weight"], players_data[i]["min"], players_data[i]["points"], players_data[i]["assists"])
        )
        #(players_data[i][1], players_data[i][2], players_data[i][3], players_data[i][4], players_data[i][5], players_data[i][6], players_data[i][7], players_data[i][8], players_data[i][9], players_data[i][10])
        print("test")
        i += 1
    #stored_data = (players_data["id"],players_data["firstname"], players_data["lastname"], players_data["team"], players_data["pos"], players_data["height"], players_data["weight"], players_data["min"], players_data["points"], players_data["assists"])
    conn.commit()
    # Close the connection
    conn.close()

def check_schema():
    conn = sqlite3.connect('nba_data.db')
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA table_info(players);")
    columns = cursor.fetchall()
    
    for column in columns:
        print(column)  # This will print column info
    
    conn.close()

check_schema()

def main():
    
    # players_data = {
    #     "id": 374,
    #     "firstname": "Dwayne",
    #     "lastname": "Wade",
    #     "team":  "Miami Heat",
    #     "pos" : "SF",
    #     "height" : 193,
    #     "weight" : 104,
    #     "min" : 21,
    #     "points" : 14,
    #     "assists" : 1
        
        
    # }
    players_data = {
    # Generate 100 players
    }
    for i in range(1, 101):
        players_data[i] = {
        "id": i,
        "firstname": f"Player{i}",
        "lastname": f"Last{i}",
        "team": f"Team{i % 10}",  #randomize team names 
        "pos": ["PG", "SG", "SF", "PF", "C"][i % 5],  
        "height": 180 + (i % 20),  
        "weight": 75 + (i % 25),  
        "min": 20 + (i % 10),  
        "points": 10 + (i % 15),  
        "assists": i % 10  # Randomize assists between 0 and 9
}
        
    create_database_table()
    insert_player_data(players_data)
    check_schema()
main()
