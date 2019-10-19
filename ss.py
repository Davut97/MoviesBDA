import requests
import  json
import  SearchFunction
from string import Template
import  csv

def findid():
    pages = 1
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=9902b134582ad4ddad59aa7e54a5164f&page=$pages'
    urlTemplate = Template(url)
    arrID=[]                    # initiliaz the IDs array
    while (pages <= 2):
        url2 = urlTemplate.substitute(pages=pages)
        response = requests.get(url2)
        data = json.loads(response.text)
        arrID += SearchFunction.extract_element_from_json(data, ['results', 'id'])  # array of titles
        pages = pages+1
    print(len(arrID))
    return arrID

