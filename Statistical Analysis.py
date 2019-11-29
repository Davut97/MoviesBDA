import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

Movies_data = pd.read_csv("Filtered Movies.csv", index_col=False)

dataCorrlation = Movies_data.corr()
f, ax = plt.subplots(figsize=(9, 8))
sns.heatmap(dataCorrlation, ax=ax, cmap="YlGnBu", linewidths=0.1)
plt.title("Correlation Heat Diagram")
plt.show()
plt.savefig("Correlation Heat Diagram")

sns.countplot(Movies_data["Rated"], label="Rating")
plt.title("Ratings Counts")
plt.xlabel("Ratings")
plt.ylabel("Count")
plt.show()
plt.savefig("Ratings Counts")

sns.countplot(Movies_data["Actors"], label="Number of Top 100 Actors in Movie")
plt.xlabel("Number of Top 100 Actors in Movie")
plt.ylabel("Count")
plt.title("Number of Top 100 Actors in Movie Count")
plt.show()
plt.savefig("Count of Top 100 Actors")

print("Mean of IMDB Votes: " + str(Movies_data["imdbVotes"].mean()))  # The mean is 79283.1397

print("Company that produced most amount of movies: ")
print(Movies_data["Production"].mode())  # Most recurring is other, which means not a famous company

print("****************************")  # Divider
# Actors vs Revenue
# Can not make a decision from the barplot alone
sns.barplot(x="Actors", y="Revenue", data=Movies_data)
plt.title("Actors vs Revenue")
plt.show()
plt.savefig("Actors vs Revenue")

data = Movies_data[['Actors', 'Revenue']]
# 0.187 => weak and likely insignificant relationship, alternative hypothesis fails
print("Correlation Coefficient for Actors & Revenue: ")
print(np.corrcoef(data.Actors, data.Revenue))
print("****************************")  # Divider

# Genre vs Revenue
action_movies = Movies_data[(Movies_data["Genre"] == "Action")]
non_action_movies = Movies_data[(Movies_data["Genre"] != "Action")]

action_mean = action_movies["Revenue"].mean()
non_action_mean = non_action_movies["Revenue"].mean()
# True => alternative Hypothesis is correct, and we can reject NULL Hypothesis
print("Mean of Action: " + str(action_mean) + " > " + " Mean of Non-Action: " + str(non_action_mean))
# print(action_mean > non_action_mean)

print("****************************")  # Divider

# Revenue vs Budget
budget_data = Movies_data[['Budget', 'Revenue']]
# # 0.51 => likely significant relationship, alternative hypothesis passes
print("Correlation Coefficient of Budget & Revenue")
print(np.corrcoef(budget_data.Budget, budget_data.Revenue))

print("****************************")  # Divider

# imdb Rating vs Votes
rating_data = Movies_data[['imdbRating', 'imdbVotes']]
# 0.34 => likely insignificant relationship, alternative hypothesis fails
print("Correlation Coefficient of IMDB Rating & IMDB Votes")
print(np.corrcoef(rating_data.imdbRating, rating_data.imdbVotes))

print("****************************")  # Divider

# Awards vs Revenue
# No Relation from Bar plot.
sns.barplot(x="Number of Awards", y="Revenue", data=Movies_data)
plt.title("Number of Awards for a Movie vs Revenue")
plt.show()
plt.savefig("Number of Awards for a Movie vs Revenue")
# Let's check corr coefficient
print("Correlation Coefficient of Number of Awards & Revenue")
print(np.corrcoef(Movies_data["Number of Awards"], Movies_data["Revenue"]))
# 0.04 => the correlation coefficient is shows that there's no relation!
print("****************************")  # Divider
