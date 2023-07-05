import sys, os
sys.path.append(os.path.abspath(os.path.join('..', '..')))

# import language_tool_python
# from pyaspeller import YandexSpeller
from spellchecker import SpellChecker
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from spacy.lang.pt.stop_words import STOP_WORDS
import spacy
from nltk.corpus import wordnet
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from re import sub
from nltk import download
download('punkt')
download('stopwords')


def sent_tokenizer_nltk(text):
    tokens = sent_tokenize(text)
    return tokens

def remove_num(text):
    text = sub(r'\d+', '', text)
    text = sub(r'\s+', ' ',text)
    return text

def remove_punct(text):
    text = sub(r"[!#$%&'()*+,-./:;<=>?@[^_`{|}~]+", ' ',text)
    text = sub(r'\s+', ' ',text)
    return text

def extract_keywords(text):
    tokens = word_tokenize(text)
    keywords = []
    for word in tokens:
        word = word.lower()
        if word not in stopwords.words('portuguese') or word.lower() not in STOP_WORDS:
            keywords.append(word)
    return ' '.join(keywords)

def get_synonyms(text):
    tokens = word_tokenize(text)
    synonyms = []
    for word in tokens:
        for syn in wordnet.synsets(word, lang="por"):
            for lemma in syn.lemmas(lang="por"):
                synonyms.append(lemma.name())
    return synonyms

def remove_accent(text):
    text = sub('[áàãâä]', 'a', sub('[éèêë]', 'e', sub('[íìîï]', 'i', sub('[óòõôö]', 'o', sub('[úùûü]', 'u', sub('[ç]','c',text))))))
    text = sub(r'\s+', ' ',text)
    return text

nlp = spacy.load('pt_core_news_sm')
def preprocess_lemma(text):
    doc = nlp(text)
    lemmas = []
    for token in doc:
        lemmas.append(token.lemma_)
    lemmas = ' '.join(lemmas)
    return lemmas

def corrector(text):
    spell_pt = SpellChecker(language='pt')
    tokens = word_tokenize(text)
    for i, token in enumerate(tokens):
        correction = spell_pt.correction(token)
        try:
            if correction != token and correction != None:
                tokens[i] = correction
        except:
            pass
    return ' '.join(tokens)


def preprocess_text(text, tipo='lemma'):
    text = remove_punct(text)
    text = remove_num(text)
    text = corrector(text)
    text = extract_keywords(text)
    if tipo == 'lemma':
        text = preprocess_lemma(text)
    else:
        pass
    text = remove_accent(text)
    return text.lower()



def jaccard_similarity(term1, term2):
    tokens1 = set(word_tokenize(term1.lower()))
    tokens2 = set(word_tokenize(term2.lower()))
    
    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)
    
    similarity = len(intersection) / len(union)
    return similarity

# def preprocess_semantic(frase):
#     tool = language_tool_python.LanguageTool('pt')
#     matches = tool.check(frase)
#     for i in matches:
#         frase = frase[:i.offset] + i.replacements[0] + frase[i.offset+i.errorLength:]
#     tool.close()
#     return frase