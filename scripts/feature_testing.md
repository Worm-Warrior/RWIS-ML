# Features and Average Accuracy

## Features Tested

### Baseline
Baseline features to drop: `DROP_COLS = ['label','station', 'obtime', 'tfs0_text', 'tfs1_text','tfs2_text','tfs3_text']`
Average acc: 0.7584766875155534


### Dropped: tfs1 - tfs3

`DROP_COLS = ['label','station', 'obtime', 'tfs0_text', 'tfs1_text','tfs2_text','tfs3_text','tfs1','tfs2','tfs3']`

Average acc: 0.7607191003148313

Increase of 0.30%

### Dropped: subf

`DROP_COLS = ['label','station', 'obtime', 'tfs0_text', 'tfs1_text','tfs2_text','tfs3_text','tfs1','tfs2','tfs3', 'subf']`

Average acc: 0.760990969581749

Increase of 0.04%

### Dropped: vsby


`DROP_COLS = ['label','station', 'obtime', 'tfs0_text', 'tfs1_text','tfs2_text','tfs3_text','tfs1','tfs2','tfs3', 'subf', 'vsby']`

Average acc: 0.7608670391542384

Increase of 0.02%