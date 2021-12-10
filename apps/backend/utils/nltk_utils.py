import re
import gensim
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

def sent_to_words(sentences):
    for sentence in sentences:
        yield gensim.utils.simple_preprocess(str(sentence), deacc=True)  # deacc=True removes punctuations

def tokenizer(doc, remove_email: bool = True):
    tokens = []

    if not doc:
        return tokens

    # remove emails
    if remove_email:
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

    bigram = gensim.models.Phrases([tokens], min_count=5, threshold=100)  # higher threshold fewer phrases.
    bigram_mod = gensim.models.phrases.Phraser(bigram)

    data_words_bigrams = [bigram_mod[doc] for doc in [tokens]]
    #print(data_words_bigrams)

    # removes smaller than 3 character
    tokens = [word_lemmatizer(w) for w in data_words_bigrams[0]]

    # remove stop words
    tokens = [s for s in tokens if s not in stopwords.words('english')]

    # print("Tokens: ", tokens)

    return tokens


def sanitizer(doc):
    tokens = []

    if not doc:
        return tokens

    # remove new line
    doc = doc.replace('\n', ' ')

    # reomve line feed
    doc = doc.replace('\r', '')

    # remove single quotes
    doc = doc.replace("\'", "")

    # keeps alphanumeric characters
    doc = re.sub(r'[\W_]+', ' ', doc)

    # convert lowercase
    doc = doc.lower()

    tokens = [word for word in word_tokenize(doc)]
    tokens = [word for word in tokens if len(word) >= 3]

    # removes smaller than 3 character
    tokens = [word_lemmatizer(w) for w in tokens]

    # print("Tokens: ", tokens)

    return tokens
