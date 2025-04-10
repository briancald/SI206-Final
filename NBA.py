import requests
import unittest




def get_api_key(filename):
    with open(filename, 'r') as file:
        api_data = file.read().strip() 
        return api_data 
    get_api_key(api_data)




def get_teams():
    url = "https://api-nba-v1.p.rapidapi.com/teams"

    querystring = {"id":"1"}

    headers = {
        "x-rapidapi-key": "71f6ebba9amsh87b761e3e6eddd5p1ac7eajsnec34507127ea",
        "x-rapidapi-host": "api-nba-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    teams_data = response.json()
    print("bbb", response.json())
    get_teams(teams_data)





def get_players():
    url = "https://api-nba-v1.p.rapidapi.com/players"

    querystring = {"team":"1","season":"2021"}

    headers = {
        "x-rapidapi-key": "71f6ebba9amsh87b761e3e6eddd5p1ac7eajsnec34507127ea",
        "x-rapidapi-host": "api-nba-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    players_data = response.json()

    get_players(players_data)



def get_statistics():
    url = "https://api-nba-v1.p.rapidapi.com/players/statistics"

    querystring = {"game":"8133"}

    headers = {
        "x-rapidapi-key": "71f6ebba9amsh87b761e3e6eddd5p1ac7eajsnec34507127ea",
        "x-rapidapi-host": "api-nba-v1.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    #print("ddd", response.json())
    statistics_data = response.json()
    get_statistics(statistics_data)
