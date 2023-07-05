import sys
import os
current_dir = os.getcwd()
while "Chatbot" not in os.listdir(current_dir):
    current_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)

from Chatbot.src.utils.preprocessing_utils import *
import json
import string
import random
import requests
import pandas as pd

#####################################################################
def log(session_id, data):
    log_folder = "data/logs"
    log_file = f"chatbot_{session_id}.json"
    log_path = os.path.join(log_folder, log_file)
    if os.path.exists(log_path):
        with open(log_path, 'r+', encoding='utf-8') as f:
            log_ = json.load(f)
            log_.append(data)
            f.seek(0)
            json.dump(log_, f, indent=4)
    else:
        with open(log_path, 'w+', encoding='utf-8') as f:
            log_ = [data]
            json.dump(log_, f, indent=4)


def clear_log(session_id):
    file_path = f"data/logs/chatbot_{session_id}.json"
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass


def get_log(session_id, key):
    file_path = f"data/logs/chatbot_{session_id}.json"
    with open(file_path, 'r', encoding="utf-8") as f:
        log_list = json.load(f)
    try:
        if log_list:
            last_log = log_list[-1]
            value = last_log[key]
            return value
        else:
            raise
    except:
        print("deu erro aqui")
        return None

#####################################################################
def generate_secret_key(length=32):
    chars = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(random.choice(chars) for _ in range(length))
    return secret_key

#####################################################################

def search_wikipedia(query):
    url = "https://pt.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "exintro": "",
        "explaintext": "",
        "titles": query
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        page_id = list(data["query"]["pages"].keys())[0]
        page_data = data["query"]["pages"][page_id]
        if "extract" in page_data:
            summary = page_data["extract"]
            return summary
        else:
            raise
    except:
            return "Not found"

#####################################################################

def get_response(context):
    with open(r"src\database\responses\responses.json","r", encoding="utf8") as f:
        data = json.load(f)
    return random.choice(data[context])

def prepared_text(text, word, place_holder):
    if place_holder in text:
        text = text.replace(place_holder, word)
    return text

def get_cause_solution(target_column, equipment, issue):
    equipment = remove_punct(remove_accent(equipment)).lower().strip()
    issue = remove_punct(remove_accent(issue)).lower().strip()

    df = pd.read_excel(r'src\database\troubleshooting_equipament.xlsx')
    df = df.applymap(lambda x: str(x).lower())
    df = df.applymap(lambda x: remove_accent(x))
    if target_column != "action":
        df = df.applymap(lambda x: remove_punct(x))
    filtered_df = df[(df['equipament'] == equipment)]
    filtered_df2 = filtered_df[(filtered_df['problem'] == issue)]
    values = [corrector(i) for i in filtered_df2[target_column].tolist()]

    if target_column == "action":
        for i in range(len(values)):
            values[i] = prepared_text(values[i], ';', '.')
            values[i] = values[i].split(';')
    return values

def get_resolutions(causes, solutions):
    template = get_response('RESOLUTION_CAUSES')
    resolutions = []
    num = 0
    for cause, solution in zip(causes, solutions):
        num += 1 
        resolution = template.replace("$cause", f"{num}. {cause}")
        resolution_options = []
        for i in solution:
            resolution_options.append(f"- {i}")
        resolutions.append(resolution + '¬'.join(resolution_options))
    return resolutions

#####################################################################

# import mysql.connector

# def buscar_id(valor, tabela):
#     # Configuração da conexão com o banco de dados
#     cnx = mysql.connector.connect(
#         host='localhost',  # Endereço do servidor MySQL
#         user='seu_usuario',  # Usuário do banco de dados
#         password='sua_senha',  # Senha do banco de dados
#         database='nome_do_banco'  # Nome do banco de dados
#     )

#     # Criação do cursor para executar consultas SQL
#     cursor = cnx.cursor()

#     # Consulta SQL para buscar o ID do valor na tabela especificada
#     query = f"SELECT id FROM {} WHERE valor = %s"
#     params = (valor,)

#     # Execução da consulta SQL
#     cursor.execute(query, params)

#     # Obtenção do resultado da consulta
#     resultado = cursor.fetchone()

#     # Fechamento do cursor e da conexão com o banco de dados
#     cursor.close()
#     cnx.close()

#     if resultado:
#         return resultado[0]  # Retorna o ID encontrado
#     else:
#         return None  # Retorna None se o valor não foi encontrado

#####################################################################

import difflib
import unicodedata

def remover_acentos(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

def similarity(termo, lista):
    similaridade_maxima = 0
    
    for palavra in lista:
        similaridade = difflib.SequenceMatcher(None, termo, palavra).ratio()
        similaridade_maxima = max(similaridade, similaridade_maxima)
        
    return similaridade_maxima

def verifiy_similarity(termo):
    termo = termo.lower().strip()
    termo = remover_acentos(termo)
    
    lista_positivo = ['sim', 'claro', 'com certeza', 'exatamente', 'sem duvida', 'obviamente', 'certamente', 'e isso mesmo', 'confirmo', 'afirmativo', 'positivo', 'sem sombra de duvidas', 'concordo', 'conforme', 'confirmado', 'absolutamente', 'efetivamente', 'indubitavelmente', 'assim e', 'sem falta']
    lista_negativo = ['nao', 'nunca', 'jamais', 'de jeito nenhum', 'negativo', 'nao concordo', 'nao confirmo', 'errado', 'incorreto', 'falso', 'de forma alguma', 'absolutamente nao', 'nada disso']
    
    similaridade_positivo = similarity(termo, lista_positivo)
    similaridade_negativo = similarity(termo, lista_negativo)
    
    if similaridade_positivo > 0.9 and similaridade_negativo <= 0.9:
        return True
    elif similaridade_positivo <= 0.9 and similaridade_negativo > 0.9:
        return False
    elif similaridade_positivo > 0.9 and similaridade_negativo > 0.9:
        return None
    else:
        return None
