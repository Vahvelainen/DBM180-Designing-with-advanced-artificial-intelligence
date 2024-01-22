import os
import csv
from tqdm import tqdm
from tools import findDirectories, readTextFile
from imagebindEncoder import ImagebindEncoder


'''
Program to create a index.csv file to be used with the textSearch.py and future scripts
Creates a simple csv files of jpg and mp3 files in given directory up to three directories deep
The rows of the csv consist only of the filepath and the embedding vector
'''

media_dir = input('Give path to the directory you wish to index: ')
media_dir = media_dir.replace("\\", "/") #For windows users

output_csv = 'index.csv'

# Find up to thee dirs deeps
dirs = findDirectories(media_dir, max_depth=3)
dirs.append(media_dir)

# Find compatible files in directiries
files = []
for dir in dirs:
    # Save files as tuples: ( filepath, filetype: ['text', 'image, 'audio'])
    # Image
    jpgs_in_this_dir = [ file for file in os.listdir(dir) if file.lower().endswith('.jpg') ]
    for jpg in jpgs_in_this_dir:
        files.append( (dir + '/' + jpg, 'image') )
    # Audio
    mp3s_in_this_dir = [ file for file in os.listdir(dir) if file.lower().endswith('.mp3') ]
    for mp3 in mp3s_in_this_dir:
        files.append( (dir + '/' + mp3, 'audio') )
    # Text
    txts_in_this_dir = [ file for file in os.listdir(dir) if file.lower().endswith('.txt') ]
    for txt in txts_in_this_dir:
        files.append( (dir + '/' + txt, 'text') )

print('Found ' + str(len(files)) + ' compatible files in directory')

encoder = ImagebindEncoder()

# Write embeddings to CSV
with open(output_csv, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Filename', 'Embedding'])  # Write header

    # Wrap the jpg_files iterable with tqdm to create a progress bar
    with tqdm(files, desc='Encoding Images') as pbar:
        for file in pbar:
            # Set the description to the current image file being processed
            filepath, filetype = file
            pbar.set_description(f"Processing {filepath}")

            embedding = []
            
            #Get embedding and write a line to the csv file 
            if filetype == 'image':
                embedding = encoder.imageEmbedding(filepath)
            elif filetype == 'audio':
                embedding = encoder.audioEmbedding(filepath)
            elif filetype == 'text':
                text = readTextFile(filepath)
                embedding = encoder.textEmbedding(text)

            csvwriter.writerow([filepath] + embedding.tolist()) 

print("Completed and written to CSV!")