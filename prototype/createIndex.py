import os
import csv

from CLIP import CLipEncoder

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