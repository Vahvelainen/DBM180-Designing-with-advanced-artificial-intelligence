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
    width, height = image.size
    # Determine the factor to scale down while maintaining the aspect ratio.
    scale_factor = min(target_width / width, target_height / height)

    # Check if the scale factor is less than 1 (image is larger than the label).
    if scale_factor < 1:
        # Resize the image while maintaining the aspect ratio.
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        image = image.resize((new_width, new_height))
        
    return image
