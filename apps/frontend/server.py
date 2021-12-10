from flask import Flask
from flask import render_template, request, jsonify
import json
import os
import requests
import base64
import sys
import re

from redis import Redis
import redis
import rq

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'apps'))

from apps.backend.utils.facultydb import FacultyDB
from apps.backend.api.search import Search

from apps.frontend.crawler.crawler import ExtractFacultyURL


from apps.frontend.utils.background_task import run_task

app = Flask(__name__, template_folder='web/templates', static_folder='web/static')
app.rootpath = "web/templates"
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'web/templates'))

faculty = FacultyDB()
uni_list = faculty.get_all_universities()
loc_list = faculty.get_all_locations()
dept_list = faculty.get_all_departments()

@app.route('/')
def home():
    return render_template("index.html", unis = uni_list, locs = loc_list, deps = dept_list)

@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route("/admin/crawl", methods=['POST'])
def doCrawl():
    redis_server = Redis(host='localhost', port=6379, db=0)
    data = json.loads(request.data.decode("utf-8"))
    search_str = data["searchText"]
    try:
        extract_url = ExtractFacultyURL(search_str)
        if not extract_url.has_valid_faculty_link():
            extract_url.close_driver()
            return jsonify({
                "msg": "Unfortunately we did not find any faculty link for the search key. "
                       "Please provide a search key which has a link to the list of department faculty."
            })
        elif is_redis_available(redis_server):
            extract_url.close_driver()
            queue = rq.Queue('crawler-worker', connection=redis_server, default_timeout=3600)
            faculty_dict = extract_url.get_faculty_link()
            queue.enqueue(run_task, faculty_dict)
            return jsonify({
                "msg": "Your request has been accepted. We will process the request asynchronously"
            })
        else:
            extract_url.close_driver()
            return jsonify(
                {
                    "msg": "An error occurred. Please contact system administrators for more details."
                }
            )
    except:
        return jsonify(
            {
                "msg": "Unexpected error occurred. Please contact system administrators for more details."
            }
        )

@app.route('/search', methods=['POST'])
def search():
    data = json.loads(request.data.decode("utf-8"))
    querytext = data['query']
    locfilter = data['selected_loc_filters']
    unifilter = data['selected_uni_filters']
    deptfilter = data["selected_dept_filters"]
    num_results = data['num_results']

    if num_results >100:
        num_of_results = 100
    search_obj = Search()
    #search_result = search_obj.get_search_results(querytext, "Manipal", "Computer", "Sikkim")
    search_result = search_obj.get_search_results(querytext, num_results, unifilter, deptfilter, locfilter)

    print(search_result)
    faculty_names = []
    faculty_homepage_url = []
    faculty_department_url = []
    faculty_department_name = []
    faculty_university_url = []
    faculty_university_name = []
    faculty_email = []
    faculty_phone = []
    faculty_location = []
    faculty_expertise = []

    for v in search_result:
        faculty_names.append(v['faculty_name'])
        faculty_homepage_url.append(v['faculty_homepage_url'])
        faculty_department_url.append(v['faculty_department_url'])
        faculty_department_name.append(v['faculty_department_name'])
        faculty_university_url.append(v['faculty_university_url'])
        faculty_university_name.append(v['faculty_university_name'])
        faculty_email.append(v['faculty_email'])
        faculty_phone.append(v['faculty_phone'])
        faculty_location.append(v['faculty_location'])
        faculty_expertise.append(v['faculty_expertise'])

    results = list(zip(faculty_names, faculty_homepage_url, faculty_department_url, faculty_department_name,
                       faculty_university_url, faculty_university_name, faculty_email, faculty_phone, faculty_location,
                       faculty_expertise))
    for r in results:
        print(r)

    return jsonify({
        "docs": results
    })


def is_redis_available(r):
    try:
        r.ping()
        print("Successfully connected to redis")
    except (redis.exceptions.ConnectionError, ConnectionRefusedError):
        print("Redis connection error!")
        return False
    return True


if __name__ == '__main__':
    # environ = os.environ.get("APP_ENV")

    app.run(debug=True, threaded=True, host='localhost', port=8095)
