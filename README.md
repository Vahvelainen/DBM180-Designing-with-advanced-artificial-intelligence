
# AI2Ethnoragphy

This is a demonstration of an ai powered media exploring tool build for the purposes of conducting an autoethnographic study.
The tool uses ImageBind by Meta AI to index different fileformats into single embedding space and uses those embeddings to explore the files.

This is a project done for the course DBM180 Designing with advanced artificial intelligence in Eindhoven University of Technology

## Quickstart

Use the following steps to use the program

### 1. Istall requirement

Create python 3.11 enviroment for pytorch with anaconda or conda.

Istall of requirements with
``` pip install -r requirements.txt ```

Non-conda enviroments might or might not work out of the box or migh require additional packages. Tested only with anaconda.

### 3. Creata an index

The project works by first creating index in the form of a csv file for the fiels you want to explore.
The program supports following fileformats:
- jpg
- mp3
- txt

Create the index file by running ```python prototype/createIndex.py``` and inserting the path to the desired folder you want to use for creating the index.
Please note that the program will explore the folders up three subfolders deep.

The index file must be done before using the other features. After creating the index file, any changes to the file locations might cause unexpet behaviour, mainly crashes for not finding the files.

### 4. Explore Graphical UI or use plain text search

To use the graphical UI run ```python prototype/GUI.py```

Commandline based text search for files can be opened with ```python prototype/textSearch.py```

## Operating principles

#### Indexing files with ImageBind

The whole operating princible is build around of capability of the ImageBind model to embed files of different modalities into one embedding space.
These embedding are saved into csv with the file name and the embeddign vector of 1024 dimensios consisting one row. This index file is build by createIndex.py and red by both GUI.py and textSearch.py
https://github.com/facebookresearch/ImageBind


#### K-means clustering

The GUI uses simple aproach of dividing data into 4 separate clusters with K-means clustering. Each cluster can be explored by dividing them to 4 subclusters making the system hierachical. 

#### Sorting with Cosine similarity

In many places for sorting files based on their embeddings Cosien similarity is used for as the metric.
This sorting is used for:
- in GUI prioritizing the files showed in the cluster preview
- Giving audiofiles three labels from audio_labels.index to show in GUI
- Finding top 5 results for query in textSearch.py
