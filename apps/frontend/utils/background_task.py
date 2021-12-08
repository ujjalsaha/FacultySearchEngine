
import sys, os

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'apps'))


from apps.frontend.crawler.crawler import ExtractFacultyURL
from apps.frontend.crawler.faculty_url_scrapper import  ScrapeFacultyWebPage


def run_task(searchkey = None):
    print('came here ==> ', searchkey)
    if not searchkey:
        return None
    extract_url = ExtractFacultyURL(searchkey)
    if not extract_url.has_valid_faculty_link():
        return None
    else:
        faculty_dict = extract_url.get_faculty_link()
        scrape_page = ScrapeFacultyWebPage(faculty_dict=faculty_dict)
        scrape_page.get_faculty_urls()
        print('total faculty page found = ', len(scrape_page.faculty_urls))
    return None
