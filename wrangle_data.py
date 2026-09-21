import pandas as pd
import numpy as np

INVALID_CONDITION = ['Other', 'Error', 'No Report', '-99']
INVALID_TEMP = -99

condition_cols= ['tfs0_text']

temp_cols = ['tfs0','tfs1', 'tmpf', 'dwpf']

# We will still drop the tfs2 and tfs3 related columns, because they have a bad rate of missing values depending on the year and station.
# tfs0 and tfs1 related columns as they are the most consistent across years and stations, through they still have some missing values.
drop_cols = ['feel', 'pcpn', 'subf', 'vsby', 'tfs3', 'tfs3_text', 'tfs2', 'tfs2_text']

dataset_files = ['dataset/rwis_data_2015.txt', 'dataset/rwis_data_2016.txt', 'dataset/rwis_data_2017.txt', 'dataset/rwis_data_2018.txt', 'dataset/rwis_data_2019.txt', 'dataset/rwis_data_2020.txt', 'dataset/rwis_data_2021.txt', 'dataset/rwis_data_2022.txt', 'dataset/rwis_data_2023.txt', 'dataset/rwis_data_2024.txt', 'dataset/rwis_data_2025.txt']
test = ['dataset/rwis_data_2015.txt']

for file in test:
    keep = ['station','obtime','longitude','latitude','tmpf','dwpf','drct',
        'sknt','gust','relh','tfs0','tfs0_text']

    df = pd.read_csv(file, usecols=keep)

    print(str(file))
    
    # The value of -99 is used as a sentinel value, so we replace it with NaN, as it should be for an invalid reading.
    print('before cleaning:\n\n')
    print(len(df))
    print(df.info())
    print(df[condition_cols[0]].value_counts().sort_values(ascending=False))


    df = df.drop_duplicates(subset=['station', 'obtime'])
    df['obtime'] = pd.to_datetime(df['obtime'], utc=True)

    num_cols = ['tmpf','dwpf','drct','sknt','gust','relh','tfs0']
    df[num_cols] = df[num_cols].replace(-99, np.nan)

    df['tfs0_text'] = (df['tfs0_text']
    .replace({'Chemical Wet': 'Chemically Wet'})
    .replace(['Other','Error','No Report','-99'], np.nan))
    df = df.dropna(subset=['tfs0_text']).reset_index(drop=True)

    # Drop rows where all of the condition columns are NaN, as this is the main label we want to predict, and if it is missing, we cannot use the row for training or testing.
    df.dropna(subset=condition_cols, how='all', inplace=True)

    print('after cleaning:\n\n')
    print(len(df))
    print(df[condition_cols[0]].value_counts().sort_values(ascending=False))
    print(df.info())
    print('--------------------')