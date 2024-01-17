import tkinter as tk
from PIL import Image, ImageTk
from tools import openFileInDefaultProgram, openAndResizeImage
from clusters import Cluster

class TkWindow():
  '''Class for handling all the components and TK stuff'''

  def __init__(self, index: Cluster, window_width=820, window_height=640) -> None:
    self.clusterings = {} #Clusters will be saved here in the explore fucntion for later retriaval

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

    self.main_frame = None
    self.clearFrame()

    # Set up the layout for the main canvas and vertical scrollbar
    self.canvas.grid(row=0, column=0, sticky='nsew')
    self.scrollbar.grid(row=0, column=1, sticky='ns')

    # Configure weight for main window to be resizable
    self.root.grid_rowconfigure(0, weight=1)
    self.root.grid_columnconfigure(0, weight=1)

    self.explore(index)

  def clearFrame(self):
    if not self.main_frame == None:
      self.main_frame.destroy()

    # Creating a main frame inside the canvas
    self.main_frame = tk.Frame(self.canvas)

    # Adding the main frame to the canvas's window
    self.canvas.create_window((0, 0), window=self.main_frame, anchor='nw')

  def mainloop(self):
    # Start the GUI event loop
    self.root.mainloop()

  def explore(self, cluster: Cluster):
    '''Open files and embeddings and lay out the carousels'''

    print(F"Exploring {cluster.str}")    
    self.clearFrame()

    self.addBreadCrumbs(cluster)

    # Do clustering or look up from the dictionary
    if cluster not in self.clusterings.keys():
      self.clusterings[cluster] = cluster.agglomerativeClustering(4)
    clustering = self.clusterings[cluster]

    for cluster2 in clustering:
      FileCarousel(self, cluster2, max_open=5)

    # Update the scrollregion of the canvas to encompass the main_frame with all carousels
    self.main_frame.update_idletasks()
    self.canvas.config(scrollregion=self.canvas.bbox('all'))

  def addBreadCrumbs(self, cluster: Cluster):
    #Add breadcrumps for going back to previous cluster
    toolbar = tk.Frame(self.main_frame)
    prev_clusters = []
    previous = cluster
    while previous.parent != None:
      previous = previous.parent
      prev_clusters.append(previous)
    prev_clusters.reverse()
    for prev_cluster in prev_clusters:
      previous_btn = tk.Button( toolbar, text=prev_cluster.label, command=lambda: self.explore(prev_cluster) )
      previous_btn.pack(side='left')
      tick_label = tk.Label(toolbar, text='>')
      tick_label.pack(side='left')
    cluster_label = tk.Label(toolbar, text=cluster.label)
    cluster_label.pack(side='left')
    toolbar.pack()

class FileCarousel():
  '''Carousel for showing files and handling actions fro them'''

  def __init__ (self, window: TkWindow, cluster: Cluster, max_open=5):
      header = cluster.label
      file_paths = cluster.files
      self.file_paths = file_paths
      self.open_index = 0

      # Create a new frame for the horizontal scrollable carousel
      carousel_frame = tk.Frame(window.main_frame)

      # Create a canvas within the carousel frame
      self.canvas = tk.Canvas(carousel_frame, height=120, width=window.window_width)
      h_scrollbar = tk.Scrollbar(carousel_frame, orient='horizontal', command=self.canvas.xview)
      self.canvas.configure(xscrollcommand=h_scrollbar.set)

      # Create a frame for the images and buttons inside the canvas
      self.images_frame = tk.Frame(self.canvas)

      # Add the images frame to the canvas's window
      self.canvas.create_window((0, 0), window=self.images_frame, anchor='nw')

      #Open files
      self.openFiles(max_open)

      # Create a frame with buttons for expanding clustering or opening more media
      action_frame = tk.Frame(carousel_frame)
      label = tk.Label(action_frame, text=header)
      label.grid(row=0, column=0)
      expand_button = tk.Button(action_frame, text='Expand', command=self.openFiles)
      expand_button.grid(row=0, column=1)
      if cluster.len > 4: #Expand button only necessary when there is somethign to divide
        explore_button = tk.Button(action_frame, text='Explore', command=lambda: window.explore(cluster))
        explore_button.grid(row=0, column=2)
      action_frame.grid(row=0, column=0, sticky='ew')

      # Position the canvas and horizontal scrollbar in the carousel frame
      self.canvas.grid(row=1, column=0, sticky='ew')
      h_scrollbar.grid(row=2, column=0, sticky='ew')

      # Pack the carousel frame into the main frame
      carousel_frame.pack()

  def openFiles(self, max_open=5):
    image_h = 80
    image_w = 100
    for iteration, _ in enumerate(self.file_paths):
      if iteration == max_open:
        break
      i = self.open_index + iteration
      if i >= len(self.file_paths):
        break
      file_path = self.file_paths[i]

      original_image = openAndResizeImage(file_path, image_w, image_h)
      photo = ImageTk.PhotoImage(original_image)

      image_label = tk.Label(self.images_frame, image=photo, width=image_w, height=image_h)
      image_label.photo = photo
      image_label.grid(row=0, column=i)

      openImage = lambda path=file_path: openFileInDefaultProgram(path)
      button = tk.Button(self.images_frame, text="Open", command=openImage)
      button.grid(row=1, column=i)
    
    self.open_index += max_open
    #Update the inner frame to match the content
    self.images_frame.update_idletasks()
    self.canvas.config(scrollregion=self.canvas.bbox('all'))
