import os
import csv
from tqdm import tqdm
from imagebindEncoder import ImagebindEncoder

'''
    A nicer version of create Index.py that:
    - Browses up to three folders deep in given picture folder
    - Gives a progressbar
'''

# Make sure to use "/" instead of "\" 
image_dir = '/Users/leevi/Datasets'
output_csv = 'index_ib.csv'

def find_directories(base_path, depth=1, max_depth=3):
    # List to hold the directories
    directories = []

    # Check if the maximum depth has been reached
    if depth > max_depth:
        return directories

    # Loop through each item in the directory
    for entry in os.scandir(base_path):
        if entry.is_dir():  # If the item is a directory
            new_path = base_path + '/' + entry.name
            directories.append(new_path)
            # Recursively find directories in the current directory
            directories.extend(find_directories(new_path, depth + 1, max_depth))

    return directories

# Find up to thee dirs deeps
dirs = find_directories(image_dir)
dirs.append(image_dir)

# Find compatible files in directiries
files = []
for dir in dirs:
    # Save files as tuples: ( filepath, filetype: ['text', 'image, 'audio'])
    jpgs_in_this_dir = [ file for file in os.listdir(dir) if file.lower().endswith('.jpg') ]
    for jpg in jpgs_in_this_dir:
        files.append( (dir + '/' + jpg, 'image') )
    mp3s_in_this_dir = [ file for file in os.listdir(dir) if file.lower().endswith('.mp3') ]
    for mp3 in mp3s_in_this_dir:
        files.append( (dir + '/' + mp3, 'audio') )

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

            csvwriter.writerow([filepath] + embedding.tolist()) 

print("Completed and written to CSV!")