import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import ttest_ind, mannwhitneyu, levene

data = pd.read_csv("Filtered Movies.csv", index_col=False)
data.columns = data.columns.str.rstrip()
print(data.columns)
print(data["Genre"])
dataCorrlation = data.corr()

f, ax = plt.subplots(figsize=(9, 8))
sns.heatmap(dataCorrlation, ax=ax, cmap="YlGnBu", linewidths=0.1)
plt.title("Correlation Heat Diagram")
plt.savefig("Figures/Correlation Heat Diagram.png")
plt.show()

sns.countplot(data["Rated"], label="Rating")
plt.title("Ratings Counts")
plt.xlabel("Ratings")
plt.ylabel("Count")
plt.savefig("Ratings Counts.png")
plt.show()

sns.countplot(data["Actors"], label="Number of Top 100 Actors in Movie")
plt.xlabel("Number of Top 100 Actors in Movie")
plt.ylabel("Count")
plt.title("Number of Top 100 Actors in Movie Count")
plt.savefig("Figures/Count of Top 100 Actors.png")
plt.show()

print("Mean of IMDB Votes: " + str(data["imdbVotes"].mean()))  # The mean is 79283.1397

print("Company that produced most amount of movies: ")
print(data["Production"].mode())  # Most recurring is other, which means not a famous company

print("****************************")  # Divider
# Actors vs Revenue
# Can not make a decision from the barplot alone
sns.barplot(x="Actors", y="Revenue", data=data)
plt.title("Actors vs Revenue")
plt.savefig("Actors vs Revenue.png")
plt.show()

data_set = data[['Actors', 'Revenue']]
# 0.187 => weak and likely insignificant relationship, alternative hypothesis fails
print("Correlation Coefficient for Actors & Revenue: ")
print(np.corrcoef(data.Actors, data.Revenue))
print("****************************")  # Divider

# Genre vs Revenue
action_movies = data[(data["Genre"] == "Action")]
non_action_movies = data[(data["Genre"] != "Action")]

action_mean = action_movies["Revenue"].mean()
non_action_mean = non_action_movies["Revenue"].mean()
# True => alternative Hypothesis is correct, and we can reject NULL Hypothesis
print("Mean of Action: " + str(action_mean) + " > " + " Mean of Non-Action: " + str(non_action_mean))
# print(action_mean > non_action_mean)

print("****************************")  # Divider

# Revenue vs Budget
budget_data = data[['Budget', 'Revenue']]
# # 0.51 => likely significant relationship, alternative hypothesis passes
print("Correlation Coefficient of Budget & Revenue")
print(np.corrcoef(budget_data.Budget, budget_data.Revenue))

print("****************************")  # Divider

# imdb Rating vs Votes
rating_data = data[['imdbRating', 'imdbVotes']]
# 0.34 => likely insignificant relationship, alternative hypothesis fails
print("Correlation Coefficient of IMDB Rating & IMDB Votes")
print(np.corrcoef(rating_data.imdbRating, rating_data.imdbVotes))

print("****************************")  # Divider

# Awards vs Revenue
# No Relation from Bar plot.
sns.barplot(x="Number of Awards", y="Revenue", data=data)
plt.title("Number of Awards for a Movie vs Revenue")
plt.savefig("Figures/Number of Awards for a Movie vs Revenue.png")
plt.show()
# Let's check corr coefficient
print("Correlation Coefficient of Number of Awards & Revenue")
print(np.corrcoef(data["Number of Awards"], data["Revenue"]))
# 0.04 => the correlation coefficient is shows that there's no relation!
print("****************************")  # Divider

revenueMean = data["Revenue"].mean()
print(revenueMean)
dataset = data[['Budget', 'Actors']]
dataset.Budget.corr(dataset.Actors, method="pearson")
np.corrcoef(dataset.Budget, dataset.Actors)
# HP2 alternative passed and we erject the null hypthosis
ax = sns.barplot(x="Actors", y="Budget", data=data)
plt.title("Famous actors in a movie vs budget")
plt.show()
mean_insideUSA = data.Revenue[data.ReleasedOutsideUSA == 0].mean()

mean_outsideUSA = data.Revenue[data.ReleasedOutsideUSA == 1].mean()
print("Testing for normality")
print(levene(data.Revenue[data.ReleasedOutsideUSA == 0], data.Revenue[data.ReleasedOutsideUSA == 1]))
outSideUSA = data.ReleasedOutsideUSA == 0
InSideUSA = data.ReleasedOutsideUSA == 1

print("faild the test we will use the MANN-WHITNEY U test")
u, p = mannwhitneyu(data[outSideUSA].Revenue, data[InSideUSA].Revenue, )
print("Results:\n\tU-statistic: %.5f\n\tp-value: %g" % (u, p * 2))
print("mean inside USA: ")
print(mean_insideUSA)
print("mean inside USA: ")
print(mean_outsideUSA)
diff_mean = mean_insideUSA - mean_outsideUSA
print("Difference in mean: ")
print(diff_mean)

plt.figure(figsize=(10, 4))
plt.hist(data.Revenue[outSideUSA], bins=np.arange(10000, 20000, 500), color="b")
plt.hist(data.Revenue[InSideUSA], bins=np.arange(10000, 20000, 500), color="r")
plt.xlabel("Realeasd out or in USA")
plt.ylabel("Revenue")
plt.yscale("log")
plt.title("Revenue inside and outside usa ")
plt.savefig("Figures/Revenue inside and outside usa.png")
plt.show()

a = sns.barplot(x="Actors", y="imdbRating", data=data)
plt.savefig("Actors vs IMBDRating.png")
plt.show()

is_others = data["Production"] == "Others"

FamousActors = data.Actors > 0
NoFamousActors = data.Actors == 0
print(ttest_ind(data.imdbRating[data.Actors > 0], data.imdbRating[data.Actors == 0]))
print("faild the test we will use the MANN-WHITNEY U test")
u, p = mannwhitneyu(data[FamousActors].imdbRating, data[NoFamousActors].imdbRating)
print("Results:\n\tU-statistic: %.5f\n\tp-value: %g" % (u, p * 2))
print(ttest_ind(data.Revenue[data.Production == "Others"], data.Revenue[data.Production != "Others"]))
print("faild the test we will use the MANN-WHITNEY U test")

Others = data.Production == "Others"
NotOthers = data.Production != "Others"
u, p = mannwhitneyu(data[Others].Revenue, data[NotOthers].Revenue, )
print("Results:\n\tU-statistic: %.5f\n\tp-value: %g" % (u, p * 2))
print(ttest_ind(data.Budget[data.Actors > 0], data.Budget[data.Actors == 0]))
print("faild the test we will use the MANN-WHITNEY U test")

u, p = mannwhitneyu(data[FamousActors].Budget, data[NoFamousActors].Budget)
print("Results:\n\tU-statistic: %.5f\n\tp-value: %g" % (u, p * 2))
ByOthers = data.Production == "Others"
NotByOthers = data.Production != "Others"
plt.figure(figsize=(10, 4))
plt.hist(data.Revenue[NotByOthers], bins=np.arange(10000, 20000, 500), color="b")
plt.hist(data.Revenue[ByOthers], bins=np.arange(10000, 20000, 500), color="r")
plt.xlabel("Production by company")
plt.ylabel("Revenue")
plt.yscale("log")
plt.title("Revenue difference between famous companies and others")
plt.show()
print(data.Budget.describe())
