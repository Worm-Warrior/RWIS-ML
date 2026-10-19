from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

training_set_path = '../dataset/testing_features/train.csv'
validation_set_path = '../dataset/testing_features/val.csv'
testing_set_path = '../dataset/testing_features/test.csv'

DROP_COLS = ['label','station', 'obtime', 'tfs0_text']

def main() -> None:
    model = HistGradientBoostingClassifier();

    print("Loading data...")
    data = pd.read_csv(training_set_path)

    for c in data.select_dtypes("float64"):
        data[c] = data[c].astype("float32")
    for c in data.select_dtypes("int64"):
        data[c] = pd.to_numeric(data[c], downcast="integer")
    for c in data.select_dtypes("object"):
        data[c] = data[c].astype("category")
        
    
    X_train = data.drop(columns=DROP_COLS)
    y_train = data['label']
    
    X_s, _, y_s, _ = train_test_split(X_train, y_train, train_size=4000000, random_state=0)
    
    print(X_train.shape)

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
