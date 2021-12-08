#  ExpertSearch v2.0

## Table of contents
* [Video Presentation](#video-presentation)
* [Using the ExpertSearch v2.0 Webapp](#using-the-expertsearch-v2.0-webapp)
* [Overview](#overview)
* [Technologies](#technologies)
* [Hardware Requirements](#hardware-requirements)
* [Access and Permission Requirements](#access-and-permission-requirements)
* [Software Requirements](#software-requirements)
* [Setup](#setup)
* [Deploy](#deploy)
* [Implementation Details](#-implementation-details) 
* [Project Team Members](#project-team-members)
* [User Stories and Contributions](#user-stories-and-contributions)
* [Improvements Areas](#improvements-areas)
* [Licensing](#licensing)
* [Acknowledgements](#acknowledgements)
* [References][#references]

## Video Presentation

#### [Software usage tutorial presentation](https://uofi.app.box.com/file/893368706848?s=ealry89ittv21gz2x30bn2lrw319vhnw) 
<sub><sup>MacOS   To open in a new tab: Cmd </sup></sub><kbd>⌘</kbd><sub><sup> + Click</sup></sub>      
<sub><sup>Windows   To open in a new tab: Cmd </sup></sub><kbd>⌃</kbd><sub><sup> + Click</sup></sub>      

## Using the ExpertSearch v2.0 Webapp
- - - - 
:warning: \
The team put all emphasis on the NLP, text retrieval, text mining techniques and aspects for faculty search. 
The webapp is the platform to display the outcomes of the implementation while putting everything together for demonstration purposes. 
However, making the webapp perfect in terms of end-to-end best user experience was not part of the goal for this project. 
The webapp still has got many improvement areas in terms of UX, UI display, communication, request response, industry standards, completeness which could be a separate project by itself.
While developing the ExpertSearch v2.0 we considered to develop the prototype and leave opportunity to build things on top of this.      
- - - - 
#### Using Search Feature
1. Launch the app in your Chrome browser using the URL: 
2. The ExpertSearch v2.0 Home Page should be displayed.
3. Now try searching a faculty by entering queries like: 
    * names can be provided such as Matt Caesar, Cheng Zhai, John Hart etc.
    * location can be provided such as Illinois, Utah etc
    * search queries can be provided such as deep learning, text information, visualization etc
4. ExpertSearch v2.0 should display search results along with the faculty attributes such as Name, Department Name, University Name, areas of interests, Phone number. email, location.
5. Few of the faculty attributes that wil be displayed, user can perform action on them such as clicking the email should open the local outlook composer, or clicking location shall opt in for google maps etc.
    
#### Using Admin Feature
1. Go to the Admin interface.
2. Admin interface is a way for admin users (currently open for all users) to add universities, department and faculty urls for the system to be able to store and append more and more faculty data to its database. This will result in broader seach results and more data availability. This is also an continuous process to enrich the system with more and more data as they are available or explored.  
1. User can provide either univseristy name or university url or department url. User can also specify University Name and Department name together
2. The ExpertSearch v2.0 system should asynchronoulsy start crawling and scraping data on the backedn system but letting the user know that the data will be added eventually. 
3. As this is eventual update, user may come back after a while and searching data related to newly entered unisersity serach results should get displayed.
4. If a faulcty is alrready present in the system, the system wont insert a deplicate record of the same facult and will silently ignore the faculty in the process.

<div style="text-align: right"> <a href="#top">Back to top</a> </div>

## Overview

The ExpertSearch v2.0 application is a faculty search webapp that uses NLP and Text Porcessing (Retrieval and Mining) abilties leveraging the modein python NLP libraries.
The ExpertSearch v2.0 application was build on top the existing ExpertSearch web application [[1]](https://github.com/CS410Assignments/ExpertSearch) that has features such as faculty search, filtering based search, displaying search results (with options to open faculty bio pages, emailing, location info), pagination etc.\
As a team, we did a deep analysis of the current ExpertSearch capabilities and found several deficiencies that can be addressed to make it a better search system. 
The deficiencies include lack of accuracy in the search results, lack of relevant search results and inconsistencies in the search results, old and out of support python library usages, undocumented code and repo etc.\
These deficiencies can be addressed using the right text retrieval and text mining techniques along with some good pratices that will improve the overall search experience in the ExpertSearch system.  
Our team involved in implementing following features as we fork the existing ExpertSearch System and added/improved core-functionalities as we build on top of it. 
Below are the core functionalities that we added/improved on the existing ExpertSearch and hence we called it **ExpertSearchv2.0**:
<details>
   <summary>Converting unstructured dataset to structured dataset. Click to learn more</summary>
   <br/>
   <p>The new ExpertSearch v2.0 system can scrapes faulty pages and using text retrieval techniques extracts structured data such as Name, email, departname name, university name, phone number, email, location, areas of interests etc and saves in the database along with the scrpaed biodata. 
   Whenver a user enters a search query, based on filter used or not with the search qury, the system grabs the biodata from the database and ranks them using BM25 ranking algorithm.
   After the ranking, the system granbs the ranked data and gets corresponding faculty attributes from the structured database entry for the faculties.
   This makes the new system much more organized with data while maintaining consistancy in displaying search results with unniformity in data.
   The existing ExpertSearch system doesn't have the structured data implementation and search results displays and very inconsistant. 
   </p>
   <img/>
</details>     
 
<details>
   <summary>Topics extraction (e.g., areas of interest) for faculties and display in search results. Click to learn more.</summary>
   <br/>
   <p>The new ExpertSearch v2.0 implemented the innovative feature of displaying areas of interest for each faculty in the search results. 
   This was achieved by performing topic mining techniques on the faculty bioodata to extract most relevant topic.
   The areas of interests filed which is being displayed in the search results of faculty is the outcome of this inovative approach.
   The existing ExpertSearch application doesn't have this feature.
   </p>
   <img/>
</details>     

<details>
   <summary>Rearchitected admin interface for auto crawling amd scraping faculty pages async. Click to learn more.</summary>
   <br/>
   <p>In the new ExpertSearch v2.0 system the admin interface has ben reengineered with many improvemtest and upgrades.
   Admin interface is primarily responsible to receive university input from user to parse, crawl, scrpe data and insert structured data to database.
   elow are few major upgrades in the Admin interface:
   </p>
   <ul>
       <li>User can now provide either univseristy name or university url or department url. User can also specify University Name and Department name together.</li>
       <li>The Admin interface receives input from user and asynchronously responds to user that the database will be updated eventually. This is `eventual consistancy` model. If user closes browser backend server will still be processing the the crawling and scraping.</li>
       <li>User can keep entering multiple requests one after another and system will eventually process one after another in the background. There is no dependency with browser session. Although the system overall performance and security loopholes are out of scope for this project.</li>
       <li>As soon system extract biodata for the faculty url, it then extracts structured data using text retrieval and topic mining techniques and saves in database as structured data.</li>
   </ul>
   <p>The existing ExpertSearch system doesn't have these robust, user friendly functionalities. The existing system doesn't also have mechanism to extract structured data from unstructured dataset.</p>
   <img/>
</details>     

<details>
   <summary>Added more filter criteria. Click to learn more.</summary>
   <br/>
   <p>ExpertSearch v2.0 maintains strictured data set in database. Based on search query with filters we can retrieve all saved biodata matching the filters and apply ranking to only filtered biodata set for a specific query. 
   Hence the new system able to offer more filter criterias comapared to the existing ExpertSearch system</p>
   <img/>
</details>     

<details>
   <summary>Improved search results with consistant display of the faculty attributes. Click to learn more.</summary>
   <br/>
   <p>New ExpertSearch v2.0 leverages the structured data to display faculty attributes in the search results display page. 
   The old ExpertSearch did runtime operations which A. makes the system slower for heavy text retrival techniques and B. missed few modern text retrival techniques for extracting fields such as department name, phone number etc.  
   We leveraged both browser provided information in html element such as "title" which mostly provides unique info. 
   We also improved the regex for extracting accurate phone numbers, email etc. 
   Since these operations are done during crawling and scraping and saved into database as structured data, hence during actual query based on the ranking results the data is fetched from database. 
   The overall improved process resulted in improved search results and faculty attributes display with no missing information thus improving consistancy.
   </p>
   <img alt="ExpertSearch Documentation Comparison" src="docs/assets/comparison_python_version.png?raw=true"/>
</details>     

<details>
   <summary>Major System upgrade from Python2.7 to Python3.9. Click to learn more.</summary>
   <br/>
   <p>New ExpertSearch v2.0 is build on latest Python3.9 and dependent packages compared to the existing ExpertSearch that is build on old and out of support Python2.7.
   With that said the team went through many research and exploration phases as few of the NLP / Text Processing libraries from old system aren't supported in Python3.9 version.
   New and modern standard libraries were tested and adopted (such as nltk, gensim etc.) and then enginnered to fit the logic of ranking, scoring, topic mining and text retrieval techniques in the new ExpertSearch v2.0 system.
   In summary, all capabilities of existing ExpertSearch system have been covered by ExpertSearch v2.0 plus additional features also offered all with new set of Python3.9 libraries which by itself is a great achievement.       
   </p>
   <img alt="ExpertSearch Documentation Comparison" src="docs/assets/comparison_python_version.png?raw=true"/>
</details>     

<details>
   <summary>Documentation and Artifacts for future development. Click to learn more</summary>
   <br/>
   <p>The new ExpertSearchv2.0 comes with well documented modules, functions and modularized codes that overall improves the readability. 
   There are also design artifacts in terms of workflow diagrams that were generated for users to understand the features and funciotnality of the code. 
   This will encourage better participation for future development. 
   When compared to the existing ExpertSeach the existing web application has almost zero documentaion and artifacts which made it very difficult for code analysis, code reusability and increased the overall development window for enhancements. 
   Below snapshot demonstrates a good comparison between the existing and new ExpertSearch.
   </p>
   <img alt="ExpertSearch Documentation Comparison" src="docs/assets/comparison_documentation.png?raw=true"/>
</details>     

<div style="text-align: right"> <a href="#top">Back to top</a> </div>

## Technologies
Below are the main technologies that were used to build ExpertSearch v2.0 
* Python3.9
* Modern text Retrieval and Text Mining techniques
* Webpages crawling and scraping
* NLP Libraries - NLTK, Gensim
* Redis Cluster
* Sqlite3 Database
* Web technologies like HTML, CSS, JQuery
* Flask based web server
 
## Hardware Requirements
1. Modern Operating System  [Minimum]\
Linux or MacOS  **[Recommended]**

2. x86 64-bit CPU  [Minimum] \
x86 64-bit CPU Multi Core **[Recommended]** 

3. 8 GB RAM  [Minimum]\
16 GB RAM  **[Recommended]**

4. 5 GB free disk space

<div style="text-align: right"> <a href="#top">Back to top</a> </div>

## Access and Permission Requirements

1. Access to the terminal window

2. A user with admin-level privileges

<div style="text-align: right"> <a href="#top">Back to top</a> </div>

## Software Requirements

1. Chrome Browser, Version 96+ and above
   * [Download and Install Chrome on MacOS](https://www.google.com/chrome/)
   * [Download and Install Chrome on Linux](https://linuxconfig.org/how-to-install-google-chrome-browser-on-linux)
 
2. Python3.9. 
   * Virtual environment is recommended.
   * [MacOS Conda Installation Guide](https://www.anaconda.com/products/individual) or [Linux Conda Installation Guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html)
   * [Managing Conda - Install python virtual environment using Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) 
   
   Run the below command in virtual environment and Make sure you have installed Python3.9.X.
   ```shell script
   python --version
   ````
      
3. `pip` package installed in python3.9 virtual environment  - _Should be default wiith Python3.9_   
   * To install pip on your virtual environment run below command
   ```shell script
   conda install pip 
    ````
4. git cli tool
    * [Install git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)   

<div style="text-align: right"> <a href="#top">Back to top</a> </div>

## Setup

1. Using Redis

   Installing Redis on MacOS or Linux
   ```shell script
   # get the stable version of redis 
   wget http://download.redis.io/redis-stable.tar.gz
  
   # extract 
   tar xvzf redis-stable.tar.gz
   cd redis-stable
  
   # install 
   make
   ```
      
2. Using git clone the repository to a path
   ```shell script
   cd <desired path where you want to download the project>
   git clone https://github.com/sudiptobilu/CourseProject.git
   cd CourseProject

3. Set Environemnt Variable\
   [Click Here](https://cmt3.research.microsoft.com/CS410Expo2021/Submission/Summary/56) to get the Google API Key from the [CMT](https://cmt3.research.microsoft.com/CS410Expo2021/Submission/Summary/56) Abstract section (Make sure you are in reviewer role. Credentials required). \
    Add the below line in your `~/.basrc` or `~/.bash_profile` 
    ```shell script
    export GOOGLE_API_KEY=<Add Google api Key from CMT Abstract section>
    ```
    Also create a `.env` file in project root directory and add the GOOGLE_API_KEY. Run the below commands
    ```shell script
    cd <path to CourseProject repo>
   
    echo "GOOGLE_API_KEY='<Add Google api Key from CMT Abstract section>'" > .env   
    ```  
    
4. Switch to the Python3.9 virtual environemnt\
   If using Conda,
   ```shell script
   # TIP: Show all conda environemt
   conda env list   
   
   # pick the Python3.9 environment name from the above output. Then run
   conda activate <python3.9 virtual environment name> 
   ```

5. Install the project requirements file on Python3.9 virtual environment
    ```shell script
    pip install -r requirements.txt
    ```
<div style="text-align: right"> <a href="#top">Back to top</a> </div>

## Deploy
1. Start Redis Server

    For MacOS or Linux 
    ```shell script
    cd <path to redis-stable>
    redis-server
    ````

2. Make sure you are on the Python3.9 environment. 
    ```shell script
   python --version
    ````

3. From the project directory, Run the below command 
    ```shell script
    # go to project directory root level
    cd <path to CourseProject repo>
    cd apps/frontend
   
    python server.py
    ````
4. Open Chrome browser and browse the below url
    ```shell script
   http://localhost:8095
    ````
5. The browser should show up ExpertSearchv2.0 search application 

:exclamation: A comprehensive software usage [video presentation](https://uofi.app.box.com/file/893368706848?s=ealry89ittv21gz2x30bn2lrw319vhnw) is also available. [Click Here](https://uofi.app.box.com/file/893368706848?s=ealry89ittv21gz2x30bn2lrw319vhnw)

<div style="text-align: right"> <a href="#top">Back to top</a> </div>

## Implementation Details 

#### ExpertSearchv2.0 Admin Functionality
- - - - 
<details>
   <summary>Click to See the Workflow Diagram of Search Functionalty</summary>
   <br/>
   <img alt="ExpertSearch Admin Functionality Workflow" src="docs/workflows/images/search.jpg?raw=true"/>
</details>

#### ExpertSearchv2.0 Search Functionality

* For search functionality the front end file is located at [web/templates/index.html](web/templates/index.html)
* User enters query to the html file (user can provide filters too) which is passed to the backend Flask server [apps/frontend/server.py::search()](apps/frontend/server.py) as a http request
* The server receives the query string and calls [apps/frontend/server.py::search()](apps/frontend/server.py)
* The `search` inturn calls an orchestration function [apps/backend/api/search.py::get_search_results()](apps/backend/api/search.py)
* The `get_search_results` is an orchestration function and calls different backend systems to retrieve the data
    * The call first goes to [apps/backend/utils/facultydb.py::get_biodata_records()](apps/backend/utils/facultydb.py) and grabs all scrpaed biodata stored in a database table column andlong with correspinding structured data id.
    * Then the corpus data is passed to [apps/backend/utils/ranker.py::score()](apps/backend/utils/ranker.py) to score the corpus biodate dataset based on search query. The function used BM25 as text retrieval alogorithm to rank corpus documents.
    * Once ranking is done the corresponding structured data ids were returned as a ranked list of faculty ids 
    * The ranked ids were taken and passed to [apps/backend/utils/facultydb.py::get_faculty_records()](apps/backend/utils/facultydb.py) to get the structured data from database
* The results dataset is now a structured data with key pair values and being disp;ayed in the front end accordingly
* The benefit of diplaying structured data is consistancy in displaying results and all the attributes and allowing actions on them. (for e.g. send email, explore location etc.)
* :warning: The entire workflow and code discussed above is all new work in the ExpertSearch v2.0 that has been done. Tasks involved adapting new libraries for Python3.9, explorations, PoCs, and then designining an effctive workflow and implementing it.   
       
   
- - - - 
<details>
   <summary>Click to See the Workflow Diagram of Admin Functionalty</summary>
   <br/>
   <img alt="ExpertSearch Admin Functionality Workflow" src="docs/workflows/images/admin.jpg?raw=true"/>
</details>

<div style="text-align: right"> <a href="#top">Back to top</a> </div>

## Project Team Members

Name             |  NetID  |  Email
| :---  | :--- | :---  
Ujjal Saha  | ujjals2 | ujjals2@illinois.edu 
Arnab KarSarkar | arnabk2 | arnabk2@illinois.edu
Sudipto Sarkar | sudipto2 | sudipto2@illinois.edu

<div style="text-align: right"> <a href="#top">Back to top</a> </div>

## User Stories and Contributions

- - - - 
1. **Epic: Crawling and Scraping** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; _(Contributions :clap: &nbsp;&nbsp;: Arnab KarSarkar, Ujjal Saha)_
    <details>
       <summary><b>User Story: </b> Crawler Implementation for a given webpage url. Click for Story Details</summary>
       <br/>
       <p>In the admin interface when admin inputs an url, this story takes the url as input and scrapes the page and extracts the faculty biodata. We also implemented intelligent logic in scraper to find right faculty page if the base url has links that leads to multiple faculty related pages.</p>
    </details>     

    <details>
       <summary><b>User Story: </b> Adding admin interface for web page indexing. Click for Story Details</summary>
       <br/>
       <p>As our project scope doesn’t include auto crawler features for the entire web, the admin interface we are implementing in ExpertSearch system is to allow the admin to enter base url of the universities and based on valid/invalid university email (different story) the admin interface will fetch the url to the crawler module to scrape faculty data.</p>
    </details>     
    
    <details>
       <summary><b>User Story: </b> Displaying accepted/rejected web page based on url. Click for Story Details</summary>
       <br/>
       <p>When admin enters the base url, this module will check if the url is a valid university url. If yes, the module forwards the url for crawling and scraping the faculty pages. If not, the module lets the admin know that base url doesn’t belong to a university or no faculty page found.</p>
    </details>     
    
- - - - 

2. **Epic: Search Experience Enhancement using Text Retrieval Techniques** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; _(Contributions :clap: &nbsp;&nbsp;: Ujjal Saha, Sudipto Sarkar)_
    <details>
       <summary><b>User Story: </b> Build a structured dataset from Unstructured datasets. Click for Story Details</summary>
       <br/>
       <p>In current ExpertSearch system the faculty data are stored as unstructured data as a file. We are implementing a functionality that will convert the unstructured data to structured data. For e.g., using text mining and text retrieval techniques we are planning to extract fields like Faculty Name, Department, University, Area of Interests, email, phone, etc, and store them in a structured form (either in csv, or database etc.) This will enhance the overall search experience.</p>
    </details>     
     
    <details>
       <summary><b>User Story: </b> Enhance the search experience with relevant search results. Click for Story Details</summary>
       <br/>
       <p>Based on search input, we will look up all biodata from structured dataset and implement a ranking function using metapy. Based on ranking results we will extract corresponding fields from the structured data and display as search results. We will enhance filter based searching feature too where user can get better accuracy because of structured dataset.</p>
    </details>     
      
    <details>
       <summary><b>User Story: </b> Better consistency in displaying attributes leveraging structured data. Click for Story Details</summary>
       <br/>
       <p>The current expert search system doesn’t show contact info (email, etc.) consistently across the search results even if the faulty page does have the data. Our improved scraping and structured data along with improved data display logic will increase the consistency in displaying the fields in search results.</p>
    </details>     

- - - - 

3. **Epic: Topic Mining** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; _(Contributions :clap: &nbsp;&nbsp;: Sudipto Sarkar, Arnab KarSarkar)_   

    <details>
       <summary><b>User Story: </b> Using text mining extract interest areas of a faculty. Click for Story Details</summary>
       <br/>
       <p>Using text mining methods we are planning to generate “Areas of Interests” data from the faculty bio. We are using guided LDA algorithm and Gensim/NLTK libraries to explore other topic mining features and we will be experimenting with parameters to generate relevant topics.</p>
    </details>     
    
    <details>
       <summary><b>User Story: </b> Display Areas of Interest in the faculty search result. Click for Story Details</summary>
       <br/>
       <p>We are enhancing the front end of ExpertSearch to display faculty search results along with additional relevant fields such as faculty areas of interest and few more.</p>
    </details>     

- - - - 

4. **Epic: Deployment** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; _(Contributions :clap: &nbsp;&nbsp;: Arnab KarSarkar, Ujjal Saha, Sudipto Sarkar)_

    <details>
       <summary><b>User Story: </b> Understand and Install current ExpertSearch System. Click for Story Details</summary>
       <br/>
       <p>Install and explore the ExpertSearch system and understand the features and functionalities (both frontend and backend). Experiment with code changes etc.</p>
    </details>     
 
    <details>
       <summary><b>User Story: </b> Deploy code into AWS. Click for Story Details</summary>
       <br/>
       <p>Being web-based framework, we will do our deployments in AWS Cloud and make it public. We will also do a git PR on the existing original ExpertSearch repo. But launching as an improved system and others to validate, we will separately host ExpertSearchv2.0 in AWS.</p>
    </details>     

    <details>
       <summary><b>User Story: </b> Validation Exercises. Click for Story Details</summary>
       <br/>
       <p>As we do development and deployment, we are doing multiple rounds of verification and validation and some will require integrated end-to-end validation steps.</p>
    </details>     

- - - - 

5. **Epic: Documentation and Presentation** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; _(Contributions :clap: &nbsp;&nbsp;: Ujjal Saha, Sudipto Sarkar, Arnab KarSarkar)_   

    **User Story**: Proposal Documentation 
       
    **User Story**: project Progress Documentation
    
    **User Story**: Final Project Report Documentation  
    
    **User Story**: Final Project Video Presentation  

- - - - 

    

<div style="text-align: right"> <a href="#top">Back to top</a> </div>

## Improvements Areas
* Crawling and Scraping activites can be tracked if implemeted a publisher and subscriber. We didn't do it as it wont add much value of our goal and focus on Text Retrieval and Mining techniques.  
* GuidedLDA couldn't be used for specialized topic mining and we settled with general LDA. Specialized Topic mining could result is more relevant topic wouds for a faculty.
* Admin interface repeated entry can be malacious and need to implement some sort of restrictions
* Making the webapp perfect in terms of end-to-end best user experience was not part of the goal for this project. The webapp still has got many improvement areas in terms of UX, UI display, communication, request response, industry standards, completeness which could be a separate project by itself.
 

## Licensing
The ExpoertSearch v2.0 was build upon existing ExpertSearch web application [[1]](https://github.com/CS410Assignments/ExpertSearch) and thus will inherit the original licensing terms and condistions of the original ExpertSearch system.  

## Acknowledgements
* Our special thanks to [Prof. Cheng Zhai](http://czhai.cs.illinois.edu/) and all the TAs in CS410 Text Information Systems Course for making the course engaging and help with all the queries.
* Many thanks to original creators of existing ExpertSearch web application [[1]](https://github.com/CS410Assignments/ExpertSearch) application and letting others build on top of it.
* Also thanks to our open source community contributors for so many contributions in NLP, Text Retrieval and Text Mining based python packages which are effective, efficient and free to use.
* Thanks to our project team members and project reviewers too for wonderful collboration and feedback and making the project successful.      
* Special thanks for University of Illinois - Urbana Champaign for providing students with endless software tools, collaboration mediums and resources such as box, sharepoint, google drive, library, zoom, slack, campuswire and many more. The availability of these tools help online students a lot.      
## References
[1] [Existing ExpertSearch web application](https://github.com/CS410Assignments/ExpertSearch)\
[2] [Coursera - CS410 Text information Systems - Course Project Overview](https://www.coursera.org/learn/cs-410/supplement/fTuOi/course-project-overview)\
[3] [NLTK API Reference](https://www.nltk.org/api/nltk.html)\
[4] [Gensim API Reference](https://radimrehurek.com/gensim/apiref.html)\
[5] [BM25 Ranker](https://github.com/dorianbrown/rank_bm25)\
[6] [Flask + Bootstrap. HTML interface for effortless Python projects](https://diyprojects.io/flask-bootstrap-html-interface-effortless-python-projects/#.YbEIE33MLok)\
[7] [AWS Cloud Hosting Service - EC2](https://aws.amazon.com/application-hosting/)\
[8] [Github ReadMe - Basic writing and formatting syntax](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)

<div style="text-align: right"> <a href="#top">Back to top</a> </div>
