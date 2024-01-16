import tkinter as tk
from PIL import Image, ImageTk
from tools import openFileInDefaultProgram, openAndResizeImage

class TkWindow():
  '''Class for handling all the components and TK stuff'''

  def __init__(self, window_width=820, window_height=640) -> None:
    self.window_width = window_width
    self.window_height = window_height
    self.root = tk.Tk()
    self.root.title("Python GUI")
    self.root.resizable(False, True)
    self.root.geometry(F"{window_width}x{window_height}")

    # Creating a canvas and a scrollbar for vertical scrolling
    self.canvas = tk.Canvas(self.root)
    self.scrollbar = tk.Scrollbar(self.root, orient='vertical', command=self.canvas.yview)
    self.canvas.configure(yscrollcommand=self.scrollbar.set)

    # Creating a main frame inside the canvas
    self.main_frame = tk.Frame(self.canvas)

    # Adding the main frame to the canvas's window
    self.canvas.create_window((0, 0), window=self.main_frame, anchor='nw')

    # Set up the layout for the main canvas and vertical scrollbar
    self.canvas.grid(row=0, column=0, sticky='nsew')
    self.scrollbar.grid(row=0, column=1, sticky='ns')

    # Configure weight for main window to be resizable
    self.root.grid_rowconfigure(0, weight=1)
    self.root.grid_columnconfigure(0, weight=1)

  def mainloop(self):
    # Update the scrollregion of the canvas to encompass the main_frame with all carousels
    self.main_frame.update_idletasks()
    self.canvas.config(scrollregion=self.canvas.bbox('all'))
    # Start the GUI event loop
    self.root.mainloop()

  def addFileCarousel(self, image_paths, max_open = 5):
      image_h = 80
      image_w = 100

      # Create a new frame for the horizontal scrollable carousel
      carousel_frame = tk.Frame(self.main_frame)

      # Create a canvas within the carousel frame
      canvas = tk.Canvas(carousel_frame, height=120, width=self.window_width)
      h_scrollbar = tk.Scrollbar(carousel_frame, orient='horizontal', command=canvas.xview)
      canvas.configure(xscrollcommand=h_scrollbar.set)

      # Create a frame for the images and buttons inside the canvas
      images_frame = tk.Frame(canvas)

      # Add the images frame to the canvas's window
      canvas.create_window((0, 0), window=images_frame, anchor='nw')
      
      for i, image_path in enumerate(image_paths):
          if i == max_open:
            break
          original_image = openAndResizeImage(image_path, image_w, image_h)
          photo = ImageTk.PhotoImage(original_image)

          image_label = tk.Label(images_frame, image=photo, width=image_w, height=image_h)
          image_label.photo = photo
          image_label.grid(row=0, column=i)

          openImage = lambda path=image_path: openFileInDefaultProgram(path)
          button = tk.Button(images_frame, text="Open", command=openImage)
          button.grid(row=1, column=i)

      # Position the canvas and horizontal scrollbar in the carousel frame
      canvas.grid(row=0, column=0, sticky='ew')
      h_scrollbar.grid(row=1, column=0, sticky='ew')

      # Update the inner frame to match the content
      images_frame.update_idletasks()
      canvas.config(scrollregion=canvas.bbox('all'))

      # Pack the carousel frame into the main frame
      carousel_frame.pack()