import re
import pandas as pd
import sys
import os
current_dir = os.getcwd()
while "Chatbot" not in os.listdir(current_dir):
    current_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)


#####################################################################
from spacy import load, displacy
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.preprocessing import LabelEncoder
import torch
from src.utils.preprocessing_utils import *


def classifier_equipament(text, path_model=r'data\models\model_NER'):
    text = preprocess_text(text,'lemma')
    nlp = load(path_model)
    doc = nlp(text)
    labels = [{"text":entidade.text,"class":entidade.label_} for entidade in doc.ents]
    return labels

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
        predicted_labels = torch.argmax(probabilities, dim=1)
        predicted_classes = label_encoder.inverse_transform(predicted_labels)
    probability = probabilities[0][predicted_labels].item()
    if probability > 0.9:
        classe = predicted_classes.item()
    else:
        classe = None
        probability = 1.0
    return {"text":text,"class":classe,"probability":probability}

def classifier_problem(text, path_model=r'data\models\model_bert_problem'):
    text = preprocess_text(text, 'lemma')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForSequenceClassification.from_pretrained(path_model)
    label_encoder = LabelEncoder()
    label_encoder.classes_ = torch.load(f'{path_model}\label_encoder_classes.pt')
    encoded_input = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        logits = model(**encoded_input).logits
        probabilities = torch.softmax(logits, dim=1)
        predicted_labels = torch.argmax(probabilities, dim=1)
        predicted_classes = label_encoder.inverse_transform(predicted_labels)
    probability = probabilities[0][predicted_labels].item()
    if probability > 0.9:
        classe = predicted_classes.item()
        num = re.findall(r'\d+', classe)
        df = pd.read_excel(r"src\utils\data\num_problems.xlsx")
        for idx, row in df.iterrows():
            if int(num[0]) == row["num"]:
                classe = row["problem"]
    else:
        classe = None
        probability = 1.0
    return {"text":text,"class":classe,"probability":probability}



def classifier_offensive(text):
    text = preprocess_text(text)
    device = torch.device('cpu')
    model_name = 'neuralmind/bert-base-portuguese-cased'
    tokenizer = BertTokenizer.from_pretrained(model_name)

    loaded_model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)
    loaded_model.load_state_dict(torch.load(r'data\models\model censure\best_model8.pt', map_location=device))
    loaded_model.to(device)

    loaded_model.eval()
    sentences = text.split(".")

    predictions = []
    with torch.no_grad():
        for sentence in sentences:
            input_encodings = tokenizer(
                sentence, truncation=True, padding=True, max_length=512, return_tensors='pt'
            )
            input_ids = input_encodings['input_ids'].to(device)
            attention_mask = input_encodings['attention_mask'].to(device)

            outputs = loaded_model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            batch_predictions = logits.argmax(dim=1).cpu().tolist()
            predictions.append(f"{batch_predictions[0]}")

    return ' '.join(predictions)