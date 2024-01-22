
from GUIcomponents import TkWindow
from clusters import readIndex

'''
GUI window for exploring the files indexed by createIndex.py clustered into groups of four clusters
'''

print('Opening index file...')
index_file = "index.csv"
index = readIndex(index_file)

window = TkWindow( index )
window.mainloop()
