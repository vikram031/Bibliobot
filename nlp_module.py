import nltk
import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Make sure NLP token tools are ready
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

# Load the lightweight English model for entity matching
nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words('english'))

# Predefined keyword rules from Chapter 4 of the report
INTENT_KEYWORDS = {
    'SEARCH_BOOK': ['find', 'search', 'show', 'have', 'books', 'looking'],
    'CHECK_AVAILABILITY': ['available', 'borrow', 'issued', 'return'],
    'GET_RECOMMENDATION': ['recommend', 'suggest', 'similar', 'like'],
    'GENERAL_QUERY': ['timing', 'hours', 'when', 'location', 'rules']
}

def classify_intent(text):
    tokens = word_tokenize(text.lower())
    filtered = [t for t in tokens if t not in stop_words]
    
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(word in filtered for word in keywords):
            return intent
            
    return 'UNRECOGNIZED'

def extract_entities(text):
    doc = nlp(text)
    return {"entities": [(ent.text, ent.label_) for ent in doc.ents]}