import nltk
nltk.download('punkt')
nltk.download('stopwords')


import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stop_words = set(stopwords.words('english'))


def standerdize_txt(sentence):
    # remove punctuation
    sentence = sentence.translate(str.maketrans("", "", string.punctuation))
    filtered_words = [word for word in words if word not in stop_words]
    # join filtered words into sentence
    filtered_sentence = " ".join(filtered_words)
    return filtered_sentence.replace(" ", "").lower()

def get_similarity(sentence1, sentence2):
    return SequenceMatcher(None, standerdize_txt(sentence1), standerdize_txt(sentence2)).ratio()