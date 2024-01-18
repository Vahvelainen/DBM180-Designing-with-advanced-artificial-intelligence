
from GUI import TkWindow
from clusters import Cluster, readIndex

print('Opening index file...')
index_file = "index_fujifilm.csv"
index = readIndex(index_file)

window = TkWindow( index )
window.mainloop()
