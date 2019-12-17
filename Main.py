# -*- coding: utf-8 -*-
import json
import os.path
from string import Template

import pandas as pd
from requests import get

from Utils import get_movies_id, write_array_to_csv, isEnglish

omdb_url = Template('http://www.omdbapi.com/?apikey=13750151&t=$title')
urlDiscoveries = Template('https://api.themoviedb.org/3/movie/$id?api_key=9902b134582ad4ddad59aa7e54a5164f')
awards = pd.read_csv("academy-awards.csv")


# region Generate File and fill budget and revenue data: create_movie_file()
# <summery> Create Movie File if doesn't exist fills Title + Budget + Revenue Data </summery>
# <para></para>
# <return> # of data rows created. Returns 0 if file exist</return>
def create_movie_file():
    # Check if the file exists first, if not get the ids and create it
    if not os.path.exists("Raw Movies.csv"):
        csvData = [["Title", "Budget", "Revenue", "Date", "Runtime"]]
        arrID2 = get_movies_id()
        for i in arrID2:
            id = i

            urlDiscoveries2 = urlDiscoveries.substitute(id=id)
            response = get(urlDiscoveries2)
            data2 = json.loads(response.text)
            try:
                if not isEnglish(data2['original_title']):
                    continue
            except:
                continue
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
                runtime = data2["runtime"]
            except:
                runtime = [""]
            csvData.append([title, budget, revenue, Date, runtime])

        write_array_to_csv('Raw Movies.csv', csvData)
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

# region get_awards
# <summery> Fills the movie list with awards data from academy-awards dataset </summery>
# <para></para>
# <return>Total Number of Awards found</return>
def get_awards():
    total_counter = 0
    awards_counter = 0
    Movies_Data = pd.read_csv("Filtered Movies.csv")
    for moviesIt in Movies_Data.itertuples():
        for awardsIt in awards.itertuples():
            if awardsIt.Film == moviesIt.Title:
                print("Found one. Movie Name: " + awardsIt.Film)
                total_counter += 1
                awards_counter += 1
        Movies_Data.at[moviesIt.Index, "Number of Awards"] = awards_counter
        awards_counter = 0
    del Movies_Data["Awards"]
    Movies_Data.to_csv("Filtered Movies.csv", index=False)
    return total_counter


# endregion

# region
# <summery> clears rated and genre </summery>
# <para></para>
# <return></return>
def clear_rated_genre():
    Movies_data = pd.read_csv("Filtered Movies.csv", index_col=False)

    rate_arr = ["Passed", "TV-PG", "TV-14", "TV-MA", "GP", "M/PG", "TV-G", "NC-17", "X",
                "TV-Y", "APPROVED", "M", "UNRATED"]
    for it in Movies_data.itertuples():
        if it.Rated in rate_arr:
            Movies_data.at[it.Index, "Rated"] = "Other"
        elif it.Rated == 'NOT RATED':
            Movies_data.at[it.Index, "Rated"] = "Unrated"

    Movies_data["Rated"] = Movies_data["Rated"].astype("category")
    Movies_data["Genre"] = Movies_data["Genre"].astype("category")
    Movies_data["Genre Category"] = Movies_data["Genre"].cat.codes
    Movies_data["Rate Category"] = Movies_data["Rated"].cat.codes

    Movies_data.to_csv("Filtered Movies.csv", index=False)


# endregion

# create_movie_file()
# filePath = "Raw Movies.csv"
# print(fill_with_data(filePath))

# get_awards()
# clear_rated_genre()

# Just makes a sound to indicate the script has finished.
# REMOVE BEFORE SUBMITTING
data = pd.read_csv("Raw Movies.csv")
print(data.head())
print('\007')
