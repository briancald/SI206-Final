import unittest
import sqlite3
import json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def setup_database(name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + name)
    cur = conn.cursor()
    return cur, conn

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












def main():
    pass

if __name__ == "__main__":
    main()