"""
  Little GUI to change the annotations in the https://github.com/dataset-ninja/sweet-pepper dataset.

  I want these to match the BUP19 and BUP20 datasets so I can combine them.

  Created: MAH 20259711

"""


import argparse
import os
import sys

from PyQt6.QtWidgets import QApplication

from engine.GUI import GoldenAnpu_SP_Annotation

def parser():
  parser = argparse.ArgumentParser(description='Extracting command line arguments', add_help=True)

  parser.add_argument('--root', action='store', default='/home/mhalstead/nfs/desktop/home/mhalstead/project_drive/data/ds')
  parser.add_argument('--imageloc', action='store', default='/home/mhalstead/nfs/desktop/home/mhalstead/project_drive/data/ds/data/img')
  parser.add_argument('--annoloc', action='store', default='/home/mhalstead/nfs/desktop/home/mhalstead/project_drive/data/ds/data/ann')
  parser.add_argument('--output', action='store', default='/home/mhalstead/nfs/desktop/home/mhalstead/project_drive/data/ds/data/ann/panoptic')

  # return the parsed arguments
  return parser.parse_args()


if __name__ == '__main__':
  # get the input flags
  flags = parser()
  # create the output directory
  os.makedirs(flags.output, exist_ok=True)
  # Now create the GUI
  app = QApplication(sys.argv)
  window = GoldenAnpu_SP_Annotation(flags)
  window.show()
  sys.exit(app.exec())
