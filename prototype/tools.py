import subprocess, os, platform
from PIL import Image, ImageTk

def openFileInDefaultProgram(filepath):
  print(F"Open file: {filepath}")
  # Open the file in defaul program
  if platform.system() == 'Darwin':       # macOS
      os.system(f"open {filepath}")
  elif platform.system() == 'Windows':    # Windows
      os.startfile(filepath)
  else:                                   # linux variants
      subprocess.call(('xdg-open', filepath))

def openAndResizeImage(image_path, target_width, target_height):
    image = Image.open(image_path)
    image.thumbnail((target_width, target_height))
    return image

def findDirectories(base_path, depth=1, max_depth=3):
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