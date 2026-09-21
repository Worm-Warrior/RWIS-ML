import pandas as pd
import numpy as np
from pathlib import Path

KEEP = ['station','obtime','longitude','latitude','tmpf','dwpf','drct',
        'sknt','gust','relh','tfs0','tfs0_text']
NUM_COLS = ['tmpf','dwpf','drct','sknt','gust','relh','tfs0']
INVALID_LABELS = ['Other','Error','No Report','-99']

out_dir = Path('dataset/stripped_csv'); out_dir.mkdir(exist_ok=True)
class_counts, other_by_station, summary = {}, [], []
dataset_files = ['dataset/rwis_data_2015.txt', 'dataset/rwis_data_2016.txt', 'dataset/rwis_data_2017.txt', 'dataset/rwis_data_2018.txt', 'dataset/rwis_data_2019.txt', 'dataset/rwis_data_2020.txt', 'dataset/rwis_data_2021.txt', 'dataset/rwis_data_2022.txt', 'dataset/rwis_data_2023.txt', 'dataset/rwis_data_2024.txt', 'dataset/rwis_data_2025.txt']

for file in dataset_files:
    year = int(file[-8:-4])
    df = pd.read_csv(file, usecols=KEEP, dtype = {'tfs0_text': str}, low_memory=False)
    n_raw = len(df)

    # Diagnostic: where does "Other" come from? (before it is dropped)
    o = (df['tfs0_text'] == 'Other').groupby(df['station']).agg(['mean', 'sum'])
    o['year'] = year
    other_by_station.append(o.reset_index())

    df = df.drop_duplicates(subset=['station', 'obtime'])
    df['obtime'] = pd.to_datetime(df['obtime'], utc=True)
    df[NUM_COLS] = df[NUM_COLS].replace(-99, np.nan)
    df['tfs0_text'] = (df['tfs0_text']
                       .replace({'Chemical Wet': 'Chemically Wet'})
                       .replace(INVALID_LABELS, np.nan))
    df = df.dropna(subset=['tfs0_text']).reset_index(drop=True)

    df['station'] = df['station'].astype('category')
    df['tfs0_text'] = df['tfs0_text'].astype('category')
    df.to_csv(out_dir / f'rwis_{year}.csv', index=False)

    class_counts[year] = df['tfs0_text'].value_counts()
    summary.append({'year': year, 'raw': n_raw, 'clean': len(df),
                    'stations': df['station'].nunique(),
                    'first': df['obtime'].min(), 'last': df['obtime'].max()})

print(pd.DataFrame(summary))
print(pd.DataFrame(class_counts).fillna(0).astype(int))
pd.concat(other_by_station).to_csv('other_by_station.csv', index=False)