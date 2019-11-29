# -*- coding: utf-8 -*-
import math

import numpy as np
import pandas as pd


#fix Production column only
def fix_Production():
    data = pd.read_csv("Raw Movies.csv")
    data["Production"] = data["Production"].fillna("Others")
    data.to_csv("Filtered Movies.csv", index=False)

# region Fix Runtime & Year & Rating & Production Columns Problems: fix_RU_Y_RA_P()
# Author: Aydın Davutoğlu
# <summery> Fix RU Y RA P Columns </summery>
# <para>/para>
# <return></return>
def fix_RU_Y_RA():
    fix_Production()
    data = pd.read_csv("Filtered Movies.csv", keep_default_na=False)
    # The API Returns this values instead of Unrated for non MPA Ratings
    # So we will replace them with unrated
    TRASH = ["PASSED", "Not Rated", "Unrated", "Approved", "N/A",""]
    for it in data.itertuples():
        if it.Rated in TRASH:
            data.at[it.Index, "Rated"] = "Unrated"
        if it.Runtime == "['']" or (it.Runtime == 'nan'):
            data.at[it.Index, "Runtime"] = "108"  # The mean of runtime
        if (not it.Genre) or it.Genre == "N/A":
            data.drop(it.Index, inplace=True)
        if it.Production == "":
            data.at[it.Index,"Production"] = "Others"
    data["Rated"] = data["Rated"].fillna("Unrated")
    del data["Year"]
    data['Year of Release'] = pd.DatetimeIndex(data['Date']).year
    del data["Date"]
    print(data.isnull().sum())
    data.to_csv("Filtered Movies.csv", index=False)



# endregion

