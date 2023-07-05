import re
import pandas as pd
import sys
import os
current_dir = os.getcwd()
while "Chatbot" not in os.listdir(current_dir):
    current_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
from src.utils.preprocessing_utils import *

#####################################################################
from spacy import load, displacy
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.preprocessing import LabelEncoder
import torch

def classifier_intent(text, path_model=r'data\models\model_bert_intent'):
    text = preprocess_text(text, 'lemma')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForSequenceClassification.from_pretrained(path_model)
    label_encoder = LabelEncoder()
    label_encoder.classes_ = torch.load(f'{path_model}\label_encoder_classes.pt')
    encoded_input = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        logits = model(**encoded_input).logits
        probabilities = torch.softmax(logits, dim=1)
    results = []
    for i, class_prob in enumerate(probabilities[0]):
        class_name = label_encoder.classes_[i]
        class_probability = class_prob.item()
        results.append({"class": class_name, "probability": class_probability})
    return results


# def classifier_equipament(text, path_model=r'data\models\model_NER'):
#     text = preprocess_text(text,'lemma')
#     nlp = load(path_model)
#     doc = nlp(text)
#     labels = [{"text":entidade.text,"class":entidade.label_} for entidade in doc.ents]
#     return labels


# def classifier_issue(text, path_model=r'data\models\model_bert_problem'):
#     tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
#     model = BertForSequenceClassification.from_pretrained(path_model)
#     label_encoder = LabelEncoder()
#     label_encoder.classes_ = torch.load(f'{path_model}\label_encoder_classes.pt')
#     encoded_input = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
#     with torch.no_grad():
#         logits = model(**encoded_input).logits
#         probabilities = torch.softmax(logits, dim=1)
#     results = []
#     for i, class_prob in enumerate(probabilities[0]):
#         class_name = label_encoder.classes_[i]
#         class_probability = class_prob.item()
#         results.append({"class": class_name, "probability": class_probability})
#     return results

def classifier_issue(text, path_model=r'data\models\model_bert_problem'):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForSequenceClassification.from_pretrained(path_model)
    label_encoder = LabelEncoder()
    label_encoder.classes_ = torch.load(f'{path_model}\label_encoder_classes.pt')
    encoded_input = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        logits = model(**encoded_input).logits
        probabilities = torch.softmax(logits, dim=1)
    max_prob_index = torch.argmax(probabilities)
    max_prob_class = label_encoder.classes_[max_prob_index]
    max_prob_value = probabilities[0][max_prob_index].item()
    return {"class": max_prob_class, "probability": max_prob_value}


