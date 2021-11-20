import nltk
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from nltk.corpus import stopwords
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import re
nltk.download('stopwords')
nltk.download('wordnet')
lemma = WordNetLemmatizer()
stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
import spacy
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.tag import StanfordNERTagger
nltk.download('punkt')
nltk.downloader.download('maxent_ne_chunker')
nltk.downloader.download('words')
nltk.downloader.download('treebank')
nltk.downloader.download('maxent_treebank_pos_tagger')
import locationtagger
from urllib import request
        
class Extract:     
    def __init__(self, doc):
        super(Extract, self).__init__()
        self.st = StanfordNERTagger('../stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz',
					   '../stanford-ner-2018-10-16/stanford-ner.jar', encoding='utf-8')		
        # NLTK Stop words
        nltk.download('stopwords')
        nltk.download('wordnet')
        from nltk.corpus import stopwords
        lemma = WordNetLemmatizer()
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        self.doc = doc
        self.stop_words = stopwords.words('english')
        self.stop_words.extend(['from', 'subject', 're', 'edu', 'use']) 
            
    def extract_expertise(self):        
        print("Start Mining")
        data = [self.doc]

        # Remove Emails
        data = [re.sub('\S*@\S*\s?', '', sent) for sent in data]

        # Remove new line characters
        data = [re.sub('\s+', ' ', sent) for sent in data]

        # Remove distracting single quotes
        data = [re.sub("\'", "", sent) for sent in data]  
        
        def sent_to_words(sentences):        
            for sentence in sentences:
                yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations
        
        def remove_stopwords(texts):            
            return [[word for word in simple_preprocess(str(doc)) if word not in self.stop_words] for doc in texts]

        def make_bigrams(texts):
            return [bigram_mod[doc] for doc in texts]

        def make_trigrams(texts):
            return [trigram_mod[bigram_mod[doc]] for doc in texts]

        def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
            """https://spacy.io/api/annotation"""
            texts_out = []
            for sent in texts:
                doc = nlp(" ".join(sent)) 
                texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
            return texts_out           

        data_words = list(sent_to_words(data))

        # Build the bigram and trigram models
        bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
        trigram = gensim.models.Phrases(bigram[data_words], threshold=100)  

        # Faster way to get a sentence clubbed as a trigram/bigram
        bigram_mod = gensim.models.phrases.Phraser(bigram)
        trigram_mod = gensim.models.phrases.Phraser(trigram)

        # See trigram example
        # print(trigram_mod[bigram_mod[data_words[0]]])        

        # Remove Stop Words
        data_words_nostops = remove_stopwords(data_words)

        # Form Bigrams
        data_words_bigrams = make_bigrams(data_words_nostops)

        # Initialize spacy 'en' model, keeping only tagger component (for efficiency)
        # python3 -m spacy download en
        nlp = spacy.load("en_core_web_sm")

        # Do lemmatization keeping only noun, adj, vb, adv
        data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

        # print(data_lemmatized[:1])

        # Create Dictionary
        id2word = corpora.Dictionary(data_lemmatized)

        # Create Corpus
        texts = data_lemmatized

        # Term Document Frequency
        corpus = [id2word.doc2bow(text) for text in texts]

        # View
        # print(corpus[:1])


        [[(id2word[id], freq) for id, freq in cp] for cp in corpus[:1]]


        # Build LDA model
        lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                   id2word=id2word,
                                                   num_topics=1, 
                                                   random_state=10,
                                                   update_every=1,
                                                   chunksize=1,
                                                   passes=50,
                                                   alpha='auto',
                                                   per_word_topics=True)
                                                   


        # Print the Keyword in the 10 topics
        '''print(lda_model.print_topics())

        doc_lda = lda_model[corpus]'''

        topics = lda_model.print_topics(num_words=3)
        for topic in topics:
            print(topic)

        shown_topics = lda_model.show_topics(num_topics=1, 
                                                     num_words=3,
                                                     formatted=False)
        LDA_topics = [[word[0] for word in topic[1]] for topic in shown_topics]

        # print(LDA_topics)
        
        from lda import guidedlda
        from sklearn.feature_extraction.text import CountVectorizer
        from nltk.corpus import wordnet
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
        def reflection_tokenizer(text):
            text=re.sub(r'[\W_]+', ' ', text) #keeps alphanumeric characters
            text=re.sub(r'\d+', '', text) #removes numbers
            text = text.lower()
            tokens = [word for word in word_tokenize(text)]
            tokens = [word for word in tokens if len(word) >= 3]
            #removes smaller than 3 character
            tokens = [word_lemmatizer(w) for w in tokens]
            tokens = [s for s in tokens if s not in self.stop_words]
            return tokens

        corrected_content = [doc1]
        seed_topic_list = LDA_topics
        lemmatize_token = reflection_tokenizer(doc1)

        from sklearn.feature_extraction.text import CountVectorizer

        token_vectorizer = CountVectorizer(tokenizer = reflection_tokenizer, min_df=1, max_df=1.0, stop_words=self.stop_words, ngram_range=(1, 4))

        X = token_vectorizer.fit_transform(corrected_content)

        tf_feature_names = token_vectorizer.get_feature_names()

        word2id = dict((v, idx) for idx, v in enumerate(tf_feature_names))

        model = guidedlda.GuidedLDA(n_topics=1, n_iter=100, random_state=7, refresh=10)
        seed_topics = {}
        for t_id, st in enumerate(seed_topic_list):
            for word in st:
                seed_topics[word2id[word]] = t_id
        model.fit(X, seed_topics=seed_topics, seed_confidence=0.15)

        n_top_words = 10
        topic_word = model.topic_word_
        for i, topic_dist in enumerate(topic_word):
             topic_words = np.array(tf_feature_names)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
             print('Topic {}: {}'.format(i, ' '.join(topic_words)))
     
    def extract_phone(self):
        return re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', self.doc)

    def extract_email(self):
        email = re.findall(r'[\w\.-]+@[\w\.-]+', self.doc)
        return email

    def extract_name(self):
        tokenized_text = word_tokenize(self.doc)
        classified_text = self.st.tag(tokenized_text)
        print(classified_text)
        names = []
        found_name = False
        name = ''
        for tup in classified_text:
            if found_name:
                if tup[1] == "PERSON":
                    name += ' '+tup[0].title()
                else:
                    break
            elif tup[1] == "PERSON":
                name += tup[0].title()
                found_name = True
        names.append(name)
        return names   

    def extract_department(self):
        tokenized_text = word_tokenize(self.doc)
        classified_text = self.st.tag(tokenized_text)
        print(classified_text)
        names = []
        found_name = False
        name = ''
        for tup in classified_text:
            if found_name:
                if tup[1] == "ORGANIZATION":
                    name += ' '+tup[0].title()
                else:
                    break
            elif tup[1] == "ORGANIZATION":
                name += tup[0].title()
                found_name = True
        names.append(name)        
        
        return names   
    
    def extract_university(self, url):        
        html = request.urlopen(url).read().decode('utf8')
        html[:60]

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title')
        
        return title.string  

    def extract_location(self, text):
        location = ""     	
        place_entity = locationtagger.find_locations(text = text)
        location = str(place_entity.cities) + " " + str(place_entity.regions) + " " + str(place_entity.countries)
        return location    

