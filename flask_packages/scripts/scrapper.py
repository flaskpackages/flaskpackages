import os
import requests
import pymongo
import urllib.parse
from bs4 import BeautifulSoup
from pymongo import MongoClient


def db_connection():
    mongopasswd = os.environ["MONGOPASSWD"]

    cluster = MongoClient("mongodb+srv://user:"+mongopasswd+"@packagescluster.3irbh.mongodb.net/test?retryWrites=true&w=majority")
    db = cluster['flask_db']
    collection = db['flask_collection']

    search_packages(collection)

def search_packages(collection):
    count = 0 # Counter for search pages in pypy.org
    while count < 41:
        count = count+1
        url = 'https://pypi.org/search/?c=Framework+%3A%3A+Flask&o=&q=&page='+str(count)
        
        r = requests.get(url)

        soup = BeautifulSoup(r.content, 'html.parser')
        
        all_packages = soup.find_all('h3',{'class':'package-snippet__title'}) 
        
        # all_packages is the information of all packages in a page.

        for package_info in all_packages:         
            ### NAME ###
            name = package_info.find('span',{'class':'package-snippet__name'}).text
            # Search the name of the package in the db, if exists, check information for updates. If not, add them to the db.
            find_on_db = list(collection.find({"name":name})) 
            
            print(name)
            
            if find_on_db == []:
                add_package_to_db(package_info, name, collection)
            else:
                update_package_on_db(package_info, name, collection)

def add_package_to_db(package_info, name, collection):
    
    ENDC = '\033[m'
    TYELLOW = '\033[93m'
    print(TYELLOW + "agregando: ",name, ENDC)

    try:
        lastest_version = package_info.find('span',{'class':'package-snippet__version'}).text
    except:
        lastest_version = ""

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

    ### VERSIONS ###

    url = 'https://pypi.org/project/'
    add = '/#history'
    project_url = urllib.parse.urljoin(url, name, add)

    response = requests.get(project_url)

    soup = BeautifulSoup(response.text, 'lxml')
    versions_number = soup.findAll('a', {'class':['card', 'release__card']})
    
    res = []

    for version in versions_number:
        try:
            version_number = version.find('p',{'class':'release__version'}).text.strip()
            date_box = version.find('p',{'class':'release__version-date'})
            date = date_box.find('time')['datetime']
            url = 'https://pypi.org/project/'+name+'/'+version_number+'/#files'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            link_block = soup.find('th', {'scope':'row'})
            link = link_block.find('a')['href']
            url = 'https://pypi.org/project/'+name+'/'+version_number+'/#files'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            link_block = soup.find('th', {'scope':'row'})
        
            try:
                link = link_block.find('a')['href']
                sha256 = soup.find('code').text
            except:
                version_number = (version_number.splitlines()[0])
                url = 'https://pypi.org/project/'+name+'/'+version_number+'/#files'
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'lxml')
                link_block = soup.find('th', {'scope':'row'})
                link = link_block.find('a')['href']
                sha256 = soup.find('code').text 
            res.append({'version':version_number, 'date':date, 'link':link, 'sha256':sha256})
        except:
            continue

    ### DOWNLOAD LINK & SHA256 ###

    package = {
        "name":name,
        "description":description,
        "lastest_version":[lastest_version],
        "versions":res,
        "maintainer":maintainer,
        "homepage":homepage_link
    }

    collection.insert_one(package)

def update_package_on_db(package_info, name, collection):
    ### VERSION ###
    
    version = package_info.find('span',{'class':'package-snippet__version'}).text
    search = collection.find({"name":name})
    for item in search:
        version_db = (item["lastest_version"][-1])
    if version == version_db:
        return

    ENDC = '\033[m'
    TGREEN = '\033[32m'
    print(TGREEN + "actualizando",name, ENDC)
    print('db version: ', version_db)
    print('new version: ', version)
    old_package = collection.find_one({"name":name})
    
    old_package["lastest_version"].append(version)

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
    
    ### VERSIONS, DOWNLOAD LINK & SHA256 ###

    url = 'https://pypi.org/project/'
    add = '/#history'
    project_url = urllib.parse.urljoin(url, name, add)

    response = requests.get(project_url)

    soup = BeautifulSoup(response.text, 'lxml')
    versions_number = soup.findAll('a', {'class':['card', 'release__card']})
    
    res = []

    for version in versions_number:
        try:
            version_number = version.find('p',{'class':'release__version'}).text.strip()
            date_box = version.find('p',{'class':'release__version-date'})
            date = date_box.find('time')['datetime']
            url = 'https://pypi.org/project/'+name+'/'+version_number+'/#files'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            link_block = soup.find('th', {'scope':'row'})
            link = link_block.find('a')['href']
            url = 'https://pypi.org/project/'+name+'/'+version_number+'/#files'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            link_block = soup.find('th', {'scope':'row'})
        
            try:
                link = link_block.find('a')['href']
                sha256 = soup.find('code').text
            except:
                version_number = (version_number.splitlines()[0])
                url = 'https://pypi.org/project/'+name+'/'+version_number+'/#files'
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'lxml')
                link_block = soup.find('th', {'scope':'row'})
                link = link_block.find('a')['href']
                sha256 = soup.find('code').text 
            res.append({'version':version_number, 'date':date, 'link':link, 'sha256':sha256})
        except:
            continue

        res.append({'version':version_number, 'date':date, 'link':link, 'sha256':sha256})

    old_package["versions"] = res
    old_package.pop('_id')
    collection.update_one({"name":name},{'$set':old_package})


if __name__ == "__main__":
    db_connection()