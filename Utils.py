# -*- coding: utf-8 -*-
import requests
import json
from string import Template
import csv

# gets a random list of movies
# and save each movie id in an array
# then it returns the array
def get_movies_id():
    pages = 1
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=9902b134582ad4ddad59aa7e54a5164f&sort_by=revenue.desc&certification_country=US&page=$pages'
    urlTemplate = Template(url)
    arrID = []  # initilias the IDs array
    while (pages <= 500):
        url2 = urlTemplate.substitute(pages=pages)
        response = requests.get(url2)
        data = json.loads(response.text)
        arrID += extract_element_from_json(data, ['results', 'id'])  # array of titles
        print("fininsd page: " + str(pages))
        pages = pages + 1

    print(len(arrID))
    return arrID


# write into the csv file
def write_array_to_csv(file_name, data):
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)


# Source: https://bcmullins.github.io/parsing-json-python/
def extract_element_from_json(obj, path):
    """
    Extracts an element from a nested dictionary or
    a list of nested dictionaries along a specified path.
    If the input is a dictionary, a list is returned.
    If the input is a list of dictionary, a list of lists is returned.
    obj - list or dict - input dictionary or list of dictionaries
    path - list - list of strings that form the path to the desired element
    """

    def extract(obj, path, ind, arr):
        """
            Extracts an element from a nested dictionary
            along a specified path and returns a list.
            obj - dict - input dictionary
            path - list - list of strings that form the JSON path
            ind - int - starting index
            arr - list - output list
        """
        key = path[ind]
        if ind + 1 < len(path):
            if isinstance(obj, dict):
                if key in obj.keys():
                    extract(obj.get(key), path, ind + 1, arr)
                else:
                    arr.append(None)
            elif isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        extract(item, path, ind, arr)
            else:
                arr.append(None)
        if ind + 1 == len(path):
            if isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        arr.append(item.get(key, None))
            elif isinstance(obj, dict):
                arr.append(obj.get(key, None))
            else:
                arr.append(None)
        return arr

    if isinstance(obj, dict):
        return extract(obj, path, 0, [])
    elif isinstance(obj, list):
        outer_arr = []
        for item in obj:
            outer_arr.append(extract(item, path, 0, []))
        return outer_arr

# checks if the string in english or not
def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True
