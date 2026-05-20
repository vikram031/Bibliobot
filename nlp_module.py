import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

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
    return {"entities": []}