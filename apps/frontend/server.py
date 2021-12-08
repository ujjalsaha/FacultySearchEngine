from flask import Flask
from flask import render_template, request, jsonify
import json
import os
import requests
import base64
import sys
import re
from apps.backend.utils.facultydb import FacultyDB
from apps.backend.api.search import Search

from redis import Redis
import redis
import rq

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'apps'))

from apps.frontend.utils.background_task import run_task

app = Flask(__name__, template_folder='web/templates', static_folder='web/static')
app.rootpath = "web/templates"
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'web/templates'))

'''environ = 'development'
dataconfig = json.loads(open("config.json", "r").read())
app.dataenv = dataconfig[environ]
app.rootpath = dataconfig[environ]["rootpath"]
app.datasetpath = dataconfig[environ]['datasetpath']
app.searchconfig = dataconfig[environ]['searchconfig']
index = metapy.index.make_inverted_index(app.searchconfig)
query = metapy.index.Document()
uni_list = json.loads(open(dataconfig[environ]["unispath"],'r').read())["unis"]
loc_list = json.loads(open(dataconfig[environ]["locspath"],'r').read())["locs"]
'''
faculty = FacultyDB()
unis = json.dumps(faculty.get_all_universities())
locs = json.dumps(faculty.get_all_locations())
depts = json.dumps(faculty.get_all_departments())

@app.route('/')
def home():
    return render_template('index.html',unis= unis,locs=locs)

@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route("/admin/crawl", methods=['POST'])
def doCrawl():
    redis_server = Redis(host='localhost', port=6379, db=0)
    if is_redis_available(redis_server):
        data = json.loads(request.data.decode("utf-8"))
        search_str = data["searchText"]
        print(type(data))
        print(data)
        queue = rq.Queue('crawler-worker', connection=redis_server)
        job = queue.enqueue(run_task, search_str)
        print('job id = ', job.get_id())
        return jsonify({
            "msg": "Your request has been accepted. We will process the request asynchronously"
        })
    else:
        return jsonify(
            {
                "error": "An error occurred. Please contact system administrators for more details."
            }
        )

@app.route('/search', methods=['POST'])
def search():
    data = json.loads(request.data.decode("utf-8"))
    querytext = data['query']
    num_results = data['num_results']

    search_obj = Search()
    search_result = search_obj.get_search_results(querytext, "Manipal", "Computer", "Sikkim")

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
    '''environ = 'development'
    dataconfig = json.loads(open("config.json", "r").read())
    app.dataenv = dataconfig[environ]
    app.rootpath = dataconfig[environ]["rootpath"]
    app.datasetpath = dataconfig[environ]['datasetpath']
    app.searchconfig = dataconfig[environ]['searchconfig']'''

    app.run(debug=True, threaded=True, host='localhost', port=8095)
