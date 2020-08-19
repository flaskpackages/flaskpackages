import os
import requests
import urllib.parse
import datetime
from bs4 import BeautifulSoup
from pymongo import MongoClient


def db_connection():
    mongopasswd = os.environ["DBPASSWD"]

    cluster = MongoClient("mongodb+srv://user:"+mongopasswd+"@packagescluster.3irbh.mongodb.net/test?retryWrites=true&w=majority")
    db = cluster['flask_db']

    search_packages(db)


def search_packages(db):

    collection = db['flask_packages']

    count = 0  # Counter for search pages in pypy.org
    while count < 42:
        count = count+1
        url = 'https://pypi.org/search/?c=Framework+%3A%3A+Flask&o=&q=&page='+str(count)

        r = requests.get(url)

        soup = BeautifulSoup(r.content, 'html.parser')

        all_packages = soup.find_all('h3', {'class': 'package-snippet__title'})

        # all_packages is the information of all packages in a page.
        for package_info in all_packages:
            # NAME
            name = package_info.find('span', {'class': 'package-snippet__name'}).text
            # Search the name of the package in the db.
            # if exists, check information for updates.
            # If not, add them to the db.
            find_on_db = list(collection.find({"name": name}))

            if find_on_db == []:
                add_package_to_db(package_info, name, collection)
            else:
                update_package_on_db(package_info, name, collection)


def add_package_to_db(package_info, name, collection):

    ENDC = '\033[m'
    TYELLOW = '\033[93m'
    print(TYELLOW + "agregando: ", name, ENDC)

    lastest_version = package_info.find('span', {'class': 'package-snippet__version'}).text

    project_url = 'https://pypi.org/project/'

    project_url = urllib.parse.urljoin(project_url, name)

    response = requests.get(project_url)

    soup = BeautifulSoup(response.content, 'html.parser')

    find_description = soup.find_all('div', {'class': 'project-description'})

    if find_description == []:
        description = ""
    else:
        description = str(find_description[0])

    try:
        homepage_info = soup.find('a', {'class': 'vertical-tabs__tab vertical-tabs__tab--with-icon vertical-tabs__tab--condensed'})
        homepage_link = homepage_info["href"]
    except:
        homepage_link = ""

    maintainer_find = soup.find('span', {'class': 'sidebar-section__user-gravatar-text'})
    maintainer = maintainer_find.text.strip()

    # LICENSE

    license = []
    meta_div = soup.find_all('div', {'class': 'sidebar-section'})
    for div in meta_div:
        for item in div:
            try:
                if item.text == 'Meta':
                    lice = div.find('p').text
                    lice = lice.split(':')
                    license.append(lice[-1])

            except:
                pass
    license = list(set(license))
    license = license[0]

    # CLASSIFIERS

    classifiers_div = soup.find('ul', {'class': 'sidebar-section__classifiers'})

    lis = classifiers_div.find_all('li')
    classifiers = {}
    for item in lis:
        if item.find('strong'):
            title = item.find('strong').text
            tag = item.find('a')
            tag = tag.text.strip()
            title = title.lower()
            title = title.replace(' ', '_')
            classifiers[title] = str(tag)

    # VERSIONS

    url = 'https://pypi.org/project/'
    add = '/#history'
    project_url_versions = urllib.parse.urljoin(url, name, add)

    response = requests.get(project_url_versions)

    soup = BeautifulSoup(response.text, 'lxml')
    versions_number = soup.findAll('a', {'class': ['card', 'release__card']})

    res = []

    for version in versions_number:
        try:
            version_number = version.find('p', {'class': 'release__version'}).text.strip()
            date_box = version.find('p', {'class': 'release__version-date'})
            date = date_box.find('time')['datetime']
            url = 'https://pypi.org/project/'+name+'/'+version_number+'/#files'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            link_block = soup.find('th', {'scope': 'row'})
            link = link_block.find('a')['href']
            url = 'https://pypi.org/project/'+name+'/'+version_number+'/#files'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            link_block = soup.find('th', {'scope': 'row'})

            try:
                link = link_block.find('a')['href']
                sha256 = soup.find('code').text
            except:
                version_number = (version_number.splitlines()[0])
                url = 'https://pypi.org/project/'+name+'/'+version_number+'/#files'
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'lxml')
                link_block = soup.find('th', {'scope': 'row'})
                link = link_block.find('a')['href']
                sha256 = soup.find('code').text
            res.append({
                         'version': version_number,
                         'date': date,
                         'link': link,
                         'sha256': sha256
                        })
        except:
            continue

    # RELEASED DATE
    find_released_date = package_info.find('span', {'class': 'package-snippet__released'}).text.strip()
    released_date = datetime.datetime.strptime(find_released_date, '%b %d, %Y')
    released_date = released_date.date()

    package = {
        "name": name,
        "description": description,
        "lastest_version": lastest_version,
        "versions": res,
        "maintainer": maintainer,
        "homepage": homepage_link,
        "classifiers": classifiers,
        "pypi_link": project_url,
        "released": str(released_date),
        "license": license
    }

    collection.insert_one(package)


