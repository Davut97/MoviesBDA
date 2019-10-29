from string import Template
from requests import get
import json
import os.path
import pandas as pd

from Utils import get_movies_id, write_array_to_csv, extract_element_from_json

omdb_url = Template('http://www.omdbapi.com/?apikey=13750151&t=$title')
urlDiscoveries = Template('https://api.themoviedb.org/3/movie/$id?api_key=9902b134582ad4ddad59aa7e54a5164f')


# region Generate File and fill budget and revenue data: create_movie_file()
# <summery> Create Movie File if doesn't exist fills Title + Budget + Revenue Data </summery>
# <para></para>
# <return> # of data rows created. Returns 0 if file exist</return>
def create_movie_file():
    # Check if the file exists first, if not get the ids and create it
    if not os.path.exists("Movies.csv"):
        csvData = [["Title", "Budget", "Revenue","Date","Runtime"]]
        arrID2 = get_movies_id()
        for i in arrID2:
            id = i

            urlDiscoveries2 = urlDiscoveries.substitute(id=id)
            response = get(urlDiscoveries2)
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
            try:
                Date = data2["release_date"]
            except:
                Date = [""]
            try:
                runtime=data2["runtime"]
            except:
                runtime=[""]
            csvData.append([title, budget, revenue,Date,runtime])

        write_array_to_csv('Movies.csv', csvData)
        return len(csvData)
    return 0


# endregion


# region Fill the movies rows with data from OMDB API: fill_with_data()
# <summery> Fills the movie list with Data </summery>
# <para>File path as string</para>
# <return> Count of rows effected. returns -1 if file not found </return>
def fill_with_data(file_path):
    try:
        Movies_Data = pd.read_csv(file_path)
    except FileNotFoundError:
        print(FileNotFoundError)
        return -1

    new_columns = ['Year', 'Rated', 'Genre', 'Director', 'Writer', 'Actors', 'Language',
                   'Country', 'Awards', 'Metascore', 'imdbRating', 'imdbVotes', 'Production']
    Movies_Data = Movies_Data.reindex(columns=Movies_Data.columns.tolist())
    counter = 0
    Movies_Data = Movies_Data.astype(str)
    for i in Movies_Data.itertuples():
        url = omdb_url.substitute(title=i.Title)
        response = get(url)
        try:
            movie = json.loads(response.text)
            counter += 1
        except Exception as err:
            print(err)
            continue
        if movie["Response"] == 'True':
            print("Adding " + movie["Title"])
            for column in new_columns:
                try:
                    print("Trying to add column " + column)
                    Movies_Data.at[i.Index, column] = movie[column]
                    print("Added: ", column)
                except Exception as e:
                    print("Failed to add Column " + column)
                    print(e)
                    Movies_Data.at[i.Index, column] = ''
        else:
            print("Server Error: " + movie["Error"])
        print("*************************************")
        print("Finished Movie")
        print("*************************************")

    Movies_Data.to_csv(file_path, index=False)
    return counter


# endregion


create_movie_file()
filePath = "C:/Users/owes4/Desktop/Thıs Wıll Work/Movies.csv"
print(fill_with_data(filePath))

