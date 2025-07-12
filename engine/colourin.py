
import numpy as np
import os

from skimage.io import imread, imsave

from engine.utils import BUPClasses


colours = [[0,0,0], [255,0,0], [255,255,0], [0,255,0], [255,105,180], [255,165,0], [138,43,226], [0,255,255]]

def coloursmap(annoloc, prefix):
  smap = imread(os.path.join(annoloc, f'{prefix}_smap.png'))
  imap = imread(os.path.join(annoloc, f'{prefix}_imap.png'))

  osmap = np.zeros([smap.shape[0], smap.shape[1], 3])

  usmap = np.unique(smap)
  print('The classes in the smap are', [BUPClasses[u] for u in usmap])
  print('The instances in the imap are:')
  for us in usmap:
    r, c = np.where(smap==us)
    osmap[r,c,0] = colours[us][0]
    osmap[r,c,1] = colours[us][1]
    osmap[r,c,2] = colours[us][2]
    uimap = np.unique(imap[r,c])
    print('\t', BUPClasses[us], uimap)

  imsave('smap.png', osmap.astype(np.uint8))
