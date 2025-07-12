import copy
import json
import numpy as np
import os
import supervisely as sly

from skimage.io import imread, imsave

from .utils import BUPClasses, getinfo

from PyQt6.QtWidgets import (
  QMainWindow,
  QWidget,
  QHBoxLayout,
  QVBoxLayout,
  QToolBar,
  QMenu,
  QLabel,
  QSizePolicy,
  QPushButton
)
from PyQt6.QtGui import QAction, QImage, QPixmap
from PyQt6.QtCore import Qt

class GoldenAnpu_SP_Annotation(QMainWindow):
  def __init__(self, flags):
    super().__init__()
    # get the input and output locations
    self.flags = flags
    self.imgF, self.P = getinfo(self.flags.root, self.flags.imageloc)
    # self.it is the image iterator, self.jt is the annotation iterator
    self.it, self.jt = 0, 0
    self.create_class_imap_index()

    # now create the basics
    self.setWindowTitle('Subclass Annotation Tool')
    self.resize(800,400)

    # Horizontal Layout
    this_widget = QWidget()
    main_layout = QHBoxLayout(this_widget)

    # Dropdown menu to
    menu_bar = self.menuBar()
    number_menu = QMenu("Image Index", self)
    menu_bar.addMenu(number_menu)
    for i in range(1,len(self.imgF)+1):
      action = QAction(str(i), self)
      action.triggered.connect(lambda checked, n=i:self.set_number(n))
      number_menu.addAction(action)

    # left panel - original image with outline
    left_panel = QVBoxLayout()
    self.image_label = QLabel()
    self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.image_label.setScaledContents(True)
    left_panel.addWidget(self.image_label)
    left_widget = QWidget()
    left_widget.setLayout(left_panel)
    left_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    # center panel - the cropped image
    center_panel = QVBoxLayout()
    self.image_cropped = QLabel()
    self.image_cropped.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.image_cropped.setScaledContents(True)
    center_panel.addWidget(self.image_cropped)
    center_widget = QWidget()
    center_widget.setLayout(center_panel)

    # right panel - subclass buttons and next button
    right_panel = QVBoxLayout()
    self.btn_red = QPushButton('Red')
    self.btn_red.setCheckable(True)
    self.btn_red.clicked.connect(lambda checked, b=self.btn_red: self.on_button_toggled(b, checked))
    right_panel.addWidget(self.btn_red)
    self.btn_green = QPushButton('Green')
    self.btn_green.setCheckable(True)
    self.btn_green.clicked.connect(lambda checked, b=self.btn_green: self.on_button_toggled(b, checked))
    right_panel.addWidget(self.btn_green)
    self.btn_yellow = QPushButton('Yellow')
    self.btn_yellow.setCheckable(True)
    self.btn_yellow.clicked.connect(lambda checked, b=self.btn_yellow: self.on_button_toggled(b, checked))
    right_panel.addWidget(self.btn_yellow)
    self.btn_mred = QPushButton('MRed')
    self.btn_mred.setCheckable(True)
    self.btn_mred.clicked.connect(lambda checked, b=self.btn_mred: self.on_button_toggled(b, checked))
    right_panel.addWidget(self.btn_mred)
    self.btn_myellow = QPushButton('MYellow')
    self.btn_myellow.setCheckable(True)
    self.btn_myellow.clicked.connect(lambda checked, b=self.btn_myellow: self.on_button_toggled(b, checked))
    right_panel.addWidget(self.btn_myellow)
    self.btn_black = QPushButton('Black')
    self.btn_black.setCheckable(True)
    self.btn_black.clicked.connect(lambda checked, b=self.btn_black: self.on_button_toggled(b, checked))
    right_panel.addWidget(self.btn_black)
    self.btn_ped = QPushButton('Peduncle')
    self.btn_ped.setCheckable(True)
    self.btn_ped.clicked.connect(lambda checked, b=self.btn_ped: self.on_button_toggled(b, checked))
    right_panel.addWidget(self.btn_ped)
    # Next button
    next_button = QPushButton("Next")
    next_button.clicked.connect(self.reset_ui)
    right_panel.addWidget(next_button)
    # Back Button
    back_button = QPushButton("Back")
    back_button.clicked.connect(self.go_back)
    right_panel.addWidget(back_button)
    right_widget = QWidget()
    right_widget.setLayout(right_panel)
    right_widget.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

    # Add panels to the main horizontal layout
    main_layout.addWidget(left_widget)
    main_layout.addWidget(center_widget)
    main_layout.addWidget(right_widget)

    self.setCentralWidget(this_widget)

    # Show initial image
    self.reset_ui()

  def create_class_imap_index(self,):
    self.imap_indexs = {k:1 for k in BUPClasses}
    self.imap_indexs_history = {} #{k:[] for k in BUPClasses}

  def go_back(self):
    if self.jt - 2 >= 0:
      self.jt -= 2
      text = self.imap_indexs_history[self.jt]
      self.imap_indexs[text] -= 1
      text = self.imap_indexs_history[self.jt+1]
      self.imap_indexs[text] -= 1
      self.imap_indexs_history.pop(self.jt+1)
      self.reset_ui()
    else:
      if self.it - 1 >= 0:
        self.it -= 1
        self.jt = 0
        self.create_class_imap_index()
        self.reset_ui()

  def set_number(self, idx):
    self.it = int(idx)-1
    self.jt = 0
    # print(self.it, self.jt)
    self.reset_ui()

  def on_button_toggled(self, button, checked):
    if checked:
      self.class_mapper(button.text(), self.jt-1)
    else:
      self.imap_indexs_history.pop(self.jt-1)
      self.imap_indexs[button.text()] -= 1

  def class_mapper(self, text, ind):
    sind = BUPClasses.index(text)
    # print(sind)
    self.smap[self.r,self.c] = sind
    self.imap[self.r,self.c] = self.imap_indexs[text]
    self.imap_indexs_history[ind] = text
    self.imap_indexs[text] += 1

  def getcroppedimg(self,):
    self.image_name = self.imgF[self.it]
    img = imread(self.image_name)
    if self.jt == 0:
      self.smap = np.zeros((img.shape[0], img.shape[1]))
      self.imap = np.zeros((img.shape[0], img.shape[1]))
    ann_file = os.path.join(self.flags.annoloc, os.path.basename(self.image_name)+'.json')
    ann = json.load(open(ann_file))
    ann_json = sly.Annotation.from_json(ann, self.P.meta)
    self.stored_ann = copy.copy(ann_json)
    if self.it >= len(self.imgF):
      print('Finished the images')
      sys.exit(1)
    if self.jt < len(ann_json.labels):
      print(self.image_name, self.it, self.jt)
      label = ann_json.labels[self.jt]
      if True:
        img2 = np.zeros(img.shape)
        label.draw(img2)
        img3 = img.copy()
        label.draw_contour(img3)
        self.r, self.c, _ = np.where(img2>0)
        hmin, hmax = np.clip(np.amin(self.r)-20, 0, img.shape[0]), np.clip(np.amax(self.r)+20, 0, img.shape[0])
        wmin, wmax = np.clip(np.amin(self.c)-20, 0, img.shape[1]), np.clip(np.amax(self.c)+20, 0, img.shape[1])
        # self.jt += 1
        self.out = img[hmin:hmax,wmin:wmax,:].copy()
        self.cls = label.obj_class.name
        self.input_image = img3.copy()
    else: # end of the image
      self.it += 1
      self.jt = 0
      self.create_class_imap_index()
      # save the imap and smap
      bn = os.path.splitext(os.path.basename(self.image_name))[0]
      imsave(os.path.join(self.flags.output, f'{bn}_smap.png'), self.smap.astype(np.uint8), check_contrast=False)
      imsave(os.path.join(self.flags.output, f'{bn}_imap.png'), self.imap.astype(np.uint8), check_contrast=False)
      # recursion
      self.getcroppedimg()

  def reset_ui(self):
    """Clear or reset the UI and load a new image"""
    self.getcroppedimg()
    h, w, _ = self.out.shape
    qimage_cropped = QImage(
        self.out.data,
        w,
        h,
        3 * w,
        QImage.Format.Format_RGB888
    )
    h, w, _ = self.input_image.shape
    qimage_original = QImage(
        self.input_image.data,
        w,
        h,
        3 * w,
        QImage.Format.Format_RGB888
    )
    pixmap = QPixmap.fromImage(qimage_original)
    self.image_label.setPixmap(pixmap)
    pixmap = QPixmap.fromImage(qimage_cropped)
    target_size = self.image_cropped.size()
    if target_size.width() > 0 and target_size.height() > 0:
        pixmap = pixmap.scaled(
            target_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
    self.image_cropped.setPixmap(pixmap)
    self.btn_red.setChecked(False)
    self.btn_green.setChecked(False)
    self.btn_yellow.setChecked(False)
    self.btn_mred.setChecked(False)
    self.btn_myellow.setChecked(False)
    self.btn_ped.setChecked(False)
    self.btn_black.setChecked(False)
    if self.cls == 'green fruit':
      self.btn_green.setChecked(True)
      self.class_mapper('Green', self.jt)
    elif self.cls == 'red fruit':
      self.btn_red.setChecked(True)
      self.class_mapper('Red', self.jt)
    elif self.cls == 'yellow fruit':
      self.btn_yellow.setChecked(True)
      self.class_mapper('Yellow', self.jt)
    elif 'peduncle' in self.cls:
      self.btn_ped.setChecked(True)
      self.class_mapper('Peduncle', self.jt)
    self.jt += 1
