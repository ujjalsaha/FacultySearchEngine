"""

import elasticsearch
print (elasticsearch.VERSION)

from elasticsearch import Elasticsearch

query_body = {
  "query": {
      "match": {
          "some_field": "search_for_this"
      }
  }
}

elastic_client = Elasticsearch(hosts=["localhost"])
# elastic_client.search(index="some_index", body=query_body)
result = elastic_client.search(
    index="some_index",
    body={
        "query": {
            "match_all": {}
        }
    }
)

result = elastic_client.search(index="some_index", body={"query": {"match_all": {}}})

print ("total hits:", len(result["hits"]["hits"]))



import logging
def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es
"""
"""
corpus=[]
db = {}
db["id"] = 1
db['faculty_name'] = "Matt Blaze"
db['faculty_homepage_urldb'] = 'https://www.mattblaze.org/'
db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
db["faculty_department_name"] =  "Department of Computer Science"
db["faculty_university_url"] = "https://www.georgetown.edu"
db["faculty_university_name"] =  "Georgetown University in Washington DC"
db["faculty_location"] = "Washington, District of Columbia, United States"
db["faculty_expertise"] =  "georgetown computer law mcdevitt paper professor research science university"
corpus.append(db)
db = {}
db["id"] = 2
db["faculty_name"] = "Philip Buffum"
db["faculty_homepage_url"] = "http://explore.georgetown.edu/people/pb925"
db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
db["faculty_department_name"] =  "Department of Computer Science"
db["faculty_university_url"] = "https://www.georgetown.edu"
db["faculty_university_name"] =  "Georgetown University in Washington DC"
db["faculty_location"] = "Washington, District of Columbia, United States"
db["faculty_expertise"] =  "expire session close georgetown log refresh privacy show modal policy"
corpus.append(db)
db = {}

db["id"] = 3
db["faculty_name"] = "Eric Burger"
db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/~eburger/"
db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
db["faculty_department_name"] =  "Department of Computer Science"
db["faculty_university_url"] = "https://www.georgetown.edu"
db["faculty_university_name"] =  "Georgetown University in Washington DC"
db["faculty_location"] = "Washington, District of Columbia, United States"
db["faculty_expertise"] =  "research science information publication policy work communication engineer georgetown free"
corpus.append(db)
db = {}

db["id"] = 4
db["faculty_name"] = "Ray Essick"
db["faculty_homepage_url"] = "http://explore.georgetown.edu/people/re268"
db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
db["faculty_department_name"] =  "Department of Computer Science"
db["faculty_university_url"] = "https://www.georgetown.edu"
db["faculty_university_name"] =  "Georgetown University in Washington DC"
db["faculty_location"] = "Washington, District of Columbia, United States"
db["faculty_expertise"] =  "expire session close loading log georgetown refresh show navigation policy"
corpus.append(db)
db = {}

db["id"] = 5
db["faculty_name"] = "Jeremy Fineman"
db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/~jfineman/"
db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
db["faculty_department_name"] =  "Department of Computer Science"
db["faculty_university_url"] = "https://www.georgetown.edu"
db["faculty_university_name"] =  "Georgetown University in Washington DC"
db["faculty_location"] = "Washington, District of Columbia, United States"
db["faculty_expertise"] =  "interest algorithm science receive datum research computer postdoctoral memory primarily"
corpus.append(db)
db = {}

db["id"] = 6
db["faculty_name"] = "Ophir Frieder"
db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/~ophir/"
db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
db["faculty_department_name"] =  "Department of Computer Science"
db["faculty_university_url"] = "https://www.georgetown.edu"
db["faculty_university_name"] =  "Georgetown University in Washington DC"
db["faculty_location"] = "Washington, District of Columbia, United States"
db["faculty_expertise"] =  "science information award georgetown computer faculty scalable medical ieee technology"
corpus.append(db)
db = {}

db["id"] = 7
db["faculty_name"] = "Nazli Goharian"
db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/~nazli/"
db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
db["faculty_department_name"] =  "Department of Computer Science"
db["faculty_university_url"] = "https://www.georgetown.edu"
db["faculty_university_name"] =  "Georgetown University in Washington DC"
db["faculty_location"] = "Washington, District of Columbia, United States"
db["faculty_expertise"] =  "student doctoral information science graduate award research computer chair join"
corpus.append(db)
db = {}

db["id"] = 8
db["faculty_name"] = "Sasha Golovnev"
db["faculty_homepage_url"] = "https://golovnev.org/"
db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
db["faculty_department_name"] =  "Department of Computer Science"
db["faculty_university_url"] = "https://www.georgetown.edu"
db["faculty_university_name"] =  "Georgetown University in Washington DC"
db["faculty_location"] = "Washington, District of Columbia, United States"
db["faculty_expertise"] =  "pdf bound low problem science computer circuit algorithm preprint complexity"
corpus.append(db)
db = {}

db["id"] = 9
db["faculty_name"] = "Bala Kalyanasundaram"
db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/~kalyan/"
db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
db["faculty_department_name"] =  "Department of Computer Science"
db["faculty_university_url"] = "https://www.georgetown.edu"
db["faculty_university_name"] =  "Georgetown University in Washington DC"
db["faculty_location"] = "Washington, District of Columbia, United States"
db["faculty_expertise"] =  "complexity science research old communication crave vita computer part personal"
corpus.append(db)
db = {}

db["id"] = 10
db["faculty_name"] = "Mark Maloof"
db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/~maloof/"
db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
db["faculty_department_name"] =  "Department of Computer Science"
db["faculty_university_url"] = "https://www.georgetown.edu"
db["faculty_university_name"] =  "Georgetown University in Washington DC"
db["faculty_location"] = "Washington, District of Columbia, United States"
db["faculty_expertise"] =  "computer science cosc program teach georgetown security machine talk learn"
corpus.append(db)
db = {}

db["id"] = 11
db["faculty_name"] = "Jami Montgomery"
db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/~jxm/Me.html"
db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
db["faculty_department_name"] =  "Department of Computer Science"
db["faculty_university_url"] = "https://www.georgetown.edu"
db["faculty_university_name"] =  "Georgetown University in Washington DC"
db["faculty_location"] = "Washington, District of Columbia, United States"
db["faculty_expertise"] =  "interest system research graphic include student network current computer project"
corpus.append(db)
db = {}

db["id"] = 12
db["faculty_name"] = "Calvin Newport"
db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/~cnewport/"
db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
db["faculty_department_name"] =  "Department of Computer Science"
db["faculty_university_url"] = "https://www.georgetown.edu"
db["faculty_university_name"] =  "Georgetown University in Washington DC"
db["faculty_location"] = "Washington, District of Columbia, United States"
db["faculty_expertise"] =  "course teach web site access cosc theory algorithm spring distribute"
corpus.append(db)
db = {}

db["id"] = 13
db["faculty_name"] = "Kobbi Nissim"
db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/~kobbi/"
db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
db["faculty_department_name"] =  "Department of Computer Science"
db["faculty_university_url"] = "https://www.georgetown.edu"
db["faculty_university_name"] =  "Georgetown University in Washington DC"
db["faculty_location"] = "Washington, District of Columbia, United States"
db["faculty_expertise"] =  "privacy datum work theory see computer science award differential cryptography"
corpus.append(db)
db = {}

db["id"] = 14
db["faculty_name"] = "Nathan Schneider"
db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/nschneid/"
db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
db["faculty_department_name"] =  "Department of Computer Science"
db["faculty_university_url"] = "https://www.georgetown.edu"
db["faculty_university_name"] =  "Georgetown University in Washington DC"
db["faculty_email"] =  "schneider@georgetown.edu"
db["faculty_phone"] =  "(202) 687-0975"
db["faculty_location"] = "Washington, District of Columbia, United States"
db["faculty_expertise"] =  "talk university chair linguistic research law program georgetown highlight computational"
corpus.append(db)
db = {}

db["id"] = 15
db["faculty_name"] = "Micah Sherr"
db["faculty_homepage_url"] = "https://seclab.cs.georgetown.edu/msherr/"
db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
db["faculty_department_name"] =  "Department of Computer Science"
db["faculty_university_url"] = "https://www.georgetown.edu"
db["faculty_university_name"] =  "Georgetown University in Washington DC"
db["faculty_location"] = "Washington, District of Columbia, United States"
db["faculty_expertise"] =  "security computer interest georgetown room academic dot system network available"
corpus.append(db)
db = {}

db["id"] = 16
db["faculty_name"] = "Lisa Singh"
db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/~singh/"
db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
db["faculty_department_name"] =  "Department of Computer Science"
db["faculty_university_url"] = "https://www.georgetown.edu"
db["faculty_university_name"] =  "Georgetown University in Washington DC"
db["faculty_email"] =  "singh@cs.georgetown.edu"
db["faculty_phone"] =  "202-687-9253"
db["faculty_location"] = "Washington, District of Columbia, United States"
db["faculty_expertise"] =  "datum social download science big meeting research report conference woman"
corpus.append(db)
db = {}

db["id"] = 17
db["faculty_name"] = "Richard Squier"
db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/~squier/"
db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
db["faculty_department_name"] =  "Department of Computer Science"
db["faculty_university_url"] = "https://www.georgetown.edu"
db["faculty_university_name"] =  "Georgetown University in Washington DC"
db["faculty_location"] = "Washington, District of Columbia, United States"
db["faculty_expertise"] =  "georgetown computer dept dot fax publication science squier teach university"
corpus.append(db)
db = {}

db["id"] = 18
db["faculty_name"] = "Justin Thaler"
db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/jthaler/"
db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
db["faculty_department_name"] =  "Department of Computer Science"
db["faculty_university_url"] = "https://www.georgetown.edu"
db["faculty_university_name"] =  "Georgetown University in Washington DC"
db["faculty_location"] = "Washington, District of Columbia, United States"
db["faculty_expertise"] =  "degree approximate function problem polynomial result algorithm complexity abstract omega"
corpus.append(db)
db = {}

db["id"] = 19
db["faculty_name"] = "Benjamin Ujcich"
db["faculty_homepage_url"] = "https://benujcich.georgetown.domains/"
db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
db["faculty_department_name"] =  "Department of Computer Science"
db["faculty_university_url"] = "https://www.georgetown.edu"
db["faculty_university_name"] =  "Georgetown University in Washington DC"
db["faculty_location"] = "Washington, District of Columbia, United States"
db["faculty_expertise"] =  "network computer interested research datum department security information secure system"
corpus.append(db)
db = {}

db["id"] = 20
db["faculty_name"] = "Nitin Vaidya"
db["faculty_homepage_url"] = "https://disc.georgetown.domains/"
db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
db["faculty_department_name"] =  "Department of Computer Science"
db["faculty_university_url"] = "https://www.georgetown.edu"
db["faculty_university_name"] =  "Georgetown University in Washington DC"
db["faculty_location"] = "Washington, District of Columbia, United States"
db["faculty_expertise"] =  "distribute algorithm science research consistency acm computer include memory computing"
corpus.append(db)
db = {}

db["id"] = 21
db["faculty_name"] = "Mahe Velauthapillai"
db["faculty_homepage_url"] = "http://usha.georgetown.edu/mahe/"
db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
db["faculty_department_name"] =  "Department of Computer Science"
db["faculty_university_url"] = "https://www.georgetown.edu"
db["faculty_university_name"] =  "Georgetown University in Washington DC"
db["faculty_location"] = "Washington, District of Columbia, United States"
db["faculty_expertise"] =  "georgetown personal language technology teach reiss programming phone address information"
corpus.append(db)
db = {}

db["id"] = 22
db["faculty_name"] = "Addison Woods"
db["faculty_homepage_url"] = "https://cs.georgetown.edu/~addison"
db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
db["faculty_department_name"] =  "Department of Computer Science"
db["faculty_university_url"] = "https://www.georgetown.edu"
db["faculty_university_name"] =  "Georgetown University in Washington DC"
db["faculty_location"] = "Washington, District of Columbia, United States"
db["faculty_expertise"] =  "teach teaching contact assistant home professor publication technology computer link"
corpus.append(db)

from pprint import pprint
pprint(corpus)
"""

