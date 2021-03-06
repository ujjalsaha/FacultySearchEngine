import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'apps'))
from apps.frontend.crawler.faculty_url_scrapper import ScrapeFacultyWebPage
from apps.frontend.crawler.crawler import ExtractFacultyURL
from apps.frontend.utils.beautiful_soup import close_driver

uni_list = [
    'Harvard University, computer science',
    'Stanford University, computer science',
    'Massachusetts Institute of Technology, computer science',
    'University of California Berkeley , computer science',
    'University of California, computer science',
    'Yale University, computer science',
    'Columbia University, computer science',
    'Princeton University, computer science',
    'New York University (NYU), computer science',
    'University of Pennsylvania, computer science',
    'University of Chicago, computer science',
    'Cornell University, computer science',
    'Duke University, computer science',
    'Johns Hopkins University, computer science',
    'University of Southern California, computer science',
    'Northwestern University, computer science',
    'Carnegie Mellon University, computer science',
    'University of Michigan, computer science',
    'Brown University, computer science',
    'Boston University, computer science',
    'California Institute of Technology, computer science',
    'Emory University, computer science',
    'Rice University, computer science',
    'University of Washington, computer science',
    'Washington University, computer science',
    'Georgetown University, computer science',
    'University of California, computer science',
    'Vanderbilt University, computer science',
    'University of Texas at Austin, computer science',
    'University of Illinois at Urbana-Champaign, computer science',
    'University of Rochester, computer science',
    'Dartmouth College , computer science',
    'University of North Carolina, computer science',
    'University of California, Davis (UCD), computer science',
    'University of Florida , computer science',
    'Tufts University , computer science',
    'University of Illinois, Chicago (UIC)  , computer science',
    'Georgia Institute of Technology (Georgia Tech) , computer science',
    'Stony Brook University , computer science',
    'University of Virginia, computer science',
    'Case Western Reserve University, computer science',
    'Rutgers - The State University of New Jersey, New Brunswick , computer science',
    'University of California, Santa Barbara (UCSB), computer science',
    'Pennsylvania State University, University Park, computer science',
    'George Washington University   , computer science',
    'University of California, Irvine (UCI), computer science',
    'University of Notre Dame   , computer science',
    'University of Miami, computer science',
    'Northeastern University , computer science',
    'Ohio State University, Columbus, computer science',
    'University at Buffalo SUNY  , computer science',
    'University of Maryland, College Park, computer science',
    'Purdue University     , computer science',
    'University of Minnesota, Twin Cities   , computer science',
    'Boston College        , computer science',
    'Michigan State University     , computer science',
    'University of Massachusetts, Amherst   , computer science',
    'University of Wisconsin-Madison , computer science',
    'Syracuse University, computer science',
    'Lehigh University, computer science',
    'University of Pittsburgh, computer science',
    'Arizona State University, Tempe , computer science',
    'Brandeis University  , computer science',
    'Temple University   , computer science',
    'Texas A&M University , computer science',
    'University of Arizona   , computer science',
    'University of Houston , computer science',
    'Binghamton University, SUNY   , computer science',
    'Drexel University     , computer science',
    'North Carolina State University , computer science',
    'Rensselaer Polytechnic Institute  , computer science',
    'University of Connecticut   , computer science',
    'University of Georgia  , computer science',
    'University of New Mexico , computer science',
    'Indiana University Bloomington , computer science',
    'Tulane University , computer science',
    'University of Colorado at Boulder , computer science',
    'Florida State University , computer science',
    'University of South Florida  , computer science',
    'Illinois Institute of Technology    , computer science',
    'University of California, Riverside (UCR)  , computer science',
    'University of California, Santa Cruz (UCSC)    , computer science',
    'Howard University     , computer science',
    'University of Texas Dallas      , computer science',
    'Santa Clara University, computer science',
    'Wake Forest University, computer science'
]
count = 0
for uni in uni_list:   
        extract_url = ExtractFacultyURL(uni)
        if extract_url.has_valid_faculty_link():
            try:
                faculty_dict = extract_url.get_faculty_link()
                scrape_page = ScrapeFacultyWebPage(faculty_dict=faculty_dict)
                scrape_page.get_faculty_urls()
                print('total faculty page found = ', len(scrape_page.faculty_urls))
            except:
                print('Ignoring university = ', uni)

close_driver()