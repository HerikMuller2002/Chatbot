from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from spacy.lang.pt.stop_words import STOP_WORDS
from nltk.corpus import wordnet
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from re import sub
from nltk import download
download('punkt')
download('stopwords')

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
    text = sub('[áàãâä]', 'a', sub('[éèêë]', 'e', sub('[íìîï]', 'i', sub('[óòõôö]', 'o', sub('[úùûü]', 'u', text)))))
    text = sub(r'\s+', ' ',text)
    return text

def preprocess_lemma(text):
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text)
    lemmas = []
    for token in tokens:
        lemmas.append(lemmatizer.lemmatize(token))
    lemmas = ' '.join(lemmas)
    return lemmas

def preprocess_stem(text):
    stemmer = SnowballStemmer("portuguese")
    tokens = word_tokenize(text)
    stems = []
    for token in tokens:
        stems.append(stemmer.stem(token))
    stems = ' '.join(stems)
    return stems



def preprocess(text, tipo=None):
    text = remove_punct(text)
    text = remove_num(text)
    text = extract_keywords(text)
    if tipo == 'lemma':
        text = preprocess_lemma(text)
    elif tipo == 'stem':
        text = preprocess_stem(text)
    else:
        pass
    text = remove_accent(text)
    return text