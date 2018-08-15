import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

#Adapted form http://dataaspirant.com/2017/06/26/random-forest-classifier-python-scikit-learn/
def random_forest_regressor(features, target):
    """
    To train the random forest regressor with features and target data
    :param features:
    :param target:
    :return: trained random forest regressor
    """
    clf = RandomForestRegressor()
    clf.fit(features, target)
    return clf

#Function that computes the machine learning model
def mlModel():

    dataset = pd.read_csv("plantData.csv")

    HEADERS = ["id", "temp", "UV", "water", "health"]

    train_x = dataset.as_matrix(columns=dataset.columns[1:-1])
    train_y = dataset.health

    # Create random forest regressor instance
    trained_model = random_forest_regressor(train_x, train_y)
    predictions = trained_model.predict(np.array([[16,  6, 0.9]]))

    return trained_model
