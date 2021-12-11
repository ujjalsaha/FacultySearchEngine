import re, os, logging

from urllib import request

import gensim
import gensim.corpora as corpora
import nltk
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup

# import guidedlda
# from sklearn.feature_extraction.text import CountVectorizer

from apps.backend.api.googleapi import GoogleAPI
from apps.backend.utils.nltk_utils import sanitizer, tokenizer, stopwords

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.downloader.download('maxent_ne_chunker', quiet=True)
nltk.downloader.download('words', quiet=True)
nltk.downloader.download('treebank', quiet=True)
nltk.downloader.download('maxent_treebank_pos_tagger', quiet=True)

# logger = logging.getLogger('ExpertSearchv2.0')
logging.basicConfig(filename='lda_model.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



class Document:

    def __init__(self, doc, faculty_url=None, department_url=None, university_url=None):
        self.doc = doc
        self.faculty_url = faculty_url
        self.department_url = department_url
        self.university_url = university_url
        self.stop_words = stopwords.words('english')
        logger = logging.getLogger('my_module_name').setLevel(logging.WARNING)

    def __extract_ner(self, tag="PERSON"):
        """
        Using StanfordNERTagger finds name entity recognition
        :param tag:
        :return:
        """
        if not self.doc:
            return ""

        matched_tokens = []

        try:
            dirname = os.path.dirname(__file__)
            model_file = os.path.join(dirname,
                                      '../../../lib/stanford-ner-2020-11-17/classifiers/english.all.3class.distsim.crf.ser.gz')
            jar_file = os.path.join(dirname, '../../../lib/stanford-ner-2020-11-17/stanford-ner.jar')

            self.st = StanfordNERTagger(model_file, jar_file, encoding='utf-8')

            tokenized_text = word_tokenize(self.doc)
            classified_text = self.st.tag(tokenized_text)

            found_name = False
            name = ''
            for tup in classified_text:
                if found_name:
                    if tup[1] == tag:
                        name += ' ' + tup[0].title()
                    else:
                        break
                elif tup[1] == tag:
                    name += tup[0].title()
                    found_name = True

            matched_tokens.append(name)
        except Exception as e:
            print("Exception encouneted while extracting name: " + str(e))
            pass

        return " ".join(matched_tokens)

    def extract_expert_ner(self):
        """
        Using StanfordNERTagger finds name entity recognition
        """
        if not self.doc:
            return ""

        matched_tokens = []

        try:
            dirname = os.path.dirname(__file__)
            model_file = os.path.join(dirname,
                                      '../../../lib/stanford-ner-2020-11-17/classifiers/english.all.3class.distsim.crf.ser.gz')
            jar_file = os.path.join(dirname, '../../../lib/stanford-ner-2020-11-17/stanford-ner.jar')

            st = StanfordNERTagger(model_file, jar_file, encoding='utf-8')

            tokenized_text = word_tokenize(self.doc)
            classified_text = st.tag(tokenized_text)

            noname = ''
            for tup in classified_text:
                if tup[1] != 'PERSON' and tup[1]!= "LOCATION":
                    noname += ' ' + tup[0].title()

            matched_tokens.append(noname)
        except Exception as e:
            print("Exception encouneted while extracting nonames: " + str(e))
            pass

        return " ".join(matched_tokens)

    def __extract_title(self, url, type=None):
        if not url:
            return ""

        html = request.urlopen(url).read().decode('utf8')

        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title')

        title = title.string.strip() if title else ""

        # Trim unwanted text from title string
        title = title.replace("welcome to", "") if "welcome to" in title else title
        title = title.replace("Welcome to", "") if "Welcome to" in title else title

        title = title.strip()

        if '|' in title:
            if type == "university":
                titles = [title.strip() for title in title.split('|') if title and "department" not in title.lower()]

            elif type == "department":
                titles = [title.strip() for title in title.split('|') if title and "university" not in title.lower()]

            else:
                titles = [title.strip() for title in title.split('|') if title]

            title = max(titles, key=len)

        return title

    def extract_expertise(self):

        if not self.doc:
            return ""

        #tokens = tokenizer(self.extract_expert_ner())
        tokens = tokenizer(self.doc)
        # print("tokens: ", tokens)

        # Create Dictionary
        id2word = corpora.Dictionary([tokens])

        # Create Corpus - # Term Document Frequency
        corpus = [id2word.doc2bow(tokens)]

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

        dirname = os.path.dirname(__file__)
        lda_dataset = os.path.join(dirname, "../../../lib/lda/lda-trained-dataset")

        try:
            lda_model.load(lda_dataset)

        except:
            lda_model.save(lda_dataset)

        """
        # Print the Keyword in the 10 topics
        print(lda_model.print_topics())
        doc_lda = lda_model[corpus]
        """

        topics = lda_model.print_topics(num_words=10)
        lda_model.update(corpus)
        lda_model.save(lda_dataset)

        '''for topic in topics:
            print(topic)'''


        shown_topics = lda_model.show_topics(num_topics=1,
                                             num_words=10,
                                             formatted=False)
        topic_list = [[word[0] for word in topic[1]] for topic in shown_topics]

        # LDA topics
        """seed_topic_list = [[word[0] for word in topic[1]] for topic in shown_topics]
        #seed_topic_list = [["internet","education","research"]]

        # print("LDA Topics: ", seed_topic_list)
        token_vectorizer = CountVectorizer(tokenizer=tokenizer,
                                           min_df=1,
                                           max_df=1.0,
                                           ngram_range=(1, 4))
        X = token_vectorizer.fit_transform([self.doc])
        tf_feature_names = token_vectorizer.get_feature_names()
        word2id = dict((v, idx) for idx, v in enumerate(tf_feature_names))
        model = guidedlda.GuidedLDA(n_topics=1, n_iter=100, random_state=7, refresh=10)
        seed_topics = {}
        for t_id, st in enumerate(seed_topic_list):
            for word in st:
                seed_topics[word2id[word]] = t_id
        model.fit(X, seed_topics=seed_topics, seed_confidence=0.15)
        n_top_words = 10
        topic_words = []
        for i, topic_dist in enumerate(model.topic_word_):
            topic_words = np.array(tf_feature_names)[np.argsort(topic_dist)][:-(n_top_words + 1):-1]
            # print('Topic {}: {}'.format(i, ' '.join(topic_words)))
        # return unqiue topic words
        return " ".join(list(set(" ".join(topic_words).split())))

        # return unqiue topic words
        # return " ".join(list(set(seed_topic_list)))
        """

        return " ".join(topic_list[0]) if topic_list and topic_list[0] else ""

    def extract_phone(self):
        if not self.doc:
            return ""

        # phone_numbers = re.findall(r'[+(]?[1-9][0-9 .\-()]{8,}[0-9]', self.doc)
        phone_numbers = re.findall(r"\(?\b[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4}\b", self.doc)
        return phone_numbers[0] if phone_numbers else None

    def extract_email(self):
        if not self.doc:
            return ""

        emails = re.findall(r'[\w.-]+@[\w.-]+', self.doc)
        return emails[0] if emails else None

    def extract_name(self):
        # name = self.__extract_ner(tag="PERSON")
        name = self.__extract_title(self.faculty_url)
        return name if name else None

    def extract_university(self):
        university_name = self.__extract_title(self.university_url)
        return university_name if university_name else None

    def extract_department(self):
        department_name =  self.__extract_title(self.department_url)
        return department_name if department_name else None

    def extract_biodata(self):
        return " ".join(sanitizer(self.doc)) if self.doc else None

    def extract_location(self):
        location = ""
        try:
            googleAPI = GoogleAPI(place_name=self.extract_university())
            comps = googleAPI.get_component(field_comp='address_components')
            for comp in comps:
                if len(comp['types']) > 1:
                    if comp['types'][0] == 'administrative_area_level_1':
                        state = comp['long_name']
                        location = location + str(comp['long_name']) + ", "
                    if comp['types'][0] == 'locality':
                        city = comp['long_name']
                        location = location + str(comp['long_name']) + ", "
                    if comp['types'][0] == 'country':
                        country = comp['long_name']
                        location = location + str(comp['long_name'])
        except:
            pass

        return location if location else "Unknown"


if __name__ == '__main__':
    #doc = "  Geoffrey Werner Challen Teaching Associate Professor 2227 Siebel Center for Comp Sci 201 N. Goodwin Ave. Urbana Illinois 61801 (217) 300-6150 challen@illinois.edu : Primary Research Area CS Education Research Areas CS Education For more information blue Systems Research Group (Defunct) Internet Class: Learn About the Internet on the Internet OPS Class: Learn Operating Systems Online CS 125 Home Page Education Ph.D. Computer Science, Harvard University, 2010 AB Physics, Harvard University, 2003 Academic Positions Associate Teaching Professor, University of Illinois, 2017 . Primary Research Area CS Education Research Areas CS Education For more information blue Systems Research Group (Defunct) Internet Class: Learn About the Internet on the Internet OPS Class: Learn Operating Systems Online CS 125 Home Page . . For more information blue Systems Research Group (Defunct) Internet Class: Learn About the Internet on the Internet OPS Class: Learn Operating Systems Online CS 125 Home Page . "
    #doc = "  Geoffrey Werner Challen Teaching Associate Professor 2227 Siebel Center for Comp Sci 201 N. Goodwin Ave. Urbana Illinois 61801 (217) 300-6150 challen@illinois.edu : Primary Research Area CS Education Research Areas CS Education For more information blue Systems Research Group (Defunct) Internet Class: Learn About the Internet on the Internet OPS Class: Learn Operating Systems Online CS 125 Home Page Education Ph.D. Computer Science, Harvard University, 2010 AB Physics, Harvard University, 2003 Academic Positions Associate Teaching Professor, University of Illinois, 2017 . Primary Research Area CS Education Research Areas CS Education For more information blue Systems Research Group (Defunct) Internet Class: Learn About the Internet on the Internet OPS Class: Learn Operating Systems Online CS 125 Home Page . . For more information blue Systems Research Group (Defunct) Internet Class: Learn About the Internet on the Internet OPS Class: Learn Operating Systems Online CS 125 Home Page . Jiaxin Lin , Kiran Patel , Brent E. Stephens , Anirudh Sivaraman , Aditya Akella Jiaxin Lin , Kiran Patel , Brent E. Stephens , Anirudh Sivaraman , Aditya Akella Jiaxin Lin , Kiran Patel , Brent E. Stephens , Anirudh Sivaraman , Aditya Akella Jiaxin Lin , Kiran Patel , Brent E. Stephens , Anirudh Sivaraman , Aditya Akella"
    #doc = "  Tandy Warnow Founder Professor of 480-2999-3344 Computer Science Area Chair, Bioinformatics and Computational Biology Group Member, Carl R. Woese Institute for Genomic Biology Affiliate, National Center for Supercomputing Applications Affiliate, Unit for Criticism and Literary Theory Affiliate, departments of Electrical and Computer Engineering, Bioengineering, Mathematics, Statistics, Animal Biology, Entomology, and Plant Biology PhD (Mathematics) University of California at Berkeley, 1991 B.S. (Mathematics) University of California at Berkeley, 1984 Brief Biosketch Fellow of the ISCB (International Society for Computational Biology), 2017 Fellow of the ACM (Association for Computing Machinery), 2015: For contributions to mathematical theory, algorithms, and software for large-scale molecular phylogenetics and historical linguistics Research Overview : My research combines mathematics, computer science, probability, and statistics, in order to develop algorithms with improved accuracy for large-scale and complex estimation problems in phylogenomics (genome-scale phylogeny estimation), multiple sequence alignment , metagenomics , and historical linguistics . I am a big fan of Blue Waters , and have benefitted from two allocations. Click here for the 2017 annual report for my Blue Waters allocation on algorithms for big data phylogenomics, proteomics, and metagenomics. Click here or here for more about my research and the students I work with, and here for a brief biosketch. Computational Phylogenetics : An introduction to designing methods for phylogeny estimation , published by Cambridge University Press (and available for purchase at Amazon and as an E-book at Google Play ). Errata are posted as I find them. The image of the Monterey Cypress is there because of the NSF-funded CIPRES project , whose purpose was to develop the methods and computational infrastructure to improve large-scale phylogeny estimation. Why I wrote this book . Research Positions Available: I have openings in my group for graduate students (PhD or MS) to work on developing computational methods for large-scale multiple sequence alignment, phylogeny estimation, metagenomics, and even historical linguistics. Strong programming skills, mathematical intuition, and interest in collaboration are necessary. If you are already a graduate student at UIUC, please contact me directly. If you are interested in applying to UIUC for graduate school and would like to work with me, please read this first and then contact me. Unfortunately, I do not have any funding available for postdoctoral researchers. However, if you have your own source of funds and have published papers directly related to my research, I'll be glad to talk with you about working together. (If you are an undergraduate , please see this page .) Current Funding : Multiple sequence alignment , funded by NSF grant ABI-1458652, beginning August 2015. This project will develop new methods for multiple sequence alignment, building on our SAT, PASTA, and UPP methods. Metagenomics , funded by NSF grant III:AF:1513629. This is a collaborative grant with the University of Maryland, for new methods for metagenomic dataset analysis, building on our TIPP method for taxon identification of reads in a metagenomic sample. Graph-Theoretic Algorithms to Improve Phylogenomic Analyses , funded by NSF grant CCF-1535977. I am the overall PI, and this project is collaborative with Satish Rao (UC Berkeley PI) and Chandra Chekuri (UIUC). We are developing new theoretical computer science and discrete algorithms for improving the estimation of large species and gene trees, and specifically enabling statistical methods to scale to ultra-large datasets. Recent NSF funding has supported work in phylogenomics, described here . This is still an area of very active research in my group. I also recently benefited from support of the John P. Simon Guggenheim Foundation , and earlier support from the David and Lucile Packard Foundation , the Radcliffe Institute for Advanced Study at Harvard University , the Program for Evolutionary Dynamics at Harvard University , and Microsoft Research, New England . The Founder Professorship is funded through the Grainger Engineering Breakthroughs Initiative , which is supporting development of research in Big Data and Bioengineering at UIUC. I am grateful to the National Science Foundation for its continuous support since 1994. See this page for completed projects funded by NSF, starting in 2001. A day in the life of an SRO at NIH (not by me) -- Stendhal, Lucien Leuwen (a quote much loved by my stepfather, Martin J. Klein , and an essential guide for all scholarship). Click here for Google Scholar Citations (i10-index 143 and h-index 60). For prospective students and postdocs Current and former students and postdocs Teaching Recent Symposia and Software Schools CIPRES Personal Conference Calendar News Articles Academic Integrity Downloadable papers Complete vita and publication list Software and research data Research data from UT-Austin Guidelines for writing scholarly papers Seminar Talks (2015-present) My F1000 recommendations Ethics in science Contact info My favorite Kimonos! "
    #doc = "  Adeel Bhutta|https://cs.indiana.edu/contact/profile/index.html?Adeel_Bhutta|https://cs.indiana.edu/|Department of Computer Science: Indiana University Bloomington|https://www.indiana.edu/|Indiana University Bloomington|aabhutta@indiana.edu|(812) 855-3147|Bloomington, Indiana, United States|computer engineering award university program processing course central science system|Adeel A Bhutta Senior Lecturer Contact Information aabhutta@indiana.edu (812) 855-3147 Luddy Hall (700 N. Woodlawn Ave) 2016 http://homes.luddy.indiana.edu/aabhutta/ Education Ph.D. in Computer Engineering at University of Central Florida, Orlando M.S. in Computer Engineering at University of Central Florida, Orlando M.S. in Computer Science at University of Central Florida, Orlando Courses Taught at Luddy A290/A590 Android App Development I & II B456 Image Processing C291 System Programming with C and Unix C323 Mobile App Development (Android) H212/C212/A592 Introduction to Computer Systems P565/465 Software Engineering I & SE for Information Systems I Y399 Project in Professional Practice (Internship Course) Biography Mr. Adeel Bhutta is currently Senior Lecturer of Computer Science in Luddy School of Informatics, Computing, and Engineering. At IU, he has proposed, developed and taught many fundamental and advanced undergraduate and graduate courses in different areas including Programming, Software Design & Development, Mobile App Development, Image Processing, and Software Engineering. Prior to joining IU, he was the Coordinator and Lecturer of Computer Technology (now called IT) at Kent State University @ Stark where he developed the COMT program from grounds-up and led one of the fastest growing programs on campus. He also taught a number of CS & ECE courses at University of Central Florida (UCF) and Valencia College. Mr. Bhutta's industrial experience includes working on optimization of Video Compression algorithms (H263) for TriMedia processors and developing application software for Voice over IP (VoIP) systems. He holds a PhD degree in Computer Engineering and two MS degrees in Computer Science as well as Computer Engineering, all from UCF. His primary areas of research in recent years have been within Computer Vision and Image Processing and he has worked on Background Subtraction, Selective Subtraction and Deep Learning. In addition, his recent research has focussed on Computer Science Education and more specifically, Active Learning Techniques. Mr. Bhutta is Senior Member of IEEE and Professional (full) Member of ACM and IET. He has regularly served on many departmental/school committees along with program committees of several International Conferences and Journals and has been awarded several fellowships, scholarships and awards. Most recently, he was awarded IU FACET's Mumford Excellence in Extraordinary Teaching Award (2021), IU's prestigious Trustees Teaching Award (2019) and Champion of Inclusion Award from SICE (2017). Research Areas Artificial Intelligence and Machine Learning Computer Vision, Speech, and Music Processing Update your profile|2021-12-09 01:01:58.023304|2021-12-09"
    #doc = "Sal Blanco|https://cs.indiana.edu/contact/profile/index.html?Saúl_Blanco|https://cs.indiana.edu/|Department of Computer Science: Indiana University Bloomington|https://www.indiana.edu/|Indiana University Bloomington|sblancor@indiana.edu||Bloomington, Indiana, United States|science computer discrete mathematics structure informatics information introduction luddy university|Saúl A. Blanco Assistant Professor Contact Information sblancor@indiana.edu Luddy Hall (700 N. Woodlawn Ave) 3066 http://homes.sice.indiana.edu/sblancor/ Education Ph.D. in Mathematics at Cornell University, 2012 Courses Taught at Luddy B351 Introduction to AI C241 Discrete Structures for Computer Science H241 Discrete Structures for Computer Science, Honors I201 Mathematical Foundations of Informatics I231 Introduction to the Mathematics of Cybersecurity I308 Information Representation I399/C290 Current Topics in Informatics/Tools in Computer Science: Games and Puzzles Research Areas Algorithms and Theoretical Computer Science Artificial Intelligence and Machine Learning Discrete Mathematics Update your profile|2021-12-09 01:01:58.023326|2021-12-09 01:01:58.023327"
    #doc = "David Crandall|https://cs.indiana.edu/contact/profile/index.html?David_Crandall|https://cs.indiana.edu/|Department of Computer Science: Indiana University Bloomington|https://www.indiana.edu/|Indiana University Bloomington|djcran@indiana.edu|(812) 856-1115|Bloomington, Indiana, United States|computer science university center research cornell vision intelligence learn machine|David J Crandall Director of Graduate Studies for Computer Science Professor of Computer Science Director of Center for Machine Learning Contact Information djcran@indiana.edu (812) 856-1115 611 N. Park Ave http://www.cs.indiana.edu/~djcran/ Education Ph.D. in Computer Science at Cornell University, 2008 M.S. in Computer Science at Cornell University, 2007 B.S., M.S. in Computer Science and Engineering at The Pennsylvania State University, 2001 Courses Taught at Luddy B490 Image Processing and Recognition B551 Elements of Artificial Intelligence B554 Probabilistic approaches to Artificial Intelligence B657 Computer Vision I210 Information Infrastructure I I399 Undergraduate Research Methods for Informatics I427 Search Informatics Biography David Crandall received the Ph.D. in computer science from Cornell University in 2008 and the M.S. and B.S. degrees in computer science and engineering from the Pennsylvania State University, University Park, in 2001. He worked as a postdoctoral associate at Cornell from 2008-2010, and as a research scientist at Eastman Kodak Company from 2001-2003. Dr. Crandall’s main research interest is computer vision, the area of computer science that tries to design algorithms that can “see”. He is particularly interested in visual object recognition and scene understanding. He is also interested in other problems that involve analyzing and modeling large amounts of uncertain data, like mining data from the web and from online social networking sites. Take a look at Dr. Crandall's lab website . Research Areas Artificial Intelligence and Machine Learning Computer Vision, Speech, and Music Processing Centers Center for Complex Networks and Systems Research Center for Machine Learning Computer Vision Lab Digital Science Center Update your profile|2021-12-09 01:01:58.023351|2021-12-09 01:01:58.023352"
    doc = "IN THIS SECTION Research and Faculty Faculty Directory Faculty Directory Faculty Fellows Faculty Directory Russell Walker Clinical Associate Professor of Managerial Economics & Decision Sciences, Kellogg School of Management Contact 2145 Sheridan Road Tech Evanston, IL 60208-3109 Email Russell Walker Affiliations Master of Science in Analytics Program Education M.B.A., Northwestern University Ph.D., Engineering Systems, Cornell University M.S., Engineering Systems, Cornell University B.S., Civil Engineering Systems, University of South Florida Biography Russell Walker, Ph.D. is Clinical Professor at the Kellogg School of Management. Dr. Walker has expertise in Big Data and Analytics, Risk Management, and International Business Strategy. He has developed and taught leading executive programs and MBA classes on Big Data and Analytics, Strategic Data-Driven Marketing, Enterprise Risk, Operational Risk, and Global Leadership. Russell founded the Kellogg Executive Education program on Risk Management. He founded and teaches the very popular Analytical Consulting Lab and Risk Lab . He was awarded the Kellogg Impact award by his MBA students for excellence and impact in teaching. He is the author of From Big Data to Big Profits: Success with Data and Analytics (Oxford, 2015) that examines how firms can best monetize data assets. This book has been awarded a medal by the prestigious Axiom book awards for excellence in business technology, and has been recognized and featured by the Harvard Business Review and MIT Sloan Sports Analytics Conference. He was named one of most influential bloggers in Big Data and Analytics, globally. He also authored the award-winning text Winning with Risk Management (2013), which examines the principles and practice of risk management through business case studies. He authored the chapter Operational Risk in Insurance , as part of Risk Management in Financial Institutions (2013). He has been recognized as a top thought leader in Big Data and Analytics by many organizations, including the International Institute of Analytics, Onalytica, Teradata, SAS, KDNuggests and the Harvard Business Review. The Aspen Institute, Harvard Business School Press, The Bank of England, The World Bank, and PRMIA have recognized his cases for excellence in showcasing lessons in risk management. His International Business Strategy research includes a study of medical tourism opportunities for Turkey and an analysis for tourism transformation in Mexico for the Secretary of Tourism of Mexico. He leads the popular Global Lab class at Kellogg, an experiential class that brings Kellogg MBAs in touch with global opportunities. He frequently speaks on the emerging global middle class and demographic shifts driving changes in international markets. He has been invited to speak at the US Department of State, The World Bank, and the International Finance Corporation. He partners with the Cuba Study Group to identify initiatives to advance the success of Cuban entrepreneurs. He serves on the Scientific and Technical Council for the Menus of Change , an initiative by the Harvard School of Public Health and the Culinary Institute of America, to develop healthier and more environmentally sound food choices. He served as a board member of the Education and Technology Committee to the Morton Arboretum, and as a board member of the Virginia Hispanic Chamber of Commerce, where he developed support programs for Hispanic entrepreneurs and worked with US senators on US Latino matters. He has been invited to share his perspective internationally at Oxford University, IESE Business School in Spain, the Sasin Graduate Institute of Business Administration in Thailand, Amsterdam Institute of Finance, and the Indian School of Business. He has advised Microsoft, World Bank, Bank of England, SEC, US Department of State, CME Group, John Deere, IBM, Teradata, Discover Financial, Capital One Financial, PepsiCo, Raytheon, Northrop Grumman, Hyatt, among others. Russell began his career with Capital One Financial, as a corporate strategist specializing in the advancement of analytics in the enterprise for the purposes of improved marketing and risk management. He received his Ph.D. from Cornell University. He also holds an MS from Cornell University, an Executive MBA from the Kellogg School of Management and a BS from the University of South Florida. Russell speaks Spanish. He enjoys travel, photography, trees, and horticulture. Russell Walker can be reached at @RussWalker1492 & russellwalkerphd.com Selected Publications Books Walker, Russell. 2015. From Big Data to Big Profits: Success with Data and Analytics . New York, London: Oxford University Press. Walker, Russell . 2015. Menus of Change Annual Report. An Initiative of the Harvard School of Public Health and the Culinary Institute of America . Menus of Change.org . Walker, Russell. 2014. Menus of Change Annual Report. An Initiative of the Harvard School of Public Health and the Culinary Institute of America . Menus of Change. Walker, Russell . 2013. Menus of Change Annual Report: An initiative of the Harvard School of Public Health and the Culinary Institute of America . Walker, Russell. 2013. Winning with Risk Management . World Scientific Publishing Company. Articles Walker, Russell. 2016. Exporting Challenges and Opportunities for Cuban Entrepreneurs. Cuba Study Group . Walker, Russell. 2015. The Increasing Importance of Operational Risk in Enterprise Risk Management. The Journal of Enterprise Risk Management . 1(1) Walker, Russell. 2013. Winning with Risk Management: Focus on Operational Risk. European Financial Review . Walker, Russell. 2010. Role of Credit Rating Agencies as Risk Information Brokers. Prepared for the Anthony T. Cluff Fund and the Financial Services Roundtable, Presented to the US SEC and US Congress . Walker, Russell. 2006. Partnerships in Training. Interfaces . Professional Experience Associate Director of the Zell Center for Risk Research at Kellogg School of Management President at Walker Bernardo Consulting Director, Board of Directors at Virginia Hispanic Chamber of Commerce Senior Strategist at Capital One Financial, Inc. BACK TO TOP"
    doc = Document(doc,
                   faculty_url="http://www.cs.utah.edu/~mflatt/",
                   department_url="https://www.eecs.psu.edu/departments/cse-faculty-list.aspx",
                   university_url="https://utah.edu/")

    # department_url = "https://www.cs.utah.edu/",
    """print("NAME:       ", doc.extract_name())
    print("DEPARTMENT: ", doc.extract_department())    
    print("UNIVERSITY: ", doc.extract_university())
    print("PHONE:      ", doc.extract_phone())
    print("EMAIL:      ", doc.extract_email())
    print("EXPERTISE:  ", doc.extract_expertise())
    print("LOCATION:   ", doc.extract_location())
    print("BIODATA:    ", doc.extract_biodata())
    """