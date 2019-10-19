from string import Template
import requests
import  json
import  csv
from ss import findid
def writeArrayToCsv(FileName,data):                                     # write into the csv file
    with open(FileName, 'w', newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)


urlDiscoveries= 'https://api.themoviedb.org/3/movie/$id?api_key=9902b134582ad4ddad59aa7e54a5164f'
urlTemplate2 = Template(urlDiscoveries)
csvData=[["Title","Budget","Revenue"]]
arrID2 =findid()
for i in arrID2:
    id = i
    urlDiscoveries2=urlTemplate2.substitute(id =id)
    response = requests.get(urlDiscoveries2)
    data2 = json.loads(response.text)
    title = data2['original_title']
    budget = data2['budget']
    revenue = data2['revenue']
    csvData.append([title,budget,revenue])

writeArrayToCsv('Movies.csv',csvData)





