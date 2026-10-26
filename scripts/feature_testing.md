# Features and Average Accuracy

## Features Tested
Baseline features to drop: `DROP_COLS = ['label','station', 'obtime', 'tfs0_text', 'tfs1_text','tfs2_text','tfs3_text']`
Average acc: 0.7584766875155534


Dropped: tfs1 - tfs3

`DROP_COLS = ['label','station', 'obtime', 'tfs0_text', 'tfs1_text','tfs2_text','tfs3_text','tfs1','tfs2','tfs3']`

Average acc: 0.7607191003148313

Increase of 0.30%