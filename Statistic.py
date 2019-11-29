import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from scipy.stats import ttest_ind

data = pd.read_csv("Filtered Movies.csv", low_memory=False)
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
print(stats.levene(data.Revenue[data.ReleasedOutsideUSA == 0], data.Revenue[data.ReleasedOutsideUSA == 1]))
outSideUSA = data.ReleasedOutsideUSA == 0
InSideUSA = data.ReleasedOutsideUSA == 1

print("faild the test we will use the MANN-WHITNEY U test")
u, p = stats.mannwhitneyu(data[outSideUSA].Revenue, data[InSideUSA].Revenue, )
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
plt.show()
plt.savefig("Revenue inside and outside usa")
a = sns.barplot(x="Actors", y="imdbRating", data=data)
plt.show()
plt.savefig("Actors vs IMBDRating")
is_others = data["Production"] == "Others"

FamousActors = data.Actors > 0
NoFamousActors = data.Actors == 0
print(ttest_ind(data.imdbRating[data.Actors > 0], data.imdbRating[data.Actors == 0]))
print("faild the test we will use the MANN-WHITNEY U test")
u, p = stats.mannwhitneyu(data[FamousActors].imdbRating, data[NoFamousActors].imdbRating)
print("Results:\n\tU-statistic: %.5f\n\tp-value: %g" % (u, p * 2))
print(ttest_ind(data.Revenue[data.Production == "Others"], data.Revenue[data.Production != "Others"]))
print("faild the test we will use the MANN-WHITNEY U test")

Others = data.Production == "Others"
NotOthers = data.Production != "Others"
u, p = stats.mannwhitneyu(data[Others].Revenue, data[NotOthers].Revenue, )
print("Results:\n\tU-statistic: %.5f\n\tp-value: %g" % (u, p * 2))
print(ttest_ind(data.Budget[data.Actors > 0], data.Budget[data.Actors == 0]))
print("faild the test we will use the MANN-WHITNEY U test")

u, p = stats.mannwhitneyu(data[FamousActors].Budget, data[NoFamousActors].Budget)
print("Results:\n\tU-statistic: %.5f\n\tp-value: %g" % (u, p * 2))
ByOthers = data.Production == "Others"
NotByOthers = data.Production != "Others"
plt.figure(figsize=(10, 4))
plt.hist(data.Revenue[NotByOthers], bins=np.arange(10000, 20000, 500), color="b")
plt.hist(data.Revenue[ByOthers], bins=np.arange(10000, 20000, 500), color="r")
plt.xlabel("Production by company")
plt.ylabel("Revenue")
plt.yscale("log")
plt.title("Revenue difference between famous companies and others ")
plt.show()
print(data.Budget.describe())
plt.savefig("Revenue difference between famous companies and others")
