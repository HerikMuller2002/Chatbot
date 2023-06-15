import string
import random

def generate_secret_key(length=32):
    chars = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(random.choice(chars) for _ in range(length))
    return secret_key

#####################################################################
from fuzzywuzzy import fuzz
from nltk.tokenize import word_tokenize, sent_tokenize
from preprocessing_utils import *

def filter_censure(text):
    with open(r'utils\data\offensive_words.txt','r', encoding='utf-8') as file:
        linhas = file.readlines()
        lines = []
        for linha in linhas:
            linha = preprocess(linha, 'lemma')
            if linha != '' and linha not in lines:
                lines.append(linha)
    text = word_tokenize(text)
    for token in text:
        for word in lines:
            similarity = fuzz.ratio(token, word)
            if similarity >= 80:
                return True
    return False