# region Fix All problems in Columns: fix_Columns()
# Author: Ahmad Nawar Droubi
# <summery> Fix All Encountered Problems in the columns </summery>
# <para>/para>
# <return></return>
def fix_Columns():
    fix_RU_Y_RA()
    Movies_Data = pd.read_csv("Filtered Movies.csv", keep_default_na=False)

    # Top 100 actors according to IMDB
    actorsList = ["Robert De Niro", "Jack Nicholson", "Marlon Brando", "Denzel Washington", "Clark Gable", "Tom Hanks",
                  "Humphrey Bogart", "Daniel Day-Lewis", "Sidney Poitier", "Gregory Peck", "Leonardo DiCaprio",
                  "Spencer Tracy", "Cary Grant", "Laurence Olivier", "James Stewart", "Steve McQueen", "Bruce Lee",
                  "Henry Fonda", "Morgan Freeman", "James Cagney", "Johnny Depp", "Charles Chaplin", "Paul Newman",
                  "Anthony Hopkins", "Katharine Hepburn", "Meryl Streep", "Ingrid Bergman", "Elizabeth Taylor",
                  "Bette Davis", "Cate Blanchett", "Audrey Hepburn", "Sophia Loren", "Vivien Leigh", "Marilyn Monroe",
                  "Julia Roberts", "Judy Garland", "Catherine Deneuve", "Grace Kelly", "Helen Mirren", "Greta Garbo",
                  "Olivia de Havilland", "Julie Andrews", "James Dean", "Al Pacino", "Kirk Douglas",
                  "Marcello Mastroianni",
                  "Gene Kelly", "Will Smith", "Harrison Ford", "John Wayne", "Gary Cooper", "Gérard Depardieu",
                  "Forest Whitaker", "Montgomery Clift", "Dustin Hoffman", "Charlton Heston", "Tom Cruise",
                  "Samuel L. Jackson", "Peter O'Toole", "Robin Williams", "Don Cheadle", "Antonio Banderas",
                  "Eddie Murphy", "Robert Downey, Jr", "Chris Evans", "Chris Hemsworth", "Mark Ruffalo",
                  "Scarlett Johansson",
                  "Paul Rudd", "Jeremy Renner", "Benedict Cumberbatch",
                  "Heath Ledger", "Diane Keaton", "Rita Hayworth", "Natalie Wood", "Joan Crawford", "Susan Sarandon",
                  "Julianne Moore", "Angelina Jolie", "Natalie Portman", "Emma Thompson", "Salma Hayek", "Kathy Bates",
                  "Steve McQueen", "Amy Adams", "Jeff Bridges", "Ben Kingsley", "Tommy Lee Jones", "Robert Redford",
                  "Jack Lemmon", "Joaquin Phoenix", "Christopher Walken", "Philip Seymour Hoffman", "George Clooney",
                  "Gene Hackman", "Bruce Willis", "Sean Connery", "Ian McKellen", "Russell Crowe", "Bill Murray",
                  "Nicolas Cage", "Joe Pesci", "Brad Pitt", "Kevin Costner", "Donald Sutherland", "Clint Eastwood",
                  "Keanu Reeves", "Jeff Goldblum"]
    actorsCounter = 0
    Movies_Data['Genre'] = Movies_Data['Genre'].astype(str)
    for it in Movies_Data.itertuples():
        try:
            genres = it.Genre.split(', ')
            Movies_Data.at[it.Index, "Genre"] = genres[0]
            if it.imdbRating == '' or it.imdbRating == 'N/A':
                Movies_Data.at[it.Index, "imdbRating"] = '0'
            # removes ',' from votes. Run this once!!
            if ',' in it.imdbVotes:
                Movies_Data.at[it.Index, "imdbVotes"] = it.imdbVotes.replace(',', '')
            if it.imdbVotes == 'nan' or it.imdbVotes == 'N/A' or it.imdbVotes == '':
                Movies_Data.at[it.Index, "imdbVotes"] = '0'
            if not it.Country or it.Country == 'nan':
                Movies_Data.at[it.Index, "Country"] = "USA"
            if not it.Language or it.Language == 'nan':
                Movies_Data.at[it.Index, "Language"] = "English"
            if it.Awards == '' or it.Awards == 'N/A' or it.Awards == 'nan':
                Movies_Data.at[it.Index, "Awards"] = "None"
            if it.Metascore == 'N/A' or it.Metascore == '' or it.Metascore == 'nan':
                Movies_Data.at[it.Index, "Metascore"] = '0'
            # extract list of actors
            # And replace them with the number of famous actors
            actorsArr = it.Actors.split(", ")
            if actorsArr[0] == '':
                Movies_Data.at[it.Index, "Actors"] = 0
            for actor in actorsArr:
                if actor in actorsList:
                    actorsCounter += 1
            Movies_Data.at[it.Index, "Actors"] = actorsCounter
            actorsCounter = 0
        except:
            print("An error was encountered :(")
    Movies_Data["imdbRating"] = Movies_Data["imdbRating"].astype(float)
    Movies_Data["Metascore"] = Movies_Data["Metascore"].astype(float)
    Movies_Data["imdbVotes"] = Movies_Data["imdbVotes"].astype(int)
    Movies_Data["Actors"] = Movies_Data["Actors"].astype(int)
    print(Movies_Data["Actors"].isnull().sum())
    print(Movies_Data["imdbRating"].isnull().sum())
    print(Movies_Data["imdbVotes"].isnull().sum())
    print(Movies_Data["imdbRating"].isnull().sum())
    print(Movies_Data["Metascore"].isnull().sum())
    print((Movies_Data["Country"] == '').sum())
    print((Movies_Data["Language"] == '').sum())

    print(Movies_Data["Actors"].max())

    print(Movies_Data.isnull().sum())
    Movies_Data.to_csv("Filtered Movies.csv", index=False)


# endregion


def replace_Metascore_With_Mean():
    Movies_Data = pd.read_csv("Filtered Movies.csv")
    Movies_Data['Metascore'].replace(0, np.NaN)
    metaMean = round(Movies_Data["Metascore"].mean())
    print("Meta Mean is: " + metaMean)
    for it in Movies_Data.itertuples():
        if math.isnan(it.Metascore) or it.Metascore == '':
            Movies_Data.at[it.Index, "Metascore"] = metaMean
    Movies_Data.to_csv("Filtered Movies.csv", index=False)


fix_Columns()
replace_Metascore_With_Mean()
