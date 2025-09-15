import unittest
import sqlite3
import json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import time


def setup_database(name):
    # Create a SQLite database and tables for meals and nutrition
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + name)
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS meals (
        meal_id INTEGER PRIMARY KEY,
        name TEXT)''')  
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS nutrition (
        meal_id INTEGER PRIMARY KEY,
        calories REAL,
        fat_total_g REAL,
        protein_g REAL,
        sodium_mg REAL,
        carbohydrates_total_g REAL,
        fiber_g REAL,
        sugar_g REAL,
        FOREIGN KEY (meal_id) REFERENCES meals(meal_id))''')
    
    return cur, conn

def insert_meals(cur, meals):
    # Insert meal data into the meals table
    inserted = 0
    for meal in meals:
        meal_id = meal['idMeal']
        name = meal['strMeal']
        cur.execute('''
            INSERT OR IGNORE INTO meals (meal_id, name)
            VALUES (?, ?)''', (meal_id, name))
        if cur.rowcount > 0:
            inserted += 1
        if inserted >= 25:
            break

    

def get_nutrition(cur):
    # Fetch nutrition data from the FatSecret API
    # Get the access token
    url = "https://oauth.fatsecret.com/connect/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "scope": "basic",
        "client_id": "85df078139c8426abd393debc1a169e6",
        "client_secret": "a27055452cdd45259b78e0d82e3f7581"
    }
    response = requests.post(url, headers=headers, data=data)
    token = response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    search_url = f"https://platform.fatsecret.com/rest/foods/search/"
    # Get the meal names from the database
    cur.execute('SELECT meal_id, name FROM meals')
    meals = cur.fetchall()
    count = 0
    out = []
    # Loop through the meals and fetch nutrition data
    for meal_id, name in meals:
        if count == 25:
            break
        params = {
        "method": "foods.search",
        "search_expression": name,
        "format": "json",
        "max_results": 1,
        }
        response = response = requests.get(search_url, headers=headers, params=params)
        if response.status_code == requests.codes.ok:
            data = json.loads(response.text)
            if data:
                # Check if the response contains food data
                if 'foods' in data and 'food' in data['foods']:
                    foodid = data['foods']['food']['food_id']
                else:
                    continue
                nutrition_url = f"https://platform.fatsecret.com/rest/food/v4"
                params = {
                    "method": "food.get",
                    "food_id": foodid,
                    "format": "json",
                }
                response = requests.get(nutrition_url, headers=headers, params=params)
                if response.status_code == requests.codes.ok:   
                    datNutrition = json.loads(response.text)
                    if datNutrition.get('food') is None:
                        continue
                    try:
                        # Extract the nutrition information
                        nutrition = datNutrition['food']['servings']['serving'][0]
                    
                        out.append({
                            'meal_id': meal_id,
                            'name': name,
                            'calories': nutrition['calories'],
                            'fat_total_g': nutrition['fat'],
                            'protein_g': nutrition['protein'],
                            'carbohydrates_total_g': nutrition['carbohydrate'],
                            'sodium_mg': nutrition['sodium'],
                            'fiber_g': nutrition['fiber'],
                            'sugar_g': nutrition['sugar'],
                        })
                        count += 1
                    except (KeyError, IndexError, TypeError):
                        continue
        
        time.sleep(1)

    # Save the nutrition data to a JSON file
    with open("nutrition.json", 'w') as f:
        json.dump(out, f, indent=2)

def insert_nutrition(cur, conn, nutrition):
    inserted = 0
    # Insert nutrition data into the nutrition table
    for item in nutrition:
        cur.execute('''
            INSERT OR IGNORE INTO nutrition
            (meal_id, calories, fat_total_g, protein_g, carbohydrates_total_g, sodium_mg, fiber_g, sugar_g)
            VALUES (?, ?, ?, ?, ?, ?, ?,?) ''', (
            item.get('meal_id'),
            item.get('calories'),
            item.get('fat_total_g'),
            item.get('protein_g'),
            item.get('carbohydrates_total_g'),
            item.get('sodium_mg'),
            item.get('fiber_g'),
            item.get('sugar_g'),
        ))
        if cur.rowcount > 0:
            inserted += 1
        if inserted >= 25:
            break


    conn.commit()


def get_meal_key(file):
    with open(file,'r') as f:
        return f.read().strip()

def get_data(file):
    try:
        with open(file, 'r') as f:
            data = json.load(f)
        return data
    except (FileNotFoundError, json.JSONDecodeError, IOError):
        return {}
    
def save_data(dict, file):
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(dict, f, indent=4)

def store_meal_data_json():
    # Fetch meal data from the MealDB API and save it to a JSON file
    allmeals = []
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    
    for letter in alphabet:
        # Fetch meals starting with the current letter
        # Add a delay to avoid hitting the API too quickly
        time.sleep(1)
        url = f'https://www.themealdb.com/api/json/v1/1/search.php?f={letter}'
        response = requests.get(url)
        data = response.json()
        if data.get('meals'):
            allmeals.extend(data['meals'])
    save_data(allmeals, "meals.json")

def main():
    cur, conn = setup_database('combined_data.db')
    insert_meals(cur, get_data('meals.json'))
    insert_nutrition(cur, conn, get_data('nutrition.json'))
  

if __name__ == "__main__":
    main()
