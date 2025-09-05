from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt

def get_accuracy_train_model_randomforest(X, y, test_size, estimators, random_state):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    rf = RandomForestClassifier(n_estimators=estimators, random_state=random_state)
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)

    return accuracy_score(y_test, y_pred)

def get_accuracy_train_model_logisticregression(X, y, test_size, estimators, random_state):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    clf = LogisticRegression(max_iter=200)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    return accuracy_score(y_test, y_pred)

def get_accuracy_train_model_linearregression(X, y, test_size, estimators, random_state):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    clf = LinearRegression()
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    return accuracy_score(y_test, y_pred)