def ExtractItems(doc):
    try:
        return Extract(doc)        
    except:
        return Extract(doc)  
     
if __name__ == '__main__':
    doc1 = "  Geoffrey Werner Challen Teaching Associate Professor 2227 Siebel Center for Comp Sci 201 N. Goodwin Ave. Urbana Illinois 61801 (217) 300-6150 challen@illinois.edu : Primary Research Area CS Education Research Areas CS Education For more information blue Systems Research Group (Defunct) Internet Class: Learn About the Internet on the Internet OPS Class: Learn Operating Systems Online CS 125 Home Page Education Ph.D. Computer Science, Harvard University, 2010 AB Physics, Harvard University, 2003 Academic Positions Associate Teaching Professor, University of Illinois, 2017 . Primary Research Area CS Education Research Areas CS Education For more information blue Systems Research Group (Defunct) Internet Class: Learn About the Internet on the Internet OPS Class: Learn Operating Systems Online CS 125 Home Page . . For more information blue Systems Research Group (Defunct) Internet Class: Learn About the Internet on the Internet OPS Class: Learn Operating Systems Online CS 125 Home Page . "
    extract_items = ExtractItems(doc1)
    print(extract_items.extract_expertise())
    print(extract_items.extract_phone())
    print(extract_items.extract_email())  
    print(extract_items.extract_name())
    print(extract_items.extract_department())
    print(extract_items.extract_university("https://illinois.edu/"))    
    print(extract_items.extract_location(doc1))
    
