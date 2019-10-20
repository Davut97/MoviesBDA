from string import Template
import requests
import json
from Utils import get_movies_id, write_array_to_csv, extract_element_from_json

# region Generate File and fill budget and revenue data
urlDiscoveries = 'https://api.themoviedb.org/3/movie/$id?api_key=9902b134582ad4ddad59aa7e54a5164f'
urlTemplate2 = Template(urlDiscoveries)
csvData = [["Title", "Budget", "Revenue"]]
arrID2 = get_movies_id()
for i in arrID2:
    id = i

    urlDiscoveries2 = urlTemplate2.substitute(id=id)
    response = requests.get(urlDiscoveries2)
    data2 = json.loads(response.text)

    try:
        title = data2['original_title']
        print(data2['original_title'])
    except:
        title = ["NA"]
    try:
        budget = data2['budget']
    except:
        budget = [""]
    try:
        revenue = data2['revenue']
    except:
        revenue = [""]
    csvData.append([title, budget, revenue])

write_array_to_csv('Movies.csv', csvData)
# endregion

