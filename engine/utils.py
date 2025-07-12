
import glob
import os
import supervisely as sly

BUPClasses = ['background', 'Red', 'Yellow', 'Green', 'MRed', 'MYellow', 'Black', 'Peduncle']

def getinfo(root, images):
  image_files = sorted(glob.glob(os.path.join(images, '*.png')))
  # print(image_files[0:2])
  project = sly.Project(root, sly.OpenMode.READ)
  return image_files, project
