from apps.backend.utils.facultydb import FacultyDB
from apps.backend.utils.ranker import Ranker
class Search:
    def __init__(self):
        pass


    def get_search_results(self, query, num_of_results, university_filter, dept_filter, location_filter):
        try:
            # print("Corpus Method")
            corpus = FacultyDB().get_biodata_records(university_filter, dept_filter, location_filter)
            #print(corpus)

            ranked_id_list = Ranker(corpus).score(query, num_of_results)
            #print(ranked_id_list)

            search_results_list  = FacultyDB().get_faculty_records(ranked_id_list)
            print(search_results_list )

            return search_results_list

        except Exception as e:
            print(f"Unexpected exception encountered: {e}")
            return []

if __name__ == '__main__':
    # print("Main")
    search = Search()
    search.get_search_results("ANOOP BN","Manipal","Sikkim")