from elasticsearch import Elasticsearch
from pprint import pprint


class ElasticSearchAPI:
    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        self.index = "faculty_index"
        self.doc_type = 'faculty'

    def add_records(self, corpus: list):

        try:
            print("Deleting old index...")
            #iterate through documents indexing them
            self.es.indices.delete(index=self.index)
            print("Old Index deleted: ", len(corpus))

        except Exception as e:
            print("Unexpected Exception occured in delete index: ", repr(e))
            pass

        print("Corpus: ", len(corpus))
        try:
            print(f"Rebuilding new index with {len(corpus)} records in corpus")
            for record in corpus:
                # print (record)
                self.es.index(index=self.index, doc_type=self.doc_type, id=record["id"], document=record)

            result = self.es.search(index=self.index, body={"query": {"match_all": {}}})
            print(f"New Index Created with record count {len(result['hits']['hits'])}")

        except Exception as e:
            print ("Unexpected Exception occured in create index: ", repr(e))

        print(f"Indexing complete: with {len(corpus)} records")

        return

    def get_search_results(self, query, n=10, university_filter=None, department_filter=None, location_filter=None):
        university_filter = university_filter if university_filter else ""
        department_filter = department_filter if department_filter else ""
        location_filter = location_filter if location_filter else ""

        query = {
            "multi_match": {
              "query":  f"{query} {university_filter} {department_filter} {location_filter}".strip(),
              "fields": ["faculty_biodata", "faculty_name", "faculty_university_name", "faculty_department_name", "faculty_location"]
            }
        }
        """
        else:
            query = {
                "multi_match": {
                  "query":  query,
                  "fields": ["faculty_biodata", "faculty_name"]
                },
                "filter": {
                    "term": {
                        "faculty_university_name": university_filter,
                        ""
                    }
                }
            }
        """
        ranked_list =  []
        try:
            # result = self.es.search(index=self.index, body={"query": {"match_all": {}}})
            # print("total hits:", len(result["hits"]["hits"]))
            # pprint(result)
            res = self.es.search(index=self.index, query=query)
            # print(res)

            # print(f"Matched Query: {res['hits']['total']['value']}")
            for record in res['hits']['hits'][:n]:
                faculty = {}
                faculty["faculty_name"] = record['_source']["faculty_name"]
                faculty["faculty_homepage_url"] = record['_source']["faculty_homepage_url"]
                faculty["faculty_department_url"] = record['_source']["faculty_department_url"]
                faculty["faculty_department_name"] = record['_source']["faculty_department_name"]
                faculty["faculty_university_url"] = record['_source']["faculty_university_url"]
                faculty["faculty_university_name"] = record['_source']["faculty_university_name"]
                faculty["faculty_email"] = record['_source']["faculty_email"]
                faculty["faculty_phone"] = record['_source']["faculty_phone"]
                faculty["faculty_location"] = record['_source']["faculty_location"]
                faculty["faculty_expertise"] = record['_source']["faculty_expertise"]
                ranked_list.append(faculty)

            # pprint(ranked_list)

        except Exception as e :
            print ("Unexpected exception error: While getting search results: ", repr(e))

        return ranked_list