def classifier_offensive(user_text):
    censored_words = ["aidético", "aidética", "aleijado", "aleijada", "analfabeto", "analfabeta", "anus", "anão", "anã", "arrombado", "apenado", "apenada", "baba-ovo", "babaca", "babaovo", "bacura", "bagos", "baianada", "baitola", "barbeiro", "barraco", "beata", "bebum", "besta", "bicha", "bisca", "bixa", "boazuda", "boceta", "boco", "boiola", "bokete", "bolagato", "bolcat", "boquete", "bosseta", "bosta", "bostana", "boçal", "branquelo", "brecha", "brexa", "brioco", "bronha", "buca", "buceta", "bugre", "bunda", "bunduda", "burra", "burro", "busseta", "bárbaro", "bêbado", "bêbedo", "caceta", "cacete", "cachorra", "cachorro", "cadela", "caga", "cagado", "cagao", "cagão", "cagona", "caipira", "canalha", "canceroso", "caralho", "casseta", "cassete", "ceguinho", "checheca", "chereca", "chibumba", "chibumbo", "chifruda", "chifrudo", "chochota", "chota", "chupada", "chupado", "ciganos", "clitoris", "clitóris", "cocaina", "cocaína", "coco", "cocô", "comunista", "corna", "cornagem", "cornisse", "corno", "cornuda", "cornudo", "cornão", "corrupta", "corrupto", "coxo", "cretina", "cretino", "criolo", "crioulo", "cruz-credo", "cu", "cú", "culhao", "culhão", "curalho", "cuzao", "cuzão", "cuzuda", "cuzudo", "debil", "débil", "debiloide", "debilóide", "deficiente", "defunto", "demonio", "demônio", "denegrir", "denigrir", "detento", "difunto", "doida", "doido", "egua", "égua", "elemento", "encostado", "esclerosado", "escrota", "escroto", "esporrada", "esporrado", "esporro", "estupida", "estúpida", "estupidez", "estupido", "estúpido", "facista", "fanatico", "fanático", "fascista", "fedida", "fedido", "fedor", "fedorenta", "feia", "feio", "feiosa", "feioso", "feioza", "feiozo", "felacao", "felação", "fenda","feia", "boba", "chata", "vai pro inferno", "puta", "quer casar comigo?", "sua gostosa","gostoso","seu gostoso","feio","bobo","babaca","filha da puta","desgraçado","filha da mãe","otário","arrombado","lazarento","vagabundo","merda","foda", "fodao", "fodão", "fode", "fodi", "fodida", "fodido", "fornica", "fornição", "fudendo", "fudeção", "fudida", "fudido", "furada", "furado", "furnica", "furnicar", "furo", "furona", "furão", "gai", "gaiata", "gaiato", "gay", "gilete", "goianada", "gonorrea", "gonorreia", "gonorréia", "gosmenta", "gosmento", "grelinho", "grelo", "gringo", "homo-sexual", "homosexual", "homosexualismo", "homossexual", "homossexualismo", "idiota", "idiotice", "imbecil", "inculto", "iscrota", "iscroto", "japa", "judiar", "ladra", "ladrao", "ladroeira", "ladrona", "ladrão", "lalau", "lazarento", "leprosa", "leproso", "lesbica", "lésbica", "louco", "macaca", "macaco", "machona", "macumbeiro", "malandro", "maluco", "maneta", "marginal", "masturba", "meleca", "meliante", "merda", "mija", "mijada", "mijado", "mijo", "minorias", "mocrea", "mocreia", "mocréia", "moleca", "moleque", "mondronga", "mondrongo", "mongol", "mongoloide", "mongolóide", "mulata", "mulato", "naba", "nadega", "nádega", "nazista", "negro", "nhaca", "nojeira", "nojenta", "nojento", "nojo", "olhota", "otaria", "otario", "otária", "otário", "paca", "palhaco", "palhaço", "paspalha", "paspalhao", "paspalho", "pau", "peia", "peido", "pemba", "pentelha", "pentelho", "perereca", "perneta", "peru", "peão", "pica", "picao", "picão", "pilantra", "pinel", "pinto", "pintudo", "pintão", "piranha", "piroca", "piroco", "piru", "pivete", "porra", "prega", "preso", "prequito", "priquito", "prostibulo", "prostituta", "prostituto", "punheta", "punhetao", "punhetão", "pus", "pustula", "puta", "puto", "puxa-saco", "puxasaco", "penis", "pênis", "rabao", "rabão", "rabo", "rabuda", "rabudao", "rabudão", "rabudo", "rabudona", "racha", "rachada", "rachadao", "rachadinha","rachadinho","rachado","ramela","remela","retardada","retardado","ridícula","roceiro","rola","rolinha","rosca","sacana","safada","safado","sapatao","sapatão","sifilis","sífilis","siririca","tarada","tarado","testuda","tesuda","tesudo","tezao","tezuda","tezudo","traveco","trocha","trolha","troucha","trouxa","troxa","tuberculoso","tupiniquim","turco","vaca","vadia","vagal","vagabunda","vagabundo","vagina","veada","veadao","veado","viada","viadagem","viadao","viadão","viado","viadão","víado","xana","xaninha","xavasca","xerereca","xexeca","xibiu","xibumba","xiíta","xochota","xota","xoxota","vacilao","vacilão","ferrar","vai se fuder","vai se ferrar","vai tomar no cu"]
    for censored_word in censored_words:
        similarity = jaccard_similarity(censored_word, user_text)
        if similarity > 0.9:
            return True
    return False

# def classifier_offensive(text):
#     device = torch.device('cpu')
#     model_name = 'neuralmind/bert-base-portuguese-cased'
#     tokenizer = BertTokenizer.from_pretrained(model_name)
#     loaded_model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)
#     loaded_model.load_state_dict(torch.load(r'data\models\model censure\best_model8.pt', map_location=device))
#     loaded_model.to(device)
#     loaded_model.eval()
#     sentences = text.split(".")
#     predictions = []
#     with torch.no_grad():
#         for sentence in sentences:
#             input_encodings = tokenizer(
#                 sentence, truncation=True, padding=True, max_length=512, return_tensors='pt'
#             )
#             input_ids = input_encodings['input_ids'].to(device)
#             attention_mask = input_encodings['attention_mask'].to(device)
#             outputs = loaded_model(input_ids, attention_mask=attention_mask)
#             logits = outputs.logits
#             batch_predictions = logits.argmax(dim=1).cpu().tolist()
#             predictions.append(f"{batch_predictions[0]}")
#     result = ' '.join(predictions)
#     if result == '0':
#         return False
#     else:
#         return True




def extract_main_equipment(text, path_model=r'data\models\model_NER'):
    text = preprocess_text(text, 'lemma')
    nlp = load(path_model)
    doc = nlp(text)
    labels = [{"text": entidade.text, "class": entidade.label_} for entidade in doc.ents]
    # Verificar se há várias classes de equipamentos mencionadas
    equipamentos = set(label["class"] for label in labels)
    if len(equipamentos) > 1:
        # Calcular a frequência de cada equipamento mencionado
        frequencias = {}
        for label in labels:
            equipamento = label["class"]
            frequencias[equipamento] = frequencias.get(equipamento, 0) + 1
        # Encontrar o equipamento com a maior frequência
        equipamento_principal = max(frequencias, key=frequencias.get)
        # Filtrar os labels para conter apenas o equipamento principal
        labels = [label for label in labels if label["class"] == equipamento_principal]
    return labels[0]
