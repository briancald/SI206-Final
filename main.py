import setup
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
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo
conn = sqlite3.connect("combined_data.db")
cur = conn.cursor()

def calcute_nutrition(position, height, weight, minutes, points):
    try:
        feet, inches = map(int, height.split('-'))
        total_inches = feet * 12 + inches
        cm = round(total_inches * 2.54, 1)
        height = cm
    except:
        height = height
    try:
        kg = round(int(weight) * 0.453592, 1)
        weight = kg
    except:
        weight = weight
    # Calculate the nutrition needs based on player stats
    baseCals = 10 *weight + 6.25 *height
    if position == "C":
        baseCals += 500
    elif position == "SF" or "PF":
        baseCals += 300
    elif position == "FG" or "PG":
        baseCals += 100
    if height > 180:
        baseCals += 200
    if minutes > 30:
        baseCals += 300
    if points > 20:
        baseCals += 400
    if points > 30:
        baseCals += 500
    
    # Calculate the macronutrient breakdown
    baseFat = (0.25 * baseCals) / 9
    baseProtein = weight * 1.6
    baseCarbs = (0.55 * baseCals) / 4
    baseFiber = baseCals * 0.014
    baseSugar = baseCals * 0.025
    baseSodium = baseCals * 1.15

    return {
        "calories": baseCals,
        "fat_total_g": baseFat,
        "protein_g": baseProtein,
        "carbohydrates_total_g": baseCarbs,
        "fiber_g": baseFiber,
        "sugar_g": baseSugar,
        "sodium_mg": baseSodium,
    }

def create_nutrition_plan(info):
    # Create a nutrition plan based on the calculated needs
    query = """SELECT meals.name, meals.meal_id, nutrition.calories, nutrition.protein_g, 
               nutrition.fat_total_g, nutrition.carbohydrates_total_g, nutrition.fiber_g, 
               nutrition.sugar_g, nutrition.sodium_mg FROM meals JOIN nutrition ON meals.meal_id = nutrition.meal_id
               WHERE nutrition.calories >= 100"""
    df = pd.read_sql_query(query, conn)
    # Filter out meals with less than 100 calories
    #Weight the meals based on their nutritional value
    df['score'] = (
        0.5 * df['protein_g'] +
        0.3 * df['carbohydrates_total_g'] +
        0.2 * df['fat_total_g']
    )
    df = df.sort_values(by='score', ascending=False)

    weekly_plan = []

    for day in range(7):
        selected_meals = []
        running_totals = {key: 0 for key in info.keys()}
        used_meals = set()
        # Shuffle the meals for each day
        df_day = df.sample(frac=1, random_state=day)
        # Select meals for the day
        for _, meal in df_day.iterrows():
            # Check if the meal has already been used
            if meal['meal_id'] in used_meals:
                continue
            temp_totals = running_totals.copy()
            # Add the meal's nutrition to the running totals
            for key in info:
                if key in meal:
                    temp_totals[key] += meal.get(key, 0)
            # Check if the total calories are within the limit
            if temp_totals['calories'] <= info['calories'] + 100:
                running_totals = temp_totals
                selected_meals.append(meal)
                used_meals.add(meal['meal_id'])
            # Check if the running totals meet the nutritional needs
            if (all(running_totals[k] >= info[k] * 0.88 for k in info) and len(selected_meals) >= 5):
                break
        # If the nutritional needs are not met, add more meals
        if not all(running_totals[k] >= info[k] * 0.9 for k in info):
            for _, meal in df_day.iterrows():
                if meal['meal_id'] in used_meals:
                    continue

                temp_totals = running_totals.copy()
                for key in info:
                    if key in meal:
                        temp_totals[key] += meal.get(key, 0)

                if temp_totals['calories'] <= info['calories'] + 100:
                    running_totals = temp_totals
                    selected_meals.append(meal)
                    used_meals.add(meal['meal_id'])

                if all(running_totals[k] >= info[k] * 0.9 for k in info):
                    break
        
        day_plan_df = pd.DataFrame(selected_meals)
        # Calculate the total calories and macronutrients for the day
        day_plan_df["day"] = f"Day {day+1}"
        weekly_plan.append(day_plan_df)
        # Print the meal plan for the day
    full_plan_df = pd.concat(weekly_plan, ignore_index=True)
    file = open("meal_plan_summary.txt", "w")
    for day in range(1, 8):
        file.write(f"\n Meal Plan for Day {day}:\n")
        day_meals = full_plan_df[full_plan_df["day"] == f"Day {day}"]
        for i, row in day_meals.iterrows():
            file.write(f"  {row['name']} | {int(row['calories'])} kcal | "
                  f"{row['protein_g']}g protein, {row['fat_total_g']}g fat, "
                  f"{row['carbohydrates_total_g']}g carbs\n")

        total_cals = day_meals['calories'].sum()
        file.write(f"  Total Calories: {int(total_cals)} kcal\n")
    return full_plan_df

