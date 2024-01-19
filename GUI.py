
from prototype.GUIcomponents import TkWindow
from prototype.clusters import readIndex

print('Opening index file...')
index_file = "index.csv"
index = readIndex(index_file)

window = TkWindow( index )
window.mainloop()
