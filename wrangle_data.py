import pandas as pd
import numpy as np

INVALID_TEXT = -99
cols = ['tfs0_text','tfs1_text','tfs2_text','tfs3_text']

df = pd.read_csv('dataset/rwis_data_2015.txt')

print(df.head(10))
print(df.count())
print(df.groupby("station")[["tfs0", "tfs1", "tfs2", "tfs3", "subf"]].apply(lambda g: g.notna().mean()))

# The value of -99 is used as a sentinel value, so we replace it with NaN, as it should be.
df = df.replace(-99, np.nan)
df = df.replace('-99', np.nan)
print(df.head(10))