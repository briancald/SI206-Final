import requests
import json
# from balldontlie import BalldontlieAPI


def get_api_key(filename):
    with open(filename, 'r') as file:
        api_data = file.read().strip()
        # api_key = api_data.split("=")[1].strip().strip('"') 
        return api_data 


# url = "https://api-nba-v1.p.rapidapi.com/players/statistics"

# querystring = {"game":"8133"}

# headers = {
# 	"x-rapidapi-key": "71f6ebba9amsh87b761e3e6eddd5p1ac7eajsnec34507127ea",
# 	"x-rapidapi-host": "api-nba-v1.p.rapidapi.com"
# }

# response = requests.get(url, headers=headers, params=querystring)
#print(response.text)
def get_season():
    url = "https://api-nba-v1.p.rapidapi.com/seasons"

    headers = {
        "x-rapidapi-key": "71f6ebba9amsh87b761e3e6eddd5p1ac7eajsnec34507127ea",
        "x-rapidapi-host": "api-nba-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    print(response.json())
    #print(f"Status Code: {response.status_code}")


def get_teams():
    url = "https://api-nba-v1.p.rapidapi.com/teams"

    querystring = {"id":"1"}

    headers = {
        "x-rapidapi-key": "71f6ebba9amsh87b761e3e6eddd5p1ac7eajsnec34507127ea",
        "x-rapidapi-host": "api-nba-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())



def get_statistics():
    url = "https://api-nba-v1.p.rapidapi.com/players/statistics"

    querystring = {"game":"8133"}

    headers = {
        "x-rapidapi-key": "71f6ebba9amsh87b761e3e6eddd5p1ac7eajsnec34507127ea",
        "x-rapidapi-host": "api-nba-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    print(response.json())