if __name__ == '__main__':
    from pprint import pprint

    corpus = []
    db = {}
    db["id"] = 1
    db['faculty_name'] = "Matt Blaze"
    db['faculty_homepage_urldb'] = 'https://www.mattblaze.org/'
    db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
    db["faculty_department_name"] = "Department of Computer Science"
    db["faculty_university_url"] = "https://www.georgetown.edu"
    db["faculty_university_name"] = "Georgetown University in Washington DC"
    db["faculty_location"] = "Washington, District of Columbia, United States"
    db["faculty_expertise"] = "georgetown computer law mcdevitt paper professor research science university"
    corpus.append(db)
    db = {}
    db["id"] = 2
    db["faculty_name"] = "Philip Buffum"
    db["faculty_homepage_url"] = "http://explore.georgetown.edu/people/pb925"
    db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
    db["faculty_department_name"] = "Department of Computer Science"
    db["faculty_university_url"] = "https://www.georgetown.edu"
    db["faculty_university_name"] = "Georgetown University in Washington DC"
    db["faculty_location"] = "Washington, District of Columbia, United States"
    db["faculty_expertise"] = "expire session close georgetown log refresh privacy show modal policy"
    corpus.append(db)
    db = {}

    db["id"] = 3
    db["faculty_name"] = "Eric Burger"
    db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/~eburger/"
    db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
    db["faculty_department_name"] = "Department of Computer Science"
    db["faculty_university_url"] = "https://www.georgetown.edu"
    db["faculty_university_name"] = "Georgetown University in Washington DC"
    db["faculty_location"] = "Washington, District of Columbia, United States"
    db[
        "faculty_expertise"] = "research science information publication policy work communication engineer georgetown free"
    corpus.append(db)
    db = {}

    db["id"] = 4
    db["faculty_name"] = "Ray Essick"
    db["faculty_homepage_url"] = "http://explore.georgetown.edu/people/re268"
    db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
    db["faculty_department_name"] = "Department of Computer Science"
    db["faculty_university_url"] = "https://www.georgetown.edu"
    db["faculty_university_name"] = "Georgetown University in Washington DC"
    db["faculty_location"] = "Washington, District of Columbia, United States"
    db["faculty_expertise"] = "expire session close loading log georgetown refresh show navigation policy"
    corpus.append(db)
    db = {}

    db["id"] = 5
    db["faculty_name"] = "Jeremy Fineman"
    db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/~jfineman/"
    db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
    db["faculty_department_name"] = "Department of Computer Science"
    db["faculty_university_url"] = "https://www.georgetown.edu"
    db["faculty_university_name"] = "Georgetown University in Washington DC"
    db["faculty_location"] = "Washington, District of Columbia, United States"
    db["faculty_expertise"] = "interest algorithm science receive datum research computer postdoctoral memory primarily"
    corpus.append(db)
    db = {}

    db["id"] = 6
    db["faculty_name"] = "Ophir Frieder"
    db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/~ophir/"
    db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
    db["faculty_department_name"] = "Department of Computer Science"
    db["faculty_university_url"] = "https://www.georgetown.edu"
    db["faculty_university_name"] = "Georgetown University in Washington DC"
    db["faculty_location"] = "Washington, District of Columbia, United States"
    db["faculty_expertise"] = "science information award georgetown computer faculty scalable medical ieee technology"
    corpus.append(db)
    db = {}

    db["id"] = 7
    db["faculty_name"] = "Nazli Goharian"
    db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/~nazli/"
    db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
    db["faculty_department_name"] = "Department of Computer Science"
    db["faculty_university_url"] = "https://www.georgetown.edu"
    db["faculty_university_name"] = "Georgetown University in Washington DC"
    db["faculty_location"] = "Washington, District of Columbia, United States"
    db["faculty_expertise"] = "student doctoral information science graduate award research computer chair join"
    corpus.append(db)
    db = {}

    db["id"] = 8
    db["faculty_name"] = "Sasha Golovnev"
    db["faculty_homepage_url"] = "https://golovnev.org/"
    db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
    db["faculty_department_name"] = "Department of Computer Science"
    db["faculty_university_url"] = "https://www.georgetown.edu"
    db["faculty_university_name"] = "Georgetown University in Washington DC"
    db["faculty_location"] = "Washington, District of Columbia, United States"
    db["faculty_expertise"] = "pdf bound low problem science computer circuit algorithm preprint complexity"
    corpus.append(db)
    db = {}

    db["id"] = 9
    db["faculty_name"] = "Bala Kalyanasundaram"
    db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/~kalyan/"
    db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
    db["faculty_department_name"] = "Department of Computer Science"
    db["faculty_university_url"] = "https://www.georgetown.edu"
    db["faculty_university_name"] = "Georgetown University in Washington DC"
    db["faculty_location"] = "Washington, District of Columbia, United States"
    db["faculty_expertise"] = "complexity science research old communication crave vita computer part personal"
    corpus.append(db)
    db = {}

    db["id"] = 10
    db["faculty_name"] = "Mark Maloof"
    db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/~maloof/"
    db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
    db["faculty_department_name"] = "Department of Computer Science"
    db["faculty_university_url"] = "https://www.georgetown.edu"
    db["faculty_university_name"] = "Georgetown University in Washington DC"
    db["faculty_location"] = "Washington, District of Columbia, United States"
    db["faculty_expertise"] = "computer science cosc program teach georgetown security machine talk learn"
    corpus.append(db)
    db = {}

    db["id"] = 11
    db["faculty_name"] = "Jami Montgomery"
    db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/~jxm/Me.html"
    db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
    db["faculty_department_name"] = "Department of Computer Science"
    db["faculty_university_url"] = "https://www.georgetown.edu"
    db["faculty_university_name"] = "Georgetown University in Washington DC"
    db["faculty_location"] = "Washington, District of Columbia, United States"
    db["faculty_expertise"] = "interest system research graphic include student network current computer project"
    corpus.append(db)
    db = {}

    db["id"] = 12
    db["faculty_name"] = "Calvin Newport"
    db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/~cnewport/"
    db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
    db["faculty_department_name"] = "Department of Computer Science"
    db["faculty_university_url"] = "https://www.georgetown.edu"
    db["faculty_university_name"] = "Georgetown University in Washington DC"
    db["faculty_location"] = "Washington, District of Columbia, United States"
    db["faculty_expertise"] = "course teach web site access cosc theory algorithm spring distribute"
    corpus.append(db)
    db = {}

    db["id"] = 13
    db["faculty_name"] = "Kobbi Nissim"
    db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/~kobbi/"
    db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
    db["faculty_department_name"] = "Department of Computer Science"
    db["faculty_university_url"] = "https://www.georgetown.edu"
    db["faculty_university_name"] = "Georgetown University in Washington DC"
    db["faculty_location"] = "Washington, District of Columbia, United States"
    db["faculty_expertise"] = "privacy datum work theory see computer science award differential cryptography"
    corpus.append(db)
    db = {}

    db["id"] = 14
    db["faculty_name"] = "Nathan Schneider"
    db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/nschneid/"
    db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
    db["faculty_department_name"] = "Department of Computer Science"
    db["faculty_university_url"] = "https://www.georgetown.edu"
    db["faculty_university_name"] = "Georgetown University in Washington DC"
    db["faculty_email"] = "schneider@georgetown.edu"
    db["faculty_phone"] = "(202) 687-0975"
    db["faculty_location"] = "Washington, District of Columbia, United States"
    db["faculty_expertise"] = "talk university chair linguistic research law program georgetown highlight computational"
    corpus.append(db)
    db = {}

    db["id"] = 15
    db["faculty_name"] = "Micah Sherr"
    db["faculty_homepage_url"] = "https://seclab.cs.georgetown.edu/msherr/"
    db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
    db["faculty_department_name"] = "Department of Computer Science"
    db["faculty_university_url"] = "https://www.georgetown.edu"
    db["faculty_university_name"] = "Georgetown University in Washington DC"
    db["faculty_location"] = "Washington, District of Columbia, United States"
    db["faculty_expertise"] = "security computer interest georgetown room academic dot system network available"
    corpus.append(db)
    db = {}

    db["id"] = 16
    db["faculty_name"] = "Lisa Singh"
    db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/~singh/"
    db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
    db["faculty_department_name"] = "Department of Computer Science"
    db["faculty_university_url"] = "https://www.georgetown.edu"
    db["faculty_university_name"] = "Georgetown University in Washington DC"
    db["faculty_email"] = "singh@cs.georgetown.edu"
    db["faculty_phone"] = "202-687-9253"
    db["faculty_location"] = "Washington, District of Columbia, United States"
    db["faculty_expertise"] = "datum social download science big meeting research report conference woman"
    corpus.append(db)
    db = {}

    db["id"] = 17
    db["faculty_name"] = "Richard Squier"
    db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/~squier/"
    db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
    db["faculty_department_name"] = "Department of Computer Science"
    db["faculty_university_url"] = "https://www.georgetown.edu"
    db["faculty_university_name"] = "Georgetown University in Washington DC"
    db["faculty_location"] = "Washington, District of Columbia, United States"
    db["faculty_expertise"] = "georgetown computer dept dot fax publication science squier teach university"
    corpus.append(db)
    db = {}

    db["id"] = 18
    db["faculty_name"] = "Justin Thaler"
    db["faculty_homepage_url"] = "https://people.cs.georgetown.edu/jthaler/"
    db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
    db["faculty_department_name"] = "Department of Computer Science"
    db["faculty_university_url"] = "https://www.georgetown.edu"
    db["faculty_university_name"] = "Georgetown University in Washington DC"
    db["faculty_location"] = "Washington, District of Columbia, United States"
    db[
        "faculty_expertise"] = "degree approximate function problem polynomial result algorithm complexity abstract omega"
    corpus.append(db)
    db = {}

    db["id"] = 19
    db["faculty_name"] = "Benjamin Ujcich"
    db["faculty_homepage_url"] = "https://benujcich.georgetown.domains/"
    db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
    db["faculty_department_name"] = "Department of Computer Science"
    db["faculty_university_url"] = "https://www.georgetown.edu"
    db["faculty_university_name"] = "Georgetown University in Washington DC"
    db["faculty_location"] = "Washington, District of Columbia, United States"
    db["faculty_expertise"] = "network computer interested research datum department security information secure system"
    corpus.append(db)
    db = {}

    db["id"] = 20
    db["faculty_name"] = "Nitin Vaidya"
    db["faculty_homepage_url"] = "https://disc.georgetown.domains/"
    db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
    db["faculty_department_name"] = "Department of Computer Science"
    db["faculty_university_url"] = "https://www.georgetown.edu"
    db["faculty_university_name"] = "Georgetown University in Washington DC"
    db["faculty_location"] = "Washington, District of Columbia, United States"
    db["faculty_expertise"] = "distribute algorithm science research consistency acm computer include memory computing computer"
    corpus.append(db)
    db = {}

    db["id"] = 21
    db["faculty_name"] = "Mahe Velauthapillai"
    db["faculty_homepage_url"] = "http://usha.georgetown.edu/mahe/"
    db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
    db["faculty_department_name"] = "Department of Computer Science"
    db["faculty_university_url"] = "https://www.georgetown.edu"
    db["faculty_university_name"] = "Georgetown University in Washington DC"
    db["faculty_location"] = "Washington, District of Columbia, United States"
    db[
        "faculty_expertise"] = "georgetown personal language technology teach reiss programming phone address information"
    corpus.append(db)
    db = {}

    db["id"] = 22
    db["faculty_name"] = "Addison Woods"
    db["faculty_homepage_url"] = "https://cs.georgetown.edu/~addison"
    db[" faculty_department_url"] = "http://www.cs.georgetown.edu"
    db["faculty_department_name"] = "Department of Computer Science"
    db["faculty_university_url"] = "https://www.georgetown.edu"
    db["faculty_university_name"] = "Georgetown University in Washington DC"
    db["faculty_location"] = "Washington, District of Columbia, United States"
    db["faculty_expertise"] = "teach teaching contact assistant home professor publication technology computer link"
    corpus.append(db)

    elasticsearchapi = ElasticSearchAPI()
    # elasticsearchapi.add_records(corpus)
    elasticsearchapi.get_search_results("Walmart")






