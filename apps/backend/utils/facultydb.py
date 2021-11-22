from datetime import datetime
import sqlite3
from sqlite3 import Error

import json


class FacultyDB:

    def __init__(self):
        pass

    def __open_connection(self):
        """
        Creates a SQLite3 database and opens a connection. Also creates tables if not present.
        Private method. Not accessible outside the class.
        :return:
        """
        conn = json_data = None

        with open("../../../config/config.json", "r") as jsonfile:
            json_data = json.load(jsonfile)

        # print(json_data)

        db_file = json_data.get("db_filename", "")
        db_file = "../../../data/sqlite3/" + db_file

        # print("Database file: ", db_file)

        # create database and open a conection
        try:
            conn = sqlite3.connect(db_file)
            # print(sqlite3.version)

        except Error as e:
            raise Exception("Unexpected SQLite3 database connection error: " + str(e))

        except Exception as e:
            raise Exception("Unexpected SQLite3 table creation error: " + str(e))

        create_faculty_info_table_sql = """ 
        CREATE TABLE IF NOT EXISTS faculty_info (
            id integer PRIMARY KEY,
            faculty_name text NOT NULL,
            faculty_homepage_url text NOT NULL,
            faculty_department_url text NOT NULL,
            faculty_department_name text NOT NULL,
            faculty_university_url text NOT NULL,
            faculty_university_name text NOT NULL,
            faculty_email text,
            faculty_phone text,
            faculty_location text,
            faculty_expertise text NOT NULL,
            faculty_biodata,
            last_modified_date text NOT NULL,
            created_date text NOT NULL
        );"""

        create_faculty_department_table_sql = """ 
        CREATE TABLE IF NOT EXISTS faculty_department (
            id integer PRIMARY KEY,
            dept_url text NOT NULL,
            dept_name text NOT NULL,
            last_modified_date text NOT NULL,
            created_date text NOT NULL
        );"""

        create_faculty_university_table_sql = """ 
        CREATE TABLE IF NOT EXISTS faculty_university (
            id integer PRIMARY KEY,
            uni_url text NOT NULL,
            uni_name text NOT NULL,
            last_modified_date text NOT NULL,
            created_date text NOT NULL
        );"""

        # create tables if not present
        try:
            c = conn.cursor()
            c.execute(create_faculty_info_table_sql)
            c.execute(create_faculty_department_table_sql)
            c.execute(create_faculty_university_table_sql)

        except Error as e:
            raise Exception("Unexpected SQLite3 table creation error: " + str(e))

        except Exception as e:
            raise Exception("Unexpected SQLite3 table creation error: " + str(e))

        return conn

    def __close_connection(self, conn):
        """
        Closes the opened connection.
        Private method. Not accessible outside the class.

        :param conn:
        :return:
        """
        try:
            if conn:
                conn.close()
        except Error as e:
            try:
                if conn:
                    conn.close()
            except Error as e:
                raise Exception("Unexpected SQLite3 connection close  error: " + str(e))

            except Exception as e:
                raise Exception("Unexpected SQLite3 connection close  error: " + str(e))

    def add_records(self, faculty_data: list):
        """
        Add records in databse tables.
        :param data: list of dictionaries. Each disctionary in below format:
                     [{"faculty_name": <>,
                       "faculty_homepage_url": <>,
                       "faculty_department_url": <>,
                       "faculty_department_name": <>,
                       "faculty_university_url": <>,
                       "faculty_university_name": <>,
                       "faculty_email": <>,
                       "faculty_phone": <>,
                       "faculty_location": <>,
                       "faculty_expertise": <>,
                       "faculty_biodata": <>,
                      }, {...}
                     ]
        """

        if not faculty_data:
            return

        faculty_records, dept_records, uni_records = [], [], []
        departments, universities = {}, {}

        # Form bulk records for faculty_info insert opertation
        for faculty in faculty_data:
            record = [None]
            record.append(faculty["faculty_name"])
            record.append(faculty["faculty_homepage_url"])
            record.append(faculty["faculty_department_url"])
            record.append(faculty["faculty_department_name"])
            record.append(faculty["faculty_university_url"])
            record.append(faculty["faculty_university_name"])
            record.append(faculty["faculty_email"])
            record.append(faculty["faculty_phone"])
            record.append(faculty["faculty_location"])
            record.append(faculty["faculty_expertise"])
            record.append(faculty["faculty_biodata"])
            record.extend([datetime.now(), datetime.now()])
            faculty_records.append(tuple(record))

            departments[faculty["faculty_university_url"]] = faculty["faculty_university_name"]
            universities[faculty["faculty_university_url"]] = faculty["faculty_university_name"]

        # Form bulk records for faculty_department insert opertation
        for dept_url, dept_name in departments.items():
            record = [None]
            record.extend([dept_url, dept_name])
            record.extend([datetime.now(), datetime.now()])
            dept_records.append(tuple(record))

        # Form bulk records for faculty_university insert opertation
        for uni_url, uni_name in universities.items():
            record = [None]
            record.extend([uni_url, uni_name])
            record.extend([datetime.now(), datetime.now()])
            uni_records.append(tuple(record))


        try:
            conn = self.__open_connection()
            c = conn.cursor()

            # insert multiple records in a single query in faculty_info table
            c.executemany('INSERT INTO faculty_info VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?);', faculty_records)
            conn.commit()
            print(c.rowcount, ' record(s) inserted to the faculty_info table.')

            # insert multiple records in a single query in faculty_department table
            c.executemany('INSERT INTO faculty_department VALUES(?,?,?,?,?);', dept_records)
            conn.commit()
            print(c.rowcount, ' record(s) inserted to the faculty_department table.')

            # insert multiple records in a single query in faculty_university table
            c.executemany('INSERT INTO faculty_university VALUES(?,?,?,?,?);', uni_records)
            conn.commit()
            print(c.rowcount, ' record(s) inserted to the faculty_university table.')

            # close the connection
            self.__close_connection(conn)

        except Error as e:
            raise Exception("Unexpected SQLite3 connection close  error: " + str(e))

        except Exception as e:
            raise Exception("Unexpected SQLite3 connection close  error: " + str(e))

    def get_biodata_records(self, university_filter=None, location_filter=None):
        """
        Get faculty biodata. if ay of the filter parameters are provided, get biodate based on filters
        :param university_filter:
        :param location_filter:
        :return:
        """
        try:
            conn = self.__open_connection()
            c = conn.cursor()

            select_biodata_sql = 'SELECT id, faculty_biodata FROM faculty_info'
            if university_filter:
                select_biodata_sql += " WHERE faculty_university_name LIKE '%" + university_filter + "'"
                if location_filter:
                    select_biodata_sql += " AND faculty_location LIKE '%" + location_filter + "'"

            elif location_filter:
                select_biodata_sql += " WHERE faculty_location LIKE '%" + location_filter + "'"

            # print("select_biodata_sql: ", select_biodata_sql)

            c.execute(select_biodata_sql)
            records = c.fetchall()

            records = [str(id) + " " + biodata for id, biodata in records] if records else []

            # print("Records: ", "\n".join(records))

            # close the connection
            self.__close_connection(conn)

        except Error as e:
            raise Exception("Unexpected SQLite3 error: " + str(e))

        except Exception as e:
            raise Exception("Unexpected SQLite3 error: " + str(e))

        return records

    def get_faculty_records(self, id: list=None):
        """
        Get faculty biodata. if ay of the filter parameters are provided, get biodate based on filters
        :param university_filter:
        :param location_filter:
        :return:
        """
        try:
            conn = self.__open_connection()
            conn.row_factory = sqlite3.Row

            ids = "('" + "','".join([str(i) for i in id]) + "')"

            select_faculty_sql = "SELECT faculty_name, " \
                                 "       faculty_homepage_url, " \
                                 "       faculty_department_url, "\
                                 "       faculty_department_name, "\
                                 "       faculty_university_url, "\
                                 "       faculty_university_name, "\
                                 "       faculty_email, "\
                                 "       faculty_phone, "\
                                 "       faculty_location, "\
                                 "       faculty_expertise "\
                                 " FROM  faculty_info "\
                                 " WHERE id IN " + ids

            # print("select_faculty_sql: ", select_faculty_sql)

            records = conn.execute(select_faculty_sql)
            records = [{k: item[k] for k in item.keys()} for item in records]

            # print("Records: ", records)

            # close the connection
            self.__close_connection(conn)

        except Error as e:
            raise Exception("Unexpected SQLite3 error: " + str(e))

        except Exception as e:
            raise Exception("Unexpected SQLite3 error: " + str(e))

        return records


