from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

training_set_path = '../dataset/testing_features/'
validation_set_path = '../dataset/testing_features/'
testing_set_path = '../dataset/testing_features/test.csv'

TRAINING_FILES = ['2015','2016','2017','2018','2019','2020','2021','2022']
FILE_PREFIX = 'rwis_'
DROP_COLS = ['label','station', 'obtime', 'tfs0_text', 'tfs1_text','tfs2_text','tfs3_text','tfs1','tfs2','tfs3', 'subf']

def main() -> None:
    model = HistGradientBoostingClassifier();
    
    scores = {};
    
    for file in TRAINING_FILES:
        path = training_set_path + FILE_PREFIX + file + '_clean' + '.csv'
    
        data = pd.read_csv(path)
    
        X_train = data.drop(columns=DROP_COLS)
        y_train = data['label']
    
        print(X_train.shape)

        print("Training model...")

        model.fit(X_train,y_train)

        test_data = pd.read_csv(testing_set_path)

        X_test = test_data.drop(columns=DROP_COLS)
        y_test = test_data['label']


        print("Model score:")
        score = model.score(X_test, y_test)
        print(score)
        scores[file] = score
        
    avg_score = sum(scores.values()) / len(scores)
    print(scores)
    print("Averaged score:")
    print(avg_score)

if __name__ == "__main__":
    main()
