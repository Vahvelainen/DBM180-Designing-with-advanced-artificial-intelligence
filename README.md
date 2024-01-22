# AI2Ethnography

This demonstration showcases an AI-powered media exploration tool built for conducting an autoethnographic study. The tool utilizes ImageBind by Meta AI to index various file formats into a single embedding space, allowing for efficient exploration of media files.

This project was developed as part of the course DBM180 Designing with Advanced Artificial Intelligence at Eindhoven University of Technology.

## Quickstart

Follow these steps to start using the program:

### 1. Install Requirements

Create a Python 3.11 environment for PyTorch with Anaconda or Conda.

Install the requirements using:
```sh
pip install -r requirements.txt
```

Non-Conda environments may or may not work seamlessly and might require additional packages. Testing has only been conducted with Anaconda.

### 2. Create an Index

The project functions by first creating an index in the form of a CSV file for the files you wish to explore.
The program supports the following file formats:
- .jpg
- .mp3
- .txt

Create the index file by running:
```sh
python prototype/createIndex.py
```
and enter the path to the folder you want to use for creating the index.
Please note that the program will traverse the folders to a depth of three subfolders.

The index file must be generated before using the other features. Any changes to file locations after creating the index may result in unexpected behavior, including crashes due to the files not being found.

### 3. Explore Using the Graphical UI or Plain Text Search

To use the graphical UI, run:
```sh
python prototype/GUI.py
```

A command-line-based text search for files can be started with:
```sh
python prototype/textSearch.py
```

## Operating Principles

### Indexing Files with ImageBind

The core principle of operation is based on the ability of the ImageBind model to embed files of different modalities into a single embedding space. These embeddings are saved into a CSV along with the filename, with each embedding vector consisting of 1024 dimensions forming one row. This index file is created by `createIndex.py` and read by both `GUI.py` and `textSearch.py`. For more information on ImageBind, visit:
https://github.com/facebookresearch/ImageBind

### K-Means Clustering

The GUI employs a straightforward approach of dividing data into four separate clusters using K-means clustering. Each cluster can be further explored by dividing them into four subclusters, making the system hierarchical.

### Sorting with Cosine Similarity

Cosine similarity is used throughout the program to sort files based on their embeddings. This sorting is implemented for:
- Prioritizing the files displayed in the cluster preview within the GUI
- Assigning three labels from `audio_labels.index` to audio files for display in the GUI
- Finding the top 5 results for a query in `textSearch.py`