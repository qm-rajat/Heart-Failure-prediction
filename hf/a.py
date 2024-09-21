import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix,accuracy_score,r2_score,classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import GradientBoostingClassifier,HistGradientBoostingClassifier
from sklearn.model_selection import RandomizedSearchCV
import pickle



data=pd.read_csv('heart.csv')
data.isnull().sum()
data.shape
data['ChestPainType'].unique()
data['RestingECG'].unique()
data['ST_Slope'].unique()

#converting non-numeric data type in numeric
data['Sex']=data['Sex'].map({"M":0,"F":1})
data['ChestPainType']=data['ChestPainType'].map({"TA":0,"ATA":1,"NAP":2,"ASY":3})
data['RestingECG']=data['RestingECG'].map({"Normal":0,"ST":1,"LVH":2})
data['ExerciseAngina']=data['ExerciseAngina'].map({"Y":0,"N":1})
data['ST_Slope']=data['ST_Slope'].map({"Up":0,"Flat":1,"Down":2})

len_live = len(data["Heartfailure"][data.Heartfailure == 0])
len_death = len(data["Heartfailure"][data.Heartfailure == 1])

arr = np.array([len_live , len_death]) 
labels = ['LIVING', 'DIED'] 


x=data.iloc[:,:-1].values
y=data.iloc[:,-1].values

x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=42,test_size=0.2)

#scaling the model using standard method

sc=StandardScaler()
x_train=sc.fit_transform(x_train)
x_test=sc.transform(x_test)

regressor=LogisticRegression(   random_state=42,
                                # penalty='l2' ,#Effective regularization for a small dataset like prevent overfitting
                                solver='liblinear'  #handle diffrent types of regularization
                            )
regressor.fit(x_train,y_train)
y_pred=regressor.predict(x_test)



forest=RandomForestClassifier(n_estimators=100,random_state=40)
forest.fit(x_train,y_train)
y_pred=forest.predict(x_test)

# model=DecisionTreeClassifier(max_depth=60 ,random_state=42)
# model.fit(x_train,y_train)
# y_pred=model.predict(x_test)


#knn clasifier
# k=8
# knn=KNeighborsClassifier(n_neighbors=k)
# knn.get_params()
# knn.fit(x_train,y_train)
# y_pred=knn.predict(x_test)




# sns.boxplot(data['Cholesterol'])
Q1=data['Cholesterol'].quantile(0.25)
Q3=data['Cholesterol'].quantile(0.75)
IQR=Q3-Q1
lowerBound=Q1-1.5*IQR
upperBound=Q3+1.5*IQR
print(IQR)
# print("lower outlier: ",lowerBound)
# print("upper outlier: ",upperBound)
filterData=data[((data['Cholesterol'])>=lowerBound) & (data['Cholesterol']<=upperBound)]
# print("FilterDta:\n",filterData)
Q1=filterData['RestingBP'].quantile(0.25)
Q3=filterData['RestingBP'].quantile(0.75)
IQR=Q3-Q1
lowerBound=Q1-1.5*IQR
upperBound=Q3+1.5*IQR
# print(IQR)
# print("lower outlier: ",lowerBound)
# print("upper outlier: ",upperBound)
filterData=filterData[((filterData['RestingBP'])>=lowerBound) & (filterData['RestingBP']<=upperBound)]
# print("filterdata:\n",filterData)
# sns.boxplot(filterData['RestingBP'])
Q1=filterData['Oldpeak'].quantile(0.25)
Q3=filterData['Oldpeak'].quantile(0.75)
IQR=Q3-Q1
lowerBound=Q1-1.5*IQR
upperBound=Q3+1.5*IQR
# print(IQR)
# print("lower outlier: ",lowerBound)
# print("upper outlier: ",upperBound)
filterData=filterData[((filterData['Oldpeak'])>=lowerBound) & (filterData['Oldpeak']<=upperBound)]
# print("filterdata:\n",filterData)
sns.boxplot(filterData['Oldpeak'])



X=filterData.drop('Heartfailure',axis=1)
y=filterData['Heartfailure']

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.21,random_state=42)

param_distributions = {
    'n_estimators':[i for i in range(100,1000)],  # Number of trees in the forest
    'max_depth': [i for i in range(10,100)],       # Maximum depth of the tree
    'min_samples_split': [i for i in range(2,20)], # Minimum number of samples required to split a node
    'min_samples_leaf': [i for i in range(1,20)],  # Minimum number of samples required at a leaf node
    'max_features': ['sqrt', 'log2'], # Number of features to consider when looking for the best split
    'bootstrap': [True, False],          # Whether bootstrap samples are used when building trees
    'criterion': ['gini', 'entropy']    # Function to measure the quality of a split

}

scaler=StandardScaler()
X_train=scaler.fit_transform(X_train)
X_test=scaler.transform(X_test)
model=RandomForestClassifier(random_state=42)

model=RandomForestClassifier(n_estimators= 300, min_samples_split= 19,
                             min_samples_leaf= 3,n_jobs=-1, max_features= 'log2', max_depth=10,criterion='gini',bootstrap=False, random_state=42)
# random_search = RandomizedSearchCV(estimator=model, param_distributions=param_distributions,
#                                    n_iter=100, cv=5, n_jobs=-1, verbose=2, scoring='accuracy')


# random_search.fit(X_train, y_train)

# best_params = random_search.best_params_
# print("Best parameters found: ", best_params)
# print(f"best score is:{random_search.best_score_}")
model.fit(X_train,y_train)

scores = cross_val_score(model, X, y, cv=15, scoring=('accuracy'))


y_pred=model.predict(X_test)
r2=r2_score(y_test,y_pred)

model_path = 'a.pkl'
with open(model_path, 'wb') as file:
    pickle.dump(model, file)

print("R2:",r2)
print(f"Accuracy is:{accuracy_score(y_test,y_pred)}")
print(f"Confusion matrix:\n{confusion_matrix(y_test,y_pred)}")
print(f"Classification Report:\n{classification_report(y_test,y_pred)}")









# Accuracy is:0.9256756756756757