import requests
# from balldontlie import BalldontlieAPI



def get_api_key(filename):
    with open(filename, 'r') as file:
        print(file)
        api_data = file.read().strip()
        # api_key = api_data.split("=")[1].strip().strip('"') 
        print(api_data)
        return api_data 
    


# def get_teams():
#     url = "https://api.balldontlie.io/v1/teams"
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         teams = response.json()["data"]
#         for team in teams:
#             print(f"ID: {team['id']}, Team: {team['full_name']}")
#     else:
#         print(f"Error: {response.status_code}")

# # Call the function
# get_teams()

# def get_players(player_id=None):
#     url = "https://api.balldontlie.io/v1/players"
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         players = response.json()["data"]
#         for player in players:
#             print(f"ID: {player['id']}, Player: {player['first_name']} {player['last_name']}")
#     else:
#         print(f"Error: {response.status_code}")