if __name__ == '__main__':
    faculty_db = FacultyDB()

    faculty_data = [{"faculty_name": "ANOOP BN",
                     "faculty_homepage_url": "https://smu.edu.in/smit/dept-faculty/faculty-list/ANOOP-BN.html",
                     "faculty_department_url": "https://smu.edu.in/smit/dept-faculty/dept-list/dept-of-computer-science-engineering-smit-sikkim-manipal-u.html",
                     "faculty_department_name": "Department of Computer Science & Engineering",
                     "faculty_university_url": "https://smu.edu.in/",
                     "faculty_university_name": "Sikkim Manipal Institute of technology",
                     "faculty_email": "anoop.bn@smit.smu.edu.in",
                     "faculty_phone": "9071897997",
                     "faculty_location": "Sikkim, India",
                     "faculty_expertise": "Image processing, Signal processing, Machine Learning, Deep Learning, Artificial Intelligence.",
                     "faculty_biodata": " ANOOP BN Assistant Professor I Department of Computer Science & Engineering   Academic Academic Expertise News & Articles Publication SUBJECTS CURRENTLY TEACHING Subject Subject code Semester INFORMATION TRANSMISSION AND CODING THEORY CS 1531 (Elective) 3rd year / 5th Semester INFORMATION THEORY CS1853 (Minor) 3rd year / 5th Semester COMPUTER NETWORKS-I CS 1508 3rd year / 5th Semester INTELLIGENT SYSTEM LAB CS 1763 4th year / 7th Semester ACADEMIC QUALIFICATIONS Degree Specialisation Institute Year of passing Ph.D Medical Image Processing using Deep Learning NITK Surathkal 2021 (Thesis Submitted) M.Tech Signal Processing NIT Calicut 2013 B.Tech Electronics and communication Engineering CUSAT 2007 Experience Institution / Organisation Designation Role Tenure Sikkim Manipal Institute of Technology, SMU Assistant Professor I Teaching and Research July 2021 Till Date NITK, Surathkal. Senior Research Fellow Research March 2020 July 2021 NITK, Surathkal. Senior Research Fellow (Project Staff DST, SERB funded project) Research May 2019 March 2020 NITK, Surathkal. Junior Research Fellow (Project Staff DST, SERB funded project) Research May 2017 May 2019 St. Josephs College of Engineering and Technology, Palai, Kerala. Assistant professor Teaching and Research January 2008 May 2017 College of Engineering Munnar, Kerala. Lecturer Teaching August 2007- January 2008 AREAS OF INTEREST, EXPERTISE AND RESEARCH Area of Interest Image processing, Signal processing, Machine Learning, Deep Learning, Artificial Intelligence. Area of Expertise Secure Image transcoding, Convolutional Neural networks, Image Denoising, Image segmentation, GANs, MATLAB, Python, Tensorflow, Keras. Area of Research Image analysis, Medical Image analysis. Professional Affiliations & Contributions Member - IEEE IEEE Student Branch Counselor, SJCET - Palai. Member IEEE Signal Processing Society Member - Internet Society Reviewer - IEEE Transactions on Medical Imaging. Reviewer - Biocybernetics and Biomedical Engineering. Reviewer - Biomedical Signal Processing and Control. Reviewer - International Journal for Light and Electron Optics. Capsule Networkbased architectures for the segmentation of sub-retinal serous fluid in optical coherence tomography images of central serous chorioretinopathy June 30, 2021 ANOOP BN SJ Pawan Rahul Sankar Anubhav Jain Mahir Jain DV Darshan BN Anoop Abhishek R Kothari M Venkatesan Jeny Rajan Medical & Biological Engineering & Computing, Springer A cascaded convolutional neural network architecture for despeckling OCT images April 01, 2021 ANOOP BN BN Anoop Kaushik S Kalmady Akhil Udathu V Siddharth GN Girish Abhishek R Kothari Jeny Rajan Biomedical Signal Processing and Control, Elsevier Stack generalized deep ensemble learning for retinal layer segmentation in Optical Coherence Tomography images October 01, 2020 ANOOP BN BN Anoop Rakesh Pavan GN Girish Abhishek R Kothari Jeny Rajan Biocybernetics and Biomedical Engineering, Elsevier A novel deep learning approach for the removal of speckle noise from optical coherence tomography images using gated convolutiondeconvolution structure December 31, 2021 ANOOP BN Sandeep N Menon VB Vineeth Reddy A Yeshwanth BN Anoop Jeny Rajan Proceedings of 3rd International Conference on Computer Vision and Image Processing, Springer, Singapore A modified unsharp masking with adaptive threshold and objectively defined amount based on saturation constraints April 30, 2019 ANOOP BN Justin Joseph BN Anoop Joseph Williams Multimedia Tools and Applications, Springer 1 2 3 Despeckling Algorithms for Optical Coherence Tomography Images: A Review January 29, 2019 http://www.octnews.org/articles/8503285/despeckling-algorithms-for-optical-coherence-tomog/"
                    },
                    {"faculty_name": "Dr. Akash Kumar Bhoi",
                     "faculty_homepage_url": "https://smu.edu.in//content/smu/academics/institution-list/smit/dept-faculty/faculty-list/akash-kumar-bhoi.html",
                     "faculty_department_url": "https://smu.edu.in/smit/dept-faculty/dept-list/dept-of-computer-science-engineering-smit-sikkim-manipal-u.html",
                     "faculty_department_name": "Department of Computer Science & Engineering",
                     "faculty_university_url": "https://smu.edu.in/",
                     "faculty_university_name": "Sikkim Manipal Institute of technology",
                     "faculty_email": "akash.b@smit.smu.edu.in",
                     "faculty_phone": "+91 8001822676",
                     "faculty_location": "Sikkim, India",
                     "faculty_expertise": "Biomedical Instrumentation, Sensor & Transducer, Digital Image Processing and Mechatronics",
                     "faculty_biodata": " Dr. Akash Kumar Bhoi Assistant Professor (Selection Grade) Research Department of Computer Science & Engineering   Academic Academic Expertise Research News & Articles Publication Student Projects CURRENT ACADEMIC ROLE & RESPONSIBILITIES Core Member of Admission Committee for the year 2016-2017 Member of Institute Purchase Committee Member of Annual Stock Verification Departmental Moderator for Semester Examination Departmental Project Coordinator for Annual Technical Project Exhibition Departmental Coordinator of ISO, AICTE, NBA and NAAC. SUBJECTS CURRENTLY TEACHING Subject Subject code Semester Digital Image Processing(DIP) EE2137 1st year M.Tech Measurement and Instrumentation EE1308 2nd Year B.Tech Research and Publication Ethics CPE-RPE PhD Coursework ACADEMIC QUALIFICATIONS Degree Specialisation Institute Year of passing Ph.D. Research area: Biomedical Signal Processing Sikkim Manipal University 2019 MTech Biomedical Instrumentation Karunya University 2011 BTech Biomedical Engineering Trident Academy of Technology, Bhubaneswar, Orissa 2009 Experience Institution / Organisation Designation Role Tenure SMIT R&D Faculty Associate, Assistant Professor I Research & Teaching 2017 - Present Sikkim Manipal Institute of Technology Assistant Professor II Research & Teaching 2012-2016 Institute of Information Science and Technologies ISTI, CNR, Italy Research Associate Research 20th Jan 2021-Present Machine Learning-based Smart Workout Mirror and Method Thereof November 11, 2020 Dr. Akash Kumar Bhoi Australian IP Patent number: 2020102642 Machine Learning And IoT -Based Smart Self Adjusting Potty Seat October 28, 2020 Dr. Akash Kumar Bhoi Australian IP Patent number: 2020102473 Machine Learning Based Fish Monitoring Machine And Method Thereof October 21, 2020 Dr. Akash Kumar Bhoi Australian IP Patent number: 2020102433 A review of pre-processing of photoplethysmography (ppg) signal and features analysis January 01, 2014 Dr. Akash Kumar Bhoi Book chapter entitled, 2014, Biomedical Engineering Advances in Medicine and Biology. Vol 73, Editors: January 01, 2014 Dr. Akash Kumar Bhoi Leon V. Berhardt Published in the book by the Nova Science Publishers, New York. 1 2 AREAS OF INTEREST, EXPERTISE AND RESEARCH Area of Interest Biomedical Instrumentation, Sensor & Transducer, Digital Image Processing and Mechatronics Area of Expertise Medical Signal Processing Area of Research Biomedical Signal Processing, Medical Image Processing & Medical Electronics Professional Affiliations & Contributions Membership Member of ISEIS (International Society for Environmental Information Sciences) Associate Member of UACEE (Universal Association of Computer and Electronics Engineers) Member of IAENG (International Association of Engineers) & member of following societies: IAENG Society of Imaging Engineering IAENG Society of Industrial Engineering IAENG Society of Operations Research Individual Membership with HTMA-SC (Healthcare Technology Management Association of South Carolina) Member of International Association of Computer Science and Information Technology (IACSIT). Individual Membership with the Intermountain Clinical Instrumentation Society (ICIS). Member of Editorial Board, Reviewer in International Journals / Conferences Reviewer International Journal of Medical Imaging (IJMI) Reviewer American Journal of Biomedical and Life Sciences (AJBLS) Editorial Board International Conferences (ICRTSE-2015, ICWTA-2015, ICACIT-2013, ICEECS-2013, ICAEEMCS-2013 etc.) Appreciated by Dr. P. D. Shendge, Convener International Conference on Industrial Instrumentation & Control (ICIC 2015) for reviewing the papers. Conference Secretary : 1st Springer International Conference on Emerging Trends and Advances in Electrical Engineering and Renewable Energy ( ETAEERE-2016 ) 1. Conference Secretary: 1 st International Conference on Emerging Trends and Advances in Electrical Engineering and Renewable Energy (ETAEERE-2016) organized by Department of Electrical and Electronics Engineering, Sikkim Manipal Institute of Technology, Sikkim, December 17 18, 2016. [Signed 4 Book Volumes Contract withSpringerNatureunder the Book Series of Lecture Notes in Electrical Engineering] 2. Organizing Chair: Workshop on Anti-Plagiarism and Intellectual Property Rights (IRR) organized by Research & Development Section, Sikkim Manipal Institute of Technology (SMIT), Sikkim, October 3-4, 2016. 3. Organizing Chair: 19 th North-East Workshop on Computational Information Processing organized by Electronics and Communication Sciences Unit ( ECSU ), Indian Statistical Institute (ISI) , Kolkata And Department of Electrical & Electronics Engineering, Sikkim Manipal Institute of Technology ( SMIT ), Sikkim, March 23 - 25, 2017. 4. Organizing Committee Member: Workshop on Super Computer Applications in Diverse Fields of Science and Technology organized by Research & Development Section, Sikkim Manipal Institute of Technology ( SMIT ), Sikkim, November 13-16, 2017. 5. Coordinator: 2 nd Manipal Student Research Colloquium (MSRC-2018 organized by Sikkim Manipal Institute of Technology ( SMIT ), Sikkim Manipal University, March 15-16, 2018. 6. Course Coordinator: Workshop on Applied Engineeding organized for B.Tech students by Department of Electrical and Electronics Engineering, Sikkim Manipal Institute of Technology (SMIT), Sikkim, February 5-9, 2018. International Conferences, Seminars, Workshop & Short-term Course: Participated in the ISRO Sponsored Two Weeks Training Programme on Remote Sensing & GIS for Natural Resources Management organized by Dept. of CSE & CA, SMIT during 18 th Jan to 29 th Jan 2016. Chaired a Session (Track-2- Power, Energy and Automation) during1 st Springer International Conference on Emerging Trends and Advances in Electrical Engineering and Renewable Energy (ETAEERE-2016) held during 17th 18th Dec, 2016. Participated in the 19 th North-East Workshop on Computational Information Processing Organized by Electronics and Communication Sciences Unit (ECSU), Indian Statistical Institute (ISI), Kolkata And Department of Electrical & Electronics Engineering, Sikkim Manipal Institute of Technology (SMIT), Sikkim, March 23 - 25, 2017 Participated in the Workshop on Super Computer Applications in Diverse Fields of Science and Technology organized by Research & Development Section, Sikkim Manipal Institute of Technology (SMIT) during 30 th May to 2 nd June, 2017. Participated in the Workshop on Intellectual Property Rights (IPR) and Patenting organized by by Research & Development Section, Sikkim Manipal Institute of Technology (SMIT) with assistance from the Patent Office, Kolkata, 2 nd Nov, 2017. Presented a paper entitledIschemia and Arrhythmia Classification Using Time-Frequency Domain Features of QRS Complex in the International Conference on Computational Intelligence and Data Science (ICCIDS 2018) organized by the Dept. of Computer Science & Engineering, The NorthCap University, Gurugram on 7 th 8 th April 2018. Attended in the Workshop on Big Data and Machine Learning organized by theDept. of Computer Science & Engineering, The NorthCap University, Gurugram on 7 th 8 th April 2018. Attended the workshop on Design of Experiments and Statistical Modeling held at National Institute of Technology, Sikkim during march 25-28, 2015 organized by SQC & OR unit, ISI, Hyderabad and NIT Sikkim. Participated in the ISRO Sponsored Two Weeks Training Programme on Remote Sensing & GIS for Natural Resources Management Organized by Dept. of CSE & CA, SMIT during 18 th Jan to 29 th Jan 2016. Attended Intensive Teaching Workshop (ITW) conducted from 18 th Dec to 28 th Dec 2012 at Sikkim Manipal Institute of Technology, Majhitar, Sikkim. Chaired a session in International Conference on Advances in Electrical and Electronics Engineering (ICAEEE-2012) at Pune. International conference on Computer Technology, ICCT-Dec 2010 at C.V. Raman College of Engineering, Odisha. International Conference on the theme Education for Peace, Social Inclusion and Sustainable Development: Towards a Paradigm Shift, ICMGU-Dec 2010 at Mahatma Gandhi University, Kerala. International Conference on Embedded System ICES-July 2010 organized by CIT, Cbe jointly with Oklahoma State Univrsity, USA. International Joint conference on Information and Communication Technology IJCICT-Jan2011 at Interscience Institute of Managment & Technology, Odisha. International Conference on Electrical and Electronics Engineering (ICEEE June-2012) organized by IRD India at Pune. Seminar-cum-Workshop on Acquisition and Analysis of Biomedical Signals2008 held at SRM University. National Workshop on Biomechanics-NWBM 2007 held at MIT, Manipal. Short term course on Contributions of Small Angle X-ray Scattering (SAXS) to Nanoscience and Nanotechnology at NIT,Rkl during may 2010. An Analytical Review of Different Approaches for Detection and Analysis of Electrocardiographic ST Segment January 01, 2019 Dr. Akash Kumar Bhoi Bhoi A K Sherpa K S Khandelwal B Mallick P K Cognitive Informatics and Soft Computing (pp. 39-51). Advances in Intelligent Systems and Computing, vol 768. Springer, Singapore. ISSN: 21945357 [Indexed in Scopus, UGC approved Journal] T Wave Analysis: Potential Marker of Arrhythmia and Ischemia Detection-A Review January 01, 2019 Dr. Akash Kumar Bhoi Bhoi A K Sherpa K S Khandelwal B Mallick P K Cognitive Informatics and Soft Computing (pp. 121-130). Advances in Intelligent Systems and Computing, vol 768. Springer, Singapore. ISSN: 21945357 [Indexed in Scopus, UGC approved Journal] Improvement of the performance of wearable textile antenna August 01, 2018 Dr. Akash Kumar Bhoi Loni J Singh V K Tripathi A K Chae G S Sharma A Bhoi A K International Journal of Engineering & Technology, 7 (2.33) 650-652, (2018) Rectenna circuit at 6.13 GHz to operate the sensor devices July 16, 2018 Dr. Akash Kumar Bhoi Saxena A Singh V K Mohini Bhardwaj S Chae G S Sharma A Bhoi A K International Journal of Engineering & Technology, 7 (2.33) 644-646, (2018) Power harvesting through flexible rectenna at dual resonant frequency for low power devices May 15, 2018 Dr. Akash Kumar Bhoi Singh V K Saxena A Khare B B Shakya V Chae G S Sharma A Bhoi A K International Journal of Engineering & Technology, 7 (2.33) 647-649, (2018) 1 2 3 4 5 ... 13 Heart rate measurement and spectral analysis using phonocardiogram (PCG) signal November 01, 2013 Dr. Akash Kumar Bhoi Yojana Shaw Wangmo S Lama November 2013, Biomedical signal processing,Students have done their project with real-time acquisition of PCG signal and detection of heart rate using NI ELVIS-II DAQ. Have faced challenges in artefact/noise removal during processing. It significantly calculated the spectral behaviour of the PCG signal. To develop a bio signal acquisition system with telemetry application February 01, 2013 Dr. Akash Kumar Bhoi Shishir Srivastava Prasant Basnett February 2013, Biomedical instrumentation, Proposed biotelemetry system comprises of ECG simulators which generated all 12 leads configuration signals and processing of these signals by FDM module. Designed a LPD (H/W & S/W) in NIELVIS-II platform and Lab view. The filtered signals were acquired through the Data acquisition system i.e. NI ELVIS-II. This hardware gives us another platform i.e. further analysis of ECG signal in Lab View which will provide enormous research opportunities. 1 Call for Book Chapters December 31, 2020 Call For Book Chapters Book Title: Advances in Greener Energy Technologies Springer Book Series: Green Energy and Technology (ISSN: 1865-3529) **Indexed in Scopus** https://www.springer.com/series/8059 Focus Area Science Technology Summer Fellowship [FAST-SF] 2018 Focus Area Science Technology Summer Fellowship [FAST-SF] 2018 Selected and attended Focus Area Science Technology Summer Fellowship [FAST-SF] -2018 offered by Inter Academy Panel [Indian Academy of Sciences, Bengaluru, Indian National Science Academy, New Delhi and The National Academy of Sciences, India, Allahabad] (Teacher category) at Indian Institute of Engineering Science and Technology (IIEST), Shibpur. Project Title: Movement Intentions Detection and Classification using EEG Signals Duration: 56 days (23rd May 2018 17th July 2018) Guide / Institution: Prof. Subhasis Bhaumik, Head, School of Mechatronics and Robotics and Professor, Dept. of Aerospace Engineering and Applied Mechanics, Indian Institute of Engineering Science and Technology, Shibpur-711103"
                    },
                    {"faculty_name": "Ashis Pradhan",
                     "faculty_homepage_url": "https://smu.edu.in//content/smu/academics/institution-list/smit/dept-faculty/faculty-list/ashis-pradhan.html",
                     "faculty_department_url": "https://smu.edu.in/smit/dept-faculty/dept-list/dept-of-computer-science-engineering-smit-sikkim-manipal-u.html",
                     "faculty_department_name": "Department of Computer Science & Engineering",
                     "faculty_university_url": "https://smu.edu.in/",
                     "faculty_university_name": "Sikkim Manipal Institute of technology",
                     "faculty_email": "ashis.p@smit.smu.edu.in",
                     "faculty_phone": "+91 7872888120",
                     "faculty_location": "Sikkim, India",
                     "faculty_expertise": "Image Processing, Computer Vision, Pattern Recognition, Machine Learning and Algorithms: Its Design, Implementation and Analysis.",
                     "faculty_biodata": " Ashis Pradhan Assistant Professor (Selection Grade) and Faculty Research Associate Department of Computer Science & Engineering   Academic Academic Expertise Research Publication Student Projects CURRENT ACADEMIC ROLE & RESPONSIBILITIES Ashis Pradhan isAssistant Professor (Selection Grade) and Faculty Research Associate at SMIT. He is: Lab-in-charge. Representative of Time-Table Officer at Department Level. Member of Budget Committee at Department Level. Member of ISO, NBA and NAAC team. Member of Departmental Academic Counseling Cell SUBJECTS CURRENTLY TEACHING Subject Subject code Semester Digital Image Processing CS-1633 (Elective) 6th semester Java Programming CS-1421 (Elective) 4th semester Advance Programming Lab CS-1464 4th Semester Unix Lab CS 1664 6th Semester Latest Trends in Computer Science CS1651 3rd Year/ 6th Semester Object Oriented Concepts & Programming using C++ CS1308 3rd semester Operating System CS1502 5th Semester ACADEMIC QUALIFICATIONS Degree Specialisation Institute Year of passing MTech Digital Image Processing Sikkim Manipal Institute of Technology 2013 BTech Computer Science Sikkim Manipal Institute of Technology 2010 Experience Institution / Organisation Designation Role Tenure Sikkim Manipal Institute of Technology Assistant Professor II Academic discipline, progress & development of students and their Academic records create interest in students for innovative ideas in their interested areas 2010 - 2014 Sikkim Manipal Institute of Technology Assistant Professor I Academic discipline, progress & development of students and their Academic records create interest in students for innovative ideas in their interested areas. Also, Motivate Students in Research as well. 2014 Till Date Image and video analysis, Design of efficient algorithms for implementing various image reconstruction techniques, Automatic digitization of contour map and 3-D model construction. Ashis Pradhan 1 AREAS OF INTEREST, EXPERTISE AND RESEARCH Area of Interest Image Processing, Computer Vision, Pattern Recognition, Machine Learning and Algorithms: Its Design, Implementation and Analysis. Area of Expertise Image Processing, Computer Vision, Pattern Recognition Area of Research Image and video analysis Professional Affiliations & Contributions Google Scholar:https://scholar.google.co.in/citations?user=4hIc-5kAAAAJ&hl=en A Study On VIDEO SUMMARIZATION' Ashis Pradhan Tanuja Subba Bijoyeta Roy International Journal of Advanced Research in Computer and Communication Engineering, Vol. 5, Issue 6, June 2016, pp. 738-741. Implementation of PCA for Recognition of Hand Gesture Representing Alphabets Ashis Pradhan Shubham Kumar Dependra Dhakal Bishal Pradhan International Journal of Advanced Research in Computer Science and Software Engineering ( ISSN: 2277 128X), Volume 6, Issue 3, March 2016, pp. 263-268. , An Approach to Calculate Depth of an Object in a 2-D Image and Map it into 3-D Space Ashis Pradhan Ashit Kr. Singh Ashit Kr. Singh, Shubhra Singh International Journal of Computer Applications (0975 8887), Volume 119, Issue No.15, June 2015, pp. 27-32 Face Detection in Night Vision Images: An Application of BPDFHE Methodology Ashis Pradhan Anurag Ray International Journal of Research in Commerce, It & Management, ISSN 2231-5756, Volume No. 4 (2014), Issue No. 06 (June), pp. 62-65. A Distance Based Hand Gesture Recognition Representing Numbers Ashis Pradhan M.K. Ghose Mohan Pradhan Global Journal of Computer Science and Technology Graphics & Vision Online ISSN: 0975-4172& Print ISSN:0975-4350, pp. 19-24, Year 2013. 1 2 3 4 Histogram equalisation technique for face detection October 31, 2013 Ashis Pradhan Anurag Ray Sujit Kumar August- November 2013, The challenge is to efficiently detect the face by contrast enhancement for images taken during night time. Design of an efficient image reconstruction algorithm for extracting contour information from maps Ashis Pradhan Aroj Subedi Ongoing project Design of an efficient algorithm for detecting a regular object from a video Ashis Pradhan Shubham Ongoing project Automatic Localization of Elevation Values in a Poor Quality Topographic Map Ashis Pradhan Ashis Pradhan Mohan P. Pradhan Automatic Localization of Elevation Values in a Poor Quality Topographic Map. International Journal of Image and Graphics, Vol. 21, No. 1 (2021) 2150009-1-15. International/Scopus Indexed. Reconstruction of Contour Lines for Digitization of Contour Map Ashis Pradhan Ashis Pradhan Mohan P. Pradhan Reconstruction of Contour Lines for Digitization of Contour Map. 3rd International Conference on Computing and Communication Systems (I3CS 2020), Publisher: Springer. International/ Scopus Indexed 1 2"
                     },
                    {"faculty_name": "Bijoyeta Roy",
                     "faculty_homepage_url": "https://smu.edu.in//content/smu/academics/institution-list/smit/dept-faculty/faculty-list/bijoyeta-roy.html",
                     "faculty_department_url": "https://smu.edu.in/smit/dept-faculty/dept-list/dept-of-computer-science-engineering-smit-sikkim-manipal-u.html",
                     "faculty_department_name": "Department of Computer Science & Engineering",
                     "faculty_university_url": "https://smu.edu.in/",
                     "faculty_university_name": "Sikkim Manipal Institute of technology",
                     "faculty_email": "bijoyeta.r@smit.smu.edu.in",
                     "faculty_phone": "+91 8100486838",
                     "faculty_location": "Sikkim, India",
                     "faculty_expertise": "Software Engineering, Database Management System",
                     "faculty_biodata": " Bijoyeta Roy Assistant Professor (Selection Grade) Department of Computer Science & Engineering   Academic Academic Expertise Publication Student Projects CURRENT ACADEMIC ROLE & RESPONSIBILITIES Bijoyeta Roy isAssistant Professor (Selection Grade) in the Department of Computer Science and Engineering at SMIT. Additionally she also handles the following: In-charge (Basic Computing Laboratory) Student Body (Teacher Member) Affiliation/Accreditation Team (Member) Semester Cordinator University Convocation Committee (Member) Teacher Guardian Floor Warder SUBJECTS CURRENTLY TEACHING Subject Subject code Semester Data Structures Cs1302 Third Semester Computer Programming using C CS1110 First Semester Data Structures Laboratory CS1361 Third Semester DBMS CS1403 Fourth Sem. Object Oriented Concepts & Programming using C++ CS1308 Third Semester Database Management Systems Lab CS 1462 Fourth Semester Python Programming CS 1435(Programme Elective I) Fourth Semester ACADEMIC QUALIFICATIONS Degree Specialisation Institute Year of passing MTech Computer Science & Engineering Sikkim Manipal Institute of Technology 2013 BE Computer Science & Engineering Assam Engineering College 2008 Experience Institution / Organisation Designation Role Tenure Sikkim Manipal Institute of Technology Assistant Professor II Working as a teacher as well as involved in other academic and non-academic activities related to the institute. July 2010-September 2015 Sikkim Manipal Institute of Technology Assistant Professor I September 2015-till date AREAS OF INTEREST, EXPERTISE AND RESEARCH Area of Interest Software Engineering, Database Management System Area of Expertise Software Selection Area of Research Software Selection, Software Reliability Professional Affiliations & Contributions Member of Technical Program Committee (IEEE ICRCICN 2015) Member of Technical Program Committee (IEEE ICRCICN 2016) Member of Technical Program Committee (IEEE ICACCP 2017) Work Experience Organisation Role Tenure WIPRO Ltd. Senior Associate August 2008-July 2010 Design and strategies of online voting system May 30, 2016 Bijoyeta Roy Sayan Mazumdar International Journal of Computer Applications (0975 8887)Volume 142 No.7 SIMBA-Search Images By Appearance April 29, 2016 Bijoyeta Roy Mrinaldeep Chakraborty International Journal of Advanced Research in Computer and Communication Engineering (IJARCCE) Vol. 4, Issue 4 Segmentation of images using density based clustering algorithms July 30, 2015 Bijoyeta Roy Atrayee Dhua Debjani Nath Sharma Sneha Singh International Journal of Advanced Research in Computer and Communication Engineering (IJARCCE) Vol. 4, Issue 5 Performance Analysis of Subspace Clustering Algorithms in Biological Data June 29, 2015 Bijoyeta Roy Shilpi Chakraborty International Journal of Advanced Research in Computer and Communication Engineering (IJARCCE) Vol. 4, Issue 2. Assessment of Object Oriented Metrics for Software Reliability June 29, 2015 Bijoyeta Roy Santanu Kumar Misra International Journal of Engineering Research & Technology (IJERT), Vol. 4 - Issue 01 1 2 3 4 A quantitative analysis of NHPP based software reliability growth models November 29, 2013 Bijoyeta Roy Aradhana Basak Aparupa Roy Deyasini Hazra In this project a general framework of two non-homogeneous poisson processes based SRGM models namely goel okumoto and delayed S shaped model are presented. The main objective of these two models is to estimate the faults or failures remaining in the system. An integrated DEMATEL and AHP approach for personnel estimation November 29, 2012 Bijoyeta Roy Akanksha Goswami Neha Preeti This project supports adequately the decision making process with the help of decision making trial and evaluation laboratory (DEMATEL) and Analytic Hierarchical Process (AHP). A decision support system for selecting software architectural styles June 29, 2013 Bijoyeta Roy Yogesh Gurung Adip Chettri In this project an integrated VIKOR-TOPSIS approach is implemented. Target Detection in brain MRI and its Classification Bijoyeta Roy Bijoyeta Roy Mousumi Gupta Abhishek Kumar Sweta Target Detection in brain MRI and its Classification. 4th International Conference on Communication, Devices and Networking (ICCDN 2020)(Accepted). International/ Scopus Indexed MUS EMO: An Automated Facial Recognition based Music Recommendation System using CNN Bijoyeta Roy Shubham Mittal Anand Ranjan Bijoyeta Roy MUS EMO: An Automated Facial Recognition based Music Recommendation System using CNN. 4th International Conference on Communication, Devices and Networking (ICCDN 2020)(Accepted). International/ Scopus Indexed 1 2 "
                    }]

    # bulk insert faulty data
    faculty_db.add_records(faculty_data)

    # get all biodata
    faculty_db.get_biodata_records()

    # get faculty info for ids 2 and 3
    faculty_db.get_faculty_records([2,3])
