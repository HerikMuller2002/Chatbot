import sys
import os
current_dir = os.getcwd()
while "Chatbot" not in os.listdir(current_dir):
    current_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)

#####################################################################
import string
import random

def generate_secret_key(length=32):
    chars = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(random.choice(chars) for _ in range(length))
    return secret_key

#####################################################################
from fuzzywuzzy import fuzz
from nltk.tokenize import word_tokenize, sent_tokenize

#####################################################################
import json
import random
from itertools import product

def get_response(context):
    with open(r"src\database\responses\responses.json","r", encoding="utf8") as f:
        data = json.load(f)
    return random.choice(data[context])

#####################################################################
import pandas as pd
def get_solution(problem, equipament):
    df = pd.read_excel(r'..\..\teste.xlsx')
    for valor1, valor2 in product(problem, equipament):
        if any((df['coluna1'] == valor1) & (df['coluna2'] == valor2)):
            prob = valor1
            equip = valor2
    df_equipament = df.loc(df['equipament']== equip)
    df_problem = df_equipament.loc(df['problem']== prob)
    a = df_problem['cause'].to_list()
    b = df_problem['action'].to_list()

    print(a)
    print()
    print(b)

