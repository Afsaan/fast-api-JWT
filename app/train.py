# Save Model Using Pickle
import pandas
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
import joblib

def train_model(dataframe):
    array = dataframe.values
    X = array[:,0:8]
    Y = array[:,8]
    # Fit the model on training set
    model = LogisticRegression()
    model.fit(X, Y)

    # save the model to disk
    filename = 'saved_model.pkl'
    joblib.dump(model, filename)