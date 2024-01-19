
from GUIcomponents import TkWindow
from clusters import readIndex

print('Opening index file...')
index_file = "index.csv"
index = readIndex(index_file)

window = TkWindow( index )
window.mainloop()
