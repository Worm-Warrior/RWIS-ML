from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
import pandas as pd
import numpy as np

training_set_path = '../dataset/clean/train.csv'
validation_set_path = '../dataset/clean/val.csv'
testing_set_path = '../dataset/clean/test.csv'

def main() -> None:
    model = HistGradientBoostingClassifier();

    print("Loading data...")
    data = pd.read_csv(training_set_path)

    X_train = data.drop(columns=['label','station', 'obtime', 'tfs0_text'])
    y_train = data['label']

    print("X_train and y_train first 5 entries")
    print(X_train.head(5))
    print(y_train.head(5))

    model.fit(X_train,y_train)

    print("Model score:")
    print(model.score(X_train,y_train))



if __name__ == "__main__":
    main()
