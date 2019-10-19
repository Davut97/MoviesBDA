import requests
import  json
import  SearchFunction
from string import Template
def findid():
    pages = 1
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=9902b134582ad4ddad59aa7e54a5164f&sort_by=revenue.desc&certification_country=US&page=$pages'
    urlTemplate = Template(url)
    arrID=[]                    # initiliaz the IDs array
    while (pages <= 200):
        url2 = urlTemplate.substitute(pages=pages)
        response = requests.get(url2)
        data = json.loads(response.text)
        arrID += SearchFunction.extract_element_from_json(data, ['results', 'id'])  # array of titles
        print("fininsd page: " + str(pages))
        pages = pages+1

    print(len(arrID))
    return arrID


