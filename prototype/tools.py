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
