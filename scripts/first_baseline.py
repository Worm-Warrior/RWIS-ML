from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
import pandas as pd
import numpy as np

training_set_path = '../dataset/clean/train.csv'
validation_set_path = '../dataset/clean/val.csv'
testing_set_path = '../dataset/clean/test.csv'

DROP_COLS = ['label','station', 'obtime', 'tfs0_text']

def main() -> None:
    model = HistGradientBoostingClassifier();

    print("Loading data...")
    data = pd.read_csv(training_set_path)

    X_train = data.drop(columns=DROP_COLS)
    y_train = data['label']

    print("X_train and y_train first 5 entries")
    print(X_train.head(5))
    print(y_train.head(5))

    print("Training model...")

    model.fit(X_train,y_train)

    test_data = pd.read_csv(testing_set_path)

    X_test = test_data.drop(columns=DROP_COLS)
    y_test = test_data['label']


    print("Model score:")
    print(model.score(X_test,y_test))



if __name__ == "__main__":
    main()