def get_player_stats(cur, playerid):
    cur.execute("SELECT firstname,lastname, minutes, points FROM players WHERE id = ?", (playerid,))
    row = cur.fetchone()
    if not row:
        raise ValueError("Player not found.")
    return {
        "firstname": row[0],
        "lastname": row[1],
        "minutes": row[2],
        "points": row[3]
    }

def plots(meal_plan, nutrition_needs, player_info,id):
    # Create plots for the meal plan
    meal_plan = meal_plan.reset_index(drop=True)
    meal_plan['day'] = meal_plan['day'].astype(str)
    summary = meal_plan.groupby('day')[['calories', 'fat_total_g', 'protein_g', 'carbohydrates_total_g',
                                        'fiber_g', 'sugar_g', 'sodium_mg']].sum()
    # Calories per day
    plt.figure(figsize=(10, 5))
    summary['calories'].plot(kind='bar', title='Calories per Day')
    plt.axhline(y=nutrition_needs['calories'], color='r', linestyle='--', label='Target')
    plt.ylabel('Calories')
    plt.xlabel('Day')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{id}_calories_per_day.png')
    # Macronutrient breakdown
    summary[['protein_g', 'fat_total_g', 'carbohydrates_total_g']].plot(kind='bar', stacked=True, figsize=(10, 6),
                                                                        title='Macronutrient Breakdown')
    plt.ylabel('Grams')
    plt.xlabel('Day')
    plt.tight_layout()
    plt.savefig(f'{id}_macros_breakdown.png')
    # Radar chart for nutrition needs
    labels = ['Fat', 'Protein', 'Carbs', 'Fiber', 'Sugar', 'Sodium']
    actual = [
        summary['fat_total_g'].mean(),
        summary['protein_g'].mean(),
        summary['carbohydrates_total_g'].mean(),
        summary['fiber_g'].mean(),
        summary['sugar_g'].mean(),
        summary['sodium_mg'].mean() / 1000
    ]
    target = [
        nutrition_needs['fat_total_g'],
        nutrition_needs['protein_g'],
        nutrition_needs['carbohydrates_total_g'],
        nutrition_needs['fiber_g'],
        nutrition_needs['sugar_g'],
        nutrition_needs['sodium_mg']/1000
    ]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    actual += actual[:1]
    target += target[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.plot(angles, actual, label='Actual')
    ax.plot(angles, target, label='Target', linestyle='--')
    ax.fill(angles, actual, alpha=0.25)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_title("Average Nutrition vs Target")
    ax.legend()
    plt.savefig(f'{id}_nutrition_radar.png')

def main():
    player_id = input("Enter Player ID: ")
    player_info = get_player_stats(cur,player_id)
    info = players.find_players_by_full_name(player_info['firstname'] + " " + player_info['lastname'])[0]
    info = commonplayerinfo.CommonPlayerInfo(info['id'])
    data = info.get_normalized_dict()
    metricts = data['CommonPlayerInfo'][0]

    height = metricts['HEIGHT']
    weight = metricts['WEIGHT']
    position = metricts['POSITION']
    minutes, seconds = map(int, player_info['minutes'].split(":"))
    needs = calcute_nutrition(position,height,weight
                              ,minutes,int(player_info['points']))
    meal_plan = create_nutrition_plan(needs)
    plots(meal_plan, needs, player_info,player_id)

if __name__ == "__main__":
    main()