'''
Functions for saving embedding indexes to csv and finding them
Might be a class later if there are any benefits to that
'''

import numpy as np
import csv 

def readIndex(index_file):
  files = []
  embeddings = []

  with open(index_file) as file_obj: 
    reader = csv.reader(file_obj) 
    for row in reader:
        # Check that csv.row is as long as embedding + the filename
        if ( len(row) == 512 + 1 ):
          files.append( row.pop(0) )
          embeddings.append( np.array(row) )

  return embeddings, files

