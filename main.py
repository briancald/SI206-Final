import unittest
import sqlite3
import json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json

def setup_database(name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + name)
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS meals (
        meal_id INTEGER PRIMARY KEY,
        name TEXT,
        category TEXT,
        area TEXT,
        instructions TEXT,
        thumbnail TEXT)''')
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        meal_id INTEGER,
        ingredient TEXT,
        measure TEXT,
        FOREIGN KEY (meal_id) REFERENCES meals(meal_id))''')
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS nutrition (
        meal_id INTEGER PRIMARY KEY,
        calories REAL,
        serving_size_g REAL,
        fat_total_g REAL,
        fat_saturated_g REAL,
        protein_g REAL,
        sodium_mg REAL,
        potassium_mg REAL,
        cholesterol_mg REAL,
        carbohydrates_total_g REAL,
        fiber_g REAL,
        sugar_g REAL,
        FOREIGN KEY (meal_id) REFERENCES meals(meal_id))''')
    
    
    return cur, conn

def insert_meals(cur, meals):
    get_data('meals.json')
    with open('meals.json', 'r') as f:
        meals = json.load(f)
    for meal in meals:
        meal_id = meal['idMeal']
        name = meal['strMeal']
        category = meal['strCategory']
        area = meal['strArea']
        instructions = meal['strInstructions']
        thumbnail = meal['strMealThumb']
        cur.execute('''
            INSERT OR IGNORE INTO meals (meal_id, name, category, area, instructions, thumbnail)
            VALUES (?, ?, ?, ?, ?, ?)''', (meal_id, name, category, area, instructions, thumbnail))
    for i in range(1, 21):
        ingredient = meal.get(f'strIngredient{i}')
        measure = meal.get(f'strMeasure{i}')
        if ingredient and ingredient.strip():
            cur.execute('''
                INSERT INTO ingredients (meal_id, ingredient, measure)
                VALUES (?, ?, ?)''', (meal_id, ingredient.strip(), measure.strip() if measure else ''))

def insert_nutrition(cur):
    apiKey = get_meal_key('nutritionAPIKey.txt')
    url = 'https://api.api-ninjas.com/v1/nutrition'
    headers = {'X-Api-Key': apiKey}






def get_meal_key(file):
    with open(file,'r') as f:
        return file.read().strip()

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
    allmeals = []
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    
    for letter in alphabet:
        url = f'https://www.themealdb.com/api/json/v1/1/search.php?f={letter}'
        response = requests.get(url)
        data = response.json()
        if data.get('meals'):
            allmeals.extend(data['meals'])
    save_data(allmeals, "meals.json")








def main():
    pass

if __name__ == "__main__":
    main()