def update_package_on_db(package_info, name, collection):
    # VERSION

    version = package_info.find('span', {'class': 'package-snippet__version'}).text
    search = collection.find({"name": name})
    for objects in search:
        version_db = (objects["lastest_version"])

    ENDC = '\033[m'
    TGREEN = '\033[32m'
    print(TGREEN + "actualizando", name, ENDC)
    print('db version: ', version_db)
    print('new version: ', version)

    if version == version_db:
        return

    old_package = collection.find_one({"name": name})

    old_package["lastest_version"] = version

    project_url = 'https://pypi.org/project/'

    project_url = urllib.parse.urljoin(project_url, name)

    response = requests.get(project_url)

    soup = BeautifulSoup(response.content, 'html.parser')

    # RELEASED DATE

    find_released_date = package_info.find('span', {'class': 'package-snippet__released'}).text.strip()
    released_date = datetime.datetime.strptime(find_released_date, '%b %d, %Y')
    released_date = released_date.date()

    # LICENSE
    license = []
    meta_div = soup.find_all('div', {'class': 'sidebar-section'})
    for div in meta_div:
        for item in div:
            try:
                if item.text == 'Meta':
                    lice = div.find('p').text
                    lice = lice.split(':')
                    license.append(lice[-1])

            except:
                pass
    license = list(set(license))
    license = license[0]

    # CLASSIFIERS

    all_packages = soup.find('ul', {'class': 'sidebar-section__classifiers'})

    lis = all_packages.find_all('li')
    classifiers = {}
    for item in lis:
        if item.find('strong'):
            title = item.find('strong').text
            all_tags = item.find_all('a')
            for tag in all_tags:
                tag = tag.text.strip()
                title = title.lower()
                title = title.replace(' ', '_')
            classifiers[title] = str(tag)

    # DESCRIPTION

    find_description = soup.find_all('div', {'class': 'project-description'})

    if find_description == []:
        description = ""
    else:
        description = str(find_description[0])

    old_package["description"] = description

    # HOMEPAGE LINK

    try:
        homepage_info = soup.find('a', {'class': 'vertical-tabs__tab vertical-tabs__tab--with-icon vertical-tabs__tab--condensed'})
        homepage_link = homepage_info["href"]
    except:
        homepage_link = ""

    old_package["homepage"] = homepage_link

    # MAINTAINER

    maintainer_find = soup.find('span', {'class': 'sidebar-section__user-gravatar-text'})
    maintainer = maintainer_find.text.strip()

    old_package["maintainer"] = maintainer

    # VERSIONS, DOWNLOAD LINK & SHA256

    url = 'https://pypi.org/project/'
    add = '/#history'
    project_url_versions = urllib.parse.urljoin(url, name, add)

    response = requests.get(project_url_versions)

    soup = BeautifulSoup(response.text, 'lxml')
    versions_number = soup.findAll('a', {'class': ['card', 'release__card']})

    res = []


    for version in versions_number:
        try:
            version_number = version.find('p', {'class': 'release__version'}).text.strip()
            if version_number == version_db:
                break
            date_box = version.find('p', {'class': 'release__version-date'})
            date = date_box.find('time')['datetime']
            url = 'https://pypi.org/project/'+name+'/'+version_number+'/#files'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            link_block = soup.find('th', {'scope': 'row'})
            link = link_block.find('a')['href']
            url = 'https://pypi.org/project/'+name+'/'+version_number+'/#files'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            link_block = soup.find('th', {'scope': 'row'})

            try:
                link = link_block.find('a')['href']
                sha256 = soup.find('code').text
            except:
                version_number = (version_number.splitlines()[0])
                url = 'https://pypi.org/project/'+name+'/'+version_number+'/#files'
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'lxml')
                link_block = soup.find('th', {'scope': 'row'})
                link = link_block.find('a')['href']
                sha256 = soup.find('code').text
        except:
            continue

        res.append({'version': version_number, 'date': date, 'link': link, 'sha256': sha256})

    old_package['pypi_link'] = project_url
    old_package['classifiers'] = classifiers
    old_package['versions'] = res
    old_package['license'] = str(license)
    old_package['released'] = str(released_date)
    old_package.pop('_id')
    collection.update_one({"name": name}, {'$set': old_package})


if __name__ == "__main__":
    db_connection()
