
from GUI import TkWindow, FileCarousel
from IndexTools import readIndex
from clusters import Cluster

# Clustering here
print('Opening index file...')
index_file = "index_fujifilm.csv"
embeddings, files = readIndex(index_file)
index = Cluster(embeddings, files, 'Index')

window = TkWindow( index )
window.mainloop()
