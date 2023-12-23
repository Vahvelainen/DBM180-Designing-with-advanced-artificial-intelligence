import os
import csv

from CLIP import CLipEncoder

'''
    Program to create a index.csv file to be used with the textSearch.py and future scripts
    Creates a simple csv files of jpg files in given directory
    The rows of the csv consist only of the filepath and the embedding vector
'''

image_dir = 'C:/Users/Leevi/Pictures/20231209'
output_csv = 'index.csv'

# List all files ending with '.jpg' in the directory
jpg_files = [file for file in os.listdir(image_dir) if file.lower().endswith('.jpg')]

encoder = CLipEncoder()

# Write embeddings to CSV
with open(output_csv, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Filename', 'Embedding'])  # Write header

    #progressbar would be nice and the count and names of images
    for image_file in jpg_files:
        image_path = image_dir + '/' + image_file
        print(image_path)

        embedding = encoder.imageEmbedding(image_path) 
        csvwriter.writerow([image_path] + embedding.tolist() )  