import logging

from rank_bm25 import BM25Okapi


class Ranker:

    def __init__(self, corpus: list):
        """
        Ranker class to do ranking of docs on Corpus
        :param corpus:
        """
        self.corpus = corpus
        self.logger = logging.getLogger('my_module_name').setLevel(logging.WARNING)

    def score(self,  query: str, n: int = 10):
        """
        Ranks list of string (docs) based on the query string using BM25 algorithm.
        :param query: the query string aginst which the scoring will be done
        :param n: no of documents to return based on the ranking
        :return: Returns a list of ids that are ranked as per the bm25 logic.
        """
        if not self.corpus or not query or n < 1:
            self.logger.error(f"Invalid Corpus or query or search result count")
            self.logger.error(f"Corpus doc Count: {len(self.corpus)}")
            self.logger.error(f"Query String: {query}")
            self.logger.error(f"Number of results requested: {n}")
            return ""

        results = []
        try:
            tokenized_corpus = [doc.split(" ") for doc in self.corpus]
            tokenized_query = query.split(" ")

            results = BM25Okapi(tokenized_corpus).get_top_n(tokenized_query, corpus, n=n)
            results = [int(result.split()[0]) for result in results] if results else []

        except Exception as e:
            print(f"Unexpected exception encountered: {e}")
            return []

        return results

if __name__ == '__main__':
    from pprint import pprint

    corpus = [
        " 1 Geoffrey Werner Challen Teaching Associate Professor 2227 Siebel Center for Comp Sci 201 N. Goodwin Ave. Urbana Illinois 61801 (217) 300-6150 challen@illinois.edu : Primary Research Area CS Education Research Areas CS Education For more information blue Systems Research Group (Defunct) Internet Class: Learn About the Internet on the Internet OPS Class: Learn Operating Systems Online CS 125 Home Page Education Ph.D. Computer Science, Harvard University, 2010 AB Physics, Harvard University, 2003 Academic Positions Associate Teaching Professor, University of Illinois, 2017 . Primary Research Area CS Education Research Areas CS Education For more information blue Systems Research Group (Defunct) Internet Class: Learn About the Internet on the Internet OPS Class: Learn Operating Systems Online CS 125 Home Page . . For more information blue Systems Research Group (Defunct) Internet Class: Learn About the Internet on the Internet OPS Class: Learn Operating Systems Online CS 125 Home Page.",
        " 2 Cheng Zhai Knowledge and information management tools and techniques should be connected to project processes and process owners. Communities of practice and subject matter experts (SMEs), for example, may generate insights that lead to improved control processes; having an internal sponsor can ensure improvements are implemented. Lessons learned register entries may be analyzed to identify common issues that can be addressed by changes to project procedures.",
        " 3 Tools and techniques that connect people to information can be enhanced by adding an element of interaction, for example, include a “contact me” function so users can get in touch with the originators of the lessons and ask for advice specific to their project and context. Interaction and support also helps people find relevant information. Asking for help is generally quicker and easier than trying to identify search terms. Search terms are often difficult to select because people may not know which keywords or key phrases to use to access the information they need.",
        " 4 A deliverable is any unique and verifiable product, result, or capability to perform a service that is required to be produced to complete a process, phase, or project. Deliverables are typically tangible components completed to meet the project objectives and can include components of the project management plan.",
        " 5 Manage Project Knowledge is the process of using existing knowledge and creating new knowledge to achieve the project's objectives and contribute to organizational learning. The key benefits of this process are that prior organizational knowledge is leveraged to produce or improve the project outcomes, and knowledge created by the project is available to support organizational operations and future projects or phases. This process is performed throughout the project. The inputs, tools and techniques, and outputs of the process are depicted in Figure 4-8. Figure 4-9 depicts the data flow diagram for the process.",
        " 6 High-level strategic and operational assumptions and constraints are normally identified in the business case before the project is initiated and will flow into the project charter. Lower-level activity and task assumptions are generated throughout the project such as defining technical specifications, estimates, the schedule, risks, etc. The assumption log is used to record all assumptions and constraints throughout the project life cycle.",
        " 7 The project charter is the document issued by the project initiator or sponsor that formally authorizes the existence of a project and provides the project manager with the authority to apply organizational resources to project activities. It documents the high-level information on the project and on the product, service, or result the project is intended to satisfy, such as."
    ]

    ranker = Ranker(corpus)
    query = "Geoffrey Werner Challen"
    results = ranker.score(query, 2)
    print(f" Result for query 0 '{query}'")
    pprint(results)

    print("\n")

    query = "Cheng Zhai Knowledge"
    results = ranker.score(query, 4)
    print(f" Result for query 1 '{query}'")
    pprint(results)

    print("\n")

    query = "are document"
    results = ranker.score(query, 4)
    print(f" Result for query 2 '{query}'")
    pprint(results)

    print("\n")

    query = "walmart costco"
    results = ranker.score(query, 4)
    print(f" Result for query 3 '{query}'")
    pprint(results)

    print("\n")

    query = "sdfkjghn sjfdkgn fds;jg ;osfdghjish955 "
    results = ranker.score(query, 4)
    print(f" Result for query 4 '{query}'")
    pprint(results)



