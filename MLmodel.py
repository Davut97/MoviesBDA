import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from Utils import trim_all_columns

data = pd.read_csv("Filtered Movies.csv", index_col=False)
data.columns = data.columns.str.rstrip()
data = trim_all_columns(data)
# region cat stuff
# data["Genre"] = data["Genre"].astype('category')
# data['Genre_cat'] = data["Genre"].cat.codes

# data["Language"] = data["Language"].astype('category')
# data['Language_cat'] = data["Language"].cat.codes
#

# data["Rated"] = data["Rated"].astype('category')
# data['Rated_cat'] = data["Rated"].cat.codes
# data["Country"] = data["Country"].astype('category')
# data['Country_cat'] = data["Country"].cat.codes

# data["Production"] = data["Production"].astype('category')
# data['Production_cat'] = data["Production"].cat.codes
# endregion

# region Logistic regression
suc_count = 0
fi_count = 0

data = pd.read_csv("Filtered Movies.csv", index_col=False)
data.columns = data.columns.str.rstrip()
data = trim_all_columns(data)
for it in data.itertuples():
    if it.Revenue > (it.Budget * 2):
        print("found successful!")
        suc_count = suc_count + 1
        data.at[it.Index, 'Is_Successful'] = 1
    else:
        print("found Unsuccessful!")
        fi_count = fi_count + 1
        data.at[it.Index, 'Is_Successful'] = 0

print(suc_count)  # 5012
print(fi_count)  # 2832
dg = pd.get_dummies(data["Genre"], prefix="Genre_dum")
data[dg.columns] = dg
dg = pd.get_dummies(data["Rated"], prefix="Rated_dum")
data[dg.columns] = dg
dg = pd.get_dummies(data["Country"], prefix="Country_dum")
data[dg.columns] = dg
dg = pd.get_dummies(data["Language"], prefix="Language_dum")
data[dg.columns] = dg
dg = pd.get_dummies(data["Production"], prefix="Production_dum")
data[dg.columns] = dg
data.drop(["Title", "Rated", "Genre", "Country", "Language", "Production"], axis=1)
x = data[["Budget", "imdbVotes"]]
y = data["Is_Successful"]
logit_model = sm.Logit(y, x)
result = logit_model.fit()
print(result.summary2())

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
logreg = LogisticRegression()
logreg.fit(X_train, y_train)
y_pred = logreg.predict(X_test)
print("Accuarcy of logistic regression classifier on test set: {:.2f}".format(logreg.score(X_test, y_test)))
confusion_matrix = metrics.confusion_matrix(y_test, y_pred)
print(confusion_matrix)
print(metrics.classification_report(y_test, y_pred))

logit_roc_auc = metrics.roc_auc_score(y_test, logreg.predict(X_test))
fpr, tpr, thresholds = metrics.roc_curve(y_test, logreg.predict_proba(X_test)[:, 1])
plt.figure()
plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % logit_roc_auc)
plt.plot([0, 1], [0, 1], 'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic')
plt.legend(loc="lower right")
plt.savefig('Figures/Log_ROC')
plt.show()
# endregion
