
# AI2Ethnoragphy

This is a demonstration of an ai powered media exploring tool build for the purposes of conducting an autoethnographic study.
The tool uses ImageBind by Meta AI to index different fileformats into single embedding space and uses those embeddings

This is a project done for the course DBM180 Designing with advanced artificial intelligence in Eindhoven University of Technology

## Quickstart

Use the following steps to use the program

### 1. Istall requirement

Create python 3.11 enviroment for pytorch with anaconda or conda.

Istall of requirements with
``` pip install -r requirements.txt ```

Non-conda enviroments might or might not work out of the box or migh require additional packages. Tested only with anaconda.

## 3. Creata an index

The project works by first creating index in the form of a csv file for the fiels you want to explore.
The program supports following fileformats:
- jpg
- mp3

Create the index file by running ```python3 prototype/createIndex.py``` and inserting the path to the desired folder you want to use for creating the index.
Please note that the program will explore the folders up three subfolders deep.

The index file must be done before using the other features. After creating the index file, any changes to the file locations might cause unexpet behaviour, mainly crashes for not finding the files.

## 4. Explore Graphical UI or use plain text search

You can run a graphical UI with ```python3 GUI.py```

Commandline based text search for files can be opened with ```python3 text_search.py```
