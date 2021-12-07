from apps.backend.utils.facultydb import FacultyDB
from apps.backend.utils.ranker import Ranker
class search:
    def __init__(self):
        print("Initialize")

    def dosearch(self, university_filter, location_filter):
        print("Corpus Method")
        faculty = FacultyDB()
        list = faculty.get_biodata_records(university_filter, location_filter)
        print(list)

        ranker = Ranker(list)
        rankedlist = ranker.score("ANOOP BN", 10)
        print(rankedlist)

if __name__ == '__main__':
    print("Main")
    search = search()
    search.dosearch("Manipal","Sikkim")
