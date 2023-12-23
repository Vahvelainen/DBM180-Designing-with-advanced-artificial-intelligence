import os
import csv
from tqdm import tqdm
from CLIP import CLipEncoder

'''
    A nicer version of create Index.py that:
    - Browses up to three folders deep in given picture folder
    - Gives a progressbar
'''


image_dir = 'C:/Users/Leevi/Pictures'
output_csv = 'index.csv'

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

# Find jpg files in the directories
jpg_files = []

for dir in dirs:
    jpgs_in_this_dir = [ file for file in os.listdir(dir) if file.lower().endswith('.jpg') ]
    for jpg in jpgs_in_this_dir:
        jpg_files.append( dir + '/' + jpg)

print('Found ' + str(len(jpg_files)) + ' jpg files in directory')

encoder = CLipEncoder()

# Write embeddings to CSV
with open(output_csv, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Filename', 'Embedding'])  # Write header

    # Wrap the jpg_files iterable with tqdm to create a progress bar
    with tqdm(jpg_files, desc='Encoding Images') as pbar:
        for image_file in pbar:
            # Set the description to the current image file being processed
            pbar.set_description(f"Processing {image_file}")
            
            #Get embedding and write a line to the csv file 
            embedding = encoder.imageEmbedding(image_file)
            csvwriter.writerow([image_file] + embedding.tolist()) 

print("Completed and written to CSV!")