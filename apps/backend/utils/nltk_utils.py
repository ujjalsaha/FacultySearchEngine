import re

import nltk
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def get_wordnet_pos(word):
    '''tags parts of speech to tokens
    Expects a string and outputs the string and
    its part of speech'''

    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)


def word_lemmatizer(text):
    '''lemamtizes the tokens based on their part of speech'''

    lemmatizer = WordNetLemmatizer()
    text = lemmatizer.lemmatize(text, get_wordnet_pos(text))
    return text


def tokenizer(doc):
    # remove emails
    doc = re.sub('\S*@\S*\s?', '', doc)

    # remove new line
    doc = doc.replace('\n', ' ')

    # reomve line feed
    doc = doc.replace('\r', '')

    # remove single quotes
    doc = doc.replace("\'", "")

    # keeps alphanumeric characters
    doc = re.sub(r'[\W_]+', ' ', doc)

    # removes numbers
    doc = re.sub(r'\d+', '', doc)

    # convert lowercase
    doc = doc.lower()

    tokens = [word for word in word_tokenize(doc)]
    tokens = [word for word in tokens if len(word) >= 3]

    # removes smaller than 3 character
    tokens = [word_lemmatizer(w) for w in tokens]

    # remove stop words
    tokens = [s for s in tokens if s not in stopwords.words('english')]

    print("Tokens: ", tokens)
    return tokens
