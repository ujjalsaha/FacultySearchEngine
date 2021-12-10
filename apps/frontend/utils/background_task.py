import sys, os

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'apps'))
from apps.frontend.crawler.faculty_url_scrapper import ScrapeFacultyWebPage


def run_task(faculty_dict=None):
    if not faculty_dict:
        return None
    else:
        scrape_page = ScrapeFacultyWebPage(faculty_dict=faculty_dict)
        scrape_page.get_faculty_urls()
        scrape_page.close_driver()
        print('total faculty page found = ', len(scrape_page.faculty_urls))
    return None
