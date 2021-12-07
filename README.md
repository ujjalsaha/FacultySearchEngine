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

1. Python3.9 virtual environment
   * [MacOS Conda Installation Guide](https://www.anaconda.com/products/individual) or [Linux Conda Installation Guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html) \
   * [Managing Conda - Install python virtual environment using Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
   
   \
   Run the below command in virtual environment and Make sure you have installed Python3.9.X.
   ```shell script
   python --version
   ````
   <br/> 
    
1. `pip` package installed in python3.9 virtual environment  - _Should be default wiith Python3.9_   
   * To install pip on your virtual environment run below command
   ```shell script
   conda install pip 
    ````
   <br/> 
    
2. git cli tool
    * [Install git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)   


## Setup

1. Set Environemnt Variable\
    `GOOGLE_API_KEY=<Add Google api Key>`
       
3. 




## Workflows 

![alt text](docs/workflows/images/search.jpg?raw=true)
<br/>
<br/>
<br/>

![alt text](docs/workflows/images/admin.jpg?raw=true)

