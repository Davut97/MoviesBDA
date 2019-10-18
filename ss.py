import requests
import  json
import  SearchFunction
from string import Template
import  csv
pages = 1
url = 'https://api.themoviedb.org/3/discover/movie?api_key=9902b134582ad4ddad59aa7e54a5164f&page=$pages'
urlTemplate = Template(url)
arrT = []
while (pages <= 10):
    url2 = urlTemplate.substitute(pages=pages)
    response = requests.get(url2)
    data = json.loads(response.text)
    arrT += SearchFunction.extract_element_from_json(data, ['results', 'id'])  # array of titles
    for i in arrT:
         print(i)
    pages = pages+1
print(len(arrT))
id=arrT[0]
print(id)
urlDiscoveries= 'https://api.themoviedb.org/3/movie/$id?api_key=9902b134582ad4ddad59aa7e54a5164f'
urlTemplate2 = Template(urlDiscoveries)
urlDiscoveries2=urlTemplate2.substitute(id =id)
response = requests.get(urlDiscoveries)
data2 = json.loads(response.text)
print(data2)
for i in arrT:

    with open('Movies-ID.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow([i])
    csvFile.close()
