import os
import requests
import pymongo
import urllib.parse
from bs4 import BeautifulSoup
from pymongo import MongoClient


def db_connection():
    mongopasswd = os.environ["MONGOPASSWD"]

    cluster = MongoClient("mongodb+srv://user:"+mongopasswd+"@packagescluster.3irbh.mongodb.net/test?retryWrites=true&w=majority")
    db = cluster['flask_packages_db']
    collection = db['flask_packages_collection']
    #collection.create_index([("name", pymongo.TEXT)], unique=True) LO CREE EN COMPASS

    search_packages(collection)

def search_packages(collection):
    count2 = 0 # Counter for packages (Use as ID for db)
    count = 0 # Counter for search pages in pypy.org
    while count < 41:
        count = count+1
        url = 'https://pypi.org/search/?c=Framework+%3A%3A+Flask&o=&q=&page='+str(count)
        
        r = requests.get(url)

        soup = BeautifulSoup(r.content, 'html.parser')
        
        all_packages = soup.find_all('h3',{'class':'package-snippet__title'}) 
        
        # all_packages is the information of all packages in a page.

        for package_info in all_packages: ## sacar count2 de id 
            count2 = count2 + 1
            
            ### NAME ###
            name = package_info.find('span',{'class':'package-snippet__name'}).text
            # Search the name of the package in the db, if exists, check information for updates. If not, add them to the db.
            find_on_db = list(collection.find({"name":name})) ### VOLVI A LA LISTA PQ NO LO PUDE HACER FUNCIONAR CON EL COL.FIND().COUNT()
            if find_on_db == []:
                add_package_to_db(package_info, name, collection)
            else:
                update_package_on_db(package_info, name, collection)

def add_package_to_db(package_info, name, collection):
    
    ENDC = '\033[m'
    TYELLOW = '\033[93m'
    print(TYELLOW + "agregando: ",name, ENDC)

    try:
        version = package_info.find('span',{'class':'package-snippet__version'}).text
    except:
        version = ""
    
    released = package_info.find('span',{'class':'package-snippet__released'}).text.strip()

    project_url = 'https://pypi.org/project/'
    
    project_url = urllib.parse.urljoin(project_url, name)

    response = requests.get(project_url)

    soup = BeautifulSoup(response.content, 'html.parser')

    find_description = soup.find_all('div',{'class':'project-description'})

    if find_description == []:
        description = ""
    else:
        description = str(find_description[0])

    try:
        homepage_info = soup.find('a', {'class':'vertical-tabs__tab vertical-tabs__tab--with-icon vertical-tabs__tab--condensed'})
        homepage_link = homepage_info["href"]
    except:
        homepage_link = ""

    maintainer_find = soup.find('span',{'class':'sidebar-section__user-gravatar-text'})
    maintainer = maintainer_find.text.strip()

    package = {
        "name":name,
        "description":description,
        "version":[version],
        "maintainer":maintainer,
        "released":released,
        "homepage":homepage_link
    }
    collection.insert_one(package)

def update_package_on_db(package_info, name, collection):
    ENDC = '\033[m'
    TGREEN = '\033[32m'
    print(TGREEN + "actulizando",name, ENDC)

    ### NO PODEMOS HACER UN APPEND A UN CURSOR DE MONGO

    ### VERSION ###
    
    #try:
    version = package_info.find('span',{'class':'package-snippet__version'}).text
    search = collection.find({"name":name})
    for item in search:
        version_db = item["version"]
    if version == version_db[0]:
        return
    version = ""
    print('siguio')
    old_package = []
    old_package["version"].append(version)
    ### RELEASED ###
    released = package_info.find('span',{'class':'package-snippet__released'}).text.strip()
    old_package["released"] = released

    project_url = 'https://pypi.org/project/'
    
    project_url = urllib.parse.urljoin(project_url, name)

    response = requests.get(project_url)

    soup = BeautifulSoup(response.content, 'html.parser')
    
    ### DESCRIPTION ###
    
    find_description = soup.find_all('div',{'class':'project-description'})

    if find_description == []:
        description = ""
    else:
        description = str(find_description[0])

    old_package["description"] = description

    
    ### HOMEPAGE LINK ###

    try:
        homepage_info = soup.find('a', {'class':'vertical-tabs__tab vertical-tabs__tab--with-icon vertical-tabs__tab--condensed'})
        homepage_link = homepage_info["href"]
    except:
        homepage_link = ""

    old_package["homepage"] = homepage_link

    ### MAINTAINER ###

    maintainer_find = soup.find('span',{'class':'sidebar-section__user-gravatar-text'})
    maintainer = maintainer_find.text.strip()

    old_package["maintainer"] = maintainer
    collection.update_one({'name': name}, {'$set': old_package})

if __name__ == "__main__":
    db_connection()


    ### DEVOLVER ESTO 
    ### https://pypi.org/project/cinq-auditor-vpc-flowlogs/2.1.1/#files OBTENER SHA256 y LINK`