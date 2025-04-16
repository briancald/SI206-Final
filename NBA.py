import requests
import json




def get_api_key(filename):
    with open(filename, 'r') as file:
        api_data = file.read().strip() 
        return api_data 
    get_api_key(api_data)




def get_more_players(api=True): 
    if api is False:
        with open("players.json", "r") as json_file:
            players_data = json.load(json_file)
        return players_data

    url = "https://api-nba-v1.p.rapidapi.com/players/statistics"

    querystring = {"team":"1","season":"2020"}

    headers = {
        "x-rapidapi-key": "71f6ebba9amsh87b761e3e6eddd5p1ac7eajsnec34507127ea",
        "x-rapidapi-host": "api-nba-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    more_play = response.json()
    with open("players.json", "w") as json_file:
        json.dump(more_play, json_file, indent=4)  # indent makes it look nice & readable
    return more_play
    


def main():

    
    players_data = get_more_players()
    print("More players:", players_data)

    
    
if __name__ == "__main__":
    main()
