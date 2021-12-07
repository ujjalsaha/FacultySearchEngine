#  ExpertSearch v2.0

## Abstract

The existing ExpertSearch system (https://github.com/CS410Assignments/ExpertSearch) has several features such as faculty search, filtering criterions, search results (with options to open faculty bio pages, emailing, location info), pagination etc. As a team, we did a deep analysis of the ExpertSearch capabilities and found several deficiencies that need to be addressed to make it a better search system. The deficiencies include lack of accuracy, lack of relevant search results and inconsistencies in the search results. These deficiencies can be addressed using the text retrieval and text mining techniques that will improve the overall search experience in the ExpertSearch system. The team will be involved in implementing features such as converting unstructured dataset to structured dataset (e.g., csv, json), identifying the key topics (e.g., areas of interest) for each of the faculties and display in the search result, introducing an admin interface that would classify faculty pages and finally improving some of the existing features in the search page for better search experience.

## Hardware Requirements
1. Modern Operating System  [Minimum]\
Linux or MacOS  **[Recommended]**

2. x86 64-bit CPU  [Minimum] \
x86 64-bit CPU Multi Core **[Recommended]** 

3. 8 GB RAM  [Minimum]\
16 GB RAM  **[Recommended]**

4. 5 GB free disk space

## Software Requirements

1. Chrome Browser, Version 96+ and above
 
2. Python3.9 virtual environment
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


## Setup

1. Set Environemnt Variable\
   [Click Here](https://cmt3.research.microsoft.com/CS410Expo2021/Submission/Summary/56) to get the Google API Key from the [CMT](https://cmt3.research.microsoft.com/CS410Expo2021/Submission/Summary/56) Abstract section (Make sure you are in reviewer role. Credentials required). \
    Add the below line in your `~/.basrc` or `~/.bash_profile` 
    ```shell script
    export GOOGLE_API_KEY=<Add Google api Key from CMT Abstract section>
    ```
    If using PyCharm, Pycharm Menu --> Preferences --> Build, Execution, Deployment --> Python Console --> Environment Variables: --> Add `GOOGLE_API_KEY=<Add Google api Key from CMT Abstract section>` --> Ok  

2. Using git clone the repository to a path
   ```shell script
   cd <desired path where you want to download the project>
   git clone https://github.com/sudiptobilu/CourseProject.git
   cd CourseProject
   ```

3. Switch to the Python3.9 virtual environemnt\
   If using Conda,
   ```shell script
   # TIP: Show all conda environemt
   conda env list   
   
   # pick the Python3.9 environment name from the above output. Then run
   conda activate <python3.9 virtual environment name> 
   ```

4. Install the project requirements file on Python3.9 virtual environment
    ```shell script
    pip install -r requirements.txt
    ```
5. Run the below command to launch the project
    ```shell script
   cd apps/frontend
   
    python server.py
    ````
6. Open Chrome browser and browse the below url
    ```shell script
   http://localhost:8095
    ````
7. The browser should show up ExpertSearchv2.0 search application 


## Workflows 

![alt text](docs/workflows/images/search.jpg?raw=true)
<br/>
<br/>
<br/>

![alt text](docs/workflows/images/admin.jpg?raw=true)

