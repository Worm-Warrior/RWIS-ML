import pandas as pd
import numpy as np

INVALID_CONDITION = ['Other', 'Error', 'No Report', '-99']
INVALID_TEMP = -99
condition_cols= ['tfs0_text','tfs1_text','tfs2_text','tfs3_text']
temp_cols = ['tfs0','tfs1','tfs2','tfs3','subf', 'tmpf', 'dwpf', 'feel']

dataset_files = ['dataset/rwis_data_2015.txt', 'dataset/rwis_data_2016.txt', 'dataset/rwis_data_2017.txt', 'dataset/rwis_data_2018.txt', 'dataset/rwis_data_2019.txt', 'dataset/rwis_data_2020.txt', 'dataset/rwis_data_2021.txt', 'dataset/rwis_data_2022.txt', 'dataset/rwis_data_2023.txt', 'dataset/rwis_data_2024.txt', 'dataset/rwis_data_2025.txt']
test = ['dataset/rwis_data_2015.txt']

for file in test:
    df = pd.read_csv(file)

    #print(df.head(10))
    print(str(file))
    
    # The value of -99 is used as a sentinel value, so we replace it with NaN, as it should be for an invalid reading.
    print('before cleaning')
    print(df[condition_cols[0]].value_counts().sort_values(ascending=False))
    
    df[condition_cols] = df[condition_cols].replace(INVALID_CONDITION, np.nan)
    df[temp_cols] = df[temp_cols].replace(INVALID_TEMP, np.nan)
    
    # Drop rows where all of the condition columns are NaN, as this is the main label we want to predict, and if it is missing, we cannot use the row for training or testing.
    df.dropna(subset=condition_cols, how='all', inplace=True)
    
    #print(df.count())
    print(df[condition_cols[0]].value_counts().sort_values(ascending=False))
    
    print('--------------------')
    # print(df.groupby("station")[["tfs0", "tfs1", "tfs2", "tfs3", "subf"]].apply(lambda g: g.notna().